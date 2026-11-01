#!/usr/bin/env bash
# Runs the whole pipeline end to end.
set -e
python src/generate_data.py
python src/explore.py
python src/train.py
python src/evaluate.py
python src/predict.py
