import os
import json
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import re
from email.utils import parsedate_to_datetime


def get_access_token():
    """Get Gmail access token from Replit connection"""
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    x_replit_token = None
    
    if os.environ.get('REPL_IDENTITY'):
        x_replit_token = 'repl ' + os.environ['REPL_IDENTITY']
    elif os.environ.get('WEB_REPL_RENEWAL'):
        x_replit_token = 'depl ' + os.environ['WEB_REPL_RENEWAL']
    
    if not x_replit_token:
        raise Exception('X_REPLIT_TOKEN not found for repl/depl')
    
    response = requests.get(
        f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-mail',
        headers={
            'Accept': 'application/json',
            'X_REPLIT_TOKEN': x_replit_token
        }
    )
    
    data = response.json()
    connection_settings = data.get('items', [{}])[0]
    
    access_token = (
        connection_settings.get('settings', {}).get('access_token') or 
        connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
    )
    
    if not access_token:
        raise Exception('Gmail not connected')
    
    return access_token


def get_gmail_service():
    """Create and return Gmail API service"""
    access_token = get_access_token()
    creds = Credentials(token=access_token)
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
    Fetch newsletters from Gmail
    
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
            # Default: look for newsletters (common patterns)
            full_query = f"(from:newsletter OR from:digest OR subject:newsletter OR subject:digest OR label:newsletters) {date_query}"
        
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
