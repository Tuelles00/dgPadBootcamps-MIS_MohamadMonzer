from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import os

def get_articles_published_last_hours(hours=24):
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Calculate the time threshold
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)

    # Query to find articles published in the last 'hours' hours
    query = {
        "published_time": {
            "$gte": start_time.isoformat(),
            "$lte": end_time.isoformat()
        }
    }

    # Find articles matching the query
    cursor = collection.find(query)
    results = list(cursor)

    # Prepare results for JSON output
    formatted_results = [{"_id": str(doc["_id"]), "url": doc.get("url"), "title": doc.get("title"), "published_time": doc.get("published_time")} for doc in results]

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, f'articles_published_last_hour.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(formatted_results, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    get_articles_published_last_hours(hours=24)  # You can change the number of hours as needed
