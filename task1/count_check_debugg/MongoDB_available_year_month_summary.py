from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db
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

# Print the result as JSON
print(json.dumps(formatted_result, indent=4, ensure_ascii=False))
