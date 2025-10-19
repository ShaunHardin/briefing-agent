# 🔐 Gmail Service Account Setup

Your app uses a Google Workspace service account to access Gmail - perfect for automation!

## Prerequisites

✅ You have Google Workspace (not personal Gmail)  
✅ You are a Workspace admin (or can ask one for help)  
✅ You have created a service account

## Quick Setup (10 minutes)

### Step 1: Enable Domain-Wide Delegation

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **IAM & Admin** → **Service Accounts**
4. Find your service account: `newsletter-summary@sodium-petal-457318-m6.iam.gserviceaccount.com`
5. Click on it → **Show Domain-Wide Delegation** → **Enable Domain-Wide Delegation**
6. Note the **Client ID** (you'll need this next)

### Step 2: Authorize in Workspace Admin

1. Go to [Google Workspace Admin Console](https://admin.google.com/)
2. Navigate to **Security** → **API Controls** → **Domain-wide Delegation**
3. Click **Add new**
4. Enter:
   - **Client ID**: (from service account)
   - **OAuth Scopes**: `https://www.googleapis.com/auth/gmail.readonly`
5. Click **Authorize**

### Step 3: Download Service Account Key

1. Back in Google Cloud Console → Service Accounts
2. Click your service account
3. Go to **Keys** tab
4. Click **Add Key** → **Create new key**
5. Choose **JSON** format
6. Download the key file

### Step 4: Add to Replit Secrets

1. Open the downloaded JSON file
2. In Replit, go to **Tools** → **Secrets**
3. Add two secrets:

**Secret 1:**
- **Key**: `GOOGLE_SERVICE_ACCOUNT_KEY`
- **Value**: Paste the entire JSON contents

**Secret 2:**
- **Key**: `GMAIL_USER_EMAIL`
- **Value**: Your Workspace email (e.g., `you@yourworkspace.com`)

4. Click "Add secret" for each

### Step 5: Test It!

1. Restart your app
2. Click "Fetch & Analyze"
3. Your newsletters should load automatically!

## Why This Works

✅ **No OAuth flow** - Service account authenticates directly  
✅ **Perfect for automation** - No user interaction needed  
✅ **Works in deployments** - Scheduled tasks work seamlessly  
✅ **Secure** - Secrets never touch GitHub  

## Troubleshooting

**"User email not specified"**:
- Make sure you added `GMAIL_USER_EMAIL` secret

**"Insufficient Permission"**:
- Check domain-wide delegation is enabled
- Verify the Gmail scope is authorized in Admin Console
- Confirm you're using the correct Client ID

**"Access denied"**:
- Ensure the user email is in your Workspace domain
- Verify the service account has domain-wide delegation

---

**Next Step**: Add your secrets and test the app!
