import json
import os
from pymongo import MongoClient

def count_articles_updated_after_publication():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Perform aggregation to find articles where last_updated is different from published_time
    pipeline = [
        {
            "$match": {
                "$expr": {
                    "$ne": ["$published_time", "$last_updated"]  # Filter documents where published_time != last_updated
                }
            }
        },
        {
            "$count": "count"  # Count the number of documents that match the criteria
        }
    ]
    
    # Execute the aggregation pipeline
    result = [list(collection.aggregate(pipeline))]

    # Prepare the result
    count_result = result[0] if result else {"count": 0}

    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'articles_updated_after_publication.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(count_result, file, ensure_ascii=False, indent=4)
    
    print(f"Count of articles updated after publication saved to {file_path}")

if __name__ == '__main__':
    count_articles_updated_after_publication()
