from flask import Flask, render_template, redirect, url_for, send_from_directory, Response
import subprocess
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Path to the count_check_debugg directory
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'count_check_debugg'))
txt_file_path = os.path.join(script_dir, 'article_counts.txt')
script_path = os.path.join(script_dir, 'count_the_nb_of_articles_at_ALMayadin.py')

# Path to the Hidden_patterns directory
hidden_patterns_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Hidden_patterns'))
detect_script_path = os.path.join(hidden_patterns_dir, 'detect_hidden_patterns.py')
detailed_patterns_path = os.path.join(hidden_patterns_dir, 'detailed_patterns.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article_counts.txt')
def serve_article_counts():
    logging.debug(f"Serving article_counts.txt from {script_dir}")
    return send_from_directory(script_dir, 'article_counts.txt')

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

@app.route('/refresh_counts')
def refresh_counts():
    logging.debug(f"Running script: {script_path}")
    subprocess.run(['python3', script_path], check=True)
    return redirect(url_for('graph'))

@app.route('/run_script', methods=['POST'])
def run_script():
    logging.debug(f"Running script: {script_path}")
    subprocess.run(['python3', script_path], check=True)
    return {'status': 'success'}

@app.route('/run_detect_patterns', methods=['POST'])
def run_detect_patterns():
    logging.debug(f"Running detection script: {detect_script_path}")
    try:
        subprocess.run(['python3', detect_script_path], check=True)
        logging.info("Script executed successfully")
        return {'status': 'success'}
    except subprocess.CalledProcessError as e:
        logging.error(f"Script failed with error: {e}")
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
