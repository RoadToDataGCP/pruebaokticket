import requests
from dotenv import load_dotenv
import os

def login(): 

    load_dotenv()

    # Load environment variables
    host = os.getenv("HOST")
    username = os.getenv("OKTICKET_USERNAME")
    password = os.getenv("OKTICKET_PASSWORD")
    scope = os.getenv("SCOPE")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    url = f"{host}/oauth/token"
    

    payload={'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password,
    'scope': scope}
    files=[

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    token = response.json().get('access_token')
    if token:
        print("Access Token:", token)
        return token
    else:
        print("Failed to retrieve access token.")
        # Optionally, you can print the error message from the response
        print("Error:", response.json())
    print(response.status_code)

    #print(response.text)
    #print(payload)
    #print(url)
    #print(response.content)


