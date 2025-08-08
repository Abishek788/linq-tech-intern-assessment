# setup_mongodb.py
from pymongo import MongoClient, ASCENDING
from pymongo.errors import CollectionInvalid

def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["linq_db"]

    # Define a light schema validator (optional but helpful)
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["category", "value", "timestamp"],
            "properties": {
                "category": {"bsonType": "string", "description": "Category label"},
                "value": {"bsonType": ["double", "int", "long", "decimal"], "description": "Numeric value"},
                "timestamp": {"bsonType": "date", "description": "UTC timestamp"}
            }
        }
    }

    # Create collection if it doesn't exist
    if "metrics" not in db.list_collection_names():
        try:
            db.create_collection("metrics", validator={"$jsonSchema": validator["$jsonSchema"]})
            print("Created collection 'metrics' with validator.")
        except CollectionInvalid:
            print("Collection 'metrics' already exists (race condition).")
    else:
        # Update validator if collection exists
        db.command("collMod", "metrics", validator=validator)
        print("Updated validator on existing 'metrics' collection.")

    # Create indexes (idempotent)
    db.metrics.create_index([("timestamp", ASCENDING)], name="ts_idx")
    db.metrics.create_index([("category", ASCENDING), ("timestamp", ASCENDING)], name="cat_ts_idx")

    print("MongoDB setup complete: DB='linq_db', collection='metrics' with indexes.")

if __name__ == "__main__":
    main()
