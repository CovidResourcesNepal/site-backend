from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from service.apiKey import APIKEY


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BQZvGqM3Ao48A6lHo_U1yfkFzb8DWPPnqhExFd6X8-8'
SAMPLE_RANGE_NAME = 'List of Fundraisers!C6:I'


def get_fundraisers_json():
    """
    Get the fundraisers data from the sheet as JSON
    """
    service = build('sheets', 'v4', developerKey=APIKEY)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    links_dict = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, fields="sheets/data/rowData/values/hyperlink", ranges=['D6:D']).execute()

    hyperlinks = links_dict['sheets'][0]['data'][0]['rowData']
    values = result.get('values', [])

    all_fundraisers = []
    if not values:
        print('No data found.')
    else:
        for i, row in enumerate(values):
            fundraiser = {
                'name': row[0].strip(),
                'platform': row[1].lower().replace(' ', '').strip(),
                'url': hyperlinks[i]['values'][0]['hyperlink'],
                'stated_goal': row[2].strip(),
                'fundraising_goal': int(row[3].replace(',', '')) if row[3] else None,
                'fund_raised': int(row[4].replace(',', '')) if row[4] else None,
                'currency': row[5].strip(),
                'category': row[6].strip()
            }
            all_fundraisers.append(fundraiser)
    return all_fundraisers

if __name__ == '__main__':
    fundraisers = get_fundraisers_json()
    print(fundraisers)