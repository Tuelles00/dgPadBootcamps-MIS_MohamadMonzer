
```markdown
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
- `pymongo`: For interacting with MongoDB.
- `tenacity`: For retrying operations with exponential backoff.
- `concurrent.futures`: For managing concurrent tasks.
- `dataclasses`: For defining simple data structures.
- `pandas`: For data manipulation and analysis.
- `dateutil`: For parsing and handling dates.

You can install these libraries using `pip`. Run the following command:

```bash
pip install requests beautifulsoup4 pymongo tenacity pandas python-dateutil
```

## Generating JSON Files

After fetching and processing all articles from Al Mayadin, you can generate JSON files from MongoDB based on year and month. To do this, use the script `mongo_data_extractor_year_month.py`. This script will generate a directory called `allJson_files` containing all available JSON files for each year and month.

## Additional Scripts

- **`count_check_debugg`**: Use this script to count the number of available articles for each year and month at Al Mayadin. It works in conjunction with the `MongoDB_available_year_month_summary.py` script.

- **`MongoDB_available_year_month_summary.py`**: This script allows you to check all the years and months that have been crawled and stored in MongoDB. It provides a summary of available data based on year and month.

## Running the Flask Application

The project includes a Flask application located in the `flask` directory. To run the application, navigate to this directory and start the Flask server:

```bash
cd flask
python app.py
```

Ensure that all required libraries are installed in your environment before running the Flask application.
```

This README provides a comprehensive overview of the project, including library dependencies and installation instructions.