from login import login 

def main():
    # Call the login function
    token = login()
    print("Login function executed successfully.")
    print("Access Token:", token)
    # Add any other main functionality here

if __name__ == "__main__":
    main()