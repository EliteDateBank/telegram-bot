import gspread
from google.oauth2.service_account import Credentials
import os

# Google Sheets setup
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "bot", "gcp-service-account.json")

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

def make_row(user_data, tg_user):
    """Prepare one row of data to write to Google Sheets."""
    return [
        user_data.get("business_name", ""),
        user_data.get("director", ""),
        user_data.get("company_name", ""),
        user_data.get("job_title", ""),
        user_data.get("phone", ""),
        user_data.get("email", ""),
        tg_user
    ]

def append_submission(sheet_name, row):
    """Append a row to the Google Sheet."""
    try:
        sheet = client.open(sheet_name).sheet1
        sheet.append_row(row)
        print("✅ Data appended successfully.")
    except Exception as e:
        print(f"⚠️ Could not append to Google Sheet: {e}")
