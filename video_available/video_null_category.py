import pymongo
import json
import os

# MongoDB connection details
mongo_uri = 'mongodb://192.168.31.136:27017/'
database_name = 'articles_db_new'
collection_name = 'articles'

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Define the query to find documents with null video_duration
query = {
    "video_duration": None
}

# Find documents matching the query
documents = collection.find(query)

# Initialize a dictionary to hold categorized documents
categorized_documents = {'video_duration_null': []}

for doc in documents:
    # Extract class value
    if 'classes' in doc and len(doc['classes']) > 0:
        class_value = doc['classes'][0].get('value', 'غير معروف')

        # Append relevant information to the "video_duration_null" category
        categorized_documents['video_duration_null'].append({
            "title": doc.get("title"),
            "category_class": class_value
        })

# Convert the categorized documents dictionary to a list of dictionaries
categorized_list = [{"category": category, "videos": videos} for category, videos in categorized_documents.items()]

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the output file path in the same directory as the script
output_file_path = os.path.join(script_dir, 'categorized_videos_null_duration.json')

# Save the categorized documents to a JSON file
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(categorized_list, file, ensure_ascii=False, indent=4)

print(f"Categorized documents with null video_duration have been saved to {output_file_path}")
