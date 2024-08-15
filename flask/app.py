from flask import Flask, render_template, redirect, url_for, send_from_directory, Response, jsonify
import subprocess
import os
import logging
import json

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Path to the frequent_keywords directory
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frequent_keywords'))
top_keywords_json_path = os.path.join(script_dir, 'top_keywords.json')
top_keywords_by_month_json_path = os.path.join(script_dir, 'top_keywords_by_month.json')
script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents.py')
monthly_script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents_each_month_year.py')

# Path to the count_check_debugg directory
count_check_debugg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'count_check_debugg'))
txt_file_path = os.path.join(count_check_debugg_dir, 'article_counts.txt')
script_path_count = os.path.join(count_check_debugg_dir, 'count_the_nb_of_articles_at_ALMayadin.py')

# Path to the Hidden_patterns directory
hidden_patterns_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Hidden_patterns'))
detect_script_path = os.path.join(hidden_patterns_dir, 'detect_hidden_patterns.py')
detailed_patterns_path = os.path.join(hidden_patterns_dir, 'detailed_patterns.json')

@app.route('/')
def index():
    return render_template('index.html')

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
    # Load the JSON file content
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

@app.route('/refresh_counts')
def refresh_counts():
    logging.debug(f"Running script: {script_path_count}")
    subprocess.run(['python3', script_path_count], check=True)
    return redirect(url_for('graph'))

@app.route('/run_script', methods=['POST'])
def run_script():
    logging.debug(f"Running script: {script_path}")
    subprocess.run(['python3', script_path], check=True)
    return {'status': 'success'}

@app.route('/run_monthly_script', methods=['POST'])
def run_monthly_script():
    logging.debug(f"Running monthly script: {monthly_script_path}")
    try:
        subprocess.run(['python3', monthly_script_path], check=True)
        logging.info("Monthly script executed successfully")
        return {'status': 'success'}
    except subprocess.CalledProcessError as e:
        logging.error(f"Monthly script failed with error: {e}")
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/run_detect_patterns', methods=['POST'])
def run_detect_patterns():
    logging.debug(f"Running detection script: {detect_script_path}")
    try:
        subprocess.run(['python3', detect_script_path], check=True)
        logging.info("Detection script executed successfully")
        return {'status': 'success'}
    except subprocess.CalledProcessError as e:
        logging.error(f"Detection script failed with error: {e}")
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
