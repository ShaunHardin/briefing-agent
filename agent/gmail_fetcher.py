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
    labels: Optional[List[str]] = None

    def __post_init__(self):
        """Initialize labels to empty list if None"""
        if self.labels is None:
            self.labels = []


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
                
                try:
                    creds = flow.run_local_server(port=0)
                except Exception:
                    print("\n⚠️  Local server failed. Using manual authorization flow instead.\n")
                    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    
                    print("Please visit this URL to authorize the application:")
                    print(auth_url)
                    print("\nAfter authorization, you'll see an authorization code.")
                    code = input("Enter the authorization code here: ").strip()
                    
                    flow.fetch_token(code=code)
                    creds = flow.credentials
            
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

    def fetch_newsletters(self, max_results: int = 10) -> List[Email]:
        """
        Fetch emails with 'newsletter' label from Gmail.

        This is a convenience method that filters for emails labeled as newsletters.

        Args:
            max_results: Maximum number of newsletter emails to fetch

        Returns:
            List of Email objects with newsletter label
        """
        return self.fetch_recent_emails(
            max_results=max_results,
            query='label:newsletter'
        )

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
            labels = message.get('labelIds', [])

            return Email(
                message_id=message_id,
                subject=subject or '(No Subject)',
                sender=sender or '(Unknown Sender)',
                date=date or '(Unknown Date)',
                body=body or '(No Content)',
                labels=labels
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
        """
        Recursively extract email body from payload.
        Prefers text/plain, falls back to text/html.
        """
        def extract_parts(part: dict, prefer_plain: bool = True) -> tuple[str, str]:
            """
            Recursively extract text/plain and text/html from parts.
            Returns: (plain_text, html_text)
            """
            plain_text = ''
            html_text = ''
            
            mime_type = part.get('mimeType', '')
            
            if 'parts' in part:
                for subpart in part['parts']:
                    sub_plain, sub_html = extract_parts(subpart, prefer_plain)
                    plain_text = plain_text or sub_plain
                    html_text = html_text or sub_html
            
            elif mime_type == 'text/plain' and 'data' in part.get('body', {}):
                try:
                    plain_text = base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8', errors='ignore')
                except Exception:
                    pass
            
            elif mime_type == 'text/html' and 'data' in part.get('body', {}):
                try:
                    html_text = base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8', errors='ignore')
                except Exception:
                    pass
            
            return plain_text, html_text
        
        plain, html = extract_parts(payload)
        return plain or html or ''
