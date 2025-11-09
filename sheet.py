# sheet.py
import os, json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# optional local path for dev
LOCAL_JSON = os.path.join(os.path.dirname(__file__), "bot", "gcp-service-account.json")

def _get_credentials():
    env_json = os.getenv("GCP_SERVICE_ACCOUNT_JSON")
    if env_json:
        info = json.loads(env_json)              # load from env var on Render
        return Credentials.from_service_account_info(info, scopes=SCOPES)
    if os.path.exists(LOCAL_JSON):               # local dev fallback
        return Credentials.from_service_account_file(LOCAL_JSON, scopes=SCOPES)
    raise RuntimeError(
        "Google credentials not found. Set GCP_SERVICE_ACCOUNT_JSON or provide bot/gcp-service-account.json"
    )

creds = _get_credentials()
client = gspread.authorize(creds)

def make_row(data, tg_user):
    return [
        data.get("business_name", ""),
        data.get("director", ""),
        data.get("company_name", ""),
        data.get("job_title", ""),
        data.get("phone", ""),
        data.get("email", ""),
        tg_user,
    ]

def append_submission(sheet_name, row):
    sh = client.open(sheet_name).sheet1
    sh.append_row(row)
