import json
import os
from pymongo import MongoClient

def count_articles_by_coverage():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Perform aggregation to group by coverage and count
    pipeline = [
        {
            "$addFields": {
                "coverage": {
                    "$arrayElemAt": [
                        {
                            "$filter": {
                                "input": "$classes",
                                "as": "class",
                                "cond": {"$eq": ["$$class.mapping", "coverage"]}
                            }
                        },
                        0
                    ]
                }
            }
        },
        {
            "$addFields": {
                "coverage": {
                    "$ifNull": ["$coverage.value", None]  # Set to None if coverage is not present
                }
            }
        },
        {
            "$group": {
                "_id": "$coverage",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}  # Sort by count in descending order
        }
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Prepare the result
    grouped_coverage = [{"coverage": doc["_id"], "count": doc["count"]} for doc in result]

    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'articles_by_coverage.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(grouped_coverage, file, ensure_ascii=False, indent=4)
    
    print(f"Articles grouped by coverage saved to {file_path}")

if __name__ == '__main__':
    count_articles_by_coverage()
