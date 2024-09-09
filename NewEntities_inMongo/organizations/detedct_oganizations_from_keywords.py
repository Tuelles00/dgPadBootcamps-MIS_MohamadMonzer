import pymongo
from pymongo import MongoClient
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# MongoDB setup
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Organization data (should be loaded from your MongoDB collection)
organization_data = [
        {"الاسم": "حزب الله", "النوع": "سياسي", "البلد": "لبنان"},
        {"الاسم": "حماس", "النوع": "سياسي", "البلد": "فلسطين"},
        {"الاسم": "جبهة النصرة", "النوع": "مسلح", "البلد": "سوريا"},
        {"الاسم": "الجيش السوري", "النوع": "عسكري", "البلد": "سوريا"},
        {"الاسم": "الجيش الوطني السوري", "النوع": "مسلح", "البلد": "سوريا"},
        {"الاسم": "إسرائيل", "النوع": "دولة", "البلد": "إسرائيل"},
        {"الاسم": "الجيش الإسرائيلي", "النوع": "عسكري", "البلد": "إسرائيل"},
        {"الاسم": "البرلمان الإسرائيلي", "النوع": "سياسي", "البلد": "إسرائيل"},
        {"الاسم": "أنصار الله", "النوع": "مسلح", "البلد": "اليمن"},
        {"الاسم": "الحكومة اليمنية", "النوع": "سياسي", "البلد": "اليمن"},
        {"الاسم": "الحشد الشعبي", "النوع": "مسلح", "البلد": "العراق"},
        {"الاسم": "الجيش العراقي", "النوع": "عسكري", "البلد": "العراق"},
        {"الاسم": "البرلمان العراقي", "النوع": "سياسي", "البلد": "العراق"},
        {"الاسم": "الحرس الثوري الإيراني", "النوع": "عسكري", "البلد": "إيران"},
        {"الاسم": "الحكومة الإيرانية", "النوع": "سياسي", "البلد": "إيران"},
        {"الاسم": "البرلمان الإيراني", "النوع": "سياسي", "البلد": "إيران"},
        {"الاسم": "الولايات المتحدة الأمريكية", "النوع": "دولة", "البلد": "الولايات المتحدة"},
        {"الاسم": "الجيش الأمريكي", "النوع": "عسكري", "البلد": "الولايات المتحدة"},
        {"الاسم": "البنك الدولي", "النوع": "مالي", "البلد": "الولايات المتحدة"},
        {"الاسم": "الأمم المتحدة", "النوع": "منظمة دولية", "البلد": "الولايات المتحدة"},
        {"الاسم": "فرنسا", "النوع": "دولة", "البلد": "فرنسا"},
        {"الاسم": "الجيش الفرنسي", "النوع": "عسكري", "البلد": "فرنسا"},
        {"الاسم": "الحكومة الفرنسية", "النوع": "سياسي", "البلد": "فرنسا"},
        {"الاسم": "المملكة المتحدة", "النوع": "دولة", "البلد": "المملكة المتحدة"},
        {"الاسم": "الجيش البريطاني", "النوع": "عسكري", "البلد": "المملكة المتحدة"},
        {"الاسم": "الحكومة البريطانية", "النوع": "سياسي", "البلد": "المملكة المتحدة"},
        {"الاسم": "اليونيسف", "النوع": "منظمة دولية", "البلد": "دولي"},
        {"الاسم": "منظمة الصحة العالمية", "النوع": "منظمة دولية", "البلد": "دولي"},
        {"الاسم": "الصليب الأحمر", "النوع": "إنساني", "البلد": "دولي"},
        {"الاسم": "صندوق النقد الدولي", "النوع": "مالي", "البلد": "دولي"},
        {"الاسم": "أمازون", "النوع": "شركة", "البلد": "الولايات المتحدة"},
        {"الاسم": "جوجل", "النوع": "شركة", "البلد": "الولايات المتحدة"},
        {"الاسم": "أبل", "النوع": "شركة", "البلد": "الولايات المتحدة"},
        {"الاسم": "هواوي", "النوع": "شركة", "البلد": "الصين"},
        {"الاسم": "تينسنت", "النوع": "شركة", "البلد": "الصين"},
        {"الاسم": "سامسونج", "النوع": "شركة", "البلد": "كوريا الجنوبية"},
        {"الاسم": "تويوتا", "النوع": "شركة", "البلد": "اليابان"},
        {"الاسم": "فولكسفاجن", "النوع": "شركة", "البلد": "ألمانيا"},
        {"الاسم": "بي بي", "النوع": "شركة", "البلد": "المملكة المتحدة"},
        {"الاسم": "شل", "النوع": "شركة", "البلد": "المملكة المتحدة"},
        {"الاسم": "الولايات المتحدة", "النوع": "دولة", "البلد": "الولايات المتحدة"},
        {"الاسم": "المقاومة الفلسطينية", "النوع": "مسلح", "البلد": "فلسطين"},
        {"الاسم": "الاتحاد الأوروبي", "النوع": "منظمة دولية", "البلد": "أوروبا"},
        {"الاسم": "وزارة الأمن الداخلي الأميركية", "النوع": "حكومي", "البلد": "الولايات المتحدة"},
        {"الاسم": "الحكومة الإسرائيلية", "النوع": "سياسي", "البلد": "إسرائيل"}
    ]



# Function to get the number of CPU cores
def get_cpu_cores():
    try:
        result = subprocess.run(['nproc'], stdout=subprocess.PIPE, text=True)
        return int(result.stdout.strip())
    except Exception as e:
        print(f"Failed to get number of CPU cores: {e}")
        return 1  # Default to 1 if there is an error

# Function to categorize documents based on organization data
def categorize_document(document):
    doc_id = document.get("_id")
    keywords = document.get("keywords", [])

    if isinstance(keywords, str):
        # Convert string keywords to list if necessary
        keywords = [keyword.strip() for keyword in keywords.split(',')]

    if keywords:
        # Check for organization names in keywords
        identified_organizations = [org['الاسم'] for org in organization_data if org['الاسم'] in keywords]
        
        # Prepare categorization data
        categorization_data = {
            "organization_categorization": {
                "identified_organizations": identified_organizations
            }
        }

        # Update the document with the categorization data
        collection.update_one(
            {"_id": doc_id},
            {"$set": categorization_data}
        )
        print(f"Updated document with ID: {doc_id}")

# Categorize and update documents using parallel processing
def categorize_and_update_documents():
    # Find all documents that do not have an 'organization_categorization' field
    documents = list(collection.find({"organization_categorization": {"$exists": False}}))

    # Determine the number of CPU cores
    num_cores = get_cpu_cores()

    # Create a ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(categorize_document, doc) for doc in documents]
        
        try:
            # Monitor the completion of tasks
            for future in as_completed(futures):
                try:
                    future.result()  # To handle any exception raised by categorize_document
                except Exception as e:
                    print(f"Error processing document: {e}")
        except KeyboardInterrupt:
            print("Processing interrupted. Shutting down...")
            # Shut down the executor gracefully
            executor.shutdown(wait=False, cancel_futures=True)
            print("Shutdown complete.")

    # Check if there are any documents without 'organization_categorization' field
    count_missing_categorization = collection.count_documents({"organization_categorization": {"$exists": False}})
    if count_missing_categorization == 0:
        print("All documents now contain the 'organization_categorization' field.")
    else:
        print(f"{count_missing_categorization} documents are still missing the 'organization_categorization' field.")

# Run the categorization and update process
if __name__ == "__main__":
    categorize_and_update_documents()
