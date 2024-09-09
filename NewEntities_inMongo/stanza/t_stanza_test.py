# import stanza

# # Download the Arabic model
# stanza.download('ar')

import stanza
import re

# Initialize the Arabic NLP pipeline
nlp = stanza.Pipeline('ar')

# Sample Arabic text
text = "فرنسا, النيجر, مالي, بوركينا فاسو, الاستعمار الفرنسي, الساحل الأفريقي, دول الساحل الأفريقي, ايكواس, الساحل الافريقي, بوركينافاسو, دول غرب آسيا, تمرد الساحل الأفريقي, تمرّد ثلاثي الساحل الأفريقي, ثلاثي الساحل الأفريقي, الهيمنة الفرنسية, إرث الاستعمار الفرنسي, المجموعة الاقتصادية لغرب اسيا, دول غرب اسيا"

# Function to remove English words from text
def remove_english(text):
    # Regex pattern to match English words
    pattern = r'[a-zA-Z]+'
    # Remove English words
    cleaned_text = re.sub(pattern, '', text)
    # Remove extra commas and spaces
    cleaned_text = re.sub(r',\s*', ', ', cleaned_text).strip()
    return cleaned_text

# Remove English words from the text
cleaned_text = remove_english(text)

# Check if the cleaned text is not empty
if cleaned_text:
    # Process the cleaned Arabic text
    doc = nlp(cleaned_text)

    # Extract and print persons and locations
    for entity in doc.entities:
        if entity.type in ["PER", "LOC"]:
            print(f"Entity: {entity.text}, Type: {entity.type}")
else:
    print("No valid Arabic text found after removing English words.")
