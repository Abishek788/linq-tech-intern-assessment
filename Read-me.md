# Technology Intern Take-Home — MongoDB + Matplotlib

## High-Level Overview

This project is a small, end-to-end pipeline that I built for the Technology Intern Take-Home.  
It covers **datastore setup**, **data ingestion**, and **visualization** using **MongoDB** and **Python (Matplotlib)**.

---

## What I Built

1. **Datastore (MongoDB, local install)**
   - Running MongoDB **locally** (not Docker) using Homebrew.
   - A setup script initializes the **`linq_db`** database and **`metrics`** collection, applies a **schema validator**, and creates **indexes** for performance.

2. **Data Ingestion (`data_ingest.py`)**
   - Generates realistic mock time-series metrics (e.g., `cpu`, `memory`, `network`, `disk`, `latency`) with timestamps.
   - Inserts documents into `linq_db.metrics`.
   - CLI flags let you control document count, categories, and time spacing.

3. **Visualization (Matplotlib)**
   - A Python script reads from MongoDB and plots each category as a line over time.
   - Exports a static chart as **`dashboard.png`**.

---

## Data Model

Each document follows a light schema:

```json
{
  "category": "cpu | memory | network | disk | latency",
  "value": <number>,
  "timestamp": "<ISODate>"
}
