import requests
import json
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow
import os
from dotenv import load_dotenv

def get_access_token():
    load_dotenv() 
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",  # Replace with the path to your client secret file
        scopes=scopes
    )
    
    credentials = flow.run_local_server()

    return credentials.token



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


# import requests
# import json
# import os
# from dotenv import load_dotenv
# from googleapiclient.discovery import build

# def get_access_token(scopes = ["https://www.googleapis.com/auth/calendar.readonly"], credentials_file="credentials.json"):
#   """Retrieves an access token for the Google Calendar API using OAuth 2.0 credentials.

#   Args:
#     scopes (list): A list of API scopes to request access for.
#     credentials_file (str, optional): Path to the OAuth 2.0 credentials JSON file.
#       If not provided, it will be retrieved from the environment variable
#       `GOOGLE_APPLICATION_CREDENTIALS`.

#   Returns:
#     str: The retrieved access token.

#   Raises:
#     ValueError: If both 'credentials_file' and 'GOOGLE_APPLICATION_CREDENTIALS'
#       are not provided.
#   """

#   if not credentials_file:
#     credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
#     if not credentials_file:
#       raise ValueError("Either 'credentials_file' or 'GOOGLE_APPLICATION_CREDENTIALS' environment variable must be set.")

#   # Read the credentials JSON file
#   with open(credentials_file) as f:
#     credentials_json = json.load(f)

#   # Use the credentials to build a Google Calendar service object
#   return build("calendar", "v3", credentials=credentials_json)

# def collectBusyTimes(start, end, cal_ids):
#   url = "https://www.googleapis.com/calendar/v3/freeBusy"
#   service = get_access_token()  # This now returns a service object

#   # Use the service object to make the request
#   response = service.freebusy().query(body={
#     "timeMin": start+'Z',  # Ensure proper "Z" formatting for UTC time
#     "timeMax": end+'Z',
#     "items": [{"id": id} for id in cal_ids]
#   }).execute()

#   return response
