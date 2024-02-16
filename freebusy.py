import requests
import json
import os
from dotenv import load_dotenv

def collectBusyTimes(cal_ids):

    url = "https://www.googleapis.com/calendar/v3/freeBusy"

    # Update these with your OAuth 2.0 credentials
    load_dotenv() 
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Update these with your obtained access token
    access_token = os.getenv("ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # cal_ids = ["7d3e6bfcdf8a27acf7fbc7301b8b32615f183e57f250740e4699fbae6d614e3d@group.calendar.google.com", "4c9d380b330580be36ca243cbf5b90b14664fbe0208dcd707c967fa7d7ef0aa7@group.calendar.google.com"]
    data = {
        "timeMin": "2022-01-01T00:00:00Z",
        "timeMax": "2022-01-01T23:59:59Z",
        "items": [{"id": id} for id in cal_ids]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


# if response.status_code == 200:
#     free_busy_info = response.json()
#     print(free_busy_info)
# else:
#     print(f"Request failed with status code {response.status_code}")
#     print(response.text)
