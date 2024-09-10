from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash 
from bson import ObjectId
from datetime import datetime  
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import nltk
from flask_caching import Cache
from pymongo import MongoClient
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import threading
import subprocess
import os
import logging
import signal
import sys
from textblob import TextBlob
from flask import Flask, render_template, redirect, url_for, send_from_directory, jsonify, request, session
import json
# from camel_tools.sentiment import SentimentAnalyzer
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re  
from datetime import datetime


warnings.simplefilter('ignore', InsecureRequestWarning)



app = Flask(__name__, template_folder='templates2')
app.secret_key = 'root_' 

# Set session lifetime to 5 minutes
# app.permanent_session_lifetime = timedelta(minutes=1)

# @app.before_request
# def clear_session_on_startup():
#     session.clear()


# Configure caching
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 1800
cache = Cache(app)

# Establish MongoDB connection
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']
auth_collection = db['auth']  # Collection for authentication








app.permanent_session_lifetime = timedelta(minutes=1)
@app.before_request
def clear_session_on_every_request():
   # session.clear()
   pass






textblob_analyzer = TextBlob

# Helper function to extract year and month from filename
def extract_year_month(filename):
    match = re.search(r'articles_(\d{4})_(\d{2})', filename)
    if match:
        year, month = match.groups()
        return year, month
    return None, None



