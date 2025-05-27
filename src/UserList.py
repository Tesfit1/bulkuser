import json
from dotenv import load_dotenv
import requests
import os
import pandas as pd

load_dotenv()
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
study_name = os.getenv("Study_name")
SESSION_FILE = "session_id.txt"
with open(SESSION_FILE) as f:
    SESSION_ID = f.read().strip()
print(f"Session ID: {SESSION_ID}")

def retrieve_users():
    base_url = f"{BASE_URL}/api/{API_VERSION}/app/cdm/users"
    # Only add study_name if it is set and not empty
    if study_name:
        url = f"{base_url}?study_name={study_name}"
    else:
        url = base_url
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {SESSION_ID}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    json_response = response.json()
    print(json.dumps(json_response, indent=4))  # Prettify JSON for debug
    users = json_response.get("users", [])
    users_df = pd.DataFrame(users)
    return users_df

retrieve_users()