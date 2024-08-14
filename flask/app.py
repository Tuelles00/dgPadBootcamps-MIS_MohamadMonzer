from flask import Flask, render_template, redirect, url_for, send_from_directory
import subprocess
import os

app = Flask(__name__)

# Path to the count_check_debugg directory
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'count_check_debugg'))
txt_file_path = os.path.join(script_dir, 'article_counts.txt')
script_path = os.path.join(script_dir, 'count_the_nb_of_articles_at_ALMayadin.py')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article_counts.txt')
def serve_article_counts():
    return send_from_directory('../count_check_debugg', 'article_counts.txt')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/refresh_counts')
def refresh_counts():
    # Run the script to refresh counts
    subprocess.run(['python3', script_path])
    return redirect(url_for('graph'))

@app.route('/run_script', methods=['POST'])
def run_script():
    subprocess.run(['python3', script_path])
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
