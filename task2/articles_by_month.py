import json
import os
from pymongo import MongoClient
from datetime import datetime

def count_articles_by_year_and_month():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Get the current year
    current_year = datetime.now().year

    # Prepare the result list
    result = []

    # Loop through each year from 2010 to the current year
    for year in range(2010, current_year + 1):
        # Loop through each month from January to December
        for month in range(1, 13):
            # MongoDB aggregation pipeline to count articles for the given year and month
            pipeline = [
                {
                    "$match": {
                        "published_time": {
                            "$regex": f"^{year}-{month:02d}"
                        }
                    }
                },
                {
                    "$count": "count"
                }
            ]

            # Execute the aggregation pipeline
            cursor = collection.aggregate(pipeline)
            count = list(cursor)

            # Extract count or set to 0 if no documents are found
            month_count = count[0]['count'] if count else 0

            # Append the result for the month if count is greater than 0
            if month_count > 0:
                result.append({
                    'year': year,
                    'month': month,
                    'count': month_count
                })

    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'articles_by_month.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    count_articles_by_year_and_month()
