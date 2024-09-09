from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db
collection = db.articles

def get_articles_published_last_hours(hours):
    """Fetch articles published in the last 'hours' hours."""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)

    query = {
        "published_time": {
            "$gte": start_time.isoformat(),
            "$lte": end_time.isoformat()
        }
    }

    cursor = collection.find(query)
    results = list(cursor)

    formatted_results = [
        {
            "_id": str(doc.get("_id")),
            "url": doc.get("url"),
            "title": doc.get("title"),
            "published_time": doc.get("published_time")
        }
        for doc in results
    ]

    return formatted_results
