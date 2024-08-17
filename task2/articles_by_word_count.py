from pymongo import MongoClient
import json
from collections import Counter
import os



#{word_count : 0}
# not {word_count : {$regex: "0"}}
# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db_new']
collection = db['articles']

# Fetch `word_count` values from MongoDB
pipeline = [
    {
        "$project": {
            "word_count": {
                "$cond": [
                    {"$regexMatch": {"input": "$word_count", "regex": "^[0-9]+$"}},
                    {"$toInt": "$word_count"},
                    0
                ]
            }
        }
    }
]

# Execute aggregation pipeline
results = collection.aggregate(pipeline)

# Extract word counts and count occurrences
word_counts = [doc['word_count'] for doc in results]
counted_word_counts = Counter(word_counts)

# Sort the counts in descending order
sorted_word_counts = sorted(counted_word_counts.items(), key=lambda x: x[1], reverse=True)

# Prepare results for JSON serialization
formatted_results = [{"word_count": wc, "count": cnt} for wc, cnt in sorted_word_counts]

# Determine the path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'word_count_summary.json')

# Save results to JSON file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(formatted_results, file, ensure_ascii=False, indent=4)

print(f"Data has been written to '{output_file}'")
