# 🔐 Gmail OAuth Setup with Replit Secrets

Your app uses Replit Secrets to securely store Gmail credentials - they'll never be committed to GitHub!

## Quick Setup (5 minutes)

### Step 1: Get Google Cloud Credentials

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Gmail API**:
   - APIs & Services → Library
   - Search "Gmail API" → Enable

4. Create **OAuth 2.0 Client ID**:
   - APIs & Services → Credentials
   - Click "+ CREATE CREDENTIALS" → OAuth client ID
   - If prompted, configure consent screen:
     - User type: **External**
     - App name: "Newsletter Digest Agent"
     - Add your email to test users
   - Application type: **Desktop app**
   - Name it anything (e.g., "Newsletter Digest")
   - Click **Create**

5. **Download the JSON file**
   - After creation, download the credentials JSON

### Step 2: Add to Replit Secrets (Secure!)

1. **Open Replit Secrets**:
   - In your Replit workspace, find **Tools** → **Secrets** (or search for "Secrets")

2. **Add the secret**:
   - Click "Add new secret"
   - **Key**: `GMAIL_CREDENTIALS`
   - **Value**: Open the downloaded JSON file and paste the **entire contents**
   - Click "Add secret"

### Step 3: First-Time Authorization

1. Click "Fetch & Analyze" in the app
2. You'll see an authorization URL
3. Visit the URL and authorize Gmail access
4. Copy the authorization code
5. Paste it back in the app
6. Done! Token saves for future use

## Why This is Secure

✅ **Secrets never touch GitHub** - Stored separately in Replit  
✅ **Encrypted at rest** - Replit handles security  
✅ **Works in deployments** - Automatically available  
✅ **Token auto-refresh** - No manual intervention after setup

## For Scheduled/Automated Use

Once you complete the OAuth flow once:
- Token saves to `data/gmail_token.pickle` (also in .gitignore)
- Auto-refreshes when expired
- Works perfectly for scheduled daily runs
- No user interaction needed

## Troubleshooting

**"Unverified app" warning**: 
- Click "Advanced" → "Go to Newsletter Digest Agent (unsafe)"
- Normal for personal projects

**Can't find Secrets pane**:
- Try Tools menu or use Cmd/Ctrl+K and search "secrets"

**Secret not loading**:
- Make sure key is exactly: `GMAIL_CREDENTIALS`
- Restart the workflow after adding secret

---

**Next Step**: Add your `GMAIL_CREDENTIALS` secret, then run the app!
