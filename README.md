# Nyaya Sutra Legal Portal - Frontend Mockup

A modern, professional web portal for legal professionals to track court cases with tier-based access control.

## 🎯 Demo Instructions

### Quick Start (Local Testing)

1. Open `index.html` in your browser
2. You'll see the case search page as an unregistered user (limited view)
3. Click "Login / Register" to access the login page
4. Use demo credentials to test different tier levels

### Demo Credentials

**Free User (Unpaid Tier):**
- Email: `unpaid@example.com`
- Password: `demo123` (any password works)
- Access: Case number, date, bench, type, status

**Premium User (Paid Tier):**
- Email: `paid@example.com`
- Password: `demo123` (any password works)
- Access: Full details including counsel, venue, print & copy features

### Features to Demonstrate

#### 1. Tier-Based Access Control
- **Unregistered**: Only case number and date visible
- **Unpaid**: + Bench, case type, and status
- **Paid**: + Counsel names, venue, print/copy functionality

#### 2. User Experience
- Clean navy/gold professional theme
- Responsive card-based layout
- Dynamic content rendering based on user tier
- Login/logout functionality with user menu

#### 3. Security Features
- Print/copy restrictions for non-paid users
- Tier-based content visibility
- Session management via localStorage

## 📁 File Structure

```
nyaya-sutra-portal/
├── index.html              # Main case search page (dynamic tier-aware)
├── dashboard.html          # Landing page with features/pricing
├── login.html              # Login page with demo credentials
├── css/
│   ├── base.css           # Core styles and variables
│   ├── components.css     # UI component styles
│   └── tiers.css          # Tier-specific styling
├── js/
│   ├── auth.js            # Authentication & user management
│   ├── tier-renderer.js   # Case card rendering logic
│   └── print-control.js   # Print/copy restrictions
└── backend/               # (Backend - not yet implemented)
```

## 🚀 Deployment Options

### Option A: CodeSandbox (Recommended)

**Files are ready!** All content is in the `public/` folder as required by CodeSandbox.

1. Push code to GitHub:
```bash
git init
git add .
git commit -m "Frontend mockup complete"
git remote add origin https://github.com/YOUR_USERNAME/nyaya-sutra-portal.git
git push -u origin main
```

2. In CodeSandbox:
   - Click "Create Sandbox"
   - Select "Import from GitHub"
   - Paste your repository URL
   - CodeSandbox will automatically detect it as a static site

**See `CODESANDBOX_DEPLOY.md` for detailed deployment instructions.**

### Option B: Local Server

```bash
# Using Python (from project root)
python -m http.server 8000
# Then open: http://localhost:8000/public/

# Using Node.js (serves public folder)
npx serve public
# Then open: http://localhost:3000

# Or open START_HERE.html directly in browser
```

## 🎨 Design Highlights

- **Color Scheme**: Navy (#0a192f) + Gold (#ffd700) for professional legal aesthetic
- **Typography**: Inter (UI) + Merriweather (headings)
- **Layout**: Card-based with clean shadows and spacing
- **Responsive**: Works on desktop, tablet, and mobile

## 📋 Next Steps (Phase 2)

1. Build Flask backend with API endpoints
2. Implement real authentication (JWT tokens)
3. Add database models (PostgreSQL/MySQL)
4. Integrate PDF scraping for AFT Delhi & CGAT
5. Add SMS/WhatsApp alert system
6. Implement payment gateway for subscriptions

## 🔗 Court Data Sources

- AFT Delhi: https://aftdelhi.nic.in/index.php/reg-benches/mumbai/mumbai-cause-list
- CGAT: https://cis.cgat.gov.in/catlive/pdf/

## 📝 Notes

- This is a frontend mockup with mock data
- Authentication is client-side only (for demo purposes)
- Backend integration pending
- All case data is currently hardcoded

---

**Prepared for**: Santosh Rai  
**Date**: February 15, 2026  
**Status**: Frontend Complete ✅
