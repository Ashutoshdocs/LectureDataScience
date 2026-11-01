# 📚 BookVerse — Data-Science Book Recommender on an Azure VM

A complete demo you can deploy in ~10 minutes:

* **Frontend** – beautiful, interactive single-page app (glassmorphism UI, animated cards, genre buttons, live drawer, modals, toasts, mobile friendly)
* **Backend** – Python **Flask** API served by **gunicorn** behind **nginx**
* **Database** – **MySQL running on the same VM** (never exposed to the internet)
* **Data science** – **pandas/numpy** pipeline that cleans messy raw data, then powers
  **Books You May Like**, **People You May Know**, similar books, best-of-genre and trending
* **2 user logins** (Alice & Bob) – each can open a **live drawer to see exactly what the other is seeing**, plus a shared real-time activity feed

> Inspired by the CodeBook data-science internship flow: *Cleaning & Structuring the Data → People You May Know → Pages (here: Books) You Might Like.*

---

## 🏗️ Architecture

```
                   Internet  (port 80 only)
                         │
┌────────────────────────┼──────────────────── Azure VM (Ubuntu 22.04) ────┐
│                        ▼                                                  │
│   ┌──────────┐   proxy   ┌─────────────────────┐   SQLAlchemy  ┌───────┐ │
│   │  nginx   │ ────────► │ gunicorn + Flask    │ ────────────► │ MySQL │ │
│   │ :80      │           │ app.py  (API + UI)  │   PyMySQL     │ :3306 │ │
│   │ /static  │           │ recommender.py      │  (localhost)  │       │ │
│   └──────────┘           └─────────────────────┘               └───▲───┘ │
│                                                                    │     │
│        data/raw/*.csv ──► data_pipeline.py (pandas clean) ─────────┘     │
│        (generate_raw_data.py)                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

## 📁 Project structure

```
bookverse/
├── app.py                  # Flask app: auth, recommendation API, live-view API
├── recommender.py          # Data-science engine (collaborative filtering etc.)
├── data_pipeline.py        # pandas CLEAN → STRUCTURE → LOAD into MySQL
├── generate_raw_data.py    # creates intentionally messy raw CSVs
├── db.py                   # SQLAlchemy tables + DB connection
├── templates/index.html    # SPA shell (login + app)
├── static/style.css        # UI styling
├── static/app.js           # interactive frontend logic
├── sql/schema.sql          # schema reference + handy demo queries
├── deploy/
│   ├── create_azure_vm.sh  # (laptop) creates RG + VM + opens port 80
│   ├── setup_vm.sh         # (VM) installs MySQL, Python, nginx; runs pipeline; starts service
│   ├── bookverse.service   # systemd unit (gunicorn)
│   └── nginx.conf          # reverse proxy
├── run_local.sh            # run on your laptop with SQLite (no MySQL needed)
├── requirements.txt
└── .env.example
```

---

## 🚀 Deploy on Azure (step by step)

### Prerequisites
* An Azure subscription
* [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) on your laptop (`az --version`)
* Git Bash / WSL / macOS / Linux terminal

### 1. Create the VM (on your laptop)
```bash
cd bookverse
bash deploy/create_azure_vm.sh
```
Optional overrides: `RG=my-rg LOCATION=eastus SIZE=Standard_B2s bash deploy/create_azure_vm.sh`

It prints the VM's **public IP** at the end.

<details><summary>Prefer the Azure Portal?</summary>

1. **Create a resource → Virtual machine**
2. Image **Ubuntu Server 22.04 LTS**, size **Standard_B2s** (2 vCPU, 4 GB)
3. Authentication: **SSH public key**, username `azureuser`
4. Inbound ports: **SSH (22)** and **HTTP (80)**
5. Review + create, then copy the public IP
</details>

### 2. Copy the code to the VM
```bash
scp -r . azureuser@<PUBLIC_IP>:~/bookverse
```
(or `git clone <your-repo>` on the VM)

### 3. Install & start everything (on the VM)
```bash
ssh azureuser@<PUBLIC_IP>
cd ~/bookverse
sudo bash deploy/setup_vm.sh
```
The script:
1. installs Python, **MySQL server**, nginx
2. creates database `bookverse` + user `bookverse` with a **random password** (saved in `/opt/bookverse/.env`)
3. creates a virtualenv and installs requirements
4. **generates messy raw data → cleans it with pandas → loads it into MySQL**
5. installs the gunicorn systemd service + nginx and prints the URL

### 4. Open the app
Go to **`http://<PUBLIC_IP>`**

| User  | Password  | Taste profile        |
|-------|-----------|----------------------|
| alice | alice123  | Fantasy · Sci-Fi     |
| bob   | bob123    | Mystery · Thriller   |

Change passwords in `/opt/bookverse/.env`, then `cd /opt/bookverse && sudo -u bookverse venv/bin/python data_pipeline.py && sudo systemctl restart bookverse`.

---

## 🎬 Demo script (2 users, live view)

1. Open the URL in **Chrome** → sign in as **alice**
2. Open it in an **Incognito/other browser** → sign in as **bob** (separate sessions)
3. As Alice, click **"See what Bob sees"** (top bar) → a live drawer slides in
4. As Bob, click around: **🔍 Mystery**, **People You May Know**, ♡ a book, open a book
5. Alice's drawer mirrors Bob's screen within ~2 seconds, toasts pop up (*"Bob ❤️ liked …"*) and the **Live activity** feed updates
6. Swap roles — Bob can watch Alice the same way
7. Open **📊 Data Insights** to walk through every cleaning step and genre stats
8. ♡ a few books, go back to **Books You May Like** → recommendations recalculate from MySQL

