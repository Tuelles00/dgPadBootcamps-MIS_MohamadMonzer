from pymongo import MongoClient
from collections import Counter
import json
import os

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db_new
collection = db.articles

# Initialize a Counter to hold the document count for each keyword
document_keyword_counts = Counter()

# Iterate over each document in the collection
for document in collection.find():
    # Extract the 'keywords' array
    keywords = document.get('keywords', [])
    
    # Use a set to ensure each keyword is only counted once per document
    unique_keywords = set(keywords)
    
    # Update the document count for each unique keyword
    document_keyword_counts.update(unique_keywords)

# Get the 10 most common keywords by document count
most_common_keywords = document_keyword_counts.most_common(10)

# Prepare the data for JSON output
result = [{"keyword": keyword, "count": count} for keyword, count in most_common_keywords]

# Define the output file path (same directory as the script)
output_file_path = os.path.join(os.path.dirname(__file__), 'most_common_keywords_by_document.json')

# Write the results to a JSON file with UTF-8 encoding to handle Arabic text
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)

# Optional: Print the location of the output file
print(f'Results saved to {output_file_path}')
