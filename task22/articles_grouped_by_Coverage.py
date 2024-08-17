from pymongo import MongoClient
import json
import os

def get_articles_grouped_by_coverage():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db_new
    collection = db.articles

    # Aggregation pipeline to group by 'coverage' and count the number of articles in each group
    pipeline = [
        {
            "$group": {
                "_id": "$classes",
                "count": {"$sum": 1}
            }
        },
        {
            "$unwind": "$_id"
        },
        {
            "$group": {
                "_id": "$_id.value",
                "count": {"$sum": "$count"}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    # Execute the aggregation pipeline
    cursor = collection.aggregate(pipeline)
    results = list(cursor)

    # Prepare results for JSON output
    formatted_results = [{"coverage": doc["_id"], "count": doc["count"]} for doc in results]

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'articles_grouped_by_Coverage.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(formatted_results, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    get_articles_grouped_by_coverage()
