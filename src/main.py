#controls the full workflow of the automation system

import json
from gmail_service import get_gmail_service, fetch_unread_emails,mark_as_read
from sheets_service import get_sheets_service,append_row
from email_parser import parse_email
from config import SCOPES,SPREADSHEET_ID,SHEET_NAME

STATE_FILE="state.json"   #stores alread process email IDs

def load_state():         #is missing->returns empty list
    try:
        with open(STATE_FILE,"r") as f:
            return json.load(f)
        
    except:
        return {"processed_ids":[]}
    
def save_state(state):   #updates file after new emails processed
    with open(STATE_FILE,"w") as f:
        json.dump(state,f,indent=2)

def main():
    gmail_service=get_gmail_service(SCOPES)   #connect to gmail
    sheets_service=get_sheets_service(SCOPES) #connect to sheets

    emails=fetch_unread_emails(gmail_service)   #fetch unread emails
    state=load_state()      #load previous state

    print(f"Found {len(emails)} unread_emails")

    for email in emails:
        msg_id=email["id"]

        if msg_id in state["processed_ids"]:   #skip duplicates
            continue
 
        data=parse_email(gmail_service,msg_id) #extract fields

        row=[      
            data["From"],
            data["Subject"],
            data["Date"],
            data["Content"]
        ]
        append_row(sheets_service,SPREADSHEET_ID,SHEET_NAME,row)    #append to google sheets

        state["processed_ids"].append(msg_id)      #save id to state

        mark_as_read(gmail_service,msg_id) #mark email read

        print(f"Processed: {data['Subject']}")

    save_state(state)      #save updated state
    print("Done.")

if __name__=="__main__":
    main()