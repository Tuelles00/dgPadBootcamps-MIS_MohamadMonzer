import os
import pymongo
from bson.objectid import ObjectId
import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
import pickle
import numpy as np

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the model and vectorizer files
model_path = os.path.join(base_dir, 'sentiment_model.pkl')
vectorizer_path = os.path.join(base_dir, 'vectorizer.pkl')

# Load sentiment model and vectorizer
with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

# MongoDB setup
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Function to get the number of CPU cores
def get_cpu_cores():
    try:
        result = subprocess.run(['nproc'], stdout=subprocess.PIPE, text=True)
        return int(result.stdout.strip())
    except Exception as e:
        print(f"Failed to get number of CPU cores: {e}")
        return 1  # Default to 1 if there is an error

# Function to get text from the URL
def get_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except requests.RequestException as e:
        print(f"Failed to fetch text from URL {url}: {e}")
        return ""

# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
    text_vect = vectorizer.transform([text])
    prediction = model.predict(text_vect)[0]
    proba = model.predict_proba(text_vect)[0]
    sentiment_score = np.max(proba)  # Take the probability of the predicted class as the score
    return prediction, sentiment_score

# Function to perform sentiment analysis for each keyword
def perform_keyword_sentiment_analysis(text, keywords):
    keyword_sentiments = {}
    for keyword in keywords:
        # Extract sentences containing the keyword
        sentences = re.findall(r'[^.!?]*\b{}\b[^.!?]*'.format(re.escape(keyword)), text, re.IGNORECASE)
        if sentences:
            keyword_text = ' '.join(sentences)
            sentiment, score = perform_sentiment_analysis(keyword_text)
            keyword_sentiments[keyword] = {
                'sentiment': sentiment,
                'score': score
            }
        else:
            keyword_sentiments[keyword] = {
                'sentiment': 'neutral',
                'score': 0.0
            }  # No sentences found for the keyword
    return keyword_sentiments

# Function to process a single document
def process_document(document):
    doc_id = document.get("_id")
    url = document.get("url", "")
    keywords = document.get("keywords", "")

    if url and keywords:
        # Handle both string and list types for keywords
        if isinstance(keywords, str):
            # If keywords is a string, split it by commas
            phrases = [phrase.strip() for phrase in keywords.split(',')]
        elif isinstance(keywords, list):
            # If keywords is already a list, use it directly
            phrases = [phrase.strip() for phrase in keywords]
        else:
            print(f"Unexpected data type for keywords in document ID {doc_id}: {type(keywords)}")
            return  # Skip processing if the data type is unexpected

        if not phrases:
            print(f"Document with ID {doc_id} has empty keywords. Skipping detailed analysis.")
            return

        # Extract text from URL
        text = get_text_from_url(url)

        # Perform overall sentiment analysis
        overall_sentiment, overall_score = perform_sentiment_analysis(text)

        # Perform sentiment analysis for each keyword
        keyword_sentiments = perform_keyword_sentiment_analysis(text, phrases)

        # Prepare analysis data
        analysis_data = {
            "khaled analysis": {
                "overall_sentiment": {
                    "sentiment": overall_sentiment,
                    "score": overall_score
                },
                "keyword_sentiments": keyword_sentiments
            }
        }

        # Update the document with the analysis data
        collection.update_one(
            {"_id": doc_id},
            {"$set": {"analysis": analysis_data}}
        )
        print(f"Updated document with ID: {doc_id}")

# Analyze and update documents using parallel processing
def analyze_and_update_documents():
    # Find documents that do not have an 'analysis.khaled analysis' field
    documents = list(collection.find({"analysis.khaled analysis": {"$exists": False}}))

    if not documents:
        print("No documents to process. Exiting...")
        return

    # Determine the number of CPU cores
    num_cores = get_cpu_cores()

    # Create a ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(process_document, doc) for doc in documents]
        
        try:
            # Monitor the completion of tasks
            for future in as_completed(futures):
                try:
                    future.result()  # To handle any exception raised by process_document
                except Exception as e:
                    print(f"Error processing document: {e}")
        except KeyboardInterrupt:
            print("Processing interrupted. Shutting down...")
            # Shut down the executor gracefully
            executor.shutdown(wait=False, cancel_futures=True)
            print("Shutdown complete.")

    # Check if there are any documents without 'analysis.khaled analysis' field
    count_missing_analysis = collection.count_documents({"analysis.khaled analysis": {"$exists": False}})
    if count_missing_analysis == 0:
        print("All articles now contain the 'analysis.khaled analysis' field.")
    else:
        print(f"{count_missing_analysis} articles are still missing the 'analysis.khaled analysis' field.")

# Run the analysis and update process
if __name__ == "__main__":
    analyze_and_update_documents()
