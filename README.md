# Article Scraper

This Python project is designed to scrape articles from the Al Mayadin website, parse their content, and store the data in a MongoDB database. It uses several libraries for web scraping, data processing, and concurrency.

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

Usage Instructions
Scrape Data from Al Mayadin

First, use the web_scraper.py script to fetch and parse article data from the Al Mayadin website. This script will scrape the articles and store the data in a MongoDB database.

Generate JSON Files

After you have collected data, use the mongo_data_extractor_year_month.py script to convert the MongoDB data into JSON files. This script will create a directory named allJson_files containing JSON files for each year and month based on the collected data.

Run the Flask Application

Navigate to the flask directory where the Flask application is located. Run the app.py script to start the Flask server:

cd path/to/flask
python app.py


Additional Scripts
count_check_debugg: Use this script to count the number of available articles for each year and month at Al Mayadin. It works in conjunction with the MongoDB_available_year_month_summary.py script.

MongoDB_available_year_month_summary.py: This script allows you to check all the years and months that have been crawled and stored in MongoDB. It provides a summary of available data based on year and month.