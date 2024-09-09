from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Remove 'Analysis' field from all documents
result = collection.update_many({}, {"$unset": {"organization_categorization": ""}})
# result2 = collection.update_many({}, {"$unset": {"Analysis": ""}})
print(f"Removed 'organization_categorization' field from {result.modified_count} documents.")
# print(f"Removed 'Analysis' field from {result2.modified_count} documents.")
