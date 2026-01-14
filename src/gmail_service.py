#login using OAuth
#fetch unread emails
#marks emails as read after processing


import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

TOKEN_FILE="token.pickle"
CREDENTIALS_FILE="credentials/credentials.json"

def get_gmail_service(scopes):
    creds=None

    if os.path.exists(TOKEN_FILE):   #no login required again
        with open(TOKEN_FILE,"rb") as f:
            creds=pickle.load(f)

    if not creds or not creds.valid:         #check validity
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow=InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE,scopes)
            creds=flow.run_local_server(port=0)
        with open(TOKEN_FILE,"wb") as f:
            pickle.dump(creds,f) #save new token
    return build("gmail","v1",credentials=creds)      #build gmail api client

def fetch_unread_emails(service):
    results=service.users().messages().list(
        userId="me",
        q="is:unread in:inbox"   #fetch_unread_emails()
    ).execute()

    return results.get("messages",[])

def mark_as_read(service,msg_id): 
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds":["UNREAD"]}     #so next time script runs->they won't be picked again
    ).execute()

