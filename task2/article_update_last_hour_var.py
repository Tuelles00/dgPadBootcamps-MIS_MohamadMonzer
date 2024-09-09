from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import os

def get_articles_published_last_hour_on_date(date_str):
    # Convert the input date string to a datetime object
    try:
        date = datetime.strptime(date_str, '%Y_%m_%d')
    except ValueError:
        print("Invalid date format. Please use yyyy_mm_dd.")
        return

    # Define the time range (last hour of the day)
    start_time = date - timedelta(hours=1)
    end_time = date

    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Query to find articles published within the last hour on the specified date
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
    file_path = os.path.join(script_dir, 'articles_published_last_hour.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(formatted_results, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        date_input = sys.argv[1]
        get_articles_published_last_hour_on_date(date_input)
    else:
        print("Please provide a date in the format yyyy_mm_dd.")
