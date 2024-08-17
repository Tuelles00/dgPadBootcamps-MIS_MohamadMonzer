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

    # Script paths in frequent_keywords directory
    script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents.py')
    monthly_script_path = os.path.join(script_dir, 'frequent_keywords_counts_the_total_occurrences_of_each_keyword_across_all_documents_each_month_year.py')

    # Path to the count_check_debugg directory
    count_check_debugg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'count_check_debugg'))

    # Script path in count_check_debugg directory
    script_path_count = os.path.join(count_check_debugg_dir, 'count_the_nb_of_articles_at_ALMayadin.py')

    # Path to the Hidden_patterns directory
    hidden_patterns_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Hidden_patterns'))

    # Script path in Hidden_patterns directory
    script_path_hidden_patterns = os.path.join(hidden_patterns_dir, 'detect_hidden_patterns.py')

    # Path to the video_available directory
    video_available_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'video_available'))

    # Script paths in video_available directory
    script_path_video_available = os.path.join(video_available_dir, 'video_null_category.py')
    script_path_video_available_null = os.path.join(video_available_dir, 'video_not_null_category.py')

    # Path to the task2 directory
    task2_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task2'))

    # Run all Python scripts in the task2 directory
    for filename in os.listdir(task2_dir):
        if filename.endswith('.py'):
            script_path_task2 = os.path.join(task2_dir, filename)
            run_script(script_path_task2)

  # Path to the task22 directory
    task22_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task22'))

    # Run all Python scripts in the task22 directory
    for filename in os.listdir(task22_dir):
        if filename.endswith('.py'):
            script_path_task22 = os.path.join(task22_dir, filename)
            run_script(script_path_task22)




    # Run specific scripts
    #run_script(script_path)
    #run_script(monthly_script_path)
    #run_script(script_path_hidden_patterns)
    #run_script(script_path_video_available)
    #run_script(script_path_video_available_null)
    ##run_script(script_path_count)  # This script may take a long time to complete

if __name__ == "__main__":
    main()
