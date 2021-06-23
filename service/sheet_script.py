from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from service.apiKey import APIKEY


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def make_fundraisers_json(row, url):
    return {
        'name': row[0].strip(),
        'platform': row[1].lower().replace(' ', '').strip(),
        'url': url,
        'stated_goal': row[2].strip(),
        'fundraising_goal': int(row[3].replace(',', '')) if row[3] else None,
        'fund_raised': int(row[4].replace(',', '')) if row[4] else None,
        'currency': row[5].strip(),
        'category': row[6].strip()
    }

def make_food_json(row, url):
    return {
        'name': row[0].strip(),
        'contact': row[1].strip().split(', '),
        'platform': row[2].strip(),
        'url': url,
        'areas': row[3].strip(),
        'detailed_location': row[4].strip(),
        'focus': row[5].strip()
    }

def make_general_json(row, url):
    return {
        'name': row[0].strip(),
        'contact': row[1].strip().split(', '),
        'platform': row[2].strip(),
        'url': url,
        'areas': row[3].strip(),
        'detailed_location': row[4].strip(),
        'focus': row[5].strip()
    }

# The ID and range of a sample spreadsheet.
SHEET_ID = {
    'fundraisers': '1BQZvGqM3Ao48A6lHo_U1yfkFzb8DWPPnqhExFd6X8-8',
    'food': '1S7JcDkfHdxu_iEZU5RklNT8buKCGv68vjetNKIg0nws',
    'general': '16ynrRYS3Qg6dVRG7UdQ2Gp4OdBpQ7doGdiCIkXdG9-0'
}
SHEET_RANGE = {
    'fundraisers': 'List of Fundraisers!C6:I',
    'food': 'Food Resources!A3:F'
}
HYPERLINK_RANGE = {
    'fundraisers': 'D6:D',
    'food': 'C3:C'
}
TO_JSON_FUNCTIONS = {
    'fundraisers': make_fundraisers_json,
    'food': make_food_json,
}



def get_json(to_extract):
    """
    Get the fundraisers data from the sheet as JSON
    """
    sheet_id = SHEET_ID[to_extract]
    sheet_range = SHEET_RANGE[to_extract]
    to_json_function = TO_JSON_FUNCTIONS[to_extract]
    hyperlink_range = HYPERLINK_RANGE[to_extract]

    service = build('sheets', 'v4', developerKey=APIKEY)
    # Call the Sheets API
    sheet = service.spreadsheets()
    if hyperlink_range:
        links_dict = sheet.get(spreadsheetId=sheet_id, fields="sheets/data/rowData/values/hyperlink", ranges=[hyperlink_range]).execute()
        hyperlinks = links_dict['sheets'][0]['data'][0]['rowData']
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get('values', [])

    all_fundraisers = []
    if not values:
        print('No data found.')
    else:
        for i, row in enumerate(values):
            try:
                url = hyperlinks[i]['values'][0]['hyperlink']
            except:
                url = None
            fundraiser = to_json_function(row, url)
            all_fundraisers.append(fundraiser)
    return all_fundraisers

if __name__ == '__main__':
    to_extract = 'fundraisers'
    fundraisers = get_json(to_extract)
    print(fundraisers)