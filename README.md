# Gmail to Google Sheets Automation System

---

## Project Overview

This project is a Python automation system that reads real unread emails from a Gmail inbox using the Gmail API and logs them into a Google Spreadsheet using the Google Sheets API.

Each qualifying email is stored as a new row in the spreadsheet with the following fields:

* From (Sender email)
* Subject
* Date & Time received
* Content (plain text body)

The system uses OAuth 2.0 authentication and ensures that:

* Only unread inbox emails are processed
* Emails are marked as read after processing
* Duplicate emails are never added
* Only new emails since the previous run are appended

---

## High-Level Architecture

```
+------------------+
|   Gmail Inbox    |
+------------------+
         |
         v
+------------------+
|   Gmail API      |
+------------------+
         |
         v
+------------------+        +-------------------+
|  email_parser.py | -----> |   state.json      |
+------------------+        | (Processed IDs)   |
         |
         v
+------------------+
| Google Sheets API|
+------------------+
         |
         v
+------------------+
| Google Sheet     |
+------------------+
```

---

##  Project Structure

```
gmail-to-sheets/
│
├── src/
│   ├── gmail_service.py
│   ├── sheets_service.py
│   ├── email_parser.py
│   └── main.py
│
├── credentials/
│   └── credentials.json   (not committed)
│
├── state.json
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup Instructions (Step-by-Step)

### 1. Create Google Cloud Project

* Go to Google Cloud Console
* Create a new project
* Enable:

  * Gmail API
  * Google Sheets API

### 2. Configure OAuth 2.0

* Configure OAuth consent screen (External)
* Create OAuth Client ID (Desktop App)
* Download `credentials.json`
* Place it inside the `credentials/` folder

### 3. Create Google Sheet

* Create a sheet named: `Gmail Logs`
* Add header row:

```
From | Subject | Date | Content
```

* Copy Spreadsheet ID and add it to `config.py`

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Project

```bash
python src/main.py
```

Browser will open for OAuth permission on first run.

---

##  OAuth Flow Explanation

The project uses **OAuth 2.0 Installed Application Flow**:

1. Application opens a browser window
2. User logs in with Google account
3. User grants Gmail & Sheets permissions
4. Google returns an access token
5. Token is stored locally in a token file
6. Future runs reuse the token automatically

No passwords or API keys are stored in code.

---

##  Duplicate Prevention Logic

Duplicate emails are prevented using:

* Gmail Message IDs (unique for every email)
* A local file: `state.json`

Before processing any email:

* The program checks if its ID exists in `state.json`
* If yes → skip
* If no → process and store ID

This guarantees that no email is logged twice, even if the script is run multiple times.

---

##  State Persistence Method

State is stored in a file called:

```
state.json
```

Example:

```json
{
  "processed_ids": ["18c1f2...", "18c1f3..."]
}
```

### Why this approach was chosen:

* Simple to implement
* Lightweight
* Works offline
* No database required
* Easy to explain
* Reliable duplicate prevention

---

##  Challenges Faced

**Challenge:**

Extracting clean email content from Gmail was difficult because emails may be:

* Plain text
* HTML
* Multipart (nested parts)

**Solution:**

* Implemented recursive parsing
* Used Base64 decoding
* Converted HTML to plain text using BeautifulSoup

This ensures readable and consistent content is stored in Google Sheets.

---

## Limitations

* Only processes inbox unread emails
* Requires manual OAuth approval on first run
* Depends on Google API availability
* Local state file can be deleted accidentally
* No real-time processing (script-based)

---

##  Proof of Execution

The following proofs are provided in the `/proof` folder:

* Gmail inbox with unread emails
* Google Sheet populated with at least 5 rows
* OAuth consent screen screenshot
* Screen recording video (2–3 minutes) showing:

  * Script execution
  * Data transfer
  * Duplicate prevention
  * Second run behavior

---

##  Bonus Features Implemented

* HTML → Plain text conversion
* Persistent state storage
* Duplicate prevention
* Token reuse
* Modular code structure

---

##  Security Measures

* `credentials.json` is excluded via `.gitignore`
* OAuth tokens are stored locally only
* No secrets committed to repository

---

##  Conclusion

This project demonstrates secure API integration, state management, and automation best practices using Python, Gmail API, and Google Sheets API.

It satisfies all mandatory technical and functional requirements specified in the assignment.

---

**End of README**
