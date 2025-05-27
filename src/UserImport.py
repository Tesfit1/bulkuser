import json
import os
import pandas as pd
from dotenv import load_dotenv
import requests

from StudyList import retrieve_studies
from SiteList import retrieve_sites
from UserList import retrieve_users

# Load environment variables
load_dotenv()
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
SESSION_FILE = "session_id.txt"
with open(SESSION_FILE) as f:
    SESSION_ID = f.read().strip()
study_name = os.getenv("Study_name")

# Load user import template
template_path = "user-import-template-24r2.csv"
df = pd.read_csv(template_path, dtype=str).fillna("")

# Retrieve current studies, sites, and users
studies_df = retrieve_studies()
sites_df = retrieve_sites()
users_df = retrieve_users()

# Prepare lookup sets for fast existence checks
study_set = set(studies_df["study"]) if "study" in studies_df else set()
site_set = set(sites_df["site"]) if "site" in sites_df else set()
user_set = set(users_df["user_name"]) if "user_name" in users_df else set()

users_to_import = []
for idx, row in df.iterrows():
    user_key = row["User Name"]
    study = row.get("Study", study_name)
    site_access = row.get("Site Access", "")
    # Check study
    if study and study not in study_set:
        print(f"Skipping user {user_key}: Study '{study}' does not exist.")
        continue
    # Check site(s)
    if site_access:
        missing_sites = [site for site in site_access.split(",") if site and site not in site_set]
        if missing_sites:
            print(f"Skipping user {user_key}: Site(s) {missing_sites} do not exist.")
            continue
    # Check user duplication
    if user_key in user_set:
        print(f"Skipping user {user_key}: User already exists.")
        continue
    users_to_import.append(row.to_dict())

if not users_to_import:
    print("No new users to import.")
    exit(0)

# Prepare payload for JSON import
payload = {
    "append_site_country_access": False,
    "users": users_to_import
}

# Send the POST request to import users
url = f"{BASE_URL}/api/{API_VERSION}/app/cdm/users_json"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SESSION_ID}"
}
response = requests.post(url, headers=headers, data=json.dumps(payload))
response.raise_for_status()
print("Import response:")
print(json.dumps(response.json(), indent=4))