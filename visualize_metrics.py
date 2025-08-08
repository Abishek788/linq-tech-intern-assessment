from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import defaultdict

# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["linq_db"]
collection = db["metrics"]

# 2. Pull all data sorted by timestamp
data = list(collection.find().sort("timestamp", 1))

if not data:
    print("No data found in MongoDB. Run data_ingest.py first.")
    exit()

# 3. Organize data by category
category_data = defaultdict(lambda: {"timestamps": [], "values": []})
for doc in data:
    category = doc["category"]
    category_data[category]["timestamps"].append(doc["timestamp"])
    category_data[category]["values"].append(doc["value"])

# 4. Plot each category
plt.figure(figsize=(10, 6))
for category, series in category_data.items():
    plt.plot(series["timestamps"], series["values"], marker="o", label=category)

plt.title("Metrics Over Time from MongoDB")
plt.xlabel("Timestamp")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
