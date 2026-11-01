"""
BookVerse - Flask web app (API + frontend).

Dev:   python app.py                 -> http://localhost:5000
Prod:  gunicorn -w 2 -b 127.0.0.1:8000 app:app   (behind nginx, see deploy/)
"""
import json
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, jsonify, render_template, request, session
from sqlalchemy import and_, delete, insert, select, update
from werkzeug.security import check_password_hash

import recommender as rec
from db import BASE_DIR, DEMO_USERS, activity_log, books, engine, friendships, ratings, user_activity, users

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
REPORT_PATH = os.path.join(BASE_DIR, "data", "cleaning_report.json")


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def login_required(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        if "user_id" not in session:
            return jsonify(error="Please log in"), 401
        return fn(*a, **kw)
    return wrapper


def uid():
    return session["user_id"]


def partner_of(username):
    others = [n for n in DEMO_USERS if n != username]
    return others[0] if others else None


def log_action(user_id, action):
    with engine.begin() as c:
        c.execute(insert(activity_log).values(user_id=user_id, action=action[:255], created_at=now()))


def touch_activity(user_id, **values):
    """Portable upsert for the user_activity row."""
    values["last_seen"] = now()
    with engine.begin() as c:
        exists = c.execute(select(user_activity.c.user_id).where(user_activity.c.user_id == user_id)).first()
        if exists:
            c.execute(update(user_activity).where(user_activity.c.user_id == user_id).values(**values))
        else:
            c.execute(insert(user_activity).values(user_id=user_id, **values))


# ------------------------------------------------------------- pages
@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    with engine.connect() as c:
        c.execute(select(1))
    return jsonify(status="ok", db=engine.dialect.name)


# -------------------------------------------------------------- auth
@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip().lower()
    with engine.connect() as c:
        row = c.execute(select(users).where(users.c.username == username)).mappings().first()
    if not row or not row["password_hash"] or not check_password_hash(row["password_hash"], data.get("password") or ""):
        return jsonify(error="Invalid username or password"), 401
    session.clear()
    session.update(user_id=row["user_id"], username=row["username"])
    log_action(row["user_id"], "signed in 👋")
    return me()


@app.post("/api/logout")
@login_required
def logout():
    log_action(uid(), "signed out")
    session.clear()
    return jsonify(ok=True)


@app.get("/api/me")
@login_required
def me():
    with engine.connect() as c:
        row = c.execute(select(users.c.user_id, users.c.username, users.c.full_name, users.c.city)
                        .where(users.c.user_id == uid())).mappings().first()
        p = partner_of(row["username"])
        prow = c.execute(select(users.c.username, users.c.full_name).where(users.c.username == p)).mappings().first()
    return jsonify(user=dict(row), partner=dict(prow) if prow else None)


# ---------------------------------------------------- recommendations
@app.get("/api/recommend/books")
@login_required
def rec_books():
    return jsonify(rec.recommend_books(uid()))


@app.get("/api/recommend/people")
@login_required
def rec_people():
    return jsonify(rec.people_you_may_know(uid()))


@app.get("/api/genres")
@login_required
def genres():
    return jsonify(rec.genre_stats())


@app.get("/api/genre/<path:genre>")
@login_required
def genre_top(genre):
    return jsonify(rec.top_in_genre(genre, uid()))


@app.get("/api/trending")
@login_required
def trending():
    return jsonify(rec.trending(uid()))


@app.get("/api/search")
@login_required
def search():
    q = (request.args.get("q") or "").strip()
    return jsonify(rec.search(q, uid()) if q else [])


@app.get("/api/book/<int:book_id>")
@login_required
def book_detail(book_id):
    base, similar = rec.similar_books(book_id, uid())
    if not base:
        return jsonify(error="Not found"), 404
    return jsonify(book=base, similar=similar)


@app.get("/api/profile")
@login_required
def profile():
    return jsonify(rec.profile(uid()))


@app.get("/api/insights")
@login_required
def insights():
    report = {}
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH) as fh:
            report = json.load(fh)
    return jsonify(report=report, genres=rec.genre_stats())


