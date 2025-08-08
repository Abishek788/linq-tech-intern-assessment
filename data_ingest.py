# data_ingest.py
import random
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
import argparse

def generate_mock_docs(n=100, categories=None, start=None, step_seconds=60):
    if categories is None:
        categories = ["cpu", "memory", "network", "disk", "latency"]
    if start is None:
        start = datetime.now(timezone.utc)

    docs = []
    for i in range(n):
        ts = start - timedelta(seconds=i * step_seconds)
        doc = {
            "category": random.choice(categories),
            "value": round(random.uniform(0.0, 100.0), 3),
            "timestamp": ts
        }
        docs.append(doc)
    return docs

def main():
    parser = argparse.ArgumentParser(description="Insert mock metrics into MongoDB.")
    parser.add_argument("--count", type=int, default=100, help="Number of documents to insert")
    parser.add_argument("--step-seconds", type=int, default=60, help="Time gap between points")
    parser.add_argument("--uri", type=str, default="mongodb://localhost:27017/", help="MongoDB URI")
    parser.add_argument("--db", type=str, default="linq_db", help="Database name")
    parser.add_argument("--collection", type=str, default="metrics", help="Collection name")
    args = parser.parse_args()

    client = MongoClient(args.uri)
    coll = client[args.db][args.collection]

    docs = generate_mock_docs(n=args.count, step_seconds=args.step_seconds)
    if not docs:
        print("No docs generated; nothing to insert.")
        return

    result = coll.insert_many(docs, ordered=False)
    print(f"Inserted {len(result.inserted_ids)} documents into {args.db}.{args.collection}")

if __name__ == "__main__":
    main()
