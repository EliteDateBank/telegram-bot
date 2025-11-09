import os
import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def _get_credentials():
    env_json = os.getenv("GCP_SERVICE_ACCOUNT_JSON")
    if env_json:
        # ✅ Use JSON from environment (Render-safe)
        info = json.loads(env_json)
        return Credentials.from_service_account_info(info, scopes=SCOPES)
    
    # 🔙 Local fallback for development
    local_path = os.path.join(os.path.dirname(__file__), "gcp-service-account.json")
    if os.path.exists(local_path):
        return Credentials.from_service_account_file(local_path, scopes=SCOPES)
    
    raise RuntimeError("❌ No Google credentials found (neither environment nor local file).")

# Initialize Google client
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
    sh.append_row(row, value_input_option="USER_ENTERED")