# ------------------------------------------------------------ actions
@app.route("/api/book/<int:book_id>/like", methods=["POST", "DELETE"])
@login_required
def like(book_id):
    with engine.begin() as c:
        title = c.execute(select(books.c.title).where(books.c.book_id == book_id)).scalar()
        if not title:
            return jsonify(error="Not found"), 404
        cond = and_(ratings.c.user_id == uid(), ratings.c.book_id == book_id)
        if request.method == "DELETE":
            c.execute(delete(ratings).where(cond))
        elif c.execute(select(ratings.c.rating_id).where(cond)).first():
            c.execute(update(ratings).where(cond).values(rating=5, rated_at=now()))
        else:
            c.execute(insert(ratings).values(user_id=uid(), book_id=book_id, rating=5, rated_at=now()))
    log_action(uid(), f"{'❤️ liked' if request.method == 'POST' else 'un-liked'} “{title}”")
    return jsonify(ok=True, liked=request.method == "POST")


@app.post("/api/friends/<int:other>")
@login_required
def add_friend(other):
    if other == uid():
        return jsonify(error="That's you!"), 400
    a, b = sorted((uid(), other))
    with engine.begin() as c:
        name = c.execute(select(users.c.full_name).where(users.c.user_id == other)).scalar()
        if not name:
            return jsonify(error="Not found"), 404
        if not c.execute(select(friendships).where(and_(friendships.c.user_a == a, friendships.c.user_b == b))).first():
            c.execute(insert(friendships).values(user_a=a, user_b=b))
    log_action(uid(), f"🤝 became friends with {name}")
    return jsonify(ok=True)


# --------------------------------------------- live "see what they see"
@app.post("/api/activity")
@login_required
def post_activity():
    d = request.get_json(silent=True) or {}
    payload = {k: d.get(k) for k in ("view", "title", "subtitle", "kind", "items")}
    touch_activity(uid(), view=(d.get("view") or "")[:60], title=(d.get("title") or "")[:200],
                   payload=json.dumps(payload), updated_at=now())
    if d.get("action"):
        log_action(uid(), d["action"])
    return jsonify(ok=True)


@app.post("/api/heartbeat")
@login_required
def heartbeat():
    touch_activity(uid())
    return jsonify(ok=True)


@app.get("/api/live/<username>")
@login_required
def live(username):
    if username not in DEMO_USERS or username == session["username"]:
        return jsonify(error="You can only watch your demo partner"), 403
    with engine.connect() as c:
        row = c.execute(
            select(users.c.full_name, user_activity.c.view, user_activity.c.title, user_activity.c.payload,
                   user_activity.c.updated_at, user_activity.c.last_seen)
            .select_from(users.outerjoin(user_activity, users.c.user_id == user_activity.c.user_id))
            .where(users.c.username == username)).mappings().first()
    if not row:
        return jsonify(error="Not found"), 404
    online = bool(row["last_seen"] and row["last_seen"] > now() - timedelta(seconds=30))
    return jsonify(username=username, full_name=row["full_name"], online=online,
                   view=row["view"], title=row["title"], updated_at=iso(row["updated_at"]),
                   last_seen=iso(row["last_seen"]),
                   payload=json.loads(row["payload"]) if row["payload"] else None)


@app.get("/api/feed")
@login_required
def feed():
    after = request.args.get("after", 0, type=int)
    q = (select(activity_log.c.id, activity_log.c.action, activity_log.c.created_at, users.c.username, users.c.full_name)
         .join(users, users.c.user_id == activity_log.c.user_id)
         .where(users.c.username.in_(list(DEMO_USERS)), activity_log.c.id > after)
         .order_by(activity_log.c.id.desc()).limit(25))
    with engine.connect() as c:
        rows = c.execute(q).mappings().all()
    return jsonify([{**dict(r), "created_at": iso(r["created_at"])} for r in rows])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")
