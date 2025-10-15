# Gmail OAuth Setup Guide

Follow these steps to set up Gmail API access with OAuth credentials.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Name it something like "Newsletter Digest Agent"

## Step 2: Enable Gmail API

1. In your Google Cloud project, go to **APIs & Services** → **Library**
2. Search for "Gmail API"
3. Click on it and press **Enable**

## Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - Choose **External** user type
   - Fill in App name: "Newsletter Digest Agent"
   - Add your email as a test user
   - Save and continue through the scopes (no need to add any)
4. Back at Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: "Newsletter Digest Desktop"
   - Click **Create**

## Step 4: Download Credentials

1. After creating, you'll see a dialog with your credentials
2. Click **DOWNLOAD JSON**
3. Save the file

## Step 5: Add to Replit

1. In your Replit project, go to the `data` folder
2. Upload or paste the contents of the downloaded JSON file
3. **Rename it to**: `gmail_credentials.json`
4. Make sure it's in: `data/gmail_credentials.json`

## Step 6: First-Time Authentication

1. Run the app (it will open an OAuth flow)
2. You'll be redirected to Google to authorize the app
3. Grant permission to read your Gmail
4. The app will save the token for future use

## Step 7: You're Done!

After the first authentication, the app will automatically refresh tokens as needed. No more manual intervention required - perfect for scheduled tasks!

## Troubleshooting

**"Unverified app" warning**: 
- Click "Advanced" → "Go to Newsletter Digest Agent (unsafe)"
- This is normal for personal projects not published on Google

**Can't find credentials file**:
- Make sure the file is named exactly `gmail_credentials.json`
- Make sure it's in the `data/` folder

**Token expired errors**:
- Delete `data/gmail_token.pickle` and re-authenticate
