import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load data
folder_neg = 'data/Negative'
folder_pos = 'data/Positive'

neg_list = []
for n in os.listdir(folder_neg):
    with open(os.path.join(folder_neg, n), 'r', encoding='utf-8', errors='ignore') as file:
        for s in file:
            neg_list.append((s.strip("\ufeff").strip(), 'negative'))

pos_list = []
for f in glob.glob('data/Positive/*.txt'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as file:
        for s in file:
            pos_list.append((s.strip("\ufeff").strip(), 'positive'))

# Combine lists
texts = [text for text, _ in neg_list + pos_list]
labels = [label for _, label in neg_list + pos_list]

# Split data
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)

# Vectorize text
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# Save model and vectorizer
with open('sentiment_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# Evaluate model
print(f"Model accuracy: {model.score(X_test_vect, y_test):.4f}")
