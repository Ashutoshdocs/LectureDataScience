#!/usr/bin/env bash
# Quick local run (SQLite, no MySQL needed):  bash run_local.sh
set -e
cd "$(dirname "$0")"
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
python generate_raw_data.py
python data_pipeline.py
echo "Open http://localhost:5000  (alice/alice123, bob/bob123)"
python app.py
