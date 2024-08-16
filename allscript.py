import os
import subprocess

def run_script(script_path):
    try:
        print(f"Running script: {script_path}")
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run script {script_path}: {e}")
    except Exception as e:
        print(f"An error occurred while running {script_path}: {e}")

def main():
    # Path to the frequent_keywords directory
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frequent_keywords'))

    # First script path
    script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents.py')
    
    # Second script path
    monthly_script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents_each_month_year.py')
    
    # Path to the count_check_debugg directory
    count_check_debugg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'count_check_debugg'))

    # Third script path
    script_path_count = os.path.join(count_check_debugg_dir, 'count_the_nb_of_articles_at_ALMayadin.py')

    # Path to the Hidden_patterns directory
    Hidden_patterns_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Hidden_patterns'))

    # Third script path
    script_path_Hidden_patterns = os.path.join(Hidden_patterns_dir, 'detect_hidden_patterns.py')

    


    # Run the scripts
    run_script(script_path)
    run_script(monthly_script_path)
    run_script(script_path_count)
    run_script(script_path_Hidden_patterns)

if __name__ == "__main__":
    main()
