from pymongo import MongoClient
import json
import os

def get_article_counts_by_word_count_range():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db_new
    collection = db.articles

    # Queries to get the count of articles with more than 500 and 600 words
    queries = {
        "more_than_500_words": {"word_count": {"$regex": "^[5-9][0-9]{2,}$"}},
        "more_than_600_words": {"word_count": {"$regex": "^[6-9][0-9]{2,}$"}}
    }

    # Dictionary to hold results
    results = {}

    for key, query in queries.items():
        # Count articles matching the word count criteria
        count = collection.count_documents(query)
        results[key] = count

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'articles_with_more_than_500_and_more_than_600_words.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    get_article_counts_by_word_count_range()
