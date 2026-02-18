# Nyaya Sutra Portal - Demo URLs & Features

**Live Site:** https://prismatic-halva-095761.netlify.app  
**Date:** February 18, 2026  
**Status:** ✅ Ready for Client Review

---

## 🌐 All Page URLs

### 1. Landing Page (Home)
**URL:** https://prismatic-halva-095761.netlify.app/dashboard.html

**Features:**
- Hero section with updated tagline: "Streamlined Legal Case Management For Legal Professionals & Individuals"
- 4 User Personas displayed horizontally:
  - 🎖️ Defence Personnel
  - 🛡️ BSF, ITBP
  - 🏛️ Central Gov Services
  - 👨‍👩‍👦 Individuals with Jawan
- Welcome message about service matters at Supreme Court, High Courts, CATs, and AFTs
- "Register if New" and "Sign In" buttons
- Search Cases section (teaser with sample cases)
- Key Features section (Hearing Alerts, Case Tracking, Audio Case Lists, Bare Acts & Forms)
- Restructured Pricing:
  - **For Individuals:** ₹50/feature/month
  - **For Legal Professionals:** ₹360-₹1,200/month
- Professional navy/gold theme throughout

---

### 2. Registration Page
**URL:** https://prismatic-halva-095761.netlify.app/register.html

**Features:**
- User type selection with visual cards:
  - 👤 Individual
  - ⚖️ Advocate
- Complete registration form:
  - Full Name
  - Email Address
  - Phone Number
  - Address
- Plan selection with 3 visual boxes:
  - Basic (₹50)
  - Standard (₹360) - Pre-selected
  - Premium (₹1,200)
- **Advocate-specific fields** (appear when Advocate is selected):
  - Date of Enrollment
  - Bar Council dropdown (Delhi, Mumbai, Pune, Bangalore, Chennai, Kolkata, Other)
- "Create Account" button
- Link to login page for existing users
- Back to home link

**Demo Flow:**
1. Select user type (Individual or Advocate)
2. Fill in personal details
3. Select a plan
4. If Advocate selected, additional fields appear
5. Click "Create Account"
6. Redirects to personalized dashboard

---

### 3. Login Page (with OTP)
**URL:** https://prismatic-halva-095761.netlify.app/login.html

**Features:**
- Title: "Sign In - For entry to Personalized Page"
- Demo credentials displayed prominently
- **Email ID / Phone No** input (flexible login)
- **Captcha field** with refresh button
- **OTP-based authentication flow:**
  1. Enter email/phone + captcha
  2. Click "Send OTP"
  3. OTP input appears (6-digit boxes)
  4. OTP auto-fills for demo
  5. Click "Verify & Sign In"
- "Register / Sign Up" link
- Back to home link

**Demo Credentials:**
- **Free User:** `unpaid@example.com` or `+91 9999999999`
- **Premium User:** `paid@example.com` or `+91 8888888888`
- **Password:** Any (not used in OTP flow)
- **Captcha:** Displayed on screen (e.g., AB12CD)
- **OTP:** Auto-filled (any 6 digits work for demo)

**Demo Flow:**
1. Enter email or phone
2. Enter captcha shown on screen
3. Click "Send OTP"
4. OTP auto-fills in 6 boxes
5. Click "Verify & Sign In"
6. Redirects to personalized dashboard

---

### 4. Personalized Dashboard (My Dashboard)
**URL:** https://prismatic-halva-095761.netlify.app/my-dashboard.html

**Features:**
- **Personalized greeting:** "Hi, [User Name]"
- User menu with tier badge and logout button
- Navigation: My Dashboard, Calendar, Search Cases

**Section A: My Cases**
- Form to add new cases:
  - Case Number input
  - Title of Case input
  - Court selector buttons: [AFT] [CAT] [High Court] [Supreme Court]
  - "Add Case" button
- List of user's cases with:
  - Case number and court badge (color-coded)
  - Case title
  - Date added
  - "View Details" and "Delete" buttons

**Section B: Search My Cases**
- Search filters:
  - Case Number
  - Case Name
  - Advocate Name
  - "Search" button
- Court filter buttons: All Courts, AFT, CAT, High Court, Supreme Court

**Section C: Orders/Judgements/Decree**
- Court selection tabs: [AFT] [CAT] [High Court] [SC]
- Placeholder for orders display (ready for backend integration)

**Section D: Synopsis**
- Judgement synopsis display area
- Placeholder (ready for content integration)

**Demo Flow:**
1. Login with demo credentials
2. See personalized greeting
3. Add a new case (e.g., "AFT/DEL/2026/1111")
4. View case in list
5. Search/filter cases
6. Delete a case

