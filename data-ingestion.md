## Overview of `data_ingest.py`

The `data_ingest.py` script is responsible for **generating and inserting mock metric data into MongoDB**. It acts as the data ingestion layer for the project, producing realistic, time-series metric entries that follow the schema enforced in the `metrics` collection. Here’s what it does step-by-step:

1. **Connects to MongoDB**  
   - Uses `pymongo.MongoClient` to connect to the local MongoDB instance at `mongodb://localhost:27017/`.  
   - Selects the `linq_db` database and its `metrics` collection, which is pre-configured by the `setup_mongodb.py` script.

2. **Generates Mock Metric Data**  
   - Creates realistic data points that include:
     - `category` → Randomly selected from predefined categories (e.g., `cpu`, `memory`, `disk`, `latency`, `network`).
     - `value` → Random numeric values within a reasonable range for the given category.
     - `timestamp` → Current UTC timestamp or simulated historical timestamps for time-series variety.
   - The generated data matches the schema validator in MongoDB to ensure it is always accepted.

3. **Inserts Data into MongoDB**  
   - Inserts the generated documents into the `metrics` collection using `insert_one()` or `insert_many()`.  
   - The script supports inserting multiple records in a single run to quickly populate the database.

4. **CLI Parameters (Optional)**  
   - Can be extended to accept arguments such as:
     - Number of documents to generate.
     - Specific categories to include.
     - Custom time ranges for timestamps.

5. **Console Output**  
   - Prints a confirmation message for each inserted record or a summary of how many documents were inserted.

---

## Why It’s Useful for This Project

The ingestion script ensures that the MongoDB instance always has fresh, realistic data to work with—making it easier to test queries, validate schema enforcement, and feed visualization tools like **Grafana** or **Matplotlib**. Since the generated data follows the schema defined in `setup_mongodb.py`, it integrates seamlessly without causing validation errors. This also makes it ideal for **demo environments** and **development testing**, where real production data may not be available.

---

## What it does
- Generates N mock metric points across categories (default: cpu, memory, network, disk, latency)
- Evenly spaces points backwards in time by `--step-seconds`
- Inserts into `linq_db.metrics`

## How to run
```bash
pip install -r requirements.txt
python3 data_ingest.py --count 200 --step-seconds 30
