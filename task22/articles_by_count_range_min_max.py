from pymongo import MongoClient
import json
import os

def categorize_articles_by_word_count():
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.31.136:27017/')
    db = client.articles_db_new
    collection = db.articles

    # Aggregation pipeline to categorize articles
    pipeline = [
        {
            "$addFields": {
                "word_count_int": {
                    "$toInt": "$word_count"
                }
            }
        },
        {
            "$bucket": {
                "groupBy": "$word_count_int",
                "boundaries": [0, 101, 301, 501, float('inf')],
                "default": "Other",
                "output": {
                    "count": {"$sum": 1}
                }
            }
        }
    ]

    # Execute the aggregation pipeline
    cursor = collection.aggregate(pipeline)
    result = list(cursor)

    # Define the boundaries and their labels
    boundaries = [0, 101, 301, 501, float('inf')]
    labels = ['low_range', 'medium_range', 'high_range', 'other']

    # Process the results to include the desired formatting
    formatted_result = []
    for i, bucket in enumerate(result):
        if i < len(boundaries) - 1:
            formatted_result.append({
                'range': f'{boundaries[i]}-{boundaries[i+1]}',
                'count': bucket['count']
            })

    # Enclose the result in square brackets
    output_data = [formatted_result]

    # Define the file path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'articles_by_count_range_min_max.json')
    
    # Write the result to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    categorize_articles_by_word_count()
