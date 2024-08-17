import json
import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db_new
collection = db.articles

# Count documents where video_duration is not null
count = collection.count_documents({'video_duration': {'$ne': None}})

# Prepare the result as a list
result = [{'count': count}]

# Define the file path
file_path = os.path.join(os.path.dirname(__file__), 'video_duration_count.json')

# Write the result to the JSON file
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print(f"Data saved to {file_path}")
