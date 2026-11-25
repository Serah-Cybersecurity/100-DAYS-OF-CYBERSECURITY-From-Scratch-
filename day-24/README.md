# Day 24 — Windows Endpoint Telemetry & SOC Triage Lab

## Overview
This project builds a standard-library Python JSONL endpoint event analyzer and test suite on Parrot OS alongside hands-on Windows Security and Sysmon lab practice.

## Project Layout
- `data/raw/`: Synthetic input JSONL datasets (`endpoint_events.jsonl`, `ws_fin_04_events.jsonl`)
- `data/processed/`: Processed outputs (when used)
- `data/quarantine/`: Quarantined malformed or invalid records (`invalid_events.jsonl`)
- `src/analyse_events.py`: Streaming JSONL validator, chronological sorter, and summary generator
- `tests/test_analyse_events.py`: Automated `unittest` suite
- `reports/`: Generated JSON summaries and investigation reports (`ws_fin_04_investigation.md`)
- `docs/`: Lab notes and documentation
- `screenshots/`: Curated, sanitized workflow screenshots

## Setup & Usage
From `~/cybersecurity-journey/day-24`:

```bash
python3 -m venv .venv
source .venv/bin/activate

# Run on Lab A synthetic dataset
python src/analyse_events.py

# Run on Lab B WS-FIN-04 synthetic dataset
python src/analyse_events.py \
  --input data/raw/ws_fin_04_events.jsonl \
  --output-report reports/ws_fin_04_summary.json

# Run automated tests
python -m unittest discover -s tests -v
