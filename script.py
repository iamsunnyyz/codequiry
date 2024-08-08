import streamlit as st
import os
import time
import zipfile
from codequiry import Codequiry

# API functions
def get_account_info(api_key):
    codequiry = Codequiry(api_key)
    account_info = codequiry.account()
    return account_info

# def get_check_history(api_key):
#     codequiry = Codequiry(api_key)
#     check_history = codequiry.checks()
#     return check_history

def create_check(api_key, check_name, lang_id):
    codequiry = Codequiry(api_key)
    response = codequiry.create_check(check_name, lang_id)
    return response

def compress_file_to_zip(file_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))

def upload_file(api_key, check_id, file_path):
    codequiry = Codequiry(api_key)
    response = codequiry.upload_file(check_id, file_path)
    return response

def start_check(api_key, check_id, dbcheck=False, webcheck=False):
    codequiry = Codequiry(api_key)
    response = codequiry.start_check(check_id)
    return response

def get_check_status(api_key, check_id):
    codequiry = Codequiry(api_key)
    response = codequiry.get_check(check_id)
    return response

def get_check_overview(api_key, check_id):
    codequiry = Codequiry(api_key)
    response = codequiry.get_overview(check_id)
    return response

def get_detailed_submission_results(api_key, check_id, submission_id):
    codequiry = Codequiry(api_key)
    response = codequiry.get_results(check_id, submission_id)
    return response

def wait_for_check_completion(api_key, check_id, interval=60, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        status_response = get_check_status(api_key, check_id)
        st.write(f"Check Status Response: {status_response}")
        status = status_response.get('status')
        
        if status == "Completed":
            return get_check_overview(api_key, check_id)
        elif status in ["Pending", "Ready", "Errors", "In Queue"]:
            pass
        attempts += 1
        time.sleep(interval)
    return None

def parse_and_display_results(raw_response):
    response_json = raw_response
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
    probability_of_plagiarism = submissions.get('result2')
    uniqueness_percentage = 100 - probability_of_plagiarism
    matches_local_db = submissions.get('matches_local')
    matches_web = submissions.get('matches_web')

    st.write(f"**Check ID:** {check_id}")
    st.write(f"**Name:** {check_name}")
    st.write(f"**Created At:** {created_at}")
    st.write(f"**Status Message:** {status_message}")
    st.write(f"**Lines of Code:** {lines_of_code}")
    st.write(f"**Similar Files:** {similar_files}")
    st.write(f"**Matches Found:** {matches_found}")
    st.write(f"**Filename:** {filename}")
    st.write(f"**Probability of Plagiarism:** {probability_of_plagiarism}%")
    st.write(f"**Uniqueness Percentage:** {uniqueness_percentage}%")
    st.write(f"**Matches Local Database:** {matches_local_db}")
    st.write(f"**Matches Web:** {matches_web}")

# Streamlit app
def main():
    st.title("Codequiry Plagiarism Check")

    # API key input
    api_key = st.text_input("Enter your Codequiry API key:", type="password")
    
    if not api_key:
        st.warning("Please enter your Codequiry API key to proceed.")
        return

    # File upload
    uploaded_file = st.file_uploader("Upload a file for plagiarism check", type=["py", "cs", "java", "txt"])

    if uploaded_file is not None:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        original_file_path = uploaded_file.name
        zip_file_path = original_file_path.replace('.', '_') + '.zip'
        compress_file_to_zip(original_file_path, zip_file_path)
        
        check_name = st.text_input("Enter a name for the check:", value="Test Check")
        lang_id = st.selectbox("Select the programming language:", [18, 19, 20])  # Example: 18 for C#, 19 for Java, 20 for Python
        
        if st.button("Start Check"):
            check_response = create_check(api_key, check_name, lang_id)
            st.write(f"Check Creation Response: {check_response}")
            check_id = check_response['id']
            
            upload_response = upload_file(api_key, check_id, zip_file_path)
            st.write(f"File Upload Response: {upload_response}")
            
            start_response = start_check(api_key, check_id, dbcheck=False, webcheck=True)
            st.write(f"Start Check Response: {start_response}")
            
            overview_response = wait_for_check_completion(api_key, check_id)
            st.write(f"Check Overview Response: {overview_response}")
            
            if overview_response:
                submission_id = overview_response['submissions'][0]['id']
                detailed_results = get_detailed_submission_results(api_key, check_id, submission_id)
                st.write(f"Detailed Submission Results: {detailed_results}")
                parse_and_display_results(detailed_results)
            else:
                st.error("Failed to retrieve check results.")

if __name__ == "__main__":
    main()
