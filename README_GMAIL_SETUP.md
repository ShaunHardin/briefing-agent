# 🔐 Quick Gmail OAuth Setup

Your app is now ready to use Gmail API with OAuth for full inbox access!

## Quick Start (5 minutes)

### 1. Get Google Cloud Credentials

Visit: **[console.cloud.google.com](https://console.cloud.google.com/)**

1. Create a new project
2. Enable **Gmail API** (APIs & Services → Library)
3. Create **OAuth 2.0 Client ID** (APIs & Services → Credentials):
   - Configure consent screen (External, add yourself as test user)
   - Create credentials: Desktop app
   - Download JSON file

### 2. Add to Your Project

1. Save the downloaded JSON file to your project
2. Rename it to: `data/gmail_credentials.json`

### 3. First-Time Auth

1. Run the app
2. Click "Fetch & Analyze" 
3. Follow the OAuth flow to authorize Gmail access
4. Done! Token saves automatically for future use

## What This Gives You

✅ **Full inbox access** - Read all emails with label:newsletter  
✅ **Auto token refresh** - No manual intervention needed  
✅ **Works with scheduled tasks** - Perfect for daily automation  
✅ **Secure** - OAuth tokens stored locally, credentials in .gitignore

## For Scheduled/Production Use

Once OAuth is complete, your saved token (`data/gmail_token.pickle`) will be used automatically. This works perfectly for:
- Scheduled deployments (daily digest runs)
- Autoscale deployments (on-demand access)
- Local development

The token auto-refreshes when expired - no maintenance required!

---

Need detailed instructions? See `setup_gmail.md`
