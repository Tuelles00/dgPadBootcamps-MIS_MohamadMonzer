import os
import pandas as pd
import json
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Fetch data from MongoDB
data_cursor = collection.find()
data = pd.DataFrame(list(data_cursor))

# Function to clean text data for encoding issues
def clean_text(text):
    if isinstance(text, str):
        return text.encode('utf-8', 'ignore').decode('utf-8')
    return text

# Display available columns in the data
print("Available columns in the data:")
print(data.columns)

# Convert 'published_time' to datetime with UTC
data['published_timestamp'] = pd.to_datetime(data['published_time'], errors='coerce', utc=True)

# Check if the conversion was successful
if data['published_timestamp'].isnull().all():
    raise ValueError("'published_time' column could not be converted to datetime. Please check the data format.")

# Clean text columns
for col in data.select_dtypes(include=['object']).columns:
    data[col] = data[col].apply(clean_text)

# Ensure 'word_count' is numeric
data['word_count'] = pd.to_numeric(data['word_count'], errors='coerce')

# Calculate additional features
data['text_length'] = data['text'].apply(lambda x: len(x) if isinstance(x, str) else 0)
data['keywords_count'] = data['keywords'].apply(lambda x: len(x.split(',')) if isinstance(x, str) else 0)

# Ensure 'published_timestamp' is available and not null
if 'published_timestamp' in data.columns and not data['published_timestamp'].isnull().all():
    data['text_length_per_day'] = data['text_length'] / data['published_timestamp'].dt.day
    data['keywords_count_per_day'] = data['keywords_count'] / data['published_timestamp'].dt.day
    print("Sample new feature values:")
    print(data[['text_length', 'keywords_count', 'published_timestamp', 'text_length_per_day', 'keywords_count_per_day']].head())
else:
    print("'published_timestamp' column is missing or contains null values. Skipping feature creation.")

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define file paths in the same directory as the script
patterns_path = os.path.join(script_dir, 'detected_patterns.json')
detailed_patterns_path = os.path.join(script_dir, 'detailed_patterns.json')

# Example pattern detection (Modify based on your actual pattern detection logic)
# Save all features and their descriptions
patterns = pd.DataFrame({
    'feature_name': ['text_length_per_day', 'keywords_count_per_day'],
    'description': [
        'Length of text divided by the day of the month from published_timestamp',
        'Number of keywords divided by the day of the month from published_timestamp'
    ]
})

# Save detected patterns to JSON file
with open(patterns_path, 'w', encoding='utf-8') as f:
    json.dump(patterns.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

print(f"Pattern detection completed. Results saved to '{patterns_path}'.")

# Save detailed patterns data to JSON file
detailed_patterns = data[['text_length_per_day', 'keywords_count_per_day', 'text_length', 'keywords_count', 'published_timestamp']].dropna()
detailed_patterns['published_date'] = detailed_patterns['published_timestamp'].apply(
    lambda x: datetime.utcfromtimestamp(x.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
)

# Convert pandas.Timestamp to Unix timestamp in milliseconds
detailed_patterns['published_timestamp'] = detailed_patterns['published_timestamp'].apply(
    lambda x: int(x.timestamp() * 1000)
)

# Round numerical values to desired precision
detailed_patterns = detailed_patterns.round({
    'text_length_per_day': 10,
    'keywords_count_per_day': 1,
    'text_length': 0,
    'keywords_count': 0
})

# Convert to JSON lines format
with open(detailed_patterns_path, 'w', encoding='utf-8') as f:
    json.dump(detailed_patterns.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

print(f"Detailed patterns data saved to '{detailed_patterns_path}'.")
