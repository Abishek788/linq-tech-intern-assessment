# Datastore Setup (MongoDB)

## Why MongoDB Was the Best Choice

For this project, I chose **MongoDB** because it’s a flexible, document-oriented NoSQL database that’s ideal for storing time-series metrics without the rigid structure of traditional SQL databases. Its ability to handle schemaless data while still allowing optional schema validation makes it perfect for scenarios where the data model may evolve over time but consistency is still important. In this setup, I implemented a dedicated `linq_db` database with a `metrics` collection, applied a JSON Schema validator to enforce key fields (`category`, `value`, `timestamp`), and created indexes to optimize time-based and category-based queries. The script is idempotent—meaning it can be run multiple times without breaking the setup—and ensures MongoDB is always ready for fast, reliable metric ingestion and retrieval.

---

## Overview of `setup_mongodb.py`

The `setup_mongodb.py` script is designed to **initialize and configure MongoDB for the project in a repeatable way**. Here’s what it does step-by-step:

1. **Connects to MongoDB**  
   - Uses `pymongo.MongoClient` to connect to a local MongoDB instance at `mongodb://localhost:27017/`.  
   - Selects (or creates) the database `linq_db`.

2. **Defines a Schema Validator**  
   - Sets up a light JSON Schema that enforces the presence of three fields in each document:  
     - `category` → String  
     - `value` → Numeric (int, long, double, decimal)  
     - `timestamp` → Date (UTC)  
   - This ensures data consistency while still keeping MongoDB’s flexibility.

3. **Creates or Updates the Collection**  
   - If the `metrics` collection does **not** exist, it is created with the validator applied.  
   - If the collection already exists, the script updates its validator using the `collMod` command.

4. **Creates Indexes**  
   - Index on `timestamp` for fast time-based queries.  
   - Compound index on `(category, timestamp)` for efficient filtering by category and time.

5. **Outputs Setup Status**  
   - Prints messages showing whether the collection was created or updated and confirms index creation.

---

## Why It’s Idempotent

A script is **idempotent** if you can run it multiple times and always get the same result **without creating duplicates or breaking the setup**.

- **Collection Creation:** It checks if the `metrics` collection exists before creating it.  
- **Validator Updates:** If the collection exists, it updates the validator instead of recreating it.  
- **Index Creation:** MongoDB’s `create_index` method will only create an index if it doesn’t already exist—otherwise, it reuses the existing one.

Because of this, you can run the script as part of a deployment process or local setup **over and over** without worrying about corrupting the database or creating duplicate structures.


- **DB**: `linq_db`
- **Collection**: `metrics`
- **Document shape**:
  ```json
  {
    "category": "cpu" | "memory" | "network" | "disk" | "latency",
    "value": Number,
    "timestamp": ISODate
  }
