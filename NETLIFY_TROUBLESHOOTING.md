# Netlify Deployment Troubleshooting

## Current Issue

Files are showing in the Netlify deploy file browser but returning 404 when accessed via URL.

## Root Cause

The Netlify site settings may not be configured to use the `public/` directory as the publish directory.

## SOLUTION: Manual Netlify Configuration Required

### Step 1: Update Site Settings in Netlify Dashboard

1. **Go to Site Settings:**
   - Visit: https://app.netlify.com/sites/prismatic-halva-095761/settings/deploys

2. **Update Build Settings:**
   - Scroll to "Build settings" section
   - Click "Edit settings" button
   - Set the following:
     - **Base directory:** (leave empty)
     - **Build command:** (leave empty or set to `echo "Static site"`)
     - **Publish directory:** `public`
   - Click "Save"

3. **Clear Cache and Redeploy:**
   - Go to: https://app.netlify.com/sites/prismatic-halva-095761/deploys
   - Click "Trigger deploy" dropdown
   - Select "Clear cache and deploy site"
   - Wait for deployment to complete (1-2 minutes)

### Step 2: Verify Deployment

After the deploy completes, test these URLs:

1. **Root (should redirect to dashboard):**
   ```
   https://prismatic-halva-095761.netlify.app/
   ```

2. **Landing Page:**
   ```
   https://prismatic-halva-095761.netlify.app/dashboard.html
   ```

3. **Registration:**
   ```
   https://prismatic-halva-095761.netlify.app/register.html
   ```

4. **Login:**
   ```
   https://prismatic-halva-095761.netlify.app/login.html
   ```

5. **My Dashboard:**
   ```
   https://prismatic-halva-095761.netlify.app/my-dashboard.html
   ```

6. **Calendar:**
   ```
   https://prismatic-halva-095761.netlify.app/calendar.html
   ```

## Alternative: Deploy via Netlify CLI

If the above doesn't work, use Netlify CLI to deploy directly:

```bash
# Install Netlify CLI (if not already installed)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Navigate to project directory
cd ~/Documents/POC/nyaya-sutra-portal

# Link to existing site
netlify link

# When prompted, select:
# - "Use current git remote origin"
# - Or manually enter site ID: prismatic-halva-095761

# Deploy to production
netlify deploy --prod --dir=public

# Follow the prompts and confirm
```

## What Should Happen

After correct configuration:

1. **Root URL** (https://prismatic-halva-095761.netlify.app/) 
   - Should redirect to `/dashboard.html`
   - Shows landing page with user personas

2. **All Pages Accessible:**
   - `/dashboard.html` - Landing page ✅
   - `/register.html` - Registration form ✅
   - `/login.html` - Login with OTP ✅
   - `/my-dashboard.html` - User dashboard ✅
   - `/calendar.html` - Calendar view ✅
   - `/index.html` - Search page ✅

3. **Assets Loading:**
   - CSS files from `/css/` folder
   - JS files from `/js/` folder
   - Images from `/assets/` folder

## Verification Checklist

After deployment, verify:

- [ ] Root URL redirects to dashboard.html
- [ ] Dashboard shows "Streamlined Legal Case Management"
- [ ] Dashboard shows 4 user persona icons
- [ ] Register button works and opens register.html
- [ ] Registration form shows user type selection
- [ ] Login page shows Email/Phone field
- [ ] Login page shows Captcha field
- [ ] All CSS styling is applied correctly
- [ ] Navigation links work

## Current File Structure (Confirmed in Deploy)

According to your deploy log, these files ARE deployed:

```
Root of deployed site:
├── assets/
│   └── (1 file)
├── css/
│   ├── base.css
│   ├── components.css
│   └── tiers.css
├── js/
│   ├── auth.js
│   ├── print-control.js
│   └── tier-renderer.js
├── calendar.html (18.4 KB) ✅
├── dashboard.html (10.2 KB) ✅
├── index.html (7.9 KB) ✅
├── login.html (13.8 KB) ✅
├── my-dashboard.html (16.6 KB) ✅
├── netlify.toml (387 B) ✅
├── register.html (14.7 KB) ✅
└── start_here.html (5.9 KB) ✅
```

## Why 404 Errors Occur

The 404 errors happen when:

1. **Publish directory not set:** Netlify doesn't know where to serve files from
2. **Old cache:** Previous deploy settings are cached
3. **Build settings override:** Site settings override netlify.toml

## The Fix

The `netlify.toml` file is now in the repository with correct settings:

```toml
[build]
  publish = "public"
  command = "echo 'No build needed - static site'"

[[redirects]]
  from = "/"
  to = "/dashboard.html"
  status = 301
```

But Netlify site settings may need manual update (Step 1 above).

## Expected Behavior After Fix

### Landing Page (dashboard.html)
Should show:
- Hero: "Streamlined Legal Case Management For Legal Professionals & Individuals"
- 4 persona cards with icons
- Updated pricing (Individuals vs Legal Professionals)
- "Register if New" and "Sign In" buttons

### Registration Page (register.html)
Should show:
- User type selection (Individual/Advocate radio buttons)
- Full registration form
- 3 plan selection boxes
- Advocate-specific fields (conditional)

### Login Page (login.html)
Should show:
- "Sign In" title
- "For entry to Personalized Page" subtitle
- Email/Phone input field
- Captcha with refresh button
- OTP input (appears after captcha verification)

### Dashboard (my-dashboard.html)
Should show:
- Personalized greeting
- "My Cases" section with add form
- Court selector buttons (AFT, CAT, High Court, Supreme Court)
- Search functionality
- Orders/Judgements section

### Calendar (calendar.html)
Should show:
- View toggle (Cause List / Calendar View)
- Court filter tabs
- Location filters
- Table view with case data
- Calendar widget with hearing dates
- News ticker

## If Still Not Working

### Check Browser Cache
1. Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
2. Or open in incognito/private window

### Check Netlify Deploy Log
1. Go to: https://app.netlify.com/sites/prismatic-halva-095761/deploys
2. Click latest deploy
3. Check "Deploy log"
4. Look for: "Publish directory: public"
5. Verify no errors in log

### Contact Netlify Support
If manual configuration doesn't work, there may be an account-level issue.

## Summary

**Action Required:** Manually set "Publish directory" to `public` in Netlify site settings, then trigger a new deploy.

**Expected Result:** All pages accessible at their respective URLs.

**Timeline:** 2-3 minutes after triggering new deploy.

---

**Last Updated:** February 18, 2026  
**Status:** Awaiting manual Netlify configuration  
**Next Deploy:** After site settings update

