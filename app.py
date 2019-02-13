from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from dotenv import load_dotenv

# getting modules
from docs import report_backup_document


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# function to load evn files before app runs


def load_env_file():
    load_dotenv()


def main():
    """Shows basic usage of the Docs API.
       Prints the title of a sample document.
       """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=os.getenv("GOOGLE_DOCUMENT_ID")).execute()
    text = 'rachmann'
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=os.getenv("GOOGLE_DOCUMENT_ID"), body={'requests': requests}).execute()

    # writing json output to document
    json_data = json.dumps(document, indent=4)
    fp = open('document.json', 'a')
    fp.write(json_data)
    fp.close()

    print(result)

    print('Document written : {}'.format(document.get('title')))


def test():
    load_env_file()
    heading_one , heading_two = report_backup_document.get_doc()
    print(heading_one)
    print(heading_two)


if __name__ == '__main__':
    test()
