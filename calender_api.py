import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import click

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """
Authenticates and returns Google Calendar API credentials.

This function checks for existing credentials stored in 'token.json'.
If valid credentials are found, they are loaded; otherwise, it initiates
an OAuth2 flow to obtain new credentials. If the credentials are expired
but have a refresh token, they are refreshed. New credentials are saved
to 'token.json' for future use.

Returns:
    google.oauth2.credentials.Credentials: The authenticated credentials
    for accessing the Google Calendar API.
"""
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials as a JSON file
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_event(summary, start_time, end_time, timezone, attendees=None):
    creds = authenticate_google_calendar()
    service= build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': timezone,
        },
        'attendees': [{'email': attendee} for attendee in attendees] if isinstance(attendees, list) else attendees,
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    click.echo(f"event created: {event.get('htmlLink')}")
    return event.get('id')