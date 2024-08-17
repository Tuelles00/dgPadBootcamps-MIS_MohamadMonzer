import json
import os
from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient("mongodb://192.168.31.136:27017/")
db = client['articles_db_new']
collection = db['articles']

# Define the aggregation pipeline to count articles by date

#first parse it into a date format
pipeline_dates = [
    {"$project": {
        "date": {
            "$dateToString": {
                "format": "%Y-%m-%d",
                "date": {
                    "$dateFromString": {
                        "dateString": "$published_time",
                        "format": "%Y-%m-%dT%H:%M:%S%z"
                    }
                }
            }
        }
    }},
    {"$group": {
        "_id": "$date",
        "count": {"$sum": 1}
    }},
    {"$sort": {"_id": -1}}  # Sort by date in dec order
]

# Execute the aggregation pipeline
date_counts = list(collection.aggregate(pipeline_dates))

# Process and format the results
formatted_results = []
for date_count in date_counts:
    formatted_results.append({
        "date": date_count['_id'],
        "count": date_count['count']
    })

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'Article_counts_by_date.json')

# Save the results to a JSON file in the same directory as the script
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(formatted_results, file, ensure_ascii=False, indent=4)

print(f"Article counts by date have been written to {file_path}")
