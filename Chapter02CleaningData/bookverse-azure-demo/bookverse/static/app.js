/* BookVerse frontend – vanilla JS single page app */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

const GENRES = {
  "Fantasy":         { c1: "#7c3aed", c2: "#c026d3", icon: "🐉" },
  "Science Fiction": { c1: "#0284c7", c2: "#6366f1", icon: "🚀" },
  "Mystery":         { c1: "#1e3a5f", c2: "#0f766e", icon: "🔍" },
  "Romance":         { c1: "#e11d48", c2: "#f472b6", icon: "💌" },
  "Thriller":        { c1: "#7f1d1d", c2: "#ea580c", icon: "⚡" },
  "History":         { c1: "#78350f", c2: "#d97706", icon: "🏛️" },
  "Self-Help":       { c1: "#047857", c2: "#65a30d", icon: "🌱" },
  "Biography":       { c1: "#3730a3", c2: "#0d9488", icon: "👤" },
};
const G = g => GENRES[g] || { c1: "#475569", c2: "#64748b", icon: "📘" };

const state = { me: null, partner: null, view: null, param: null, liveOpen: false, liveStamp: null, lastFeedId: 0, feedPrimed: false };
const timers = {};

/* ---------------- helpers ---------------- */
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const initials = n => (n || "?").split(/\s+/).map(p => p[0]).slice(0, 2).join("").toUpperCase();
const hue = s => [...String(s)].reduce((h, c) => (h * 31 + c.charCodeAt(0)) % 360, 7);
const avatar = (name, cls = "") => `<div class="avatar ${cls}" style="--h:${hue(name)}">${esc(initials(name))}</div>`;
const stars = r => { const f = Math.round(r); return "★".repeat(f) + "☆".repeat(5 - f); };
const ago = iso => {
  if (!iso) return "never";
  const s = Math.max(0, (Date.now() - new Date(iso)) / 1000);
  if (s < 10) return "just now"; if (s < 60) return `${Math.floor(s)}s ago`;
  if (s < 3600) return `${Math.floor(s / 60)}m ago`; return `${Math.floor(s / 3600)}h ago`;
};

