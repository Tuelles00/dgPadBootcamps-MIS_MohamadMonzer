import json
import os
from pymongo import MongoClient

def group_and_count_articles_by_thumbnail_presence():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db_new
    collection = db.articles

    # Perform aggregation to group by presence of thumbnail and count documents in each group
    pipeline = [
        {"$group": {
            "_id": {"$cond": [{"$ifNull": ["$thumbnail", False]}, "Has Thumbnail", "No Thumbnail"]},  # Group by presence of thumbnail
            "count": {"$sum": 1}  # Count the number of documents in each group
        }},
        {"$sort": {"_id": 1}},  # Sort by presence of thumbnail
        {"$project": {
            "_id": 0,  # Exclude the _id field
            "thumbnail_presence": "$_id",  # Rename _id to thumbnail_presence
            "count": 1  # Include the count field
        }}
    ]
    
    # Execute the aggregation pipeline
    grouped_articles = list(collection.aggregate(pipeline))

    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'articles_grouped_by_thumbnail_presence.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(grouped_articles, file, ensure_ascii=False, indent=4)
    
    print(f"Articles grouped by thumbnail presence saved to {file_path}")

if __name__ == '__main__':
    group_and_count_articles_by_thumbnail_presence()
