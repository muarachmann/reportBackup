from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1L5ZK9ia043t-6kmCJpkIcjU9eHLrBtf7wyAtwHsyJiU'


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
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
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
        documentId=DOCUMENT_ID, body={'requests': requests}).execute()

    # writing json output to document
    json_data = json.dumps(document, indent=4)
    fp = open('document.json', 'a')
    fp.write(json_data)
    fp.close()

    print(result)

    print('Document written : {}'.format(document.get('title')))


if __name__ == '__main__':
    main()
