# Article Scraper

This Python project is designed to scrape articles from a website, parse their content, and store the data in a MongoDB database. It uses several libraries for web scraping, data processing, and concurrency.

## Features

- Fetch and parse sitemaps.
- Extract article metadata and content.
- Store article data in MongoDB.
- Concurrently process multiple articles for efficiency.

## Libraries

This project requires the following Python libraries:

- `requests`: For making HTTP requests to fetch web pages.
- `beautifulsoup4`: For parsing HTML and XML content.
- `json`: For handling JSON data.
- `pymongo`: For interacting with MongoDB.
- `tenacity`: For retrying operations with exponential backoff.
- `concurrent.futures`: For managing concurrent tasks.
- `subprocess`: For executing system commands.
- `dataclasses`: For defining simple data structures.

You can install these libraries using `pip`. Run the following command:

```bash
pip install requests beautifulsoup4 pymongo tenacity