**Demo Cases Pre-loaded:**
- AFT/DEL/2023/1234 - Rajesh Kumar vs. Union of India
- CAT/DEL/2024/5678 - Suresh Patel vs. Ministry of Defence

---

### 5. Calendar & Cause List
**URL:** https://prismatic-halva-095761.netlify.app/calendar.html

**Features:**
- **View Toggle:**
  - 📋 Cause List (Table View)
  - 📅 Calendar View

**Cause List (Table View):**
- Comprehensive table with columns:
  - S.No
  - Court Name/No
  - Case No
  - Title of Case
  - Advocate Names
  - Orders of Case
  - Penultimate Hearing
  - Next Date of Hearing
- Court filter tabs: [AFT] [CAT] [High Court] [Supreme Court]
- Location filters: Delhi, Mumbai, Jaipur, Offbeat Benches
- Sample data displayed

**Calendar View:**
- Interactive monthly calendar (February 2026)
- Hearing dates highlighted in blue
- Click on dates to see scheduled hearings
- Previous/Next month navigation
- Court filter tabs: [AFT] [CAT] [High Court] [SC]
- Location filters: Delhi, Mumbai, Jaipur, Offbeat Benches

**News Section:**
- Scrolling news ticker with latest legal updates
- Sample news: "Supreme Court announces new guidelines for service matters • AFT Delhi to conduct special hearings..."

**Demo Flow:**
1. View Cause List table
2. Filter by court (AFT, CAT, etc.)
3. Filter by location (Delhi, Mumbai, etc.)
4. Switch to Calendar View
5. Click on highlighted dates (15, 18, 20, 22, 25)
6. See hearing details popup
7. Navigate to next/previous month

---

### 6. Search Cases (Public)
**URL:** https://prismatic-halva-095761.netlify.app/index.html

**Features:**
- Redirects logged-in users to My Dashboard
- For non-logged-in users:
  - Search input field
  - Sample case cards (limited view)
  - "Login to View Details" buttons
  - Tier-based content display

**Note:** This page now primarily serves as a redirect. Logged-in users are automatically sent to their personalized dashboard.

---

### 7. Demo Guide
**URL:** https://prismatic-halva-095761.netlify.app/START_HERE.html

**Features:**
- Interactive demo instructions
- Links to all pages
- Demo credentials
- Testing guide

---

## 🎯 Key Features Summary

### ✅ Implemented Features

1. **User Segmentation**
   - Clear distinction between Individuals and Legal Professionals
   - Different pricing tiers
   - Advocate-specific registration fields

2. **OTP Authentication**
   - Email OR Phone number login
   - Captcha security
   - 6-digit OTP verification
   - Auto-fill for demo purposes

3. **Personalized Dashboard**
   - User-specific greeting
   - My Cases management (add/edit/delete)
   - Search and filter functionality
   - Court-specific organization

4. **Court Selector System**
   - Buttons for: AFT, CAT, High Court, Supreme Court
   - Color-coded badges
   - Consistent across all pages

5. **Calendar & Cause List**
   - Dual view (Table and Calendar)
   - Location-based filtering
   - Hearing date highlights
   - Interactive calendar widget

