from pymongo import MongoClient
import json
import os

def get_top_10_most_updated_articles():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Aggregation pipeline to get the top 10 most updated articles
    pipeline = [
        {
            "$sort": {
                "last_updated": -1  # Sort by last updated in descending order
            }
        },
        {
            "$group": {
                "_id": "$title",
                "update_count": {"$sum": 1},  # Count the number of updates
                "latest_update": {"$max": "$last_updated"},  # Get the most recent update time
                "url": {"$first": "$url"}
            }
        },
        {
            "$sort": {
                "update_count": -1  # Sort by update count in descending order
            }
        },
        {
            "$limit": 10  # Limit to the top 10 articles
        },
        {
            "$project": {
                "_id": 0,
                "title": "$_id",
                "update_count": 1,
                "latest_update": 1,
                "url": 1
            }
        }
    ]

    # Execute the aggregation pipeline
    cursor = collection.aggregate(pipeline)
    results = list(cursor)

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'top_10_most_updated_by_title.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    get_top_10_most_updated_articles()
