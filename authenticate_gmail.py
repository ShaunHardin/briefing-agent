"""
Gmail OAuth Authentication for Replit Environment.
Run this script, then click the link to authorize.
"""

import os
import json
from flask import Flask, request
from google_auth_oauthlib.flow import Flow
from threading import Thread
import webbrowser

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

app = Flask(__name__)
creds_data = None
server_started = False

@app.route('/oauth2callback')
def oauth2callback():
    global creds_data
    
    try:
        flow = Flow.from_client_secrets_file(
            'data/credentials.json',
            scopes=SCOPES,
            redirect_uri='http://localhost:5000/oauth2callback'
        )
        
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials
        
        os.makedirs('data', exist_ok=True)
        with open('data/token.json', 'w') as token:
            token.write(creds.to_json())
        
        creds_data = creds
        
        return """
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: #4CAF50;">✅ Authorization Successful!</h1>
                <p>Your Gmail connection is now authenticated.</p>
                <p>You can close this window and return to the terminal.</p>
                <p style="margin-top: 40px; color: #666;">
                    Next step: Run <code>python demo_gmail_connection.py</code>
                </p>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: #f44336;">❌ Authorization Failed</h1>
                <p>Error: {str(e)}</p>
                <p>Please try again.</p>
            </body>
        </html>
        """

def main():
    print("=" * 70)
    print("Gmail Authentication for Replit")
    print("=" * 70)
    print()
    
    if os.path.exists('data/token.json'):
        response = input("Token already exists. Re-authenticate? (y/n): ").strip().lower()
        if response != 'y':
            print("✅ Keeping existing token.")
            return
    
    if not os.path.exists('data/credentials.json'):
        print("❌ Error: credentials.json not found in data/ directory")
        return
    
    print("Starting OAuth server on port 5000...")
    print()
    
    flow = Flow.from_client_secrets_file(
        'data/credentials.json',
        scopes=SCOPES,
        redirect_uri='http://localhost:5000/oauth2callback'
    )
    
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    
    print("📋 Please click this link to authorize Gmail access:")
    print("-" * 70)
    print(auth_url)
    print("-" * 70)
    print()
    print("After authorizing, you'll be redirected back and see a success message.")
    print()
    print("⏳ Waiting for authorization...")
    
    def run_server():
        app.run(host='0.0.0.0', port=5000, debug=False)
    
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    import time
    while creds_data is None:
        time.sleep(1)
    
    print()
    print("✅ Authentication successful! Token saved to data/token.json")
    print()
    print("You can now run: python demo_gmail_connection.py")

if __name__ == '__main__':
    main()
