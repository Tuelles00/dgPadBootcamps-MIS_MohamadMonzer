from pymongo import MongoClient
import json
from collections import Counter
import os

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db_new']
collection = db['articles']

# Initialize Counter
author_counter = Counter()

# Fetch articles with author field
pipeline = [
    {
        "$match": {
            "author": {"$exists": True, "$ne": ""}
        }
    },
    {
        "$project": {
            "author": 1
        }
    }
]

# Execute the aggregation pipeline
results = collection.aggregate(pipeline)

# Process authors and count occurrences
for doc in results:
    author = doc.get('author')
    author_counter[author] += 1

# Prepare results for JSON serialization
formatted_results = [{"author": author, "count": count} for author, count in author_counter.items()]

# Save results to JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'author_counts.json')

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(formatted_results, file, ensure_ascii=False, indent=4)

print(f"Data has been written to '{output_file}'")
