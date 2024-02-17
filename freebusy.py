import requests
import json
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

def get_access_token():
    load_dotenv() 
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": client_secret,
            }
        },
        scopes=scopes,
    )
    flow.run_local_server()

    credentials = flow.credentials
    return credentials.token


def collectBusyTimes(start, end, cal_ids):
    url = "https://www.googleapis.com/calendar/v3/freeBusy"
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "timeMin": start, #"2022-01-01T00:00:00Z",
        "timeMax": end, #"2022-01-01T23:59:59Z",
        "items": [{"id": id} for id in cal_ids]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print('\n\n', response, '\n\n')
    return response


