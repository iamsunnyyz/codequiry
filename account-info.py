import streamlit as st
from codequiry import Codequiry

def get_account_info(api_key):
    try:
        codequiry = Codequiry(api_key)
        account_info = codequiry.account()
        return account_info
    except Exception as e:
        st.error(f"Error retrieving account information: {e}")
        return None

def get_check_history(api_key):
    try:
        codequiry = Codequiry(api_key)
        check_history = codequiry.checks()
        return check_history
    except Exception as e:
        st.error(f"Error retrieving check history: {e}")
        return None

def display_account_info(account_info):
    if account_info:
        st.subheader("Account Information")
        st.write(f"Email: {account_info.get('email', 'N/A')}")
        st.write(f"Name: {account_info.get('user', 'N/A')}")
        st.write(f"Pro Checks Remaining: {account_info.get('pro_checks_remaining', 'N/A')}")
        st.write(f"Submissions: {account_info.get('submissions', 'N/A')}")
    else:
        st.warning("No account information available.")

def display_check_history(check_history):
    if check_history:
        st.subheader("Check History")
        for check in check_history:
            st.write(f"Check ID: {check.get('id')}")
            st.write(f"Name: {check.get('name')}")
            st.write(f"Created At: {check.get('created_at')}")
            st.write(f"Status: {check.get('status')}")
            st.write("-------")

def main():
    st.title("Codequiry Account Information and Check History")
    
    API_KEY = st.text_input("Enter your Codequiry API Key")
    
    if API_KEY:
        account_info = get_account_info(API_KEY)
        display_account_info(account_info)
        
        check_history = get_check_history(API_KEY)
        display_check_history(check_history)

if __name__ == "__main__":
    main()
