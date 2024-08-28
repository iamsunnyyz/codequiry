import os
import time
import json
import zipfile
import streamlit as st
from codequiry import Codequiry

def get_latest_cs_file(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.cs')]
    latest_file = max(files, key=os.path.getctime)
    return latest_file

def compress_file(file_path):
    zip_filename = file_path + '.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    return zip_filename

def get_account_info(api_key):
    codequiry = Codequiry(api_key)
    account_info = codequiry.account()
    st.write("Account Information:", account_info)

def create_check(api_key, check_name, lang_id):
    codequiry = Codequiry(api_key)
    response = codequiry.create_check(check_name, lang_id)
    return response

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

def calculate_probability_of_plagiarism(lines, similar_files, matches_found, matches_local, matches_web):
    if lines == 0:
        return 0

    # Base ratio of matches to lines
    base_ratio = matches_found / lines

    # Increase the weight based on the number of similar files
    similarity_factor = similar_files / (lines * 10)  # Arbitrary scaling factor for similar files

    # Increase weight for local and web matches
    match_factor = (matches_local + matches_web) / (lines * 5)  # Arbitrary scaling factor for matches

    # Combine the factors with some weight coefficients to generate the probability
    probability_of_plagiarism = (base_ratio + similarity_factor + match_factor) * 100
    
    # Cap the probability at 100%
    return min(probability_of_plagiarism, 100)


def parse_and_display_results(response_json):
    check = response_json.get('check', {})
    submissions = response_json.get('submissions', [{}])[0]

    check_id = check.get('id')
    check_name = check.get('name')
    created_at = check.get('created_at')
    status = check.get('status')
    status_message = check.get('status_message')
    lines_of_code = check.get('lines')
    similar_files = check.get('similar_files')
    matches_found = check.get('matches_found')

    filename = submissions.get('filename')
    matches_local_db = submissions.get('matches_local', 0)
    matches_web = submissions.get('matches_web', 0)

    # Calculate the Probability of Plagiarism
    probability_of_plagiarism = calculate_probability_of_plagiarism(
        lines_of_code, similar_files, matches_found, matches_local_db, matches_web
    )
    probability_of_uniqueness = 100 - probability_of_plagiarism

    st.write(f"**Check ID:** {check_id}")
    st.write(f"**Name:** {check_name}")
    st.write(f"**Created At:** {created_at}")
    st.write(f"**Status:** {status}")
    st.write(f"**Status Message:** {status_message}")
    st.write(f"**Lines of Code:** {lines_of_code}")
    st.write(f"**Similar Files:** {similar_files}")
    st.write(f"**Matches Found:** {matches_found}")
    st.write(f"**Filename:** {filename}")
    st.write(f"**Probability of Plagiarism:** **{probability_of_plagiarism}%**")
    st.write(f"**Probability of Uniqueness:** **{probability_of_uniqueness}%**")
    st.write(f"**Matches Local Database:** {matches_local_db}")
    st.write(f"**Matches Web:** {matches_web}")

def main():
    st.title("Codequiry Plagiarism Check")

    API_KEY = os.getenv("CODEQUIRY_API_KEY")
    
    # Display account information
    st.subheader("Account Information")
    get_account_info(API_KEY)

    # Create new check
    check_name = "Test Check"
    lang_id = 18  # Example: C# language ID
    check_response = create_check(API_KEY, check_name, lang_id)
    check_id = check_response['id']

    # Upload file
    latest_cs_file = get_latest_cs_file('.')
    zip_file_path = compress_file(latest_cs_file)
    upload_file(API_KEY, check_id, zip_file_path)

    # Start the check
    start_check(API_KEY, check_id)

    # Display real-time result updates
    st.subheader("Plagiarism Check Results")

    result_box = st.empty()  # Placeholder for the results

    while True:
        status_response = get_check_status(API_KEY, check_id)
        status_id = status_response.get('check', {}).get('status_id')

        # Update the results in the box
        with result_box.container():
            parse_and_display_results(status_response)

        # Check if the status is 'Completed' (status_id == 4)
        if status_id == 4:
            break  # Exit the loop once the check is completed

        time.sleep(10)  # Wait 10 seconds before fetching the status again

if __name__ == "__main__":
    main()
