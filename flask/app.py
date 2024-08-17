import subprocess
import os
import logging
import signal
import sys
from flask import Flask, render_template, redirect, url_for, send_from_directory, jsonify
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Path to the main script to run at startup
main_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main_scripts_forAll.py'))

# Paths to various directories and scripts
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frequent_keywords'))
top_keywords_json_path = os.path.join(script_dir, 'top_keywords.json')
top_keywords_by_month_json_path = os.path.join(script_dir, 'top_keywords_by_month.json')
script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents.py')
monthly_script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents_each_month_year.py')

count_check_debugg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'count_check_debugg'))
txt_file_path = os.path.join(count_check_debugg_dir, 'article_counts.txt')
script_path_count = os.path.join(count_check_debugg_dir, 'count_the_nb_of_articles_at_ALMayadin.py')

hidden_patterns_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Hidden_patterns'))
detect_script_path = os.path.join(hidden_patterns_dir, 'detect_hidden_patterns.py')
detailed_patterns_path = os.path.join(hidden_patterns_dir, 'detailed_patterns.json')

# Define the path to the JSON file
video_available_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'video_available'))
json_file_path = os.path.join(video_available_dir, 'categorized_videos_v2.json')
json_file_path2 = os.path.join(video_available_dir, 'categorized_videos_null_duration.json')

# Define the path to the directory containing JSON files for task2 
JSON_DIR =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task2'))

# To store the process handle
process = None

def load_json(filename):
    with open(os.path.join(JSON_DIR, filename), 'r', encoding='utf-8') as file:
        return json.load(file)

# Define the path to the directory containing JSON files for task2  part 2 
JSON_DIR2 =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task22'))

# To store the process handle
process = None

def load_json2(filename):
    with open(os.path.join(JSON_DIR2, filename), 'r', encoding='utf-8') as file:
        return json.load(file)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aggregation2')
def aggregation2():
    # Load JSON files specific to aggregation2
    articles_by_coverage = load_json('articles_by_coverage.json')
    articles_grouped_by_thumbnail_presence = load_json('articles_grouped_by_thumbnail_presence.json')
    articles_grouped_by_word_count = load_json('articles_grouped_by_word_count.json')
    articles_updated_after_publication = load_json('articles_updated_after_publication.json')
    article_count_by_year = load_json('article_count_by_year.json')
    most_popular_keywords_last_7_days = load_json('most_popular_keywords_last_7_days.json')
    recent_post_data = load_json('recent_post_data.json')
    top_10_post_ids_by_lowest_word_count = load_json('top_10_post_ids_by_lowest_word_count.json')
    top_10_post_ids_by_word_count = load_json('top_10_post_ids_by_word_count.json')
    video_duration_count = load_json('video_duration_count.json')

    # Pass the data to the template
    return render_template('aggregation2.html',
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

    # Pass the data to the template
    return render_template('aggregation.html',
                           author_counts=articles_by_author,
                           category_counts=articles_by_category,
                           keyword_counts=articles_by_keywords,
                           language_counts=articles_by_lang,
                           word_count_summary=articles_by_word_count,
                           top_10_classes=top_10_classes,
                           recent_articles=recent_articles,
                           top_author=top_author,
                           top_keywords=top_keywords,
                           articles_counts_by_date=articles_counts_by_date)

@app.route('/video')
def video():
    # Load the categorized videos data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        categorized_videos = json.load(file)

    # Load the categorized videos null duration data
    with open(json_file_path2, 'r', encoding='utf-8') as file:
        categorized_videos_null_duration = json.load(file)
    
    # Render the HTML template with both datasets
    return render_template('video.html',
                            categorized_videos=categorized_videos,
                            categorized_videos_null_duration=categorized_videos_null_duration)

@app.route('/article_counts.txt')
def serve_article_counts():
    logging.debug(f"Serving article_counts.txt from {count_check_debugg_dir}")
    return send_from_directory(count_check_debugg_dir, 'article_counts.txt')

@app.route('/detailed_patterns.json')
def serve_detailed_patterns():
    logging.debug(f"Serving detailed_patterns.json from {hidden_patterns_dir}")
    return send_from_directory(hidden_patterns_dir, 'detailed_patterns.json')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/hidden_patterns')
def hidden_patterns():
    return render_template('hidden_patterns.html')

@app.route('/counter_page')
def counter_page():
    try:
        with open(top_keywords_json_path, 'r', encoding='utf-8') as json_file:
            top_keywords_data = json.load(json_file)
        with open(top_keywords_by_month_json_path, 'r', encoding='utf-8') as json_file:
            top_keywords_by_month_data = json.load(json_file)
        return render_template('counter_page.html', 
                               top_keywords_data=top_keywords_data,
                               top_keywords_by_month_data=top_keywords_by_month_data)
    except Exception as e:
        logging.error(f"Error loading JSON file: {e}")
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/refresh_top_keywords_chart', methods=['POST'])
def refresh_top_keywords_chart():
    logging.debug(f"Running script: {script_path}")
    try:
        subprocess.run(['python3', script_path], check=True)
        logging.info("Top keywords script executed successfully")
        return jsonify({'status': 'success'})
    except subprocess.CalledProcessError as e:
        logging.error(f"Top keywords script failed with error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/refresh_total_occurrences_chart', methods=['POST'])
def refresh_total_occurrences_chart():
    logging.debug(f"Running monthly script: {monthly_script_path}")
    try:
        subprocess.run(['python3', monthly_script_path], check=True)
        logging.info("Monthly script executed successfully")
        return jsonify({'status': 'success'})
    except subprocess.CalledProcessError as e:
        logging.error(f"Monthly script failed with error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/run_detect_patterns', methods=['POST'])
def run_detect_patterns():
    logging.debug(f"Running detection script: {detect_script_path}")
    try:
        subprocess.run(['python3', detect_script_path], check=True)
        logging.info("Detection script executed successfully")
        return jsonify({'status': 'success'})
    except subprocess.CalledProcessError as e:
        logging.error(f"Detection script failed with error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def run_initial_script():
    """Run the main script on startup in the background."""
    global process
    logging.debug(f"Running initial script in the background: {main_script_path}")
    try:
        process = subprocess.Popen(['python3', main_script_path])  # Run in the background
        logging.info("Initial main script started successfully in the background")
    except Exception as e:
        logging.error(f"Failed to start initial script: {e}")

def terminate_process(signal, frame):
    if process:
        logging.debug(f"Terminating the script process with PID: {process.pid}")
        process.terminate()
        process.wait()
        logging.info("Process terminated successfully")

    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGTERM, terminate_process)
    
    run_initial_script()  # Run the main script at startup in the background
    app.run(host='0.0.0.0', port=5000, debug=True)
