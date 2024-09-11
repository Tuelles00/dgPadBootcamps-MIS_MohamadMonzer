
from pymongo import MongoClient
from collections import Counter
import re
import unicodedata
import json
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from transformers import AutoTokenizer, AutoModel
import torch

# Function to normalize and clean keywords
def clean_keyword(keyword):
    if keyword:
        keyword = unicodedata.normalize('NFKC', keyword)
        keyword = re.sub(r'[^\w\s]', '', keyword)  # Remove special characters
        return keyword.strip().lower()
    return None

# Function to filter out single characters
def is_valid_keyword(keyword):
    return len(keyword) > 1  # Only consider keywords longer than 1 character

# Load the pre-trained BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')
model = AutoModel.from_pretrained('bert-base-multilingual-cased')

# Function to get embeddings for a keyword
def get_embedding(keyword):
    inputs = tokenizer(keyword, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    # Get the embedding for the [CLS] token (representative of the entire input)
    return outputs.last_hidden_state[:, 0, :].numpy()

# Connect to MongoDB
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client.articles_db
collection = db.articles

# Retrieve all keywords from the collection
keywords = []
for doc in collection.find({}, {"keywords": 1}):
    cleaned_keywords = [clean_keyword(keyword) for keyword in doc.get("keywords", [])]
    valid_keywords = filter(is_valid_keyword, filter(None, cleaned_keywords))
    keywords.extend(valid_keywords)

# Count the frequency of each keyword
keyword_counts = Counter(keywords)

# Get the 10 most common keywords
top_10_keywords = keyword_counts.most_common(10)

# Calculate embeddings for the top 10 keywords
embeddings = [get_embedding(keyword) for keyword, _ in top_10_keywords]

# Flatten the list of embeddings
embeddings = torch.tensor(embeddings).squeeze().numpy()

# Apply PCA for dimensionality reduction (optional, for better clustering)
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=2)  # Adjust the number of clusters as needed
clusters = kmeans.fit_predict(reduced_embeddings)

# Prepare data with automatic categorization for JSON file
result = []
for (keyword, count), cluster in zip(top_10_keywords, clusters):
    category = f"Category {cluster + 1}"
    result.append({"keyword": keyword, "count": count, "category": category})

# Define the path for the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, 'top_keywords.json')

# Write results to JSON file
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print(f"Results saved to {json_file_path}")
