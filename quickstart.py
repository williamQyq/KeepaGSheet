from time import sleep
import os
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

from Laptops import Laptops


class GsheetApi:
    def __init__(self) -> None:
        self.SERVICE_ACCOUNT_FILE = 'keys.json'
        self.creds = None
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SAMPLE_SPREADSHEET_ID = '1yzaW4RLlLHc4kgxn1rn2WpaAxsh-g1tLBxhOb1WKIFQ'
        self.SAMPLE_RANGE_NAME = 'Keepa Data!A2'
        self.CLEAR_RANGES = ['Keepa Data!A2:F']
        if os.path.exists(self.SERVICE_ACCOUNT_FILE):
            serviceAccountFilePath = os.path.join(
                os.path.join(os.getcwd(), self.SERVICE_ACCOUNT_FILE))
            self.creds = service_account.Credentials.from_service_account_file(
                serviceAccountFilePath, scopes=self.SCOPES)
        else:
            serviceAccountFilePath = self.getExePath(self.SERVICE_ACCOUNT_FILE)
            self.creds = service_account.Credentials.from_service_account_file(
               serviceAccountFilePath, scopes=self.SCOPES)

    def getExePath(self, fileName):
        PATH = os.path.join(os.path.dirname(sys.executable), fileName)
        return PATH

    def updateSpreadSheet(self, aoa, spreadSheetID, range, clearRanges):
        DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = build(
            'sheets', 'v4', credentials=self.creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)

        sheet = service.spreadsheets()
        for range in clearRanges:  # clear all sheet range in clearRanges
            sheet.values().clear(spreadsheetId=spreadSheetID,
                                 range=range,
                                 body={}).execute()

        sheet.values().update(spreadsheetId=spreadSheetID,
                              range=range,
                              valueInputOption="USER_ENTERED",
                              body={"values": aoa}).execute()


def main():
    """Shows basic usage of the Keepa Search API.
    Prints search words products detial to a sample spreadsheet.
    """
    # search_words = sys.argv[1]

    while True:
        print("[Search Tool] Enter laptop search words: press enter to quit")
        search = input()

        if(search == ""):
            print("Ending...")
            break

        print("[Search Tool] Enter maximum sales rank: ex. default 15000")
        sr = input()
        if(sr == ""):
            sr = 15000

        laptop = Laptops(search, maxSalesRank=sr)

        try:
            aoa = laptop.getSearchedProductDetail()
            gsheet = GsheetApi()
            gsheet.updateSpreadSheet(aoa, gsheet.SAMPLE_SPREADSHEET_ID,
                                     gsheet.SAMPLE_RANGE_NAME, gsheet.CLEAR_RANGES)
        except Exception as e:
            print(f'[Warning]{e}...')

    sleep(3)


if __name__ == '__main__':
    main()
