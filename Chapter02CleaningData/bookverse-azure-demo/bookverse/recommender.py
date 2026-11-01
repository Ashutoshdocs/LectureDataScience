"""
Recommendation engine (pandas + numpy).

* Books You May Like  -> user-based collaborative filtering
                         (mean-centred cosine similarity, significance weighted)
* People You May Know -> mutual friends + taste similarity + shared genres
* Similar books       -> item-item cosine similarity
* Top in genre        -> Bayesian-average rating (fair to books with few ratings)
* Trending            -> most 4-5 star ratings in the last 30 days
"""
from collections import defaultdict

import numpy as np
import pandas as pd
from sqlalchemy import select

from db import books, engine, friendships, ratings, users


# ------------------------------------------------------------- loading
def load():
    with engine.connect() as c:
        b = pd.read_sql(select(books), c)
        r = pd.read_sql(select(ratings.c.user_id, ratings.c.book_id, ratings.c.rating, ratings.c.rated_at),
                        c, parse_dates=["rated_at"])
        u = pd.read_sql(select(users.c.user_id, users.c.username, users.c.full_name, users.c.city), c)
        f = pd.read_sql(select(friendships.c.user_a, friendships.c.user_b), c)
    return b, r, u, f


def book_stats(b, r):
    s = r.groupby("book_id")["rating"].agg(avg_rating="mean", num_ratings="count")
    out = b.merge(s, left_on="book_id", right_index=True, how="left")
    out["avg_rating"] = out["avg_rating"].fillna(0).round(2)
    out["num_ratings"] = out["num_ratings"].fillna(0).astype(int)
    return out.set_index("book_id", drop=False)


def liked_by(r, user_id):
    return set(r.loc[(r.user_id == user_id) & (r.rating >= 4), "book_id"].astype(int))


def book_dict(row, liked, **extra):
    d = {
        "book_id": int(row.book_id), "title": row.title, "author": row.author, "genre": row.genre,
        "year": None if pd.isna(row.year) else int(row.year),
        "pages": None if pd.isna(row.pages) else int(row.pages),
        "avg_rating": float(row.avg_rating), "num_ratings": int(row.num_ratings),
        "liked": int(row.book_id) in liked,
    }
    d.update(extra)
    return d


# ---------------------------------------------------------- similarity
def _cosine(X, mask):
    norms = np.linalg.norm(X, axis=1)
    norms[norms == 0] = 1
    S = (X @ X.T) / np.outer(norms, norms)
    overlap = mask.astype(float) @ mask.astype(float).T
    return S * np.minimum(overlap, 5) / 5          # down-weight tiny overlaps


def user_similarity(r):
    m = r.pivot_table(index="user_id", columns="book_id", values="rating", aggfunc="mean")
    means = m.mean(axis=1)
    centred = m.sub(means, axis=0).fillna(0)
    S = _cosine(centred.values, m.notna().values)
    return m, means, pd.DataFrame(S, index=m.index, columns=m.index)


def favourite_genres(r, b, top=2):
    j = r[r.rating >= 4].merge(b[["book_id", "genre"]], on="book_id")
    counts = j.groupby(["user_id", "genre"]).size().reset_index(name="n")
    counts = counts.sort_values(["user_id", "n"], ascending=[True, False])
    return counts.groupby("user_id")["genre"].apply(lambda s: list(s[:top])).to_dict()