6. **Professional Design**
   - Navy (#0a192f) + Gold (#ffd700) theme
   - Responsive layout
   - Clean, uncluttered interface
   - Proper alignment across all sections

7. **Navigation**
   - Consistent header across pages
   - User menu with tier badge
   - Logout functionality
   - Breadcrumb-style navigation

---

## 🔄 User Flows

### New User Journey:
```
Landing Page → Register (select user type) → 
Login (OTP) → My Dashboard → Add Cases → 
View Calendar → Search Cases
```

### Returning User Journey:
```
Login (OTP) → My Dashboard → 
Manage Cases / View Calendar / Search
```

### Guest User Journey:
```
Landing Page → View Features/Pricing → 
Register or Login
```

---

## 🎨 Design Highlights

- **Color Scheme:** Navy (#0a192f) + Gold (#ffd700)
- **Court Colors:**
  - AFT: Blue (#1976d2)
  - CAT: Green (#2e7d32)
  - High Court: Purple (#7b1fa2)
  - Supreme Court: Red (#c62828)
- **Typography:** Inter (UI) + Merriweather (headings)
- **Layout:** Card-based with clean shadows
- **Responsive:** Works on desktop, tablet, mobile

---

## 📱 Responsive Design

All pages are fully responsive:
- **Desktop (> 1024px):** Full layout with side-by-side sections
- **Tablet (768px - 1024px):** Adjusted grid layouts
- **Mobile (< 768px):** Single column, stacked layout

---

## 🧪 Testing Instructions

### Test 1: Registration Flow
1. Go to: https://prismatic-halva-095761.netlify.app/dashboard.html
2. Click "Register if New"
3. Select "Advocate"
4. Fill in details
5. Select "Standard" plan
6. Verify advocate fields appear
7. Click "Create Account"
8. Verify redirect to dashboard

### Test 2: Login Flow (Free User)
1. Go to: https://prismatic-halva-095761.netlify.app/login.html
2. Enter: `unpaid@example.com`
3. Enter captcha shown on screen
4. Click "Send OTP"
5. Verify OTP auto-fills
6. Click "Verify & Sign In"
7. Verify redirect to dashboard with "Free User" badge

### Test 3: Login Flow (Premium User)
1. Go to login page
2. Enter: `paid@example.com`
3. Complete OTP flow
4. Verify "Premium User" badge
5. Verify full access to features

### Test 4: Case Management
1. Login as any user
2. Go to My Dashboard
3. Add a new case:
   - Case No: "TEST/2026/001"
   - Title: "Test Case"
   - Court: AFT
4. Verify case appears in list
5. Search for the case
6. Delete the case

### Test 5: Calendar View
1. Login as any user
2. Click "Calendar" in navigation
3. View Cause List table
4. Switch to Calendar View
5. Click on date 20 (has hearing)
6. Verify popup shows hearing details
7. Filter by court (CAT)
8. Filter by location (Mumbai)

### Test 6: Responsive Design
1. Open any page
2. Resize browser window
3. Verify layout adjusts properly
4. Test on mobile device
5. Verify all features accessible

---

## 💡 What's Mock Data (For Demo)

The following use mock/demo data:
- ✅ OTP verification (any 6 digits work)
- ✅ Captcha validation (shown on screen)
- ✅ Case data (hardcoded examples)
- ✅ Calendar hearings (demo dates: 15, 18, 20, 22, 25)
- ✅ News ticker (static content)
- ✅ User authentication (localStorage)

**For Production:** These will need backend APIs.

---

## 🔜 Not Yet Implemented (Backend Required)

- ❌ Real OTP sending via SMS/Email
- ❌ Database storage for users and cases
- ❌ Real court data scraping/API
- ❌ Payment gateway integration
- ❌ Bar Council validation
- ❌ Email/SMS alerts for hearings
- ❌ PDF generation for orders/judgements
- ❌ Real news feed integration

---

## 📊 Page Inventory

| # | Page | URL | Status | Purpose |
|---|------|-----|--------|---------|
| 1 | Landing | /dashboard.html | ✅ Complete | Marketing & pricing |
| 2 | Registration | /register.html | ✅ Complete | User signup |
| 3 | Login | /login.html | ✅ Complete | OTP authentication |
| 4 | My Dashboard | /my-dashboard.html | ✅ Complete | Personal case management |
| 5 | Calendar | /calendar.html | ✅ Complete | Cause list & calendar |
| 6 | Search | /index.html | ✅ Complete | Public case search (redirects if logged in) |
| 7 | Demo Guide | /START_HERE.html | ✅ Complete | Testing instructions |

**Total Pages:** 7  
**Status:** All functional and deployed

---

## 🎬 Demo Script (5 Minutes)

### Minute 1: Landing Page
- Show updated hero with 4 personas
- Highlight restructured pricing
- Point out "Register if New" and "Sign In" buttons

### Minute 2: Registration
- Click "Register if New"
- Select "Advocate"
- Show advocate-specific fields
- Demonstrate plan selection

### Minute 3: Login with OTP
- Enter demo credentials
- Show captcha
- Demonstrate OTP flow
- Show auto-fill for demo

### Minute 4: Personalized Dashboard
- Show personalized greeting
- Add a new case
- Demonstrate court selector
- Show search functionality

### Minute 5: Calendar View
- Switch to Calendar
- Show table view
- Switch to calendar view
- Click on hearing date
- Show filters (court and location)

---

## 📞 Support & Feedback

**For Questions or Changes:**
- Review all pages thoroughly
- Test all user flows
- Note any modifications needed
- Provide feedback on design/functionality

**Next Steps After Approval:**
1. Backend API development
2. Real OTP integration
3. Database setup
4. Payment gateway
5. Court data integration
6. Production deployment

---

## ✅ Summary

**Status:** ✅ All pages complete and deployed  
**Functionality:** ✅ All mockup requirements implemented  
**Design:** ✅ Professional and responsive  
**Ready for:** ✅ Client review and feedback

**Live Site:** https://prismatic-halva-095761.netlify.app

---

**Prepared by:** Development Team  
**Date:** February 18, 2026  
**Version:** 2.0 (Client Mockup Implementation)

