import os
import json
import pickle
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import re
from email.utils import parsedate_to_datetime

# Gmail API scopes for reading messages
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Token storage path
TOKEN_PATH = 'data/gmail_token.pickle'
CREDENTIALS_PATH = 'data/gmail_credentials.json'


def get_gmail_service():
    """Get Gmail API service with OAuth authentication"""
    creds = None
    
    # Load saved credentials if they exist
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired token
            creds.refresh(Request())
        else:
            # Check if credentials file exists
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Gmail OAuth credentials not found at {CREDENTIALS_PATH}. "
                    "Please download your OAuth 2.0 credentials from Google Cloud Console "
                    "and save them as 'data/gmail_credentials.json'"
                )
            
            # Run OAuth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            
            # For Replit, we need to use the out-of-band flow
            # since we can't use localhost callback
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)


def extract_email_body(payload):
    """Extract text content from email payload"""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
            elif part['mimeType'] == 'text/html' and not body:
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    else:
        if 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    
    return body


def clean_text(text):
    """Remove HTML tags and clean up text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    return text.strip()


def fetch_newsletters(days_back=7, max_results=50, query=None):
    """
    Fetch newsletters from Gmail using OAuth
    
    Args:
        days_back: Number of days to look back
        max_results: Maximum number of emails to fetch
        query: Gmail search query (e.g., 'from:newsletter@example.com')
    
    Returns:
        List of newsletter dictionaries
    """
    try:
        service = get_gmail_service()
        
        # Build query
        date_query = f"after:{(datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')}"
        
        if query:
            full_query = f"{query} {date_query}"
        else:
            # Default: look for newsletter label
            full_query = f"label:newsletter {date_query}"
        
        # Fetch messages
        results = service.users().messages().list(
            userId='me',
            q=full_query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        newsletters = []
        
        for msg in messages:
            # Get full message
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            # Extract headers
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            
            # Extract body
            body = extract_email_body(message['payload'])
            
            # Parse date
            date_str = headers.get('Date', '')
            try:
                email_date = parsedate_to_datetime(date_str) if date_str else datetime.now()
            except:
                email_date = datetime.now()
            
            newsletter = {
                'id': msg['id'],
                'subject': headers.get('Subject', 'No Subject'),
                'from': headers.get('From', 'Unknown'),
                'date': email_date.isoformat(),
                'body': clean_text(body),
                'raw_body': body
            }
            
            newsletters.append(newsletter)
        
        return newsletters
    
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []
    except FileNotFoundError as e:
        print(f'Setup Error: {e}')
        return []
