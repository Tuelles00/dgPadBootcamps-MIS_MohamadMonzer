import json
import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db
collection = db.articles

# Find the most recent document
most_recent_document = collection.find().sort('published_time', -1).limit(1).next()

# Extract the desired information
recent_postid = most_recent_document.get('postid')
url = most_recent_document.get('url')
title = most_recent_document.get('title')
keywords = most_recent_document.get('keywords')

# Prepare the result
result = {
    'postid': recent_postid,
    'url': url,
    'title': title,
    'keywords': keywords
}

# Define the file path
file_path = os.path.join(os.path.dirname(__file__), 'recent_post_data.json')

# Read existing data
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
else:
    data = []

# Append new result
data.append(result)

# Write to the JSON file
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Data saved to {file_path}")
