import requests
from bs4 import BeautifulSoup
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import subprocess
from pymongo import MongoClient, errors
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type, RetryError
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# Define the Article dataclass
@dataclass
class Article:
    url: str
    postid: Optional[str] = None
    title: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    thumbnail: Optional[str] = None
    video_duration: Optional[str] = None
    word_count: Optional[str] = None
    lang: Optional[str] = None
    published_time: Optional[str] = None
    last_updated: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    classes: List[Dict] = field(default_factory=list)
    text: Optional[str] = None
    filename: Optional[str] = None

# Custom logger for tenacity retries
def log_retry(retry_state):
    print(f"Retrying {retry_state.fn.__name__} due to {retry_state.outcome.exception()}. Attempt {retry_state.attempt_number} of {retry_state.retry_state.max_attempt_number}.")

# Function to fetch and parse a sitemap with retry logic
@retry(wait=wait_fixed(2), stop=stop_after_attempt(5), retry=retry_if_exception_type(requests.RequestException), after=log_retry)
def fetch_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we raise an error for bad responses
    return BeautifulSoup(response.content, 'xml')

# Function to count articles in a given sitemap URL with retry logic
def count_articles_in_sitemap(sitemap_url):
    try:
        sitemap_soup = fetch_sitemap(sitemap_url)
        article_urls = [loc.text for loc in sitemap_soup.find_all("loc")]
        return len(article_urls)
    except RetryError as e:
        print(f"Skipping sitemap {sitemap_url} after failed attempts: {e}")
        return 0

# Function to fetch and parse an article with retry logic
@retry(wait=wait_fixed(2), stop=stop_after_attempt(5), retry=retry_if_exception_type(requests.RequestException), after=log_retry)
def fetch_article(article_url, filename):
    try:
        article_response = requests.get(article_url)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.content, 'html.parser')

        script_tag = article_soup.find('script', type='text/tawsiyat')
        metadata = {}
        if script_tag:
            metadata = json.loads(script_tag.string.strip())

        # Convert keywords to list if it's a string
        keywords = metadata.get("keywords", "").split(',') if isinstance(metadata.get("keywords", ""), str) else metadata.get("keywords", [])

        paragraphs = article_soup.find_all('p')
        article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])

        article = Article(
            url=metadata.get("url", article_url),
            postid=metadata.get("postid"),
            title=metadata.get("title"),
            keywords=keywords,
            thumbnail=metadata.get("thumbnail"),
            video_duration=metadata.get("video_duration"),
            word_count=metadata.get("word_count"),
            lang=metadata.get("lang"),
            published_time=metadata.get("published_time"),
            last_updated=metadata.get("last_updated"),
            description=metadata.get("description"),
            author=metadata.get("author"),
            classes=metadata.get("classes", []),
            text=article_text,
            filename=filename
        )

        return article

    except RetryError as e:
        print(f"Skipping article {article_url} after failed attempts: {e}")
        return None

# Function to get the number of CPU cores
def get_cpu_cores():
    try:
        result = subprocess.run(['nproc'], stdout=subprocess.PIPE, text=True)
        print(f"Number of CPUs is {result.stdout.strip()}")
        return int(result.stdout.strip())
    except Exception as e:
        print(f"Failed to get number of CPU cores: {e}")
        return 1  # Default to 1 if there is an error

# Function to save all data from MongoDB to a JSON file
def save_mongodb_to_json():
    # Reconnect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['articles_db']
    collection = db['articles']  # Collection name

    # Retrieve all documents from the collection
    try:
        articles = list(collection.find({}))
    except errors.PyMongoError as e:
        print(f"Error retrieving documents from MongoDB: {e}")
        client.close()
        return

    # Define the output file path
    output_file = 'articles_db_data.json'
    
    # Save documents to JSON file with UTF-8 encoding
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, default=str, indent=4)  # Ensure ASCII is not escaped
        print(f"Data successfully saved to {output_file}")
    except IOError as e:
        print(f"Error saving data to JSON file: {e}")

    # Close the MongoDB connection
    client.close()


# Number of threads for concurrent processing
num_threads = get_cpu_cores()

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string if needed
db = client['articles_db']  # Updated database name

