import json
from transformers import pipeline

# Load keywords from JSON file
def load_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Initialize a zero-shot classification pipeline
def initialize_classifier():
    return pipeline("zero-shot-classification")

# Define candidate labels for categories
candidate_labels = ["Palestine", "Israel", "Gaza", "Media", "Conflict", "War", "Resistance"]

# Classify a single keyword
def classify_keyword(classifier, keyword):
    result = classifier(keyword, candidate_labels)
    return result['labels'][0]  # Return the most likely category

# Categorize keywords based on classification results
def categorize_keywords(keywords_data, classifier):
    categorized_keywords = {label: [] for label in candidate_labels}

    for category, kwds in keywords_data.items():
        for keyword in kwds:
            detected_category = classify_keyword(classifier, keyword)
            categorized_keywords[detected_category].append(keyword)

    return categorized_keywords

# Save categorized keywords to JSON file
def save_categorized_keywords(file_path, categorized_keywords):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(categorized_keywords, file, ensure_ascii=False, indent=4)

def main():
    # File paths
    input_file_path = 'top_keywords.json'
    output_file_path = 'categorized_keywords.json'

    # Load keywords
    keywords_data = load_keywords(input_file_path)

    # Initialize classifier
    classifier = initialize_classifier()

    # Categorize keywords
    categorized_keywords = categorize_keywords(keywords_data, classifier)

    # Save results
    save_categorized_keywords(output_file_path, categorized_keywords)

    print(f"Categorized keywords have been saved to '{output_file_path}'.")

if __name__ == "__main__":
    main()
