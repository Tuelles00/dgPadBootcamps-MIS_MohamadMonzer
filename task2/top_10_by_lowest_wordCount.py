import json
import os
from pymongo import MongoClient
from bson import ObjectId

def get_top_10_post_ids_by_lowest_word_count():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db_new
    collection = db.articles

    # Perform aggregation to get top 10 articles by lowest word_count
    pipeline = [
        {"$sort": {"word_count": 1}},  # Sort by word_count in ascending order
        {"$limit": 10},                 # Limit to top 10 documents
        {"$project": {"_id": 1, "postid": 1}}  # Project _id and postid fields
    ]
    
    # Execute the aggregation pipeline
    lowest_10_articles = list(collection.aggregate(pipeline))

    # Convert ObjectId to string
    for article in lowest_10_articles:
        article['_id'] = str(article['_id'])

    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'top_10_post_ids_by_lowest_word_count.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(lowest_10_articles, file, ensure_ascii=False, indent=4)
    
    print(f"Top 10 post IDs by lowest word count saved to {file_path}")

if __name__ == '__main__':
    get_top_10_post_ids_by_lowest_word_count()
