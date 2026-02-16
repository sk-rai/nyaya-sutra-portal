# CodeSandbox Deployment Guide

## ✅ Files Ready for CodeSandbox

Your project is now properly structured for CodeSandbox deployment with a `public/` folder.

## 📁 Current Structure

```
nyaya-sutra-portal/
├── public/                    # ← CodeSandbox serves from here
│   ├── index.html            # Main page
│   ├── login.html            # Login page
│   ├── dashboard.html        # Landing page
│   ├── START_HERE.html       # Demo guide
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   └── assets/               # Images/icons
├── package.json              # Node.js config
├── sandbox.config.json       # CodeSandbox config
└── README.md                 # Documentation
```

## 🚀 Deployment Options

### Option 1: GitHub Import (Recommended)

1. **Push to GitHub:**
```bash
cd ~/Documents/POC/nyaya-sutra-portal
git init
git add .
git commit -m "Frontend mockup ready for CodeSandbox"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nyaya-sutra-portal.git
git push -u origin main
```

2. **Import to CodeSandbox:**
   - Go to https://codesandbox.io
   - Click "Create Sandbox"
   - Select "Import from GitHub"
   - Paste your repo URL: `https://github.com/YOUR_USERNAME/nyaya-sutra-portal`
   - CodeSandbox will auto-detect it as a static site

3. **Access Your Demo:**
   - CodeSandbox will provide a URL like: `https://xxxxx.csb.app`
   - Share this URL with your client

### Option 2: Direct Upload to CodeSandbox

1. **Create New Sandbox:**
   - Go to https://codesandbox.io
   - Click "Create Sandbox"
   - Select "Static" template

2. **Upload Files:**
   - Delete default files
   - Drag and drop your entire `public/` folder
   - Upload `package.json` and `sandbox.config.json` to root

3. **Verify Structure:**
   ```
   / (root)
   ├── public/
   │   ├── index.html
   │   ├── login.html
   │   ├── dashboard.html
   │   ├── css/
   │   ├── js/
   │   └── assets/
   ├── package.json
   └── sandbox.config.json
   ```

### Option 3: Convert Existing Sandbox

If you already have a sandbox:

1. Click "Convert to Devbox" button
2. In terminal, run:
```bash
npm install -g serve
serve public
```
3. Access via the preview URL

## 🧪 Testing After Deployment

1. **Open the deployed URL**
2. **Test unregistered view** - Should see limited case info
3. **Click Login** - Should navigate to login page
4. **Login with demo credentials:**
   - Unpaid: `unpaid@example.com` / `demo123`
   - Paid: `paid@example.com` / `demo123`
5. **Verify tier changes** - Content should update based on login

## 🔧 Troubleshooting

### Blank White Screen
**Cause:** Files not in `public/` folder  
**Fix:** Ensure all HTML/CSS/JS files are inside `public/`

### 404 Errors on CSS/JS
**Cause:** Incorrect file paths  
**Fix:** All paths in HTML should be relative (e.g., `css/base.css` not `/css/base.css`)

### Login Not Working
**Cause:** localStorage might be blocked  
**Fix:** Check browser console (F12) for errors, ensure cookies/storage enabled

### Styles Not Loading
**Cause:** Google Fonts blocked or CSS path wrong  
**Fix:** Check network tab in browser dev tools

## 📋 Pre-Deployment Checklist

- ✅ All files in `public/` folder
- ✅ `package.json` in root
- ✅ `sandbox.config.json` in root
- ✅ CSS paths are relative (no leading `/`)
- ✅ JS paths are relative (no leading `/`)
- ✅ All 3 HTML files present
- ✅ Demo credentials documented

## 🎯 Demo URLs to Share

Once deployed, share these pages:

1. **Main Demo:** `https://your-sandbox.csb.app/index.html`
2. **Login Page:** `https://your-sandbox.csb.app/login.html`
3. **Landing Page:** `https://your-sandbox.csb.app/dashboard.html`
4. **Quick Start:** `https://your-sandbox.csb.app/START_HERE.html`

## 💡 Tips for Client Demo

1. **Start with START_HERE.html** - It has all instructions
2. **Show the progression** - Unregistered → Unpaid → Paid
3. **Emphasize the tier system** - Core feature
4. **Mention it's a mockup** - Backend integration pending

## 🔗 Useful Links

- CodeSandbox: https://codesandbox.io
- Your Local Files: `~/Documents/POC/nyaya-sutra-portal`
- Documentation: See `README.md` and `DEMO_GUIDE.md`

---

**Ready to deploy!** 🚀

All files are properly structured for CodeSandbox. Choose your preferred deployment method above.
