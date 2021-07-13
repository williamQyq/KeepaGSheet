from __future__ import print_function
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google.oauth2 import service_account 

from Laptops import getKeepaLaptop


SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1yzaW4RLlLHc4kgxn1rn2WpaAxsh-g1tLBxhOb1WKIFQ'
SAMPLE_RANGE_NAME = 'Keepa Data!A2'
CLEAR_RANGE = 'Keepa Data!A2:E'
CLEAR_SALES_RANGE = 'Product Research!H2:H'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    search_words = sys.argv[1]

    aoa = getKeepaLaptop(search_words)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    resultClear = sheet.values().clear( spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=CLEAR_RANGE,
                                        body={}).execute()
    resultSalesClear = sheet.values().clear( spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=CLEAR_SALES_RANGE,
                                        body={}).execute()
                                        

    result = sheet.values().update( spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME,
                                    valueInputOption="USER_ENTERED",
                                    body={"values":aoa}).execute()
 
if __name__ == '__main__':
    main()