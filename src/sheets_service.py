#login to google sheet api
#add new row to spreadsheet

import os
import pickle
from googleapiclient.discovery import build  #used to save and load login tokens
from google.auth.transport.requests import Request       #create googlesheets api client
from google_auth_oauthlib.flow import InstalledAppFlow    #handles oAuth login


TOKEN_FILE="token_sheets.pickle"              #saved login session 
CREDENTIALS_FILE="credentials/credentials.json"  #OAuth client config

def get_sheets_service(scopes):
    creds=None

    if os.path.exists(TOKEN_FILE):          #loads previous login session
        with open(TOKEN_FILE,"rb") as f:
            creds=pickle.load(f)

    if not creds or not creds.valid:            #if token expired or missing
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE,scopes)
            creds=flow.run_local_server(port=0)
        with open(TOKEN_FILE,"wb") as f:
            pickle.dump(creds,f)         #save new token
    return build("sheets","v4",credentials=creds)      #creates object to call google sheets API

def append_row(service,spreadsheet_id,sheet_name,row):       #writes data into spreadsheet
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values":[row]}

    ).execute()