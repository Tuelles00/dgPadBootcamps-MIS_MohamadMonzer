from pymongo import MongoClient
from collections import Counter
import re
import unicodedata
import json
import os
from dateutil.parser import parse

# Function to normalize and clean keywords
def clean_keyword(keyword):
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

# Initialize dictionary to hold results
results_by_month = {}

# Retrieve all documents from the collection
for doc in collection.find({}, {"keywords": 1, "published_time": 1}):
    published_time = doc.get("published_time")
    if published_time:
        try:
            # Parse the published_time to get year and month
            parsed_date = parse(published_time)
            year = parsed_date.year
            month = parsed_date.month
            year_month = f"{year}-{month:02d}"  # Format month as two digits

            # Initialize the month entry if it doesn't exist
            if year_month not in results_by_month:
                results_by_month[year_month] = []

            # Clean and validate keywords
            cleaned_keywords = [clean_keyword(keyword) for keyword in doc.get("keywords", [])]
            valid_keywords = filter(is_valid_keyword, filter(None, cleaned_keywords))
            results_by_month[year_month].extend(valid_keywords)

        except (ValueError, TypeError) as e:
            print(f"Error processing document with published_time: {published_time}. Error: {e}")

    else:
        print("No published_time found for document:", doc)

# Process each month's keywords to find the top 10
final_results = []
for year_month, keywords in results_by_month.items():
    if keywords:
        keyword_counts = Counter(keywords)
        top_10_keywords = keyword_counts.most_common(10)
        monthly_results = [{"keyword": keyword, "count": count} for keyword, count in top_10_keywords]
        final_results.append({"month": year_month, "keywords": monthly_results})
    else:
        print(f"No valid keywords found for {year_month}")

# Define the path for the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, 'top_keywords_by_month.json')

# Write results to JSON file
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(final_results, file, ensure_ascii=False, indent=4)

print(f"Results saved to {json_file_path}")
