from pymongo import MongoClient
import json
import os

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db_new']
collection = db['articles']

# Define the aggregation pipeline to count articles by language
pipeline = [
    {
        "$group": {
            "_id": "$lang",
            "count": {"$sum": 1}
        }
    }
]

# Execute aggregation pipeline
results = collection.aggregate(pipeline)

# Prepare results for JSON serialization
formatted_results = [{"lang": doc['_id'], "count": doc['count']} for doc in results]

# Determine the path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'language_count_summary.json')

# Save results to JSON file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(formatted_results, file, ensure_ascii=False, indent=4)

print(f"Data has been written to '{output_file}'")
