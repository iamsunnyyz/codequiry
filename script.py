import os
import requests
import time
import json
import streamlit as st
from codequiry import Codequiry

def get_account_info(api_key):
    codequiry = Codequiry(api_key)
    account_info = codequiry.account()
    st.write("Account Information:", account_info)
    return account_info

# def get_check_history(api_key):
#     codequiry = Codequiry(api_key)
#     check_history = codequiry.checks()
#     st.write("Check History:", check_history)
#     return check_history

def create_check(api_key, check_name, lang_id):
    codequiry = Codequiry(api_key)
    response = codequiry.create_check(check_name, lang_id)
    st.write("Check Creation Response:", response)
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
        st.write("Raw Upload Response:", response.text)
        response_json = response.json()
        st.write("Upload Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        st.write("Request Exception:", e)
    except ValueError as e:
        st.write("JSON Decode Error:", e)

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
        st.write("Raw Start Check Response:", response.text)
        response_json = response.json()
        st.write("Start Check Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        st.write("Request Exception:", e)
    except ValueError as e:
        st.write("JSON Decode Error:", e)

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
        st.write("Raw Check Status Response:", response.text)
        response_json = response.json()
        st.write("Check Status Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        st.write("Request Exception:", e)
    except ValueError as e:
        st.write("JSON Decode Error:", e)

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
        st.write("Raw Check Overview Response:", response.text)
        response_json = response.json()
        st.write("Check Overview Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        st.write("Request Exception:", e)
    except ValueError as e:
        st.write("JSON Decode Error:", e)

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
        st.write("Raw Detailed Submission Results Response:", response.text)
        response_json = response.json()
        st.write("Detailed Submission Results Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        st.write("Request Exception:", e)
    except ValueError as e:
        st.write("JSON Decode Error:", e)

def wait_for_check_completion(api_key, check_id, interval=60, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        status_response = get_check_status(api_key, check_id)
        status = status_response.get('status')
        
        if status == 4:  # Assuming status 4 means results available
            st.write("Check completed. Fetching results...") 
            return get_check_overview(api_key, check_id)
        elif status in [1, 2, 3, 7]:  # Pending, Ready, Errors, In Queue
            st.write("Check status:", status)
        else:
            st.write("Unknown status:", status)
        
        attempts += 1
        time.sleep(interval)
    
    st.write("Check did not complete within the expected time.")
    return None

def parse_and_display_results(raw_response):
    try:
        response_json = json.loads(raw_response)
        check = response_json.get('check', {})
        submissions = response_json.get('submissions', [{}])[0]

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

    except json.JSONDecodeError as e:
        st.write(f"JSON Decode Error: {e}")
    except Exception as e:
        st.write(f"Error: {e}")

def main():
    st.title("Codequiry Plagiarism Check")

    API_KEY = os.getenv("CODEQUIRY_API_KEY")
    
    st.subheader("Account Information")
    get_account_info(API_KEY)
    
    # st.subheader("Check History")
    # get_check_history(API_KEY)
    
    check_name = "Test Check"
    lang_id = 18  # Example: C# language ID
    
    st.subheader("Create New Check")
    check_response = create_check(API_KEY, check_name, lang_id)
    check_id = check_response['id']
    
    st.subheader("Upload File")
    file_path = 'code-check.zip'  # Update this path to your zip file location
    upload_file(API_KEY, check_id, file_path)
    
    st.subheader("Start Check")
    start_check(API_KEY, check_id, dbcheck=False, webcheck=True)
    
    st.subheader("Wait for Check Completion")
    overview_response = wait_for_check_completion(API_KEY, check_id)
    if overview_response:
        st.write("Check Overview:", overview_response)
        
        submission_id = overview_response['submissions'][0]['id']
        detailed_results = get_detailed_submission_results(API_KEY, check_id, submission_id)
        st.write("Detailed Submission Results:", detailed_results)
        
        parse_and_display_results(detailed_results)
    else:
        st.error("No results available.")

if __name__ == "__main__":
    main()
