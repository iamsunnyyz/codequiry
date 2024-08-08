from codequiry import Codequiry
import os

def get_account_info(api_key):
    codequiry = Codequiry(api_key)
    account_info = codequiry.account()
    print("Account Information:", account_info)
    return account_info

def main():
    API_KEY = "79e85a511702092a479d9ba4a859e0cc80516d6b7effb10a6e813c21a026527e"
    
    # Get account information
    get_account_info(API_KEY)

if __name__ == "__main__":
    main()