# Gmail API Setup Instructions

This guide will help you set up Gmail API access for the Newsletter Digest Agent.

## Prerequisites

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

## Step 5: Test the Connection

Run the demo script:

```bash
python demo_gmail_connection.py
```

On first run:
- A browser window will open
- Sign in with your Google account
- Grant permissions to read your Gmail
- The token will be saved for future use

## Troubleshooting

**Error: "Credentials file not found"**
- Make sure `credentials.json` is in the `data/` directory

**Error: "Access blocked: This app's request is invalid"**
- Make sure you added yourself as a test user in the OAuth consent screen

**Error: "The user did not consent to the scopes required"**
- You need to grant permission to read your Gmail

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
