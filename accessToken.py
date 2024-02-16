import requests
import json
from urllib.parse import urlencode

# OAuth 2.0 credentials
client_id = "220481371601-hom4p2h07ere96j4ctumhhb64dao3c93.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "http://localhost:8000/auth/callback"

# Authorization endpoint
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"

# Token endpoint
token_url = "https://oauth2.googleapis.com/token"

# Scopes required by the application
scopes = [
    "https://www.googleapis.com/auth/calendar"
]

# Step 1: Generate authorization URL
params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": " ".join(scopes),
    "response_type": "code",
}

authorization_url = authorization_base_url + "?" + urlencode(params)

# Step 2: Obtain user consent
print("Go to the following URL and grant permission to access your Google Calendar:")
print(authorization_url)
authorization_code = input("Enter the authorization code from the URL: ")

# Step 3: Exchange authorization code for access token
token_data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "code": authorization_code,
    "grant_type": "authorization_code",
}

response = requests.post(token_url, data=token_data)
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info["access_token"]
    print("Access token obtained successfully:", access_token)
else:
    print(f"Failed to obtain access token. Status code: {response.status_code}")
    print(response.text)
