from pymongo import MongoClient
from collections import Counter
import re
import unicodedata
import json
import os

# Function to normalize and clean keywords
def clean_keyword(keyword):
    # Remove special characters and normalize Arabic characters
    if keyword:
        keyword = unicodedata.normalize('NFKC', keyword)
        keyword = re.sub(r'[^\w\s]', '', keyword)  # Remove special characters
        return keyword.strip().lower()
    return None

# Function to filter out single characters
def is_valid_keyword(keyword):
    return len(keyword) > 1  # Only consider keywords longer than 1 character

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db
collection = db.articles

# Retrieve all keywords from the collection
keywords = []
for doc in collection.find({}, {"keywords": 1}):
    # Extend the list with cleaned keywords
    cleaned_keywords = [clean_keyword(keyword) for keyword in doc.get("keywords", [])]
    # Filter out None values and single characters
    valid_keywords = filter(is_valid_keyword, filter(None, cleaned_keywords))
    keywords.extend(valid_keywords)

# Count the frequency of each keyword
keyword_counts = Counter(keywords)

# Get the 10 most common keywords
top_10_keywords = keyword_counts.most_common(10)

# Prepare data for JSON file
result = [{"keyword": keyword, "count": count} for keyword, count in top_10_keywords]

# Define the path for the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, 'top_keywords.json')

# Write results to JSON file
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print(f"Results saved to {json_file_path}")