async function api(path, opts = {}) {
  const res = await fetch(path, {
    method: opts.method || "GET", credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    body: opts.body ? JSON.stringify(opts.body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 && !path.includes("/login")) { showLogin(); throw new Error("unauthorized"); }
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

function toast(html, ms = 3500) {
  const t = document.createElement("div");
  t.className = "toast"; t.innerHTML = html;
  $("#toasts").appendChild(t);
  setTimeout(() => { t.style.opacity = 0; t.style.transition = ".4s"; setTimeout(() => t.remove(), 400); }, ms);
}

/* ---------------- card builders ---------------- */
function coverHTML(b) {
  const g = G(b.genre);
  return `<div class="cover" style="--c1:${g.c1};--c2:${g.c2}">
      <span class="emoji">${g.icon}</span>
      <div><div class="cover-title">${esc(b.title)}</div><div class="cover-author">${esc(b.author)}</div></div>
    </div>`;
}

function bookCard(b, i = 0) {
  const g = G(b.genre);
  return `<article class="book" data-id="${b.book_id}" style="animation-delay:${i * 40}ms">
    ${b.match ? `<span class="match">${b.match}% match</span>` : ""}
    <button class="like ${b.liked ? "on" : ""}" data-like="${b.book_id}" title="Like">${b.liked ? "♥" : "♡"}</button>
    ${coverHTML(b)}
    <div>
      <div class="title">${esc(b.title)}</div>
      <div class="sub">${esc(b.author)}${b.year ? " · " + b.year : ""}</div>
    </div>
    <div class="stars">${stars(b.avg_rating)}<small>${b.avg_rating.toFixed(1)} (${b.num_ratings})</small></div>
    <span class="genre-tag" style="--c:${g.c1}">${esc(b.genre)}</span>
    ${b.reason ? `<div class="reason">💡 ${esc(b.reason)}</div>` : ""}
  </article>`;
}

function personCard(p, i = 0) {
  return `<article class="person glass" style="animation-delay:${i * 50}ms">
    <div class="person-head">
      ${avatar(p.full_name, "lg")}
      <div><b>${esc(p.full_name)}</b><small>@${esc(p.username)} · 📍 ${esc(p.city)}</small></div>
      <div class="score-ring" style="--p:${p.strength}" title="Connection strength"><span>${p.strength}%</span></div>
    </div>
    <div class="chips">${p.reasons.map(r => `<span class="chip">✓ ${esc(r)}</span>`).join("")}</div>
    ${p.mutual_names.length ? `<div class="mutual">👥 Friends with ${p.mutual_names.map(esc).join(", ")}${p.mutual_count > 3 ? ` +${p.mutual_count - 3}` : ""}</div>` : ""}
    ${p.top_genres.length ? `<div class="chips">${p.top_genres.map(g => `<span class="genre-tag" style="--c:${G(g).c1}">${G(g).icon} ${esc(g)}</span>`).join("")}</div>` : ""}
    <button class="btn ghost" data-friend="${p.user_id}">＋ Add friend</button>
  </article>`;
}

const skeleton = n => `<div class="grid">${Array.from({ length: n }, () => `<div class="skel"></div>`).join("")}</div>`;
const barRow = (label, pct, value, color) =>
  `<div class="bar-row"><span>${esc(label)}</span><div class="bar"><i style="--c:${color}" data-w="${pct}"></i></div><b>${esc(value)}</b></div>`;
const animateBars = () => requestAnimationFrame(() => $$(".bar i").forEach(i => (i.style.width = i.dataset.w + "%")));

/* ---------------- views ---------------- */
const VIEWS = {
  foryou: {
    title: "Books You May Like", sub: "Collaborative filtering: readers with taste like yours loved these.",
    load: () => api("/api/recommend/books"), kind: "books", action: "is browsing ✨ Books You May Like",
  },
  people: {
    title: "People You May Know", sub: "Ranked by mutual friends, taste similarity and shared genres.",
    load: () => api("/api/recommend/people"), kind: "people", action: "is looking at 🤝 People You May Know",
  },
  trending: {
    title: "Trending Now", sub: "Most 4–5★ ratings in the last 30 days.",
    load: () => api("/api/trending"), kind: "books", action: "is checking 🔥 Trending books",
  },
  genre: {
    title: g => `${G(g).icon} Best of ${g}`, sub: () => "Ranked by Bayesian average — fair to books with few ratings.",
    load: g => api(`/api/genre/${encodeURIComponent(g)}`), kind: "books", action: g => `is exploring ${G(g).icon} ${g}`,
  },
  search: {
    title: q => `Results for “${q}”`, sub: () => "Matching titles and authors.",
    load: q => api(`/api/search?q=${encodeURIComponent(q)}`), kind: "books", action: q => `searched for “${q}”`,
  },
  shelf: {
    title: "My Shelf", sub: "Your taste profile, liked books and friends.",
    load: () => api("/api/profile"), kind: "shelf", action: "is viewing 📖 their shelf",
  },
  insights: {
    title: "Data Insights", sub: "How the raw data was cleaned and what readers like across genres.",
    load: () => api("/api/insights"), kind: "insights", action: "is reading 📊 Data Insights",
  },
};
const val = (v, p) => (typeof v === "function" ? v(p) : v);

async function navigate(view, param = null, { silent = false } = {}) {
  const cfg = VIEWS[view];
  state.view = view; state.param = param;
  $$(".nav-btn").forEach(b => b.classList.toggle("active", b.dataset.view === view));
  $$(".chip-btn").forEach(b => b.classList.toggle("active", view === "genre" && b.dataset.genre === param));
  const title = val(cfg.title, param), sub = val(cfg.sub, param);
  $("#viewTitle").textContent = title; $("#viewSubtitle").textContent = sub;
  if (!silent) $("#content").innerHTML = skeleton(8);

  let data;
  try { data = await cfg.load(param); } catch (e) { $("#content").innerHTML = `<div class="empty">⚠️ ${esc(e.message)}</div>`; return; }
  if (state.view !== view || state.param !== param) return; // user moved on

  const c = $("#content");
  c.style.animation = "none"; c.offsetHeight; c.style.animation = "";
  let items;
  if (cfg.kind === "books") { renderBooks(data); items = data; }
  else if (cfg.kind === "people") { renderPeople(data); items = data; }
  else if (cfg.kind === "shelf") { renderShelf(data); items = { liked: data.liked_books.slice(0, 12), taste: data.taste, friends: data.friends }; }
  else { renderInsights(data); items = { summary: data.report.summary, genres: data.genres }; }

  publish({ view, title, subtitle: sub, kind: cfg.kind, items, action: silent ? null : val(cfg.action, param) });
}

function renderBooks(list) {
  $("#content").innerHTML = list.length ? `<div class="grid">${list.map(bookCard).join("")}</div>`
    : `<div class="empty">📭 Nothing here yet — like a few books to train your recommendations.</div>`;
}

function renderPeople(list) {
  $("#content").innerHTML = list.length ? `<div class="people">${list.map(personCard).join("")}</div>`
    : `<div class="empty">You already know everyone! 🎉</div>`;
}

function renderShelf(d) {
  const max = Math.max(1, ...d.taste.map(t => t.pct));
  $("#content").innerHTML = `
    <div class="stat-grid">
      <div class="stat glass"><b>${d.liked_books.length}</b><small>books loved (4★+)</small></div>
      <div class="stat glass"><b>${d.ratings_count}</b><small>total ratings</small></div>
      <div class="stat glass"><b>${d.friends.length}</b><small>friends</small></div>
      <div class="stat glass"><b>${d.taste[0] ? G(d.taste[0].genre).icon : "—"}</b><small>top genre: ${esc(d.taste[0]?.genre || "n/a")}</small></div>
    </div>
    <div class="two-col">
      <div class="panel glass"><h3>🎯 Your taste profile</h3>
        ${d.taste.map(t => barRow(t.genre, (t.pct / max) * 100, t.pct + "%", G(t.genre).c1)).join("") || '<p class="muted">No likes yet.</p>'}
      </div>
      <div class="panel glass"><h3>👥 Friends</h3><div class="friends-list">
        ${d.friends.map(f => `<div class="friend">${avatar(f.full_name)}<div><b>${esc(f.full_name)}</b><small>📍 ${esc(f.city)} · ${f.top_genres.map(esc).join(", ") || "—"}</small></div></div>`).join("") || '<p class="muted">No friends yet.</p>'}
      </div></div>
    </div>
    <div class="panel glass"><h3>❤️ Books you loved</h3>
      ${d.liked_books.length ? `<div class="grid">${d.liked_books.map(bookCard).join("")}</div>` : '<p class="muted">Tap ♡ on any book.</p>'}
    </div>`;
  animateBars();
}

function renderInsights(d) {
  const r = d.report || {}, s = r.summary || {};
  const tables = r.tables || [];
  const maxRatings = Math.max(1, ...d.genres.map(g => g.ratings));
  $("#content").innerHTML = `
    <div class="stat-grid">
      ${tables.map(t => `<div class="stat glass"><b>${t.rows_out}</b><small>clean ${esc(t.table)}</small>
        <div class="delta">from ${t.rows_in} raw rows (−${t.rows_in - t.rows_out})</div></div>`).join("")}
      <div class="stat glass"><b>${s.sparsity_pct ?? "—"}%</b><small>rating-matrix sparsity</small></div>
      <div class="stat glass"><b>${s.avg_rating ?? "—"}★</b><small>average rating</small></div>
    </div>
    <div class="two-col">
      <div class="panel glass"><h3>🧹 Cleaning pipeline <small class="muted">(pandas · ${esc(r.generated_at || "")})</small></h3>
        ${tables.map(t => `<div class="clean-table"><h4>${esc(t.table)} <span>${t.rows_in} → ${t.rows_out} rows</span></h4>
          ${t.steps.map(st => `<div class="step ${st.affected ? "" : "zero"}"><span>${esc(st.step)}</span><b>${st.affected}</b></div>`).join("")}</div>`).join("")}
      </div>
      <div>
        <div class="panel glass"><h3>📚 What people like — ratings by genre</h3>
          ${d.genres.map(g => barRow(`${G(g.genre).icon} ${g.genre}`, (g.ratings / maxRatings) * 100, g.ratings, G(g.genre).c1)).join("")}
        </div>
        <div class="panel glass"><h3>💖 % of ratings that are 4–5★</h3>
          ${d.genres.map(g => barRow(g.genre, g.loved_pct, g.loved_pct + "%", G(g.genre).c2)).join("")}
        </div>
      </div>
    </div>
    <div class="panel glass"><h3>🧠 The algorithms</h3><div class="algo">
      <div><b>✨ Books You May Like</b>User-based collaborative filtering. Ratings are mean-centred per user, cosine similarity finds your 20 closest "taste neighbours" (weighted down when overlap is small), and unseen books are scored by their weighted ratings.</div>
      <div><b>🤝 People You May Know</b>score = 1.5 × mutual friends + 4 × taste similarity + shared favourite genres. Same idea as Facebook's friend suggestions, plus reading taste.</div>
      <div><b>📖 Similar books</b>Item-item cosine similarity on the rating matrix — "readers who liked this also liked…".</div>
      <div><b>🏆 Best of genre</b>Bayesian average (v·R + m·C)/(v + m) so a book with one 5★ rating doesn't beat a book with thirty 4.6★ ratings.</div>
    </div></div>`;
  animateBars();
}

/* ---------------- modal ---------------- */
async function openBook(id) {
  $("#modal").classList.remove("hidden");
  $("#modalBody").innerHTML = `<div class="skel" style="height:300px"></div>`;
  const { book: b, similar } = await api(`/api/book/${id}`);
  const g = G(b.genre);
  $("#modalBody").innerHTML = `
    <div class="detail">
      ${coverHTML(b)}
      <div>
        <span class="genre-tag" style="--c:${g.c1}">${g.icon} ${esc(b.genre)}</span>
        <h2>${esc(b.title)}</h2>
        <div class="muted">by ${esc(b.author)}</div>
        <div class="facts">
          <div><b class="stars">${stars(b.avg_rating)}</b>${b.avg_rating.toFixed(2)} avg</div>
          <div><b>${b.num_ratings}</b>ratings</div>
          <div><b>${b.year ?? "—"}</b>published</div>
          <div><b>${b.pages ?? "—"}</b>pages</div>
        </div>
        <button class="btn ${b.liked ? "added" : "primary"}" data-like="${b.book_id}">${b.liked ? "♥ Loved" : "♡ Love this book"}</button>
      </div>
    </div>
    <h3 style="margin-bottom:12px">Readers who liked this also liked</h3>
    <div class="grid small">${similar.map(bookCard).join("")}</div>`;
  publish({ view: "book", title: `📖 ${b.title}`, subtitle: "Book details", kind: "books", items: [b, ...similar], action: `opened “${b.title}”` });
}
function closeModal() {
  $("#modal").classList.add("hidden");
  if (state.view) navigate(state.view, state.param, { silent: true }); // refresh likes + re-publish screen
}

/* ---------------- actions ---------------- */
async function toggleLike(id, el) {
  const on = !(el.classList.contains("on") || el.classList.contains("added"));
  await api(`/api/book/${id}/like`, { method: on ? "POST" : "DELETE" });
  $$(`[data-like="${id}"]`).forEach(b => {
    if (b.classList.contains("like")) { b.classList.toggle("on", on); b.textContent = on ? "♥" : "♡"; }
    else { b.className = `btn ${on ? "added" : "primary"}`; b.textContent = on ? "♥ Loved" : "♡ Love this book"; }
  });
  republishLiked(id, on);
  toast(on ? "❤️ Added to your shelf — recommendations updated" : "Removed from your shelf");
  pollFeed();
}

async function addFriend(id, el) {
  await api(`/api/friends/${id}`, { method: "POST" });
  el.className = "btn added"; el.textContent = "✓ Friends"; el.disabled = true;
  toast("🤝 Friend added");
  pollFeed();
}

function publish(p) { state.lastPub = p; api("/api/activity", { method: "POST", body: p }).catch(() => {}); }
function republishLiked(id, on) {
  const p = state.lastPub; if (!p) return;
  const lists = Array.isArray(p.items) ? [p.items] : [p.items?.liked || []];
  lists.forEach(l => l.forEach(b => { if (b && b.book_id == id) b.liked = on; }));
  publish({ ...p, action: null });
}

/* ---------------- live: see what partner sees ---------------- */
function miniBook(b) {
  const g = G(b.genre);
  return `<div class="mini"><div class="mini-cover" style="--c1:${g.c1};--c2:${g.c2}">${g.icon}</div>
    <div><b>${esc(b.title)}</b><small>${esc(b.reason || `${b.author} · ${b.avg_rating}★`)}</small></div>
    ${b.liked ? '<span class="heart">♥</span>' : ""}</div>`;
}
function miniPerson(p) {
  return `<div class="mini">${avatar(p.full_name)}<div><b>${esc(p.full_name)}</b><small>${esc((p.reasons || []).join(" · "))}</small></div></div>`;
}

function renderLive(d) {
  const body = $("#liveBody");
  $("#liveName").textContent = `${d.full_name}'s screen`;
  $("#liveStatus").innerHTML = d.online ? `<span style="color:var(--ok)">● online</span> · updated ${ago(d.updated_at)}` : `○ offline · last seen ${ago(d.last_seen)}`;
  const p = d.payload;
  if (!p) { $("#liveViewTitle").textContent = "—"; body.innerHTML = `<div class="empty">${esc(d.full_name)} hasn't opened anything yet.</div>`; return; }
  $("#liveViewTitle").textContent = p.title;
  if (state.liveStamp === d.updated_at) return; // nothing changed
  state.liveStamp = d.updated_at;
  let html = `<div class="live-sub">${esc(p.subtitle || "")}</div>`;
  if (p.kind === "books") html += p.items.map(miniBook).join("") || '<div class="empty">Empty list</div>';
  else if (p.kind === "people") html += p.items.map(miniPerson).join("");
  else if (p.kind === "shelf") {
    html += (p.items.taste || []).map(t => barRow(t.genre, t.pct, t.pct + "%", G(t.genre).c1)).join("");
    html += `<div class="live-sub" style="margin-top:8px">Loved books</div>` + (p.items.liked || []).map(miniBook).join("");
  } else if (p.kind === "insights") {
    const max = Math.max(1, ...p.items.genres.map(g => g.ratings));
    html += p.items.genres.map(g => barRow(g.genre, (g.ratings / max) * 100, g.ratings, G(g.genre).c1)).join("");
  }
  body.innerHTML = html;
  body.classList.remove("flash"); body.offsetHeight; body.classList.add("flash");
  animateBars();
}

async function pollLive() {
  if (!state.partner) return;
  try {
    const d = await api(`/api/live/${state.partner.username}`);
    $("#partnerDot").classList.toggle("online", d.online);
    if (state.liveOpen) renderLive(d);
  } catch (_) {}
}

function toggleLive(open = !state.liveOpen) {
  state.liveOpen = open; state.liveStamp = null;
  $("#live").classList.toggle("open", open);
  $("#watchBtn").classList.toggle("on", open);
  clearInterval(timers.live);
  if (open) { pollLive(); timers.live = setInterval(pollLive, 2000); }
  else timers.live = setInterval(pollLive, 8000);
}

/* ---------------- activity feed ---------------- */
async function pollFeed() {
  try {
    const items = await api(`/api/feed?after=${state.lastFeedId}`);
    if (!items.length) return;
    state.lastFeedId = Math.max(state.lastFeedId, ...items.map(i => i.id));
    const ul = $("#feed");
    items.reverse().forEach(it => {
      const li = document.createElement("li");
      li.innerHTML = `${avatar(it.full_name)}<div><b>${esc(it.full_name.split(" ")[0])}</b> ${esc(it.action)}<small>${ago(it.created_at)}</small></div>`;
      ul.prepend(li);
      if (state.feedPrimed && it.username !== state.me.username)
        toast(`${avatar(it.full_name)}<span><b>${esc(it.full_name.split(" ")[0])}</b> ${esc(it.action)}</span>`);
    });
    while (ul.children.length > 25) ul.lastChild.remove();
    state.feedPrimed = true;
  } catch (_) {}
}

/* ---------------- auth & boot ---------------- */
function showLogin() {
  Object.values(timers).forEach(clearInterval);
  $("#app").classList.add("hidden"); $("#login").classList.remove("hidden");
  $("#live").classList.remove("open"); state.liveOpen = false;
}

async function startApp(me) {
  state.me = me.user; state.partner = me.partner;
  state.lastFeedId = 0; state.feedPrimed = false; $("#feed").innerHTML = "";
  $("#login").classList.add("hidden"); $("#app").classList.remove("hidden");
  $("#meAvatar").outerHTML = avatar(state.me.full_name).replace('class="avatar ', 'id="meAvatar" class="avatar ');
  $("#meName").textContent = state.me.full_name; $("#meCity").textContent = "📍 " + state.me.city;
  const pfirst = state.partner ? state.partner.full_name.split(" ")[0] : "partner";
  $("#watchLabel").textContent = `See what ${pfirst} sees`;

  const genres = await api("/api/genres");
  $("#genreNav").innerHTML = genres.map(g =>
    `<button class="chip-btn" data-genre="${esc(g.genre)}" style="--c:${G(g.genre).c1}">${G(g.genre).icon} ${esc(g.genre)}</button>`).join("");

  navigate("foryou");
  pollFeed(); pollLive();
  timers.feed = setInterval(pollFeed, 4000);
  timers.live = setInterval(pollLive, 8000);
  timers.beat = setInterval(() => api("/api/heartbeat", { method: "POST" }).catch(() => {}), 10000);
  toast(`👋 Welcome back, ${esc(state.me.full_name.split(" ")[0])}!`);
}

function bind() {
  $$(".profile-pick").forEach(b => b.addEventListener("click", () => {
    $$(".profile-pick").forEach(x => x.classList.remove("sel")); b.classList.add("sel");
    $("#username").value = b.dataset.user; $("#password").focus();
  }));
  $("#loginForm").addEventListener("submit", async e => {
    e.preventDefault(); $("#loginError").textContent = "";
    try { startApp(await api("/api/login", { method: "POST", body: { username: $("#username").value, password: $("#password").value } })); }
    catch (err) { $("#loginError").textContent = err.message; }
  });
  $("#logoutBtn").addEventListener("click", async () => { await api("/api/logout", { method: "POST" }).catch(() => {}); showLogin(); });

  $("#nav").addEventListener("click", e => {
    const nb = e.target.closest(".nav-btn"); if (nb) return navigate(nb.dataset.view);
    const gb = e.target.closest(".chip-btn"); if (gb) return navigate("genre", gb.dataset.genre);
  });

  let t;
  $("#search").addEventListener("input", e => {
    clearTimeout(t); const q = e.target.value.trim();
    t = setTimeout(() => (q ? navigate("search", q) : navigate("foryou")), 350);
  });

  document.addEventListener("click", e => {
    const like = e.target.closest("[data-like]");
    if (like) { e.stopPropagation(); return toggleLike(like.dataset.like, like); }
    const fr = e.target.closest("[data-friend]");
    if (fr) return addFriend(fr.dataset.friend, fr);
    const book = e.target.closest(".book");
    if (book) return openBook(book.dataset.id);
  });

  $("#watchBtn").addEventListener("click", () => toggleLive());
  $("#liveClose").addEventListener("click", () => toggleLive(false));
  $("#modalClose").addEventListener("click", closeModal);
  $("#modal").addEventListener("click", e => { if (e.target.id === "modal") closeModal(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") { if (!$("#modal").classList.contains("hidden")) closeModal(); else if (state.liveOpen) toggleLive(false); } });
}

bind();
api("/api/me").then(startApp).catch(showLogin);
