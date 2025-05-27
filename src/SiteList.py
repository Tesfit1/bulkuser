import json
from dotenv import load_dotenv
import requests
import os
import pandas as pd
from io import StringIO 

load_dotenv()
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
# SESSION_ID = os.getenv("SESSION_ID")
SESSION_FILE = "session_id.txt"
with open(SESSION_FILE) as f:
    SESSION_ID = f.read().strip()
print(f"Session ID: {SESSION_ID}")
study_name = os.getenv("Study_name")

def retrieve_sites():
    url = f"{BASE_URL}/api/{API_VERSION}/app/cdm/sites?study_name={study_name}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {SESSION_ID}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    json_response = response.json()
    print(json.dumps(json_response, indent=4))  # Prettify JSON for debug
    sites = json_response.get("sites", [])
    sites_df = pd.DataFrame(sites)
    # print(sites_df)
    return sites_df

retrieve_sites()

