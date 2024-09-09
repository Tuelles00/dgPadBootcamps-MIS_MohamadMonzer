from pymongo import MongoClient
import stanza
import re
import subprocess

# Initialize the Arabic NLP pipeline
nlp = stanza.Pipeline('ar')

# Function to remove English words from text
def remove_english(text):
    # Regex pattern to match English words
    pattern = r'[a-zA-Z]+'
    # Remove English words
    cleaned_text = re.sub(pattern, '', text)
    # Remove extra commas and spaces
    cleaned_text = re.sub(r',\s*', ', ', cleaned_text).strip()
    return cleaned_text

# Function to classify keywords
def classify_keywords(keywords):
    print(f'Original Keywords: {keywords}')
    cleaned_keywords = remove_english(keywords)
    print(f'Cleaned Keywords: {cleaned_keywords}')
    
    if cleaned_keywords:
        print('Text is cleaned')
        try:
            # Process the cleaned Arabic text
            doc = nlp(cleaned_keywords)
            print('Doc start')
            results = {'persons': [], 'locations': [], 'organizations': []}
            for ent in doc.entities:
                print(f'Entity: {ent.text}, Type: {ent.type}')
                if ent.type == 'PER':
                    results['persons'].append(ent.text)
                elif ent.type == 'LOC':
                    results['locations'].append(ent.text)
                elif ent.type == 'ORG':
                    results['organizations'].append(ent.text)
            print(f'Classification Results: {results}')
            return results
        except Exception as e:
            print(f'Error processing keywords: {e}')
            return {'persons': [], 'locations': [], 'organizations': []}
    else:
        return {'persons': [], 'locations': [], 'organizations': []}

# Function to process a single document
def process_document(document):
    if 'keywords' in document:
        keywords = document['keywords']
        classified_keywords = classify_keywords(keywords)
        result = {
            'classification': classified_keywords
        }
        return document['_id'], result
    return None

# Function to get the number of CPU cores
def get_cpu_cores():
    try:
        result = subprocess.run(['nproc'], stdout=subprocess.PIPE, text=True)
        return int(result.stdout.strip())
    except Exception as e:
        print(f"Failed to get number of CPU cores: {e}")
        return 1  # Default to 1 if there is an error

# MongoDB setup
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']
stanza_collection = db['organization_categorization']

# Get number of CPU cores
num_cores = get_cpu_cores()

# Process documents in parallel
def main():
    # Fetch all documents that do not have 'organization_categorization.stanza' field
    documents = collection.find({
        "organization_categorization.stanza": {"$exists": False}
    })

    # Optionally, test with a limited number of documents to simplify debugging
    documents = list(documents)[:100]

    # Sequential processing for debugging
    for doc in documents:
        result = process_document(doc)
        if result:
            doc_id, classification_result = result
            # Update the document with classification results
            collection.update_one(
                {'_id': doc_id},
                {'$set': {'organization_categorization.stanza': classification_result}}
            )
            print(f'Updated document ID: {doc_id}')

    print("Classification results updated in MongoDB.")

if __name__ == "__main__":
    main()
