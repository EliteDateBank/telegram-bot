import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

# ✅ Correct scopes — both Sheets and Drive included
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ✅ Path to your Google Cloud service-account key
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "gcp-service-account.json")


def get_worksheet(sheet_name: str):
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sh = client.open(sheet_name)
    return sh.sheet1  # First worksheet


def append_submission(sheet_name: str, row: list[str]):
    ws = get_worksheet(sheet_name)
    ws.append_row(row, value_input_option="USER_ENTERED")


def make_row(data: dict, telegram_user: str):
    return [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("business_name", ""),
        data.get("director", ""),
        data.get("company_name", ""),
        data.get("job_title", ""),
        data.get("phone", ""),
        data.get("email", ""),
        telegram_user,
    ]