# Ensure the unique index is created on the 'url' field
collection = db['articles']  # Collection name
try:
    collection.create_index([('url', 1)], unique=True)
    print("Index created successfully.")
except errors.DuplicateKeyError as e:
    print(f"Index creation failed: {e}")

# Function to get the year and month for MongoDB document naming
def extract_year_month(sitemap_url):
    year_month = sitemap_url.split('-')[-2:]
    year = year_month[0]
    month = year_month[1].split('.')[0]
    return year, month

# Step 1: Retrieve monthly sitemaps from the main sitemap index
sitemap_index_url = "https://www.almayadeen.net/sitemaps/all.xml"
try:
    sitemap_soup = fetch_sitemap(sitemap_index_url)
    monthly_sitemaps = [loc.text for loc in sitemap_soup.find_all("loc")]
except Exception as e:
    print(f"Failed to fetch sitemap index: {e}")
    monthly_sitemaps = []

# Ask the user for the year to process
year_to_process = input("Enter the year to scrape data for (e.g., 2024): ")

# Global counters
total_articles_count = 0
total_articles_saved = 0
total_articles_limit = 10000

# Define batch size for processing articles
batch_size = 50  # Adjust based on system performance

# Function to process a single sitemap
def process_sitemap(sitemap_url):
    global total_articles_count, total_articles_saved

    # Extract the year and month from the sitemap URL for MongoDB document naming
    year, month = extract_year_month(sitemap_url)
    
    # Skip if the year does not match the one we're interested in
    if year != year_to_process:
        return

    if total_articles_count >= total_articles_limit:
        return

    # Count articles in the sitemap
    total_articles_in_sitemap = count_articles_in_sitemap(sitemap_url)
    if total_articles_in_sitemap == 0:
        print(f"Skipping sitemap {sitemap_url} due to failure in counting articles.")
        return

    print(f"Sitemap URL: {sitemap_url}, Number of articles: {total_articles_in_sitemap}")

    print(f"Processing sitemap {sitemap_url}")
    try:
        monthly_soup = fetch_sitemap(sitemap_url)
        article_urls = [loc.text for loc in monthly_soup.find_all("loc")]
    except RetryError as e:
        print(f"Skipping sitemap {sitemap_url} after failed attempts: {e}")
        return

    filename = f"articles_{year}_{month}"

    # Initialize the count for remaining articles in this sitemap
    remaining_articles_in_sitemap = total_articles_in_sitemap

    # Process articles in chunks to handle large numbers efficiently
    for i in range(0, len(article_urls), batch_size):
        if total_articles_count >= total_articles_limit:
            break

        batch_urls = article_urls[i:i + batch_size]
        articles_data = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(fetch_article, url, filename): url for url in batch_urls}
            
            for future in as_completed(futures):
                article_data = future.result()
                if article_data:
                    articles_data.append(article_data)
                    total_articles_count += 1
                    remaining_articles_in_sitemap -= 1

                    # Save to MongoDB
                    try:
                        collection.update_one({'url': article_data.url}, {'$set': article_data.__dict__}, upsert=True)
                        total_articles_saved += 1
                    except errors.DuplicateKeyError:
                        # Handle duplicate entries if needed
                        pass
                    except errors.PyMongoError as e:
                        print(f"Error saving article to MongoDB: {e}")

                    print(f"Processed article {article_data.url}")

        print(f"Remaining articles in sitemap {sitemap_url}: {remaining_articles_in_sitemap}")
        print(f"Total articles processed: {total_articles_count}")

    print(f"Finished processing sitemap {sitemap_url}. Total articles processed: {total_articles_count}")

# Main processing loop
try:
    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_sitemap, url) for url in monthly_sitemaps]
        for future in as_completed(futures):
            future.result()  # This will also raise exceptions if any occurred
    print(f"Getting year {year_to_process} successful. Data saved to MongoDB.")
except KeyboardInterrupt:
    print("Interrupted by user. Saving data to JSON file...")
    save_mongodb_to_json()
    print("Data successfully saved to JSON file. Exiting.")
    client.close()
    print("MongoDB connection closed.")
    print(f"Total articles processed: {total_articles_count}")
    print(f"Total articles saved to MongoDB: {total_articles_saved}")
