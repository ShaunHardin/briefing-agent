"""
Demo script to test Gmail connection.
Fetches and displays your 5 most recent emails.
"""

from agent.gmail_fetcher import GmailFetcher


def main():
    """Test Gmail connection by fetching recent emails"""
    print("=" * 60)
    print("Gmail Connection Test")
    print("=" * 60)
    print()
    
    try:
        print("Initializing Gmail fetcher...")
        fetcher = GmailFetcher()
        print("✓ Authentication successful!")
        print()
        
        print("Fetching your 5 most recent emails...")
        emails = fetcher.fetch_recent_emails(max_results=5)
        
        if not emails:
            print("No emails found.")
            return
        
        print(f"✓ Found {len(emails)} emails")
        print()
        print("=" * 60)
        
        for i, email in enumerate(emails, 1):
            print(f"\nEmail #{i}")
            print("-" * 60)
            print(f"From:    {email.sender}")
            print(f"Subject: {email.subject}")
            print(f"Date:    {email.date}")
            print(f"Preview: {email.body[:100]}...")
            print("-" * 60)
        
        print()
        print("✓ Gmail connection test successful!")
        print()
        print("Next steps:")
        print("  - Try filtering newsletters with: fetch_recent_emails(query='label:newsletters')")
        print("  - Run tests with: pytest evals/test_gmail.py")
        
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print()
        print("Please follow the setup instructions in SETUP.md")
    except Exception as e:
        print(f"✗ Error: {e}")
        print()
        print("Check that you've completed the OAuth setup correctly.")


if __name__ == "__main__":
    main()
