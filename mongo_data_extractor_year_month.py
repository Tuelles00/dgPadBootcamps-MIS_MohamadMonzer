from pymongo import MongoClient
import json
import os
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db_new
collection = db.articles

# Define the aggregation pipeline
pipeline = [
    {
        '$project': {
            # Extract year and month from filename using regular expressions
            'filename': 1,
            'year': {
                '$regexFind': {'input': '$filename', 'regex': r'articles_(\d{4})_(\d{1,2})'}
            }
        }
    },
    {
        '$addFields': {
            # Extract year and month from the regexFind result
            'year': {
                '$arrayElemAt': [{ '$split': ['$year.match', '_'] }, 1]
            },
            'month': {
                '$arrayElemAt': [{ '$split': ['$year.match', '_'] }, 2]
            }
        }
    },
    {
        '$group': {
            '_id': '$year',
            'months': { '$addToSet': '$month' }
        }
    },
    {
        '$project': {
            '_id': 0,
            'year': '$_id',
            'months': 1
        }
    },
    {
        '$sort': {'year': 1}  # Optional: Sort by year
    }
]

# Execute the aggregation pipeline
result = list(collection.aggregate(pipeline))

# Format the result into the desired JSON structure
formatted_result = [{"year": item["year"], "months": item["months"]} for item in result]

# Utility function to convert ObjectId to string
def convert_objectid(data):
    if isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

# Loop through each year and month combination
for item in formatted_result:
    year = item['year']
    months = item['months']
    
    for month in months:
        if month is None:
            print(f"Skipping year {year} with month None")
            continue

        # Construct regex to match both formats (e.g., 09 and 9)
        month_pattern = f'{int(month)}'  # Converts '09' to '9' if applicable

        # Query for each year and month combination
        query = {
            'filename': {
                '$regex': f'articles_{year}_{month_pattern}'
            }
        }
        documents = list(collection.find(query))
        
        # Convert ObjectId fields to strings
        converted_documents = [convert_objectid(doc) for doc in documents]
        
        # Define the output file name
        filename = f"articles_{year}_{month.zfill(2)}.json"
        
        # Ensure the directory exists
        if not os.path.exists('allJson_files'):
            os.makedirs('allJson_files')
        
        # Save documents to JSON file, ensuring keywords remain as a list
        with open(os.path.join('allJson_files', filename), 'w', encoding='utf-8') as file:
            json.dump(converted_documents, file, indent=4, ensure_ascii=False)
        
        print(f"Saved data for {year}-{month.zfill(2)} to {filename}")

print("Data extraction and saving complete.")
