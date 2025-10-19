"""
Gmail Fetcher - Connects to Gmail API and retrieves emails.
Implements the interface defined by our test suite.
"""

import os
import base64
from dataclasses import dataclass
from typing import List, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


@dataclass
class Email:
    """Email data structure"""
    message_id: str
    subject: str
    sender: str
    date: str
    body: str


class GmailFetcher:
    """Fetches emails from Gmail using the Gmail API"""
    
    def __init__(self, credentials_path: str = 'data/credentials.json', 
                 token_path: str = 'data/token.json'):
        """
        Initialize Gmail fetcher with authentication.
        
        Args:
            credentials_path: Path to OAuth credentials JSON file
            token_path: Path to store/load access token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0"""
        creds = None
        
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {self.credentials_path}. "
                        "Please download OAuth credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)
    
    def fetch_recent_emails(self, max_results: int = 10, 
                           query: Optional[str] = None) -> List[Email]:
        """
        Fetch recent emails from Gmail.
        
        Args:
            max_results: Maximum number of emails to fetch
            query: Gmail search query (e.g., "label:newsletters", "from:sender@example.com")
        
        Returns:
            List of Email objects
        """
        try:
            params = {
                'userId': 'me',
                'maxResults': max_results
            }
            
            if query:
                params['q'] = query
            
            results = self.service.users().messages().list(**params).execute()
            messages = results.get('messages', [])
            
            emails = []
            for message in messages:
                email = self._get_email_details(message['id'])
                if email:
                    emails.append(email)
            
            return emails
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def _get_email_details(self, message_id: str) -> Optional[Email]:
        """
        Get detailed information for a specific email.
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Email object or None if error
        """
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id, 
                format='full'
            ).execute()
            
            headers = message['payload'].get('headers', [])
            subject = self._get_header(headers, 'Subject')
            sender = self._get_header(headers, 'From')
            date = self._get_header(headers, 'Date')
            body = self._get_email_body(message['payload'])
            
            return Email(
                message_id=message_id,
                subject=subject or '(No Subject)',
                sender=sender or '(Unknown Sender)',
                date=date or '(Unknown Date)',
                body=body or '(No Content)'
            )
        
        except HttpError as error:
            print(f'Error fetching email {message_id}: {error}')
            return None
    
    def _get_header(self, headers: List[dict], name: str) -> Optional[str]:
        """Extract a specific header value from email headers"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return None
    
    def _get_email_body(self, payload: dict) -> str:
        """Extract email body from payload"""
        body = ''
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
        elif 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(
                payload['body']['data']
            ).decode('utf-8')
        
        return body
