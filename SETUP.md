# Gmail API Setup Instructions

✅ **Status: OAuth setup is complete and working!**

This document explains how the Gmail API was configured for reference. The OAuth credentials are already in place and the connection is active.

## Current Setup

- OAuth credentials: `data/credentials.json` (gitignored)
- Access token: `data/token.json` (gitignored, auto-refreshes)
- Test mode: 7-day token expiry (re-authenticate weekly)
- Status: ✅ Connected and fetching emails

---

## For Reference: How This Was Set Up

If you need to recreate the OAuth setup or set this up elsewhere:

### Prerequisites

- A Google account
- Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name your project (e.g., "Newsletter Digest Agent")
4. Click "Create"

## Step 2: Enable Gmail API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

## Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" (unless you have a Google Workspace)
   - App name: "Newsletter Digest Agent"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" for now
   - Add your email as a test user
   - Click "Save and Continue"

4. Back at "Create OAuth client ID":
   - Application type: "Desktop app"
   - Name: "Newsletter Digest Desktop"
   - Click "Create"

5. Download the JSON file (click the download icon)

## Step 4: Add Credentials to Your Project

1. Create the `data` directory in your project (if it doesn't exist):
   ```bash
   mkdir -p data
   ```

2. Rename the downloaded JSON file to `credentials.json`

3. Move it to the `data` directory in your project

## Step 5: Authenticate

**Note:** This step has already been completed for this project.

To authenticate (or re-authenticate after 7 days):

1. The OAuth flow requires manual code entry in Replit
2. You'll receive an authorization code after granting permissions
3. The token is saved to `data/token.json`

To test the connection:

```bash
python demo_gmail_connection.py
```

This will fetch and display your 5 most recent emails.

## Re-Authentication (After 7 Days)

Since the app is in "Testing" mode, tokens expire after 7 days. When you need to re-authenticate:

1. Delete `data/token.json`
2. Run `python demo_gmail_connection.py`
3. Follow the OAuth flow again

## Troubleshooting

**Error: "Credentials file not found"**
- Make sure `credentials.json` is in the `data/` directory
- Check that it's not corrupted (valid JSON format)

**Error: "Access blocked: This app's request is invalid"**
- Make sure you added yourself as a test user in the OAuth consent screen
- Verify the app is in "Testing" publishing status

**Error: "Token has been expired or revoked"**
- Delete `data/token.json` and re-authenticate
- This is normal after 7 days in Testing mode

## Security Notes

- `credentials.json` and `token.json` are in `.gitignore`
- Never commit these files to version control
- The app only has read-only access to your Gmail
- Tokens can be revoked at any time in your Google Account settings

## Next Steps

Once the connection is working:
1. Run tests: `pytest evals/test_gmail.py -v` (should see 10 passing tests)
2. Start building the newsletter synthesis features
3. Create filters for newsletter-specific emails

## Known Edge Cases

The Gmail fetcher handles most common email formats, but be aware of:

- **Large attachments**: Currently ignored; body extraction focuses on text/plain and text/html parts
- **Non-UTF8 encodings**: Decoded with `errors='ignore'` to prevent crashes, but may lose some characters
- **Embedded images**: Not extracted; only text content is retrieved
- **Very large emails**: May hit API size limits; consider pagination if needed

These edge cases will be addressed as needed based on real-world newsletter data.
