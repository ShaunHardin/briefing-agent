#!/usr/bin/env python3
"""
Simple integration test for Gmail service account access
Run: python test_gmail_connection.py
"""

import os
import sys
from agent.gmail_service_account import fetch_newsletters

def test_gmail_connection():
    """Test Gmail API connection and newsletter fetching"""
    
    print("="*60)
    print("Gmail Service Account Integration Test")
    print("="*60)
    
    # Check for required secrets
    print("\n1. Checking Replit Secrets...")
    
    service_account_key = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY')
    user_email = os.environ.get('GMAIL_USER_EMAIL')
    
    if not service_account_key:
        print("   ❌ GOOGLE_SERVICE_ACCOUNT_KEY not found in secrets")
        return False
    else:
        print("   ✅ Service account key found")
    
    if not user_email:
        print("   ❌ GMAIL_USER_EMAIL not found in secrets")
        return False
    else:
        print(f"   ✅ User email found: {user_email}")
    
    # Test Gmail connection
    print("\n2. Testing Gmail API connection...")
    
    try:
        newsletters = fetch_newsletters(days_back=7, max_results=5)
        
        print(f"   ✅ Successfully connected to Gmail")
        print(f"   📧 Found {len(newsletters)} newsletters")
        
        if newsletters:
            print("\n3. Sample newsletters:")
            for i, nl in enumerate(newsletters[:3], 1):
                print(f"\n   Newsletter {i}:")
                print(f"   - From: {nl['from']}")
                print(f"   - Subject: {nl['subject']}")
                print(f"   - Date: {nl['date'][:10]}")
                print(f"   - Body preview: {nl['body'][:100]}...")
        else:
            print("\n   ⚠️  No newsletters found with label:newsletter in the last 7 days")
            print("   💡 Try adding the 'newsletter' label to some emails in Gmail")
        
        print("\n" + "="*60)
        print("✅ TEST PASSED - Gmail connection working!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"   ❌ Error connecting to Gmail: {e}")
        print("\n" + "="*60)
        print("❌ TEST FAILED")
        print("="*60)
        print("\nTroubleshooting:")
        print("1. Verify domain-wide delegation is enabled for your service account")
        print("2. Check that gmail.readonly scope is authorized in Workspace Admin")
        print("3. Ensure GMAIL_USER_EMAIL is a valid Workspace email")
        print("4. Confirm the service account JSON is correct")
        return False

if __name__ == "__main__":
    success = test_gmail_connection()
    sys.exit(0 if success else 1)