# ------------------------------------------------ Books You May Like
def recommend_books(user_id, n=12):
    b, r, u, _ = load()
    stats, liked = book_stats(b, r), liked_by(r, user_id)
    m, means, S = user_similarity(r)
    if user_id not in m.index:
        return top_books(stats, liked, n, reason="Popular with readers")

    names = u.set_index("user_id")["full_name"]
    sims = S.loc[user_id].drop(user_id)
    neigh = sims[sims > 0].sort_values(ascending=False).head(20)
    rated = set(m.columns[m.loc[user_id].notna()])
    cands = [c for c in m.columns if c not in rated]
    if neigh.empty or not cands:
        return top_books(stats, liked, n, exclude=rated, reason="Popular with readers")

    sub = m.loc[neigh.index, cands]
    dev = sub.sub(means[neigh.index], axis=0).values
    w = neigh.values[:, None]
    mask = ~np.isnan(dev)
    num = np.nansum(dev * w, axis=0)
    den = (np.abs(w) * mask).sum(axis=0)
    support = mask.sum(axis=0)
    # shrink low-evidence predictions toward the user's own mean (lambda = 1.0)
    pred = np.clip(means[user_id] + num / (den + 1.0), 1, 5)
    # hybrid boost: share of the user's loved books in each candidate's genre
    mine = r[(r.user_id == user_id) & (r.rating >= 4)].merge(b[["book_id", "genre"]], on="book_id")
    affinity = mine.genre.value_counts(normalize=True)
    aff = stats.loc[cands, "genre"].map(affinity).fillna(0).values
    score = np.where(support > 0, pred + 0.15 * np.log1p(support) + 0.6 * aff, -np.inf)

    out, per_genre = [], defaultdict(int)
    for i in np.argsort(-score):
        if len(out) >= n or not np.isfinite(score[i]):
            break
        bid = cands[i]
        g = stats.loc[bid, "genre"]
        if per_genre[g] >= 5:          # diversity: max 5 books per genre
            continue
        per_genre[g] += 1
        fans = sub[bid][sub[bid] >= 4]
        if not fans.empty:
            top_fan = neigh[fans.index].idxmax()
            reason = f"{names[top_fan]} ({neigh[top_fan] * 100:.0f}% taste match) rated it {fans[top_fan]:.0f}★"
        else:
            reason = f"Readers like you would rate it ~{pred[i]:.1f}★"
        out.append(book_dict(stats.loc[bid], liked, match=int(round(pred[i] / 5 * 100)),
                             reason=reason, support=int(support[i])))
    return out


def top_books(stats, liked, n, exclude=(), reason=None):
    s = stats[~stats.book_id.isin(exclude)].sort_values(["avg_rating", "num_ratings"], ascending=False)
    return [book_dict(row, liked, reason=reason) for row in s.head(n).itertuples()]


# ----------------------------------------------- People You May Know
def friends_map(f):
    adj = defaultdict(set)
    for a, c in f.itertuples(index=False):
        adj[int(a)].add(int(c)); adj[int(c)].add(int(a))
    return adj


def people_you_may_know(user_id, n=8):
    b, r, u, f = load()
    adj = friends_map(f)
    _, _, S = user_similarity(r)
    fav = favourite_genres(r, b)
    names = u.set_index("user_id")["full_name"]
    mine = adj[user_id]
    out = []
    for row in u.itertuples():
        cand = int(row.user_id)
        if cand == user_id or cand in mine:
            continue
        mutual = sorted(mine & adj[cand])
        taste = float(S.loc[user_id, cand]) if user_id in S.index and cand in S.index else 0.0
        shared = [g for g in fav.get(user_id, []) if g in fav.get(cand, [])]
        score = 1.5 * len(mutual) + 4 * max(taste, 0) + 1.0 * len(shared)
        if score <= 0:
            continue
        reasons = []
        if mutual: reasons.append(f"{len(mutual)} mutual friend{'s' if len(mutual) > 1 else ''}")
        if taste > 0.15: reasons.append(f"{taste * 100:.0f}% similar taste")
        if shared: reasons.append("Both love " + " & ".join(shared))
        out.append({
            "user_id": cand, "username": row.username, "full_name": row.full_name, "city": row.city,
            "mutual_count": len(mutual), "mutual_names": [names[m] for m in mutual[:3]],
            "taste_match": int(round(max(taste, 0) * 100)), "shared_genres": shared,
            "top_genres": fav.get(cand, []), "reasons": reasons, "score": round(score, 2),
            "strength": int(round(100 * (1 - np.exp(-score / 3)))),  # 0-100 connection strength
        })
    return sorted(out, key=lambda d: -d["score"])[:n]


