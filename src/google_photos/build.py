import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials


def authenticate():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # if creds and creds.expired and creds.refresh_token:
        #     creds.refresh(Request())
        # else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    google_photos = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    return google_photos


def authenticate_with_service_account():
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'photos-manager-347304-af417add9d6f.json', SCOPES)
    google_photos = build('photoslibrary', 'v1', credentials=credentials, static_discovery=False)
    return google_photos