from pymongo import MongoClient
import json
from collections import Counter
import os

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Initialize Counters
keyword_counter = Counter()
empty_keyword_counter = 0

# Fetch articles with keywords
pipeline = [
    {
        "$match": {
            "keywords": {"$exists": True}
        }
    },
    {
        "$project": {
            "keywords": 1
        }
    }
]

# Execute the aggregation pipeline
results = collection.aggregate(pipeline)

# Process keywords and count occurrences
for doc in results:
    keywords = doc.get('keywords', [])
    if keywords:
        keyword_counter.update(keywords)
    else:
        empty_keyword_counter += 1

# Prepare results for JSON serialization
formatted_results = [{"keyword": keyword, "count": count} for keyword, count in keyword_counter.items()]

# Include the count of articles with empty keywords
formatted_results.append({"keyword": None, "count": empty_keyword_counter})

# Save results to JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'keyword_counts.json')

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(formatted_results, file, ensure_ascii=False, indent=4)

print(f"Data has been written to '{output_file}'")
