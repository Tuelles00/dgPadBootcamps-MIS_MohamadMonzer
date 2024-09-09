from pymongo import MongoClient
import json
import os

def count_articles_by_specific_word_counts():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db
    collection = db.articles

    # Define the word counts to search for
    target_word_counts = ['100', '200']

    # Initialize a list to hold the results
    results = []

    # Count articles for each target word count and store the result as a dictionary in the list
    for word_count in target_word_counts:
        count = collection.count_documents({"word_count": word_count})
        results.append({'word_count': word_count, 'count': count})

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'articles_100_200_specific.json')
    
    # Write the result to the JSON file with square brackets around it
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    count_articles_by_specific_word_counts()
