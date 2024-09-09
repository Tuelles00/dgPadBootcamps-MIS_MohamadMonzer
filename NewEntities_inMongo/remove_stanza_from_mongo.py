from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Remove 'organization_categorization.stanza' field from all documents
result = collection.update_many(
    {},  # Empty filter to match all documents
    {"$unset": {"organization_categorization.stanza": ""}}  # Unset the specific field
)

print(f"Removed 'organization_categorization.stanza' field from {result.modified_count} documents.")
