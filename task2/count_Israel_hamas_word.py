from pymongo import MongoClient
import json
import os

def count_articles_by_keyword(keywords):
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Dictionary to hold counts of each keyword
    keyword_counts = {}

    for keyword in keywords:
        # MongoDB query to count articles containing the keyword
        count = collection.count_documents({"text": {"$regex": keyword, "$options": "i"}})
        keyword_counts[keyword] = count

    # Prepare the result
    result = [{
        "keyword_counts": keyword_counts
    }]

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'count_Israel_hamas_word.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    # List of keywords to count
    keywords = ["اسرائيل", "حماس"]
    count_articles_by_keyword(keywords)
