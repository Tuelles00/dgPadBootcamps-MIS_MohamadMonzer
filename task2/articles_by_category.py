# don't have category
# {
#                     "classes": {
#                         "$not": {
#                             "$elemMatch": {"mapping": "category"}
#                         }}}

# have category:
# {"classes.mapping": "category"}from pymongo import MongoClient
from pymongo import MongoClient
import json
import os

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Define the aggregation pipeline
pipeline = [
    {
        "$project": {
            "categories": {
                "$filter": {
                    "input": "$classes",
                    "as": "item",
                    "cond": {"$eq": ["$$item.mapping", "category"]}
                }
            }
        }
    },
    {
        "$addFields": {
            "has_category": {
                "$gt": [{"$size": "$categories"}, 0]
            }
        }
    },
    {
        "$project": {
            "category": {
                "$cond": {
                    "if": "$has_category",
                    "then": {"$arrayElemAt": ["$categories.value", 0]},
                    "else": None
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$category",
            "count": {"$sum": 1}
        }
    },
    {
        "$group": {
            "_id": None,
            "categories": {
                "$push": {
                    "category": "$_id",
                    "count": "$count"
                }
            },
            "total_with_category": {
                "$sum": {
                    "$cond": [{ "$ne": ["$_id", None] }, "$count", 0]
                }
            },
            "total_without_category": {
                "$sum": {
                    "$cond": [{ "$eq": ["$_id", None] }, "$count", 0]
                }
            }
        }
    },
    {
        "$project": {
            "categories": 1,
            "total_with_category": 1,
            "total_without_category": 1
        }
    }
]

# Execute the aggregation pipeline
results = collection.aggregate(pipeline)

# Prepare results for JSON serialization
result_data = list(results)[0]  # Get the single document from the results
categories = result_data.get("categories", [])
total_with_category = result_data.get("total_with_category", 0)
total_without_category = result_data.get("total_without_category", 0)

# Add category for those without a category if not already present
if total_without_category > 0:
    existing_categories = [item['category'] for item in categories if item['category'] is None]
    if not existing_categories:
        categories.append({
            "category": None,
            "count": total_without_category
        })

# Save results to JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'category_counts.json')

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(categories, file, ensure_ascii=False, indent=4)

print(f"Data has been written to '{output_file}'")
