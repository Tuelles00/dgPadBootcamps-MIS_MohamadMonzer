import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, wait_fixed, stop_after_attempt

# Function to fetch and parse a sitemap with retry logic
@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def fetch_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we raise an error for bad responses
    return BeautifulSoup(response.content, 'xml')

# Function to count articles in a given sitemap URL
@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def count_articles_in_sitemap(sitemap_url):
    sitemap_soup = fetch_sitemap(sitemap_url)
    article_urls = [loc.text for loc in sitemap_soup.find_all("loc")]
    return len(article_urls)

# Number of threads for concurrent processing
def get_cpu_cores():
    try:
        result = subprocess.run(['nproc'], stdout=subprocess.PIPE, text=True)
        return int(result.stdout.strip())
    except Exception:
        return 1  # Default to 1 if there is an error

num_threads = get_cpu_cores()

# Main script to count articles in all sitemaps
def main():
    sitemap_index_url = "https://www.almayadeen.net/sitemaps/all.xml"
    sitemap_soup = fetch_sitemap(sitemap_index_url)
    monthly_sitemaps = [loc.text for loc in sitemap_soup.find_all("loc")]

    sitemap_article_counts = {}

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(count_articles_in_sitemap, url): url for url in monthly_sitemaps}
        
        for future in as_completed(futures):
            sitemap_url = futures[future]
            try:
                article_count = future.result()
                sitemap_article_counts[sitemap_url] = article_count
                print(f"Sitemap URL: {sitemap_url}, Articles Count: {article_count}")
            except Exception as e:
                print(f"Failed to count articles for {sitemap_url}: {e}")

    total_articles = sum(sitemap_article_counts.values())
    print("\nSummary:")
    for url, count in sitemap_article_counts.items():
        print(f"Sitemap URL = {url}, Articles in each = {count}")
    print(f"Total articles count = {total_articles}")

if __name__ == "__main__":
    main()