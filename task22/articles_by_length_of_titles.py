from pymongo import MongoClient
from bson.son import SON
import json
import os

def get_articles_grouped_by_title_length():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db_new
    collection = db.articles

    # Aggregation pipeline to group articles by the length of their title
    pipeline = [
        {
            "$addFields": {
                "title_length": {
                    "$strLenCP": "$title"
                }
            }
        },
        {
            "$bucket": {
                "groupBy": "$title_length",
                "boundaries": [0, 20, 40, 60, 80, 100, 200],
                "default": "Other",
                "output": {
                    "count": {"$sum": 1},
                    "articles": {"$push": {
                        "url": "$url",
                        "title": "$title",
                        "title_length": "$title_length"
                    }}
                }
            }
        }
    ]

    # Execute the aggregation pipeline
    cursor = collection.aggregate(pipeline)
    results = list(cursor)

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'articles_by_length_of_titles.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    get_articles_grouped_by_title_length()