---

## 🧠 The data science

### 1. Cleaning & structuring (`data_pipeline.py`)
`generate_raw_data.py` creates realistic **dirty** CSVs. The pandas pipeline fixes them and logs every step (shown in the UI):

| Table | Problems fixed |
|---|---|
| books | whitespace, exact duplicates, 30+ genre spellings (`sci-fi`, `SCIFI`, `Thrillers`, `Bio`…) → 8 canonical genres, lowercase titles, missing authors, `"2015.0"` / `"unknown"` years, missing pages → genre median |
| users | missing IDs, duplicate users, repeated spaces in names, upper-case & invalid emails, missing city, duplicate usernames |
| ratings | `"4 stars"`, `"5/5"`, empty and out-of-range (0, 9, -1) ratings, 3 mixed timestamp formats (ISO / dd/mm/yyyy / epoch), orphan user/book IDs, re-ratings (keep latest) |
| friendships | self-friendships, A-B vs B-A duplicates, orphan IDs |

### 2. Books You May Like — user-based collaborative filtering
1. Build the **user × book rating matrix** (pandas `pivot_table`, ~84 % sparse)
2. **Mean-centre** each user's ratings (removes "generous vs strict rater" bias)
3. **Cosine similarity** between users, down-weighted when they share < 5 books
4. Take the 20 most similar users and predict unseen books:
   `pred = user_mean + Σ sim·(rating − neighbour_mean) / (Σ|sim| + 1)`
5. Small hybrid boost for genres the user already loves, max 5 books per genre for variety
6. Every card explains itself: *"Arjun Bose (42 % taste match) rated it 5★"*

### 3. People You May Know
`score = 1.5 × mutual_friends + 4 × taste_similarity + shared_favourite_genres`, shown as a connection-strength ring with reasons (*"2 mutual friends · Both love Fantasy"*).

### 4. Other views
* **Similar books** – item-item cosine similarity ("readers who liked this also liked")
* **Best of genre** – Bayesian average `(v·R + m·C)/(v + m)` so one lucky 5★ doesn't win
* **Trending** – most 4–5★ ratings in the last 30 days
* **My Shelf** – your taste profile by genre, friends and loved books

### 5. "See what the other user sees"
Every time a user renders a screen, the frontend posts a JSON snapshot to `POST /api/activity`, stored in the MySQL `user_activity` table. The partner's drawer polls `GET /api/live/<username>` every 2 s. A heartbeat (`/api/heartbeat`) drives the online dot, and `activity_log` feeds the shared live-activity list. Only the two demo users can watch each other.

---

## 🔌 API reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/login` · `/api/logout` | session auth |
| GET | `/api/me` | current user + partner |
| GET | `/api/recommend/books` | Books You May Like |
| GET | `/api/recommend/people` | People You May Know |
| GET | `/api/genre/<genre>` | best of a genre |
| GET | `/api/genres` | stats per genre |
| GET | `/api/trending` · `/api/search?q=` | trending · search |
| GET | `/api/book/<id>` | book details + similar books |
| POST/DELETE | `/api/book/<id>/like` | like / unlike (writes a 5★ rating) |
| POST | `/api/friends/<user_id>` | add friend |
| GET | `/api/profile` · `/api/insights` | shelf · cleaning report |
| POST | `/api/activity` · `/api/heartbeat` | publish screen · presence |
| GET | `/api/live/<username>` · `/api/feed` | partner's screen · activity feed |
| GET | `/health` | health check (shows DB type) |

---

## 💻 Run locally (no Azure, no MySQL)
```bash
bash run_local.sh        # creates venv, builds data into SQLite, starts on :5000
```
To use a local MySQL instead, copy `.env.example` to `.env` and set `DATABASE_URL`.

---

## 🛠️ Operations & troubleshooting

```bash
sudo systemctl status bookverse        # app status
sudo journalctl -u bookverse -f        # app logs
sudo tail -f /var/log/nginx/error.log  # nginx errors
sudo mysql bookverse                   # SQL shell (see sql/schema.sql for demo queries)
curl http://localhost/health           # {"db":"mysql","status":"ok"}
```

| Problem | Fix |
|---|---|
| Browser can't reach the IP | Check NSG rule for port 80: `az vm open-port -g bookverse-rg -n bookverse-vm --port 80` |
| `502 Bad Gateway` | App not running → `sudo journalctl -u bookverse -n 50` |
| Both tabs show the same user | Use **incognito** or two different browsers — sessions are cookie-based |
| Reset all data | `cd /opt/bookverse && sudo -u bookverse venv/bin/python generate_raw_data.py && sudo -u bookverse venv/bin/python data_pipeline.py` |
| Updated code | Re-copy to `~/bookverse` and rerun `sudo bash deploy/setup_vm.sh` (keeps `.env`) |

### 🔒 Security notes
* MySQL listens on localhost only; port 3306 is **not** opened in the NSG
* DB password and Flask `SECRET_KEY` are random and stored in `/opt/bookverse/.env` (mode 600)
* Passwords are hashed (Werkzeug scrypt); demo passwords are for demos only
* For anything beyond a demo, add HTTPS (e.g. `sudo apt install certbot python3-certbot-nginx` with a domain) and restrict SSH to your IP

### 💸 Clean up (stop paying)
```bash
az group delete --name bookverse-rg --yes --no-wait
```
