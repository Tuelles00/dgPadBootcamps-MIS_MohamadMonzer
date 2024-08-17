import json
import os
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from collections import Counter
from dateutil import parser

def get_most_popular_keywords_last_7_days():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db_new
    collection = db.articles

    # Calculate the date range for the last 7 days
    end_date = datetime.now(timezone.utc)  # Use timezone-aware datetime
    start_date = end_date - timedelta(days=7)

    # Convert to ISO format for querying
    start_date_iso = start_date.isoformat()
    end_date_iso = end_date.isoformat()

    # Fetch articles published in the last 7 days
    query = {
        "published_time": {
            "$gte": start_date_iso,
            "$lt": end_date_iso
        }
    }

    # Projection to only get the keywords
    projection = {
        "published_time": 1,
        "keywords": 1
    }

    documents = list(collection.find(query, projection))

    # Dictionary to store keywords by day
    keywords_by_day = {}

    for doc in documents:
        published_time_str = doc.get('published_time')
        if published_time_str:
            published_time = parser.isoparse(published_time_str)
            day_str = published_time.date().isoformat()  # Use ISO format for date

            keywords = doc.get('keywords', [])
            if isinstance(keywords, str):
                # Split keywords by comma if it's a string
                keywords_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
            elif isinstance(keywords, list):
                # Use the list as is if it's already a list
                keywords_list = [kw.strip() for kw in keywords if isinstance(kw, str) and kw.strip()]
            else:
                # Skip if keywords is neither a string nor a list
                keywords_list = []

            if day_str not in keywords_by_day:
                keywords_by_day[day_str] = []

            keywords_by_day[day_str].extend(keywords_list)

    # Convert dictionary to list of dictionaries
    keyword_counts_by_day = []
    for day, keywords in keywords_by_day.items():
        keyword_counts = Counter(keywords)
        day_entry = {
            "date": day,
            "keyword_counts": [{"keyword": kw, "count": count} for kw, count in keyword_counts.items()]
        }
        keyword_counts_by_day.append(day_entry)

    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'most_popular_keywords_last_7_days.json')

    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(keyword_counts_by_day, file, ensure_ascii=False, indent=4)

    print(f"Most popular keywords by day in the last 7 days saved to {file_path}")

if __name__ == '__main__':
    get_most_popular_keywords_last_7_days()
