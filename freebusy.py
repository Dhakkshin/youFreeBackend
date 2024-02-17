import requests
import json
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def get_access_token():
    load_dotenv() 
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",
        scopes=scopes
    )

    # Print the authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')
    print("Authorization URL:", auth_url)

    # Configure the flow to run in headless mode
    flow.run_local_server()

    # Get the credentials object
    creds = flow.credentials

    # Print the received authorization response
    print("Received authorization response:", creds)
    
    # Save the credentials to a file
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())

    return creds.token


def collectBusyTimes(start, end, cal_ids):
    url = "https://www.googleapis.com/calendar/v3/freeBusy"
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "timeMin": start+'Z', #"2022-01-01T00:00:00Z",
        "timeMax": end+'Z', #"2022-01-01T23:59:59Z",
        "items": [{"id": id} for id in cal_ids]
    }
    # print(start, end, sep='\n\n')
    # print(headers, json.dumps(data), sep='\n\n')
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # print('\n\n', response, '\n\n')
    return response


