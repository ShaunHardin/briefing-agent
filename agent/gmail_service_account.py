import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import re
from email.utils import parsedate_to_datetime

# Gmail API scopes for reading messages
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service(user_email=None):
    """
    Get Gmail API service with service account authentication
    
    Args:
        user_email: Email address to impersonate (required for domain-wide delegation)
    
    Returns:
        Gmail API service
    """
    # Get service account credentials from Replit Secrets
    service_account_info = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY')
    
    if not service_account_info:
        raise EnvironmentError(
            "Service account credentials not found in Replit Secrets. "
            "Please add GOOGLE_SERVICE_ACCOUNT_KEY secret with your service account JSON. "
            "See README_GMAIL_SETUP.md for instructions."
        )
    
    # Parse service account JSON
    service_account_dict = json.loads(service_account_info)
    
    # Create credentials
    credentials = service_account.Credentials.from_service_account_info(
        service_account_dict,
        scopes=SCOPES
    )
    
    # If user_email provided, delegate to that user
    if user_email:
        credentials = credentials.with_subject(user_email)
    
    # Build and return Gmail service
    return build('gmail', 'v1', credentials=credentials)


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


def fetch_newsletters(days_back=7, max_results=50, query=None, user_email=None):
    """
    Fetch newsletters from Gmail using service account
    
    Args:
        days_back: Number of days to look back
        max_results: Maximum number of emails to fetch
        query: Gmail search query (e.g., 'from:newsletter@example.com')
        user_email: Email address to access (required for domain-wide delegation)
    
    Returns:
        List of newsletter dictionaries
    """
    try:
        # Get user email from environment if not provided
        if not user_email:
            user_email = os.environ.get('GMAIL_USER_EMAIL')
        
        if not user_email:
            raise EnvironmentError(
                "User email not specified. "
                "Please set GMAIL_USER_EMAIL in Replit Secrets (e.g., your@workspace.com)"
            )
        
        service = get_gmail_service(user_email=user_email)
        
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
    except Exception as e:
        print(f'Error: {e}')
        return []