#detect trend
@app.route('/trends_over_time')
def trends_over_time():
     # Aggregation to get trends over all years
    pipeline_all_years = [
        {
            "$project": {
                "year_month": {
                    "$concat": [
                        {"$substr": ["$published_time", 0, 4]},  # Extract year
                        "_",
                        {"$substr": ["$published_time", 5, 2]}   # Extract month
                    ]
                },
                "persons": {
                    "$ifNull": ["$organization_categorization.stanza.classification.persons", []]
                },
                "locations": {
                    "$ifNull": ["$organization_categorization.stanza.classification.locations", []]
                },
                "organizations": {
                    "$ifNull": ["$organization_categorization.stanza.classification.organizations", []]
                }
            }
        },
        {
            "$group": {
                "_id": "$year_month",
                "persons_count": {"$sum": {"$size": "$persons"}},
                "locations_count": {"$sum": {"$size": "$locations"}},
                "organizations_count": {"$sum": {"$size": "$organizations"}}
            }
        },
        {"$sort": {"_id": -1}}  # Sort by year_month in descending order
    ]

    # Aggregation to get trends for the last year by month
    current_year = datetime.now().year
    pipeline_last_year = [
        {"$match": {"$expr": {"$eq": [{"$substr": ["$published_time", 0, 4]}, str(current_year)]}}},
        {
            "$project": {
                "month": {"$substr": ["$published_time", 5, 2]},  # Extract month
                "personCount": {
                    "$cond": {
                        "if": {"$isArray": {"$ifNull": ["$organization_categorization.stanza.classification.persons", []]}},
                        "then": {"$size": {"$ifNull": ["$organization_categorization.stanza.classification.persons", []]}},
                        "else": 0
                    }
                },
                "locationCount": {
                    "$cond": {
                        "if": {"$isArray": {"$ifNull": ["$organization_categorization.stanza.classification.locations", []]}},
                        "then": {"$size": {"$ifNull": ["$organization_categorization.stanza.classification.locations", []]}},
                        "else": 0
                    }
                },
                "organizationCount": {
                    "$cond": {
                        "if": {"$isArray": {"$ifNull": ["$organization_categorization.stanza.classification.organizations", []]}},
                        "then": {"$size": {"$ifNull": ["$organization_categorization.stanza.classification.organizations", []]}},
                        "else": 0
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$month",
                "persons_count": {"$sum": "$personCount"},
                "locations_count": {"$sum": "$locationCount"},
                "organizations_count": {"$sum": "$organizationCount"}
            }
        },
        {"$sort": {"_id": 1}}  # Sort by month in ascending order
    ]

    trends_all_years = list(collection.aggregate(pipeline_all_years))
    trends_last_year = list(collection.aggregate(pipeline_last_year))

    return render_template('analysis/trends_over_time.html', trends_all_years=trends_all_years, trends_last_year=trends_last_year)



@app.route('/trends_over_time_by_words')
# @cache.cached(timeout=300)  # Cache for 5 minutes (300 seconds)
def trends_over_time_by_words():
    current_year = datetime.now().year 

    # Aggregation pipelines
    pipeline_top_keywords = [
        {
            "$unwind": "$organization_categorization.stanza.classification.persons"
        },
        {
            "$group": {
                "_id": "$organization_categorization.stanza.classification.persons",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    pipeline_top_locations = [
        {
            "$unwind": "$organization_categorization.stanza.classification.locations"
        },
        {
            "$group": {
                "_id": "$organization_categorization.stanza.classification.locations",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    pipeline_top_organizations = [
        {
            "$unwind": "$organization_categorization.stanza.classification.organizations"
        },
        {
            "$group": {
                "_id": "$organization_categorization.stanza.classification.organizations",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    pipeline_current_year_persons = [
        {
            "$match": {
                "filename": {
                    "$regex": f"^articles_{current_year}_",
                    "$options": "i"
                }
            }
        },
        {
            "$unwind": "$organization_categorization.stanza.classification.persons"
        },
        {
            "$group": {
                "_id": "$organization_categorization.stanza.classification.persons",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    pipeline_current_year_locations = [
        {
            "$match": {
                "filename": {
                    "$regex": f"^articles_{current_year}_",
                    "$options": "i"
                }
            }
        },
        {
            "$unwind": "$organization_categorization.stanza.classification.locations"
        },
        {
            "$group": {
                "_id": "$organization_categorization.stanza.classification.locations",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    pipeline_current_year_organizations = [
        {
            "$match": {
                "filename": {
                    "$regex": f"^articles_{current_year}_",
                    "$options": "i"
                }
            }
        },
        {
            "$unwind": "$organization_categorization.stanza.classification.organizations"
        },
        {
            "$group": {
                "_id": "$organization_categorization.stanza.classification.organizations",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    # Run aggregations
    top_persons = list(collection.aggregate(pipeline_top_keywords))
    top_locations = list(collection.aggregate(pipeline_top_locations))
    top_organizations = list(collection.aggregate(pipeline_top_organizations))

    top_persons_last_year = list(collection.aggregate(pipeline_current_year_persons))
    top_locations_last_year = list(collection.aggregate(pipeline_current_year_locations))
    top_organizations_last_year = list(collection.aggregate(pipeline_current_year_organizations))

    print("Top Persons Last Year:", top_persons_last_year)
    print("Top Locations Last Year:", top_locations_last_year)
    print("Top Organizations Last Year:", top_organizations_last_year)


    # Handle potential empty or None results
    return render_template(
        'analysis/trends_over_time_by_words.html',
        top_persons=top_persons or [],
        top_locations=top_locations or [],
        top_organizations=top_organizations or [],
        top_persons_last_year=top_persons_last_year or [],
        top_locations_last_year=top_locations_last_year or [],
        top_organizations_last_year=top_organizations_last_year or []
    )


###################analysis.khaled analysis.keywords
@app.route('/articles_by_sentiment', methods=['GET', 'POST'])
def articles_by_sentiment():
    if request.method == 'POST':
        year_month = request.form.get('year_month')
        if year_month:
            filename = f"articles_{year_month}"
            return redirect(url_for('articles_by_sentiment', filename=filename))
        else:
            return "Year and month parameter is missing or invalid."

    filename = request.args.get('filename', '')
    if filename:
        query = {"filename": filename, "analysis.khaled analysis": {"$exists": True}}
        pipeline = [
            {"$match": query},
            {"$project": {
                "postid": 1,
                "filename": 1,
                "overall_sentiment": "$analysis.khaled analysis.overall_sentiment",
                "keyword_sentiments": "$analysis.khaled analysis.keyword_sentiments"
            }}
        ]

        try:
            # Perform the aggregation
            result = list(collection.aggregate(pipeline))
            
            # Handle the result data
            for doc in result:
                doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
                doc.setdefault('overall_sentiment', {})
                doc.setdefault('keyword_sentiments', {})
                doc.setdefault('filename', '')

            # Save the result to a JSON file
            with open('articles_by_sentiment.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            # Return JSON response if the request is AJAX (fetch or XMLHttpRequest)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(result)

            # Otherwise, render the template
            return render_template('analysis/articles_by_sentiment.html', articles=result)
        except Exception as e:
            print("Error:", e)
            return str(e)
    
    # Render the form if filename is not provided
    return render_template('analysis/articles_by_sentiment_form.html')



@app.route('/get_post_details')
def get_post_details():
    postid = request.args.get('postid')
    document = collection.find_one({'postid': postid})

    if document:
        # Ensure keyword_sentiments is properly included in the response
        response = {
            'postid': document.get('postid'),
            'keyword_sentiments': document.get('analysis', {}).get('khaled analysis', {}).get('keyword_sentiments', {})
        }
    else:
        response = {'error': 'Post ID not found'}

    return jsonify(response)

###################analysis.khaled analysis.keywords







def get_word_count_distribution():
    pipeline = [
        {
            "$addFields": {
                "word_count_int": {
                    "$toInt": "$word_count"
                }
            }
        },
        {
            "$bucket": {
                "groupBy": "$word_count_int",
                "boundaries": [0, 101, 301, 501, float('inf')],
                "default": "Other",
                "output": {
                    "count": {"$sum": 1}
                }
            }
        }
    ]
    cursor = collection.aggregate(pipeline)
    result = list(cursor)

    # Define the boundaries and their labels
    boundaries = [0, 101, 301, 501, float('inf')]
    labels = ['low_range', 'medium_range', 'high_range', 'other']

    # Process the results to include the desired formatting
    formatted_result = []
    for i, bucket in enumerate(result):
        if i < len(boundaries) - 1:
            formatted_result.append({
                'range': f'{boundaries[i]}-{boundaries[i+1]}',
                'count': bucket['count']
            })

    return formatted_result



def get_language_counts():
    pipeline = [
        {
            "$group": {
                "_id": "$lang",
                "count": {"$sum": 1}
            }
        }
    ]
    results = collection.aggregate(pipeline)
    return list(results)

def get_articles_updated_after_publication():
    pipeline = [
        {
            "$match": {
                "$expr": {
                    "$ne": ["$published_time", "$last_updated"]
                }
            }
        },
        {
            "$count": "count"
        }
    ]
    results = list(collection.aggregate(pipeline))
    if results:
        count = results[0].get('count', 0)
        #print(f"Debug: Articles Updated After Publication Count: {count}")  # Debug #print
        return count
    return 0

def get_date_counts():
    pipeline_dates = [
        {"$project": {
            "date": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": {
                        "$dateFromString": {
                            "dateString": "$published_time",
                            "format": "%Y-%m-%dT%H:%M:%S%z"
                        }
                    }
                }
            }
        }},
        {"$group": {
            "_id": "$date",
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": -1}}  # Sort by date in descending order
    ]
    results = collection.aggregate(pipeline_dates)
    return list(results)

def get_video_duration_count():
    count = collection.count_documents({'video_duration': {'$ne': None}})
    return count

def get_thumbnail_count():
    pipeline = [
        {"$match": {"thumbnail": {"$ne": None}}},  # Filter for documents where thumbnail is not null
        {"$count": "thumbnail_count"}  # Count the number of documents
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        count = result[0].get('thumbnail_count', 0)
        #print(f"Debug: Thumbnail Count: {count}")  # Debug #print
        return count
    return 0


def get_progress_data():
    # Define the aggregation pipeline
    pipeline = [
        {
            "$project": {
                "categories": {
                    "$filter": {
                        "input": "$classes",
                        "as": "item",
                        "cond": {"$eq": ["$$item.mapping", "category"]}
                    }
                }
            }
        },
        {
            "$addFields": {
                "has_category": {
                    "$gt": [{"$size": "$categories"}, 0]
                }
            }
        },
        {
            "$project": {
                "category": {
                    "$cond": {
                        "if": "$has_category",
                        "then": {"$arrayElemAt": ["$categories.value", 0]},
                        "else": None
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1}
            }
        },
        {
            "$group": {
                "_id": None,
                "categories": {
                    "$push": {
                        "category": "$_id",
                        "count": "$count"
                    }
                },
                "total_with_category": {
                    "$sum": {
                        "$cond": [{ "$ne": ["$_id", None] }, "$count", 0]
                    }
                },
                "total_without_category": {
                    "$sum": {
                        "$cond": [{ "$eq": ["$_id", None] }, "$count", 0]
                    }
                }
            }
        },
        {
            "$project": {
                "categories": 1,
                "total_with_category": 1,
                "total_without_category": 1
            }
        }
    ]

    # Execute the aggregation pipeline
    results = collection.aggregate(pipeline)
    result_data = list(results)[0]  # Get the single document from the results
    categories = result_data.get("categories", [])
    total_with_category = result_data.get("total_with_category", 0)
    total_without_category = result_data.get("total_without_category", 0)

    # Add category for those without a category if not already present
    if total_without_category > 0:
        existing_categories = [item['category'] for item in categories if item['category'] is None]
        if not existing_categories:
            categories.append({
                "category": None,
                "count": total_without_category
            })

    return categories
def get_count_by_date_range(start_time, end_time):
    query = {
        "published_time": {
            "$gte": start_time.isoformat(),
            "$lte": end_time.isoformat()
        }
    }
    count = collection.count_documents(query)
    return count


def get_articles_published_last_hours(hours):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    query = {
        "published_time": {
            "$gte": start_time.isoformat(),
            "$lte": end_time.isoformat()
        }
    }
    articles = list(collection.find(query))
    return articles

def get_article_counts_by_year_month():
    current_year = datetime.now().year
    result = []

    for year in range(2010, current_year + 1):
        for month in range(1, 13):
            pipeline = [
                {
                    "$match": {
                        "published_time": {
                            "$regex": f"^{year}-{month:02d}"
                        }
                    }
                },
                {
                    "$count": "count"
                }
            ]

            cursor = collection.aggregate(pipeline)
            count = list(cursor)
            month_count = count[0]['count'] if count else 0

            if month_count > 0:
                result.append({
                    'year': year,
                    'month': month,
                    'count': month_count
                })
    #print(result)
    return result

# Define the path to the directory containing JSON files for task2 
JSON_DIR =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'task2'))

# To store the process handle
process = None

def load_json(filename):
    with open(os.path.join(JSON_DIR, filename), 'r', encoding='utf-8') as file:
        return json.load(file)



JSON_DIR2 =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task2'))
def load_json2(filename):
    with open(os.path.join(JSON_DIR2, filename), 'r', encoding='utf-8') as file:
        return json.load(file)
    


    ###aggregation3
@app.route('/aggregation3')
def aggregation3():
    # Load JSON files based on the script names
    articles_100_200_specific = load_json2('articles_100_200_specific.json')
    articles_by_count_range_min_max = load_json2('articles_by_count_range_min_max.json')
    articles_by_length_of_titles = load_json2('articles_by_length_of_titles.json')
    articles_by_month = load_json2('articles_by_month.json')
    articles_grouped_by_Coverage = load_json2('articles_grouped_by_Coverage.json')

    # Pass the data to the template
    return render_template('main/aggregation3.html',
                           articles_100_200_specific=articles_100_200_specific,
                           articles_by_count_range_min_max=articles_by_count_range_min_max,
                           articles_by_length_of_titles=articles_by_length_of_titles,
                           articles_by_month=articles_by_month,
                           articles_grouped_by_Coverage=articles_grouped_by_Coverage)


# Define the directory path
JSONupdatelasthourvar_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task2'))

def JSONupdatelasthourvar(filename):
    # Load the JSON file from the defined directory
    file_path = os.path.join(JSONupdatelasthourvar_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
@app.route('/update_charts/<date>')
def update_charts(date):
    # Run the Python script with the date input
    script_path = os.path.join(JSONupdatelasthourvar_DIR, 'article_update_last_hour_var.py')
    subprocess.call(['python3', script_path, date])
    return redirect(url_for('aggregation4'))  # Replace 'aggregation4' with the actual route for rendering the chart page



###aggregation4
@app.route('/aggregation4')
def aggregation4():
    # Load JSON files based on the script names
    articles_in_2024_08_10 = load_json2('articles_in_2024_08_10.json')
    articles_published_last_hour = load_json2('articles_published_last_hour.json')
    articles_with_more_than_500_and_more_than_600_words = load_json2('articles_with_more_than_500_and_more_than_600_words.json')
    count_Israel_hamas_word = load_json2('count_Israel_hamas_word.json')
    top_10_most_updated_by_title = load_json2('top_10_most_updated_by_title.json')

    # Pass the data to the template
    return render_template('main/aggregation4.html',
                           articles_in_2024_08_10=articles_in_2024_08_10,
                           articles_published_last_hour=articles_published_last_hour,
                           articles_with_more_than_500_and_more_than_600_words=articles_with_more_than_500_and_more_than_600_words,
                           count_Israel_hamas_word=count_Israel_hamas_word,
                           top_10_most_updated_by_title=top_10_most_updated_by_title)


###aggregation2
@app.route('/aggregation2')
def aggregation2():
    # Load JSON files specific to aggregation2
    articles_by_coverage = load_json2('articles_by_coverage.json')
    articles_grouped_by_thumbnail_presence = load_json2('articles_grouped_by_thumbnail_presence.json')
    articles_grouped_by_word_count = load_json2('articles_grouped_by_word_count.json')
    articles_updated_after_publication = load_json2('articles_updated_after_publication.json')
    article_count_by_year = load_json2('article_count_by_year.json')
    most_popular_keywords_last_7_days = load_json2('most_popular_keywords_last_7_days.json')
    recent_post_data = load_json2('recent_post_data.json')
    top_10_post_ids_by_lowest_word_count = load_json2('top_10_post_ids_by_lowest_word_count.json')
    top_10_post_ids_by_word_count = load_json2('top_10_post_ids_by_word_count.json')
    video_duration_count = load_json2('video_duration_count.json')

    # Pass the data to the template
    return render_template('main/aggregation2.html',
                           articles_by_coverage=articles_by_coverage,
                           articles_grouped_by_thumbnail_presence=articles_grouped_by_thumbnail_presence,
                           articles_grouped_by_word_count=articles_grouped_by_word_count,
                           articles_updated_after_publication=articles_updated_after_publication,
                           article_count_by_year=article_count_by_year,
                           most_popular_keywords_last_7_days=most_popular_keywords_last_7_days,
                           recent_post_data=recent_post_data,
                           top_10_post_ids_by_lowest_word_count=top_10_post_ids_by_lowest_word_count,
                           top_10_post_ids_by_word_count=top_10_post_ids_by_word_count,
                           video_duration_count=video_duration_count)

#### search and search by author
@app.route('/search', methods=['GET', 'POST'])
def search_articles():
    if request.method == 'POST':
        keyword = request.form['keyword']
        # MongoDB query to find articles with keywords containing the user-input keyword
        query = {'keywords': {'$regex': keyword}}
        articles = collection.find(query, {'postid': 1, 'keywords': 1, 'text': 1, '_id': 0})
        articles_list = []

        for article in articles:
            # Count occurrences of the keyword in the text
            text = article.get('text', '')
            keyword_count = len(re.findall(keyword, text))
            article['keyword_count'] = keyword_count  # Add count to the article dictionary
            articles_list.append(article)

        return render_template('main/search_results.html', articles=articles_list, keyword=keyword)
    
    # Render the search form initially
    return render_template('main/search_form.html')


@app.route('/search_by_author', methods=['GET', 'POST'])
def search_by_author():
    if request.method == 'POST':
        author_name = request.form['author_name']
        # MongoDB query to find articles by the specified author
        pipeline = [
            {
                "$match": {
                    "author": {"$regex": author_name, "$options": "i"}
                }
            },
            {
                "$project": {
                    "postid": 1,
                    "author": 1,
                    "title": 1,
                    "_id": 0
                }
            }
        ]

        # Execute the aggregation pipeline
        results = collection.aggregate(pipeline)

        # Process results to create a list of dictionaries
        articles_by_author = list(results)

        return render_template('main/author_search_results.html', articles=articles_by_author, author_name=author_name)
    
    # Render the search form initially
    return render_template('main/author_search_form.html')
###--------------------------

#### aggregation1
@app.route('/aggregation')
def aggregation():
    # Load all JSON files
    articles_by_author = load_json('author_counts.json')
    articles_by_category = load_json('category_counts.json')
    articles_by_keywords = load_json('keyword_counts.json')
    articles_by_lang = load_json('language_count_summary.json')
    articles_by_word_count = load_json('word_count_summary.json')
    top_10_classes = load_json('top_10_classes.json')
    recent_articles = load_json('recent_articles.json')
    top_author = load_json('Top_author.json')
    top_keywords = load_json('Top_keywords.json')
    articles_counts_by_date = load_json("Article_counts_by_date.json")
 # Load word cloud data
    word_cloud_data = load_json('Top_keywords.json')


    # Pass the data to the template
    return render_template('main/aggregation.html',
                           author_counts=articles_by_author,
                           category_counts=articles_by_category,
                           keyword_counts=articles_by_keywords,
                           language_counts=articles_by_lang,
                           word_count_summary=articles_by_word_count,
                           top_10_classes=top_10_classes,
                           recent_articles=recent_articles,
                           top_author=top_author,
                           top_keywords=top_keywords,
                           articles_counts_by_date=articles_counts_by_date,
			   word_cloud_data=word_cloud_data)





def run_script_in_thread():
    threading.Thread(target=run_initial_script).start()


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Existing data fetching functions
    language_counts = get_language_counts()
    date_counts = get_date_counts()
    video_duration_count = get_video_duration_count()
    thumbnail_count = get_thumbnail_count()
    updated_after_publication_count = get_articles_updated_after_publication()
    word_count_distribution = get_word_count_distribution()
    counts_by_year_month = get_article_counts_by_year_month()
    
    # New function to get progress data
    progress_data = get_progress_data()
    
    return render_template('main/index.html', 
                           language_counts=language_counts, 
                           date_counts=date_counts, 
                           video_duration_count=video_duration_count, 
                           thumbnail_count=thumbnail_count, 
                           updated_after_publication_count=updated_after_publication_count, 
                           word_count_distribution=word_count_distribution,
                           progress_data=progress_data,
                           counts_by_year_month=counts_by_year_month,
                           username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Fetch user from the 'auth' collection
        user = auth_collection.find_one({'username': username})
        
        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('auth/auth.html', error_message='Invalid username or password')

    return render_template('auth/auth.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        existing_user = auth_collection.find_one({'username': username})
        if existing_user:
            return render_template('auth/signup.html', error_message='Username already exists')

        # Hash the password and insert the new user into the database
        hashed_password = generate_password_hash(password)
        auth_collection.insert_one({
            'username': username,
            'password': hashed_password
        })
        
        return redirect(url_for('login'))
    
    return render_template('auth/signup.html')

from functools import wraps





@app.route('/run_script', methods=['POST'])
def run_script():
    run_script_in_thread()
    return redirect(url_for('index'))


@app.route('/articles_published_last_hour')
@cache.cached(timeout=1800, key_prefix='articles_last_hour')
def articles_published_last_hour():
    articles = get_articles_published_last_hours(hours=24)
    return render_template('articles/articles_published_last_hour.html', articles=articles)




def terminate_process(signal, frame):
    if process:
        logging.debug(f"Terminating the script process with PID: {process.pid}")
        process.terminate()
        process.wait()
        logging.info("Process terminated successfully")

    sys.exit(0)





# Load sentiment analysis model (run this only once during initialization)
sentiment_analyzer = pipeline("sentiment-analysis")

def get_articles_published_last_hours(hours):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    query = {
        "published_time": {
            "$gte": start_time.isoformat(),
            "$lte": end_time.isoformat()
        }
    }
    articles = list(collection.find(query))

    # Perform sentiment analysis on article titles
    for article in articles:
        title = article.get('title', '')
        if title:
            sentiment_result = sentiment_analyzer(title)
            article['sentiment'] = sentiment_result[0]  # Adds sentiment score to article data

    return articles






# Ensure you have stopwords for Arabic; if not, you might need to download them
nltk.download('stopwords')
arabic_stopwords = stopwords.words('arabic')

# Topic Modeling using Scikit-learn for Arabic text
def perform_topic_modeling(texts, num_topics=5):
    # Convert texts to a matrix of token counts
    vectorizer = CountVectorizer(stop_words=arabic_stopwords, token_pattern=r'\b\w+\b')  # Adjust token_pattern if needed
    X = vectorizer.fit_transform(texts)

    # Fit the LDA model
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(X)

    # Get topics
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-10:]  # Get top 10 words
        top_words = [feature_names[i] for i in top_words_idx]
        topics.append(f"Topic {topic_idx + 1}: " + ", ".join(top_words))

    return topics

def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

@app.route('/analysis_articles_published_last_hour')
def analysis_articles_published_last_hour():
    try:
        # Fetch articles published in the last 24 hours
        articles = get_articles_published_last_hours(hours=24)
        
        # Convert ObjectId to string
        articles = [{**article, '_id': serialize_objectid(article['_id'])} for article in articles]
        
        # Aggregate sentiment data
        sentiment_scores = [article['sentiment']['score'] for article in articles]
        print(f'sentiment_score: {sentiment_scores}')
        average_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        # Prepare data for the gauge chart
        sentiment_data = {
            'average_score': average_score,
            'min_score': min(sentiment_scores, default=0),
            'max_score': max(sentiment_scores, default=0)
        }
        
        # Extract texts for topic modeling
        texts = [article['text'] for article in articles]
        topics = perform_topic_modeling(texts, num_topics=3)
        
        return render_template('analysis/analysis_articles_last_hour.html', 
                               articles=articles, 
                               sentiment_data=sentiment_data, 
                               topics=topics)
    except ValueError as e:
        # Handle the specific error indicating empty vocabulary
        if "empty vocabulary" in str(e):
            # Run the script to get fresh data
            run_script()

            # Return a loading page to inform the user
            return render_template('analysis/loading.html')

        # Handle any other unexpected errors
        return str(e), 500  # Return the error message for debugging
    
    

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    results = sentiment_analyzer(text)
    return results[0]  # Return the first result


@app.route('/analysis_category_count')
def analysis_category_count():
    category_pipeline = [
    {
        "$project": {
            "categories": {
                "$filter": {
                    "input": "$classes",
                    "as": "item",
                    "cond": {"$eq": ["$$item.mapping", "category"]}
                }
            }
        }
    },
    {
        "$addFields": {
            "has_category": {
                "$gt": [{"$size": "$categories"}, 0]
            }
        }
    },
    {
        "$project": {
            "category": {
                "$cond": {
                    "if": "$has_category",
                    "then": {"$arrayElemAt": ["$categories.value", 0]},
                    "else": None  # Use None for Python
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$category",
            "count": {"$sum": 1}
        }
    },
    {
        "$group": {
            "_id": None,  # Use None for Python
            "categories": {
                "$push": {
                    "category": "$_id",
                    "count": "$count"
                }
            },
            "total_with_category": {
                "$sum": {
                    "$cond": [{"$ne": ["$_id", None]}, "$count", 0]  # Use None for Python
                }
            },
            "total_without_category": {
                "$sum": {
                    "$cond": [{"$eq": ["$_id", None]}, "$count", 0]  # Use None for Python
                }
            }
        }
    },
    {
        "$project": {
            "categories": 1,
            "total_with_category": 1,
            "total_without_category": 1
        }
    }
]


    # Execute the aggregation pipeline
    results = list(collection.aggregate(category_pipeline))
    print("this is the result of analysis category count")
    print(results)

    if results:
        result_data = results[0]
        categories = result_data.get("categories", [])
        total_with_category = result_data.get("total_with_category", 0)
        total_without_category = result_data.get("total_without_category", 0)

        # Perform sentiment analysis
        articles = [
            # Sample data for testing; replace this with your actual article data
            {
                'published_time': '2024-08-30 12:00',
                'title': 'Sample Article',
                'sentiment': analyze_sentiment("Sample text for sentiment analysis")
            }
            # Add more articles if available
        ]

        # Add category for those without a category if not already present
        if total_without_category > 0:
            existing_categories = [item['category'] for item in categories if item['category'] is None]
            if not existing_categories:
                categories.append({
                    "category": None,
                    "count": total_without_category
                })
    else:
        categories = []
        total_with_category = 0
        total_without_category = 0
        articles = []

    return render_template('analysis/analysis_category_count.html',
                           categories=categories,
                           total_with_category=total_with_category,
                           total_without_category=total_without_category,
                           articles=articles)

@app.route('/stanza_classification', methods=['GET', 'POST'])
def stanza_classification():
    # Get search inputs from the user
    person_query = request.form.get('person_query', '').strip()
    location_query = request.form.get('location_query', '').strip()
    organization_query = request.form.get('organization_query', '').strip()

    # Initialize the search queries
    combined_results = []
    query_conditions = []  # A list to store all conditions

    # Check for person_query and add it to the conditions if it exists
    if person_query:
        query_conditions.append({"organization_categorization.stanza.classification.persons": {"$regex": person_query, "$options": "i"}})

    # Check for location_query and add it to the conditions if it exists
    if location_query:
        query_conditions.append({"organization_categorization.stanza.classification.locations": {"$regex": location_query, "$options": "i"}})

    # Check for organization_query and add it to the conditions if it exists
    if organization_query:
        query_conditions.append({"organization_categorization.stanza.classification.organizations": {"$regex": organization_query, "$options": "i"}})

    # Combine conditions into a single query with $and operator
    if query_conditions:
        mongo_query = {"$and": query_conditions}  # Match documents that satisfy all conditions
    else:
        mongo_query = {}  # No search criteria provided, fetch all documents

    # Perform the aggregation with dynamic conditions
    aggregation_pipeline = [
        {"$match": mongo_query},
        {"$project": {
            "postid": 1,
            "persons": "$organization_categorization.stanza.classification.persons",
            "locations": "$organization_categorization.stanza.classification.locations",
            "organizations": "$organization_categorization.stanza.classification.organizations"
        }},
        {"$unwind": {"path": "$persons", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$locations", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$organizations", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": "$postid",  # Group by postid
            "persons": {"$addToSet": "$persons"},
            "locations": {"$addToSet": "$locations"},
            "organizations": {"$addToSet": "$organizations"}
        }}
    ]

    results = list(collection.aggregate(aggregation_pipeline))

    # Extract results for the combined display
    for result in results:
        postid = result.get('_id')
        if person_query:
            combined_results.extend({"category": person, "value": "Person", "postid": postid} for person in result.get('persons', []) if person_query in person)
        if location_query:
            combined_results.extend({"category": location, "value": "Location", "postid": postid} for location in result.get('locations', []) if location_query in location)
        if organization_query:
            combined_results.extend({"category": organization, "value": "Organization", "postid": postid} for organization in result.get('organizations', []) if organization_query in organization)

    return render_template('analysis/stanza_classification.html',
                           person_query=person_query,
                           location_query=location_query,
                           organization_query=organization_query,
                           combined_results=combined_results)


### to fetch news from al mayadin website
# Global news storage
news_storage = []
def fetch_news():
    url = "https://www.almayadeen.net/shortnews"
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if the expected elements are present
    news_blocks = soup.find_all('div', class_='single-latest-news')
    #print("Found News Blocks:", len(news_blocks))  # #print the number of news blocks found

    news_list = []

    for news in news_blocks:
        # #print the full news block to debug extraction issues
        #print("News Block:", news)

        title = news.find('h3').text.strip() if news.find('h3') else "No title found"
        time = news.find('div', class_='time').text.strip() if news.find('div', class_='time') else "No time found"
        date = news.find('div', class_='date').text.strip() if news.find('div', class_='date') else "No date found"
        link = news.find('a')['href'] if news.find('a') else "No link found"
        category = news.find('div', class_='latest-news-meta blue-text').text.strip() if news.find('div', class_='latest-news-meta blue-text') else "No category found"

        news_item = {
            'title': title,
            'time': time,
            'date': date,
            'link': "https://www.almayadeen.net" + link if link != "No link found" else "No link found",
            'category': category
        }

        #print("Extracted News Item:", news_item)  # #print each extracted news item for debugging

        news_list.append(news_item)
    
    return news_list

# Function to update news storage
def update_news_storage():
    global news_storage
    while True:
        new_news = fetch_news()
        for item in new_news:
            if item not in news_storage:
                if len(news_storage) >= 10:  # Limit the number of news items
                    news_storage.pop(0)  # Remove the oldest item
                news_storage.append(item)
        threading.Event().wait(15)  # Wait for 15 seconds

# Start background thread for updating news
threading.Thread(target=update_news_storage, daemon=True).start()

@app.route('/news')
def get_news():
    return jsonify(news_storage)






####main_scripts_forAll.py
main_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main_scripts_forAll.py'))
def run_initial_script():
    """Run the main script on startup in the background."""
    global process
    logging.debug(f"Running initial script in the background: {main_script_path}")
    try:
        process = subprocess.Popen(['python3', main_script_path])  # Run in the background
        logging.info("Initial main script started successfully in the background")
    except Exception as e:
        logging.error(f"Failed to start initial script: {e}")


FLAG_FILE = 'initial_script_done.flag'
def check_and_run_initial_script():
    if not os.path.isfile(FLAG_FILE):
        run_initial_script()
        # Create the flag file to indicate the script has run
        with open(FLAG_FILE, 'w') as f:
            f.write('done')






### to update current month 
def run_script():
    # Correct path relative to the location of app.py
    script_path = '../web_scraper_uptodate_currentmonthonly.py'
    # Get the absolute path
    absolute_script_path = os.path.abspath(script_path)
    subprocess.run(['python', absolute_script_path], check=True)

def initialize_app():
    run_script()



if __name__ == '__main__':
    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGTERM, terminate_process)
    
    # run_initial_script()  # Run the main script at startup in the background
    app.run(host='0.0.0.0', port=5000, debug=True)
