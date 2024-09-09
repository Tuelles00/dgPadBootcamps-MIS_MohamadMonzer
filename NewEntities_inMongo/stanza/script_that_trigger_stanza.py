import subprocess
import time
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

def check_documents_remaining():
    # Check if there are any documents without the 'organization_categorization.stanza' field
    count = collection.count_documents({
        "organization_categorization.stanza": {"$exists": False}
    })
    return count

def run_classification_script():
    try:
        result = subprocess.run(['python3', 'classification_stanza_person_location.py'], check=True)
        print("Classification script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running classification script: {e}")

def main():
    while check_documents_remaining() > 0:
        run_classification_script()
        print("Classification results updated in MongoDB.")
        time.sleep(5)  # Wait for 5 seconds before re-running

    print("All documents have been processed.")

if __name__ == "__main__":
    main()
