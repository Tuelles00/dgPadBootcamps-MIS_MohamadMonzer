from pymongo import MongoClient
import json
from collections import Counter
import os

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Initialize Counter for classes
class_counter = Counter()


#example
# {
#   "classes": {
#     "$elemMatch": {
#       "value": "طوفان الأقصى"
#     }
#   }
# }



# Fetch documents with classes field
pipeline = [
    {
        "$match": {
            "classes": {"$exists": True, "$ne": []}
        }
    },
    {
        "$unwind": "$classes"
    },
    {
        "$match": {
            "classes.mapping": {"$exists": True},
            "classes.value": {"$exists": True}
        }
    },
    {
        "$project": {
            "class_value": "$classes.value",
            "class_mapping": "$classes.mapping"
        }
    }
]

# Execute the aggregation pipeline
results = collection.aggregate(pipeline)

# Process classes and count occurrences
for doc in results:
    value = doc.get('class_value')
    mapping = doc.get('class_mapping')
    class_counter[(value, mapping)] += 1

# Prepare results for JSON serialization
sorted_classes = sorted(class_counter.items(), key=lambda x: x[1], reverse=True)[:10]
formatted_results = [
    {
        "value": value,
        "mapping": mapping,
        "count": count
    }
    for (value, mapping), count in sorted_classes
]

# Save results to JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'top_10_classes.json')

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(formatted_results, file, ensure_ascii=False, indent=4)

print(f"Data has been written to '{output_file}'")
