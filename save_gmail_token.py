"""
Simple script to save Gmail token using authorization code.
"""

import os
import json
from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    print("=" * 70)
    print("Save Gmail Token")
    print("=" * 70)
    print()
    
    if not os.path.exists('data/credentials.json'):
        print("❌ Error: credentials.json not found")
        return
    
    print("Paste the full URL you were redirected to:")
    print("(It should contain '?state=...&code=...')")
    print()
    redirect_url = input("URL: ").strip()
    
    if 'code=' not in redirect_url:
        print("❌ Error: No authorization code found in URL")
        return
    
    try:
        flow = Flow.from_client_secrets_file(
            'data/credentials.json',
            scopes=SCOPES,
            redirect_uri='http://localhost:5000/oauth2callback'
        )
        
        flow.fetch_token(authorization_response=redirect_url)
        creds = flow.credentials
        
        os.makedirs('data', exist_ok=True)
        with open('data/token.json', 'w') as token:
            token.write(creds.to_json())
        
        print()
        print("✅ Success! Token saved to data/token.json")
        print()
        print("Now run: python demo_gmail_connection.py")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you pasted the complete redirect URL.")

if __name__ == '__main__':
    main()
