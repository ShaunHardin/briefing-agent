#!/usr/bin/env python3
"""
Test script to check for newsletter-labeled emails in live Gmail.
"""

from agent.gmail_fetcher import GmailFetcher

def main():
    print("🔍 Connecting to Gmail...")
    fetcher = GmailFetcher()
    
    print("\n📧 Fetching emails with 'newsletter' label...")
    newsletters = fetcher.fetch_newsletters(max_results=5)
    
    if newsletters:
        print(f"\n✅ Found {len(newsletters)} newsletter(s):\n")
        for i, email in enumerate(newsletters, 1):
            print(f"{i}. Subject: {email.subject}")
            print(f"   From: {email.sender}")
            print(f"   Date: {email.date}")
            print(f"   Labels: {email.labels}")
            print(f"   Body preview: {email.body[:100]}...")
            print()
    else:
        print("\n⚠️  No emails found with 'newsletter' label.")
        print("\nLet's check what labels you have:")
        
        # Fetch some recent emails to see what labels exist
        print("\n📬 Fetching 5 recent emails to check labels...")
        recent = fetcher.fetch_recent_emails(max_results=5)
        
        if recent:
            print(f"\n✅ Found {len(recent)} recent email(s):\n")
            all_labels = set()
            for i, email in enumerate(recent, 1):
                print(f"{i}. Subject: {email.subject}")
                print(f"   From: {email.sender}")
                print(f"   Labels: {email.labels}")
                all_labels.update(email.labels)
                print()
            
            print(f"\n📋 All unique labels found: {sorted(all_labels)}")
        else:
            print("\n⚠️  No recent emails found.")

if __name__ == "__main__":
    main()
