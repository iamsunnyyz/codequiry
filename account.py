from codequiry import Codequiry
import os

def get_account_info(api_key):
    codequiry = Codequiry(api_key)
    account_info = codequiry.account()
    print("Account Information:", account_info)
    return account_info

def main():
    API_KEY = os.getenv("CODEQUIRY_API_KEY")
    
    # Get account information
    get_account_info(API_KEY)

if __name__ == "__main__":
    main()