#!/usr/bin/env bash
# =============================================================================
#  Run ON THE AZURE VM from the project folder:   sudo bash deploy/setup_vm.sh
#
#  Installs MySQL + Python + nginx on the same VM, creates the database,
#  runs the data-science pipeline and starts the app as a systemd service.
#  Safe to re-run (it rebuilds the data and restarts the service).
# =============================================================================
set -euo pipefail

if [[ $EUID -ne 0 ]]; then echo "Please run with sudo"; exit 1; fi

SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR=/opt/bookverse
APP_USER=bookverse
DB_NAME=bookverse
DB_USER=bookverse
ENV_FILE="$APP_DIR/.env"

echo "==> [1/7] Installing system packages (python, mysql, nginx)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-venv python3-pip mysql-server nginx rsync openssl

echo "==> [2/7] Starting MySQL"
systemctl enable --now mysql

echo "==> [3/7] Copying app to $APP_DIR"
id -u $APP_USER >/dev/null 2>&1 || useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin $APP_USER
mkdir -p "$APP_DIR"
rsync -a --delete --exclude ".env" --exclude "venv" --exclude "*.db" --exclude "__pycache__" "$SRC_DIR/" "$APP_DIR/"

echo "==> [4/7] Creating database + credentials"
if [[ -f "$ENV_FILE" ]]; then
  echo "    keeping existing $ENV_FILE"
  DB_PASS=$(grep -oP '(?<=bookverse:)[^@]+' "$ENV_FILE")
else
  DB_PASS=$(openssl rand -hex 16)
  SECRET=$(openssl rand -hex 32)
  cat > "$ENV_FILE" <<EOF
DATABASE_URL=mysql+pymysql://$DB_USER:$DB_PASS@localhost:3306/$DB_NAME?charset=utf8mb4
SECRET_KEY=$SECRET
ALICE_PASSWORD=alice123
BOB_PASSWORD=bob123
EOF
fi
mysql <<SQL
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
ALTER USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL

echo "==> [5/7] Python virtualenv + dependencies"
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip -q
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" -q
chown -R $APP_USER:$APP_USER "$APP_DIR"
chmod 600 "$ENV_FILE"

echo "==> [6/7] Data science pipeline: generate raw data -> clean -> load into MySQL"
cd "$APP_DIR"
sudo -u $APP_USER "$APP_DIR/venv/bin/python" generate_raw_data.py
sudo -u $APP_USER "$APP_DIR/venv/bin/python" data_pipeline.py

echo "==> [7/7] systemd service + nginx reverse proxy"
cp "$APP_DIR/deploy/bookverse.service" /etc/systemd/system/bookverse.service
cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/bookverse
ln -sf /etc/nginx/sites-available/bookverse /etc/nginx/sites-enabled/bookverse
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl daemon-reload
systemctl enable bookverse
systemctl restart bookverse
systemctl restart nginx

sleep 2
if curl -fs http://127.0.0.1/health >/dev/null; then STATUS="✅ healthy"; else STATUS="⚠️  check: journalctl -u bookverse -n 50"; fi
IP=$(curl -fs -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text" || hostname -I | awk '{print $1}')

cat <<EOF

=====================================================
  BookVerse is running  $STATUS
  Open:   http://$IP
  Logins: alice / alice123   ·   bob / bob123
  Logs:   sudo journalctl -u bookverse -f
=====================================================
EOF
