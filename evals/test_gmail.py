"""
Test suite for Gmail fetcher functionality.
Following TDD: Tests written first, then implementation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agent.gmail_fetcher import GmailFetcher, Email


class TestGmailFetcher:
    """Test Gmail connection and email fetching"""
    
    @patch('agent.gmail_fetcher.GmailFetcher._authenticate')
    def test_can_initialize_fetcher(self, mock_auth):
        """Test that GmailFetcher can be initialized"""
        mock_service = Mock()
        mock_auth.return_value = mock_service
        
        fetcher = GmailFetcher()
        assert fetcher is not None
        assert hasattr(fetcher, 'service')
    
    @patch('agent.gmail_fetcher.GmailFetcher._authenticate')
    def test_fetch_recent_emails_returns_list(self, mock_auth):
        """Test that fetch_recent_emails returns a list"""
        mock_service = Mock()
        mock_auth.return_value = mock_service
        
        mock_messages = Mock()
        mock_messages.list().execute.return_value = {'messages': []}
        mock_service.users().messages.return_value = mock_messages
        
        fetcher = GmailFetcher()
        emails = fetcher.fetch_recent_emails(max_results=5)
        
        assert isinstance(emails, list)
    
    @patch('agent.gmail_fetcher.GmailFetcher._authenticate')
    def test_fetch_recent_emails_with_results(self, mock_auth):
        """Test fetching emails returns Email objects with expected fields"""
        mock_service = Mock()
        mock_auth.return_value = mock_service
        
        mock_message_data = {
            'id': 'msg123',
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': 'Test Newsletter'},
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'Date', 'value': 'Mon, 1 Jan 2025 12:00:00 +0000'}
                ],
                'body': {
                    'data': 'VGVzdCBib2R5IGNvbnRlbnQ='
                }
            }
        }
        
        mock_messages_list = Mock()
        mock_messages_list.list().execute.return_value = {
            'messages': [{'id': 'msg123'}]
        }
        
        mock_messages_get = Mock()
        mock_messages_get.get(userId='me', id='msg123', format='full').execute.return_value = mock_message_data
        
        mock_messages = Mock()
        mock_messages.list.return_value = mock_messages_list.list()
        mock_messages.get.return_value = mock_messages_get.get(userId='me', id='msg123', format='full')
        
        mock_service.users().messages.return_value = mock_messages
        
        fetcher = GmailFetcher()
        emails = fetcher.fetch_recent_emails(max_results=1)
        
        assert len(emails) > 0
        email = emails[0]
        assert isinstance(email, Email)
        assert hasattr(email, 'subject')
        assert hasattr(email, 'sender')
        assert hasattr(email, 'date')
        assert hasattr(email, 'body')
        assert hasattr(email, 'message_id')
    
    def test_email_has_valid_structure(self):
        """Test that Email dataclass has correct structure"""
        
        email = Email(
            message_id='test123',
            subject='Test Subject',
            sender='test@example.com',
            date='2025-01-01',
            body='Test body'
        )
        
        assert email.message_id == 'test123'
        assert email.subject == 'Test Subject'
        assert email.sender == 'test@example.com'
        assert email.date == '2025-01-01'
        assert email.body == 'Test body'
    
    @patch('agent.gmail_fetcher.GmailFetcher._authenticate')
    def test_handles_connection_errors_gracefully(self, mock_auth):
        """Test that connection errors are handled properly"""
        mock_auth.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception) as exc_info:
            fetcher = GmailFetcher()
        
        assert "Connection failed" in str(exc_info.value)
    
    @patch('agent.gmail_fetcher.GmailFetcher._authenticate')
    def test_fetch_with_query_filter(self, mock_auth):
        """Test fetching emails with a query filter (e.g., newsletters only)"""
        mock_service = Mock()
        mock_auth.return_value = mock_service
        
        mock_messages = Mock()
        mock_messages.list().execute.return_value = {'messages': []}
        mock_service.users().messages.return_value = mock_messages
        
        fetcher = GmailFetcher()
        emails = fetcher.fetch_recent_emails(max_results=5, query="label:newsletters")
        
        assert isinstance(emails, list)
