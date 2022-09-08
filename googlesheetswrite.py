import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account


def sheets_write(data):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

        credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        SAMPLE_SPREADSHEET_ID = '1b2efbObEozcLoaWfU42uSHaDHI4z-AiXni_XuKDzQ48'

        service = build('sheets', 'v4', credentials=credentials)

        sheet = service.spreadsheets()
        sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='L2!A1:G',
                                        valueInputOption="USER_ENTERED", body={'values': data}).execute()

        print('Successfully recorded in google sheets!')

