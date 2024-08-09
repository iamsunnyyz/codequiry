import os
import requests
import time
import json
import zipfile
import streamlit as st
from codequiry import Codequiry

def get_latest_cs_file(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.cs')]
    latest_file = max(files, key=os.path.getctime)
    st.write("Latest file selected:", latest_file)
    return latest_file

def compress_file(file_path):
    zip_filename = file_path + '.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    st.write("Compressed file:", zip_filename)
    return zip_filename

def get_account_info(api_key):
    codequiry = Codequiry(api_key)
    account_info = codequiry.account()
    st.write("Account Information retrieved.")
    return account_info

def create_check(api_key, check_name, lang_id):
    codequiry = Codequiry(api_key)
    response = codequiry.create_check(check_name, lang_id)
    st.write("Check created successfully.")
    return response

def upload_file(api_key, check_id, file_path):
    url = 'https://codequiry.com/api/v1/check/upload'
    headers = {
        'apikey': api_key
    }
    files = {
        'file': open(file_path, 'rb')
    }
    data = {
        'check_id': check_id
    }
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response_json = response.json()
        st.write("File uploaded successfully.")
        return response_json
    except requests.exceptions.RequestException as e:
        st.error(f"File upload failed: {e}")
    except ValueError as e:
        st.error(f"Error decoding response: {e}")

def start_check(api_key, check_id, dbcheck=False, webcheck=False):
    url = 'https://codequiry.com/api/v1/check/start'
    headers = {
        'apikey': api_key
    }
    params = {
        'check_id': check_id
    }
    if dbcheck:
        params['dbcheck'] = 1
    if webcheck:
        params['webcheck'] = 1
    try:
        response = requests.post(url, headers=headers, params=params)
        response_json = response.json()
        st.write("Check started successfully.")
        return response_json
    except requests.exceptions.RequestException as e:
        st.error(f"Check start failed: {e}")
    except ValueError as e:
        st.error(f"Error decoding response: {e}")

def get_check_status(api_key, check_id):
    url = 'https://codequiry.com/api/v1/check/get'
    headers = {
        'apikey': api_key
    }
    params = {
        'check_id': check_id
    }
    try:
        response = requests.post(url, headers=headers, params=params)
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve check status: {e}")
    except ValueError as e:
        st.error(f"Error decoding response: {e}")

def get_check_overview(api_key, check_id):
    url = 'https://codequiry.com/api/v1/check/overview'
    headers = {
        'apikey': api_key
    }
    params = {
        'check_id': check_id
    }
    try:
        response = requests.post(url, headers=headers, params=params)
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve check overview: {e}")
    except ValueError as e:
        st.error(f"Error decoding response: {e}")

def get_detailed_submission_results(api_key, check_id, submission_id):
    url = 'https://codequiry.com/api/v1/check/results'
    headers = {
        'apikey': api_key
    }
    params = {
        'check_id': check_id,
        'submission_id': submission_id
    }
    try:
        response = requests.post(url, headers=headers, params=params)
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve detailed results: {e}")
    except ValueError as e:
        st.error(f"Error decoding response: {e}")

def wait_for_check_completion(api_key, check_id, interval=60, max_attempts=10):
    attempts = 0
    status_message = st.empty()
    while attempts < max_attempts:
        status_response = get_check_status(api_key, check_id)
        status = status_response.get('status')
        
        if status == 4:  # Assuming status 4 means results available
            status_message.text("Check completed. Fetching results...") 
            return get_check_overview(api_key, check_id)
        elif status in [1, 2, 3, 7]:  # Pending, Ready, Errors, In Queue
            status_message.text(f"Check status: {status}")
        else:
            status_message.text(f"Unknown status: {status}")
        
        attempts += 1
        time.sleep(interval)
    
    status_message.text("Check did not complete within the expected time.")
    return None

def parse_and_display_results(response_json):
    try:
        check = response_json.get('check', {})
        submissions = response_json.get('submissions', [{}])[0]

        # Extract relevant information
        check_id = check.get('id')
        check_name = check.get('name')
        created_at = check.get('created_at')
        status_message = check.get('status_message')
        lines_of_code = check.get('lines')
        similar_files = check.get('similar_files')
        matches_found = check.get('matches_found')

        filename = submissions.get('filename')
        probability_of_plagiarism = submissions.get('result2')  # Assuming this is the percentage
        matches_local_db = submissions.get('matches_local')
        matches_web = submissions.get('matches_web')

        # Display the parsed results
        st.write(f"Check ID: {check_id}")
        st.write(f"Name: {check_name}")
        st.write(f"Created At: {created_at}")
        st.write(f"Status Message: {status_message}")
        st.write(f"Lines of Code: {lines_of_code}")
        st.write(f"Similar Files: {similar_files}")
        st.write(f"Matches Found: {matches_found}")
        st.write(f"Filename: {filename}")
        st.write(f"Probability of Plagiarism: {probability_of_plagiarism}%")
        st.write(f"Matches Local Database: {matches_local_db}")
        st.write(f"Matches Web: {matches_web}")

    except Exception as e:
        st.error(f"Error parsing and displaying results: {e}")

def main():
    st.title("Codequiry Plagiarism Check")

    API_KEY = os.getenv("CODEQUIRY_API_KEY")
    
    st.subheader("Account Information")
    get_account_info(API_KEY)
    
    check_name = "Test Check"
    lang_id = 18  # Example: C# language ID
    
    st.subheader("Create New Check")
    check_response = create_check(API_KEY, check_name, lang_id)
    check_id = check_response['id']
    
    st.subheader("Upload File")
    latest_cs_file = get_latest_cs_file('.')
    zip_file_path = compress_file(latest_cs_file)
    upload_file(API_KEY, check_id, zip_file_path)
    
    st.subheader("Start Check")
    start_check(API_KEY, check_id, dbcheck=False, webcheck=True)
    
    st.subheader("Wait for Check Completion")
    overview_response = wait_for_check_completion(API_KEY, check_id)
    if overview_response:
        st.write("Check Overview retrieved.")
        
        submission_id = overview_response['submissions'][0]['id']
        detailed_results = get_detailed_submission_results(API_KEY, check_id, submission_id)
        st.write("Detailed Submission Results retrieved.")
        
        parse_and_display_results(detailed_results)
    else:
        st.error("No results available.")

if __name__ == "__main__":
    main()
