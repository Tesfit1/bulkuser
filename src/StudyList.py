import json
from dotenv import load_dotenv
import requests
import os
import pandas as pd

load_dotenv()
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
SESSION_FILE = "session_id.txt"
with open(SESSION_FILE) as f:
    SESSION_ID = f.read().strip()
print(f"Session ID: {SESSION_ID}")

def retrieve_studies():
    url = f"{BASE_URL}/api/{API_VERSION}/app/cdm/studies"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {SESSION_ID}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    json_response = response.json()
    print(json.dumps(json_response, indent=4))  # Prettify JSON for debug
    studies = json_response.get("studies", [])
    studies_df = pd.DataFrame(studies)
    return studies_df

studies_df = retrieve_studies()