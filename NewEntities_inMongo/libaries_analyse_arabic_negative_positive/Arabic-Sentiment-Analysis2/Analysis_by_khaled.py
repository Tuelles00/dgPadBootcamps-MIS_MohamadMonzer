import pymongo
from bson.objectid import ObjectId
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from pymongo import MongoClient
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

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

# Function to count phrase occurrences
def count_phrases(text, phrases):
    text = re.sub(r'\s+', ' ', text).strip()
    phrase_counter = Counter()
    for phrase in phrases:
        count = len(re.findall(re.escape(phrase), text))
        phrase_counter[phrase] = count
    return phrase_counter

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

        # Extract text from URL
        text = get_text_from_url(url)

        # Analyze text overall
        total_analysis = count_phrases(text, phrases)

        # Prepare analysis data
        analysis_data = {
            "khaled analysis": {
                "total_analysis": total_analysis
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
    # Find all documents that do not have an 'analysis.khaled analysis' field
    documents = list(collection.find({"analysis.khaled analysis": {"$exists": False}}))

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

    # Check for documents with missing 'analysis.khaled analysis' and empty 'keywords'
    count_missing_keywords = collection.count_documents({"analysis.khaled analysis": {"$exists": False}, "keywords": {"$in": [None, ""]}})
    if count_missing_keywords > 0:
        print(f"{count_missing_keywords} articles are missing 'analysis.khaled analysis' and have empty 'keywords'.")

# Run the analysis and update process
if __name__ == "__main__":
    analyze_and_update_documents()
