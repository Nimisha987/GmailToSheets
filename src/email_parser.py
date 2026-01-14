#take a gmail message->extract from,subject, data and body(plain text)


import base64
from bs4 import BeautifulSoup
from dateutil import parser
import re


def parse_email(service,msg_id):
    msg=service.users().messages().get(userId="me",id=msg_id,format="full").execute()
    headers=msg["payload"]["headers"] #extracting headers

    data={"From":"","Subject":"","Date":"","Content":""}

    for h in headers:
        if h["name"]=="From":
            data["From"]=h["value"]
        elif h["name"]=="Subject":
            data["Subject"]=h["value"]
        elif h["name"]=="Date":
            data["Date"]=str(parser.parse(h["value"]))

    body=""
    def extract(parts):
        nonlocal body
        for part in parts:
            if part.get("mimeType")=="text/plain":  #if body is plain text
                body=base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8",errors="ignore")
                return
            elif part.get("mimeType")=="text/html":
                html=base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8",errors="ignore")
                soup=BeautifulSoup(html,"html.parser")
                body=soup.get_text()
                return
            elif part.get("parts"):
                extract(part["parts"])
    if "parts" in msg["payload"]:
        extract(msg["payload"]["parts"])
    else:
        body=base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode("utf-8",errors="ignore")
    MAX_LEN = 30000
    clean_body = body.strip()
    clean_body = re.sub(r'https?://\S+', '[LINK]', clean_body)


    if len(clean_body) > MAX_LEN:
        clean_body = clean_body[:MAX_LEN] + "\n\n[TRUNCATED]"


    data["Content"] = clean_body

    return data

