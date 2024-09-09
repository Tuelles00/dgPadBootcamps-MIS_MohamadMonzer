from pymongo import MongoClient
import json
import os
from datetime import datetime

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Define the aggregation pipeline to get the 10 most recent articles
pipeline = [
    {
        "$sort": {"published_time": -1}  # Sort by published_time in descending order
    },
    {
        "$limit": 10  # Limit to 10 documents
    },
    {
        "$project": {
            "title": 1,  # Project the title field
            "_id": 1,    # Include the _id field (MongoDB ObjectId)
            "published_time": 1  # Include the published_time field
        }
    }
]

# Execute the aggregation pipeline
results = collection.aggregate(pipeline)

# Extract titles, IDs, and format the published_time
articles = []
for doc in results:
    published_time = doc.get('published_time')
    
    if isinstance(published_time, str):
        try:
            # Parse the string to a datetime object
            published_time = datetime.fromisoformat(published_time.replace("Z", "+00:00"))
        except ValueError:
            formatted_time = None
        else:
            # Format the datetime object to 'YYYY-MM-DD HH:MM:SS'
            formatted_time = published_time.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(published_time, datetime):
        # If it's already a datetime object
        formatted_time = published_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_time = None

    articles.append({
        "title": doc.get('title'),
        "postid": str(doc['_id']),
        "published_time": formatted_time
    })

# Save results to JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'recent_articles.json')

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)

print(f"Data has been written to '{output_file}'")