def friends_of(user_id):
    b, r, u, f = load()
    adj, fav = friends_map(f), favourite_genres(r, b)
    sub = u[u.user_id.isin(adj[user_id])]
    return [{"user_id": int(x.user_id), "username": x.username, "full_name": x.full_name,
             "city": x.city, "top_genres": fav.get(int(x.user_id), [])} for x in sub.itertuples()]


# --------------------------------------------------- browse helpers
def top_in_genre(genre, user_id, n=12, m_prior=3):
    b, r, _, _ = load()
    stats, liked = book_stats(b, r), liked_by(r, user_id)
    C = r.rating.mean()
    g = stats[stats.genre == genre].copy()
    g["bayes"] = (g.num_ratings * g.avg_rating + m_prior * C) / (g.num_ratings + m_prior)
    g = g.sort_values("bayes", ascending=False).head(n)
    return [book_dict(row, liked, reason=f"Score {row.bayes:.2f} (Bayesian avg of {row.num_ratings} ratings)")
            for row in g.itertuples()]


def trending(user_id, n=12, days=30):
    b, r, _, _ = load()
    stats, liked = book_stats(b, r), liked_by(r, user_id)
    recent = r[(r.rated_at >= r.rated_at.max() - pd.Timedelta(days=days)) & (r.rating >= 4)]
    counts = recent.groupby("book_id").size().sort_values(ascending=False).head(n)
    return [book_dict(stats.loc[bid], liked, reason=f"🔥 {c} readers loved it in the last {days} days")
            for bid, c in counts.items()]


def search(q, user_id, n=24):
    b, r, _, _ = load()
    stats, liked = book_stats(b, r), liked_by(r, user_id)
    mask = stats.title.str.contains(q, case=False, regex=False) | stats.author.str.contains(q, case=False, regex=False)
    return [book_dict(row, liked) for row in stats[mask].head(n).itertuples()]


def similar_books(book_id, user_id, n=6):
    b, r, _, _ = load()
    stats, liked = book_stats(b, r), liked_by(r, user_id)
    if book_id not in stats.index:
        return None, []
    m = r.pivot_table(index="user_id", columns="book_id", values="rating", aggfunc="mean")
    centred = m.sub(m.mean(axis=1), axis=0).fillna(0)
    S = pd.DataFrame(_cosine(centred.values.T, m.notna().values.T), index=m.columns, columns=m.columns)
    base = book_dict(stats.loc[book_id], liked)
    if book_id not in S.index:
        return base, []
    sims = S[book_id].drop(book_id).sort_values(ascending=False).head(n)
    return base, [book_dict(stats.loc[i], liked, match=int(round(max(s, 0) * 100)),
                            reason=f"Loved by the same readers ({max(s, 0) * 100:.0f}% similarity)") for i, s in sims.items()]


def profile(user_id):
    b, r, _, _ = load()
    stats, liked = book_stats(b, r), liked_by(r, user_id)
    mine = r[(r.user_id == user_id) & (r.rating >= 4)].sort_values("rated_at", ascending=False)
    taste = (mine.merge(b[["book_id", "genre"]], on="book_id").genre.value_counts(normalize=True) * 100).round(1)
    return {
        "liked_books": [book_dict(stats.loc[i], liked, reason=f"You rated it {rt:.0f}★")
                        for i, rt in zip(mine.book_id, mine.rating)],
        "taste": [{"genre": g, "pct": float(p)} for g, p in taste.items()],
        "friends": friends_of(user_id),
        "ratings_count": int((r.user_id == user_id).sum()),
    }


def genre_stats():
    b, r, _, _ = load()
    j = r.merge(b[["book_id", "genre", "title"]], on="book_id")
    stats = book_stats(b, r)
    out = []
    for g, grp in j.groupby("genre"):
        best = stats[stats.genre == g].sort_values(["avg_rating", "num_ratings"], ascending=False).iloc[0]
        out.append({"genre": g, "books": int((b.genre == g).sum()), "ratings": int(len(grp)),
                    "avg_rating": round(float(grp.rating.mean()), 2), "readers": int(grp.user_id.nunique()),
                    "loved_pct": round(float((grp.rating >= 4).mean() * 100), 1), "top_book": best.title})
    return sorted(out, key=lambda d: -d["ratings"])
