from pymongo import MongoClient
import json
import os

def count_articles_by_date(date):
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Count articles for the specified date
    count = collection.count_documents({"published_time": {"$regex": f"^{date}"}})

    # Prepare the result
    result = [{
        "date": date,
        "count": count
    }]

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'articles_in_2024_08_10.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    # Set the date for which to count articles
    specific_date = '2024-08-10'
    count_articles_by_date(specific_date)
