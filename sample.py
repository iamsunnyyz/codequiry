import requests
import time
from codequiry import Codequiry

def get_account_info(api_key):
    codequiry = Codequiry(api_key)
    account_info = codequiry.account()
    print("Account Information:", account_info)
    return account_info

def get_check_history(api_key):
    codequiry = Codequiry(api_key)
    check_history = codequiry.checks()
    print("Check History:", check_history)
    return check_history

def create_check(api_key, check_name, lang_id):
    codequiry = Codequiry(api_key)
    response = codequiry.create_check(check_name, lang_id)
    print("Check Creation Response:", response)
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
        # Print raw response text
        print("Raw Upload Response:", response.text)
        # Attempt to parse JSON response
        response_json = response.json()
        print("Upload Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
    except ValueError as e:
        print("JSON Decode Error:", e)

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
        # Print raw response text
        print("Raw Start Check Response:", response.text)
        # Attempt to parse JSON response
        response_json = response.json()
        print("Start Check Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
    except ValueError as e:
        print("JSON Decode Error:", e)

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
        # Print raw response text
        print("Raw Check Status Response:", response.text)
        # Attempt to parse JSON response
        response_json = response.json()
        print("Check Status Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
    except ValueError as e:
        print("JSON Decode Error:", e)

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
        # Print raw response text
        print("Raw Check Overview Response:", response.text)
        # Attempt to parse JSON response
        response_json = response.json()
        print("Check Overview Response JSON:", response_json)
        return response_json
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
    except ValueError as e:
        print("JSON Decode Error:", e)

def wait_for_check_completion(api_key, check_id, interval=30, max_attempts=60):
    """
    Wait for the check to complete by polling its status.

    :param api_key: API key for authentication
    :param check_id: ID of the check to monitor
    :param interval: Time in seconds between status checks
    :param max_attempts: Maximum number of attempts to check the status
    :return: The final status of the check
    """
    attempts = 0
    while attempts < max_attempts:
        status_response = get_check_status(api_key, check_id)
        status = status_response.get('status')
        
        if status == 4:  # Assuming status 4 means results available
            print("Check completed. Fetching results...")
            return get_check_overview(api_key, check_id)
        elif status in [1, 2, 3, 7]:  # Pending, Ready, Errors, In Queue
            print("Check status:", status)
        else:
            print("Unknown status:", status)
        
        attempts += 1
        time.sleep(interval)
    
    print("Check did not complete within the expected time.")
    return None

def main():
    API_KEY = "79e85a511702092a479d9ba4a859e0cc80516d6b7effb10a6e813c21a026527e"
    
    # Get account information
    get_account_info(API_KEY)
    
    # Retrieve and print check history
    get_check_history(API_KEY)
    
    # Create a new check
    check_name = "Test Check"
    lang_id = 18  # Example: C# language ID
    check_response = create_check(API_KEY, check_name, lang_id)
    check_id = check_response['id']
    
    # Upload a file to the check
    file_path = 'quicksort.zip'  # Update this path to your zip file location
    upload_response = upload_file(API_KEY, check_id, file_path)
    
    # Start the check
    start_check(API_KEY, check_id, dbcheck=False, webcheck=True)
    
    # Wait for the check to complete and get the results
    overview_response = wait_for_check_completion(API_KEY, check_id)
    if overview_response:
        print("Check Overview:", overview_response)
    else:
        print("No results available.")

if __name__ == "__main__":
    main()
