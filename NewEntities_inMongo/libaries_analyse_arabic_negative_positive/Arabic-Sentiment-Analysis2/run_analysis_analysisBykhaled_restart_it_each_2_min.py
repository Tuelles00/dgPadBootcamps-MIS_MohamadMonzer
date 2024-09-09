import subprocess
import time
import os
import signal
import pymongo
from pymongo import MongoClient

# MongoDB setup (adjust as necessary)
client = MongoClient('mongodb://192.168.31.136:27017/')
db = client['articles_db']
collection = db['articles']

# Define the path to 2_khaled_ML_sentiment_analysis.py
base_dir = os.path.abspath(os.path.dirname(__file__))
analysis_script_path = os.path.join(base_dir, '2_khaled_ML_sentiment_analysis.py')

def check_conditions():
    # Check if all articles contain the 'analysis.khaled analysis' field
    count_missing_analysis = collection.count_documents({"analysis.khaled analysis": {"$exists": False}})
    if count_missing_analysis == 0:
        print("All articles now contain the 'analysis.khaled analysis' field.")
        return True
    
    # Check if there are documents with missing 'analysis.khaled analysis' but with empty keywords
    documents_with_empty_keywords = list(collection.find({"analysis.khaled analysis": {"$exists": False}, "keywords": ""}))
    if documents_with_empty_keywords:
        print(f"Found {len(documents_with_empty_keywords)} documents with empty keywords.")
        return True
    
    return False

def run_analysis_script():
    while True:
        # Start the analysis script
        process = subprocess.Popen(
            ["python3", analysis_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line buffered
        )

        start_time = time.time()  # Get the current time

        try:
            # Continuously read the output and monitor the runtime
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    print("Output:", output.strip())  # Print the output for debugging

                # Optional: Handle stderr if needed
                error_output = process.stderr.readline()
                if error_output:
                    print(f"Error: {error_output.strip()}")

                # Check if 2 minutes have passed
                if time.time() - start_time > 120:  # 120 seconds = 2 minutes
                    print("2 minutes elapsed, preparing to terminate the script...")
                    break

                # Check if the exit conditions are met
                if check_conditions():
                    print("Exit conditions met, stopping the runner script...")
                    process.terminate()
                    return

        except Exception as e:
            print(f"An error occurred while running or stopping the script: {e}")

        finally:
            # Wait 3 seconds before forcefully killing the script
            print("Waiting for 3 seconds before killing the script...")
            time.sleep(3)
            
            # Terminate the process if it is still running
            if process.poll() is None:
                print("Terminating the script...")
                process.terminate()  # Gracefully terminate the script
                time.sleep(5)  # Additional wait to ensure termination
                if process.poll() is None:
                    print("Force killing the script...")
                    os.kill(process.pid, signal.SIGKILL)

            process.wait()  # Ensure the process has completely finished

        # Wait for 3 seconds before restarting
        print("Waiting for 3 seconds before restarting the script...")
        time.sleep(3)  # Sleep for 3 seconds before restarting

if __name__ == "__main__":
    run_analysis_script()
