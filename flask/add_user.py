from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson import ObjectId

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['auth']

# User details
username = 'root'
password = 'root'  # Replace with your desired password
hashed_password = generate_password_hash(password)  # Hash the password

# Insert the new user with a specific _id
collection.insert_one({
    '_id': ObjectId("66de9dfbbfa58f38e2eae37e"),  # Use a specific _id if needed
    'username': username,
    'password': hashed_password
})

print(f"User {username} added successfully.")
