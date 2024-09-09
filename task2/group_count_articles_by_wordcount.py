import json
import os
from pymongo import MongoClient
from bson import ObjectId

def group_and_count_articles_by_word_count():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Perform aggregation to group by word_count and count documents in each group
    pipeline = [
        {"$group": {
            "_id": "$word_count",  # Group by word_count
            "count": {"$sum": 1}   # Count the number of documents in each group
        }},
        {"$sort": {"_id": 1}},    # Sort by word_count in ascending order
        {"$project": {
            "_id": 0,              # Exclude the _id field
            "word_count": "$_id",  # Rename _id to word_count
            "count": 1             # Include the count field
        }}
    ]
    
    # Execute the aggregation pipeline
    grouped_articles = list(collection.aggregate(pipeline))

    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'articles_grouped_by_word_count.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(grouped_articles, file, ensure_ascii=False, indent=4)
    
    print(f"Articles grouped by word count saved to {file_path}")

if __name__ == '__main__':
    group_and_count_articles_by_word_count()
