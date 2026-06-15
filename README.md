# LLM Eval Framework

A lightweight framework to benchmark, score, and track LLM performance across model versions — with a live dashboard to visualize drift over time.

---

## What it does

- Runs custom benchmarks against any LLM (math, reasoning, code, summarization)
- Scores responses using keyword match, exact match, and length penalty
- Stores all results in a local SQLite database
- Tracks regression across model versions (v1, v2, v3...)
- Visualizes scores, latency, and drift on an interactive dashboard

---

## Tech stack

- Python · SQLAlchemy · SQLite
- Streamlit · Plotly
- Anthropic / Google Gemini API

---


## Dashboard preview

Score by benchmark · Latency comparison · Drift over time · Radar chart

---
