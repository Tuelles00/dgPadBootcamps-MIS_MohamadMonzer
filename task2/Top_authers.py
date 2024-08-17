import json
import os
from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient("mongodb://192.168.31.136:27017/")
db = client['articles_db_new']
collection = db['articles']

# Define the aggregation pipeline
pipeline = [
    {"$unwind": "$author"},
    {"$match": {
        "author": {"$ne": "", "$ne": None, "$regex": "^.{2,}$"}  # Ensure keywords are at least 2 characters long
    }},
    {"$group": {
        "_id": "$author",
        "count": {"$sum": 1}
    }},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]

# Execute the aggregation pipeline
top_author = list(collection.aggregate(pipeline))

# Process and clean the results
cleaned_results = []
for author in top_author:
    # Clean the keyword by removing commas and extra whitespace
    clean_kw = author['_id'].replace(',', '').strip()
    # Append cleaned result to the list
    cleaned_results.append({
        "author": clean_kw,
        "count": author['count']
    })

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'Top_author.json')

# Save the results to a JSON file in the same directory as the script
with open(file_path, 'w', encoding='utf-8') as file:
    # Write the list directly
    json.dump(cleaned_results, file, ensure_ascii=False, indent=4)

print(f"Top author have been written to {file_path}")
