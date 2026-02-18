# Implementation Roadmap - Client Mockup Changes

**Date:** February 18, 2026  
**Based on:** 4 paper mockups from client

---

## 🎯 Quick Summary

### What's New:
- **4 new major features** (Registration, User Dashboard, Calendar, News)
- **3 existing pages need updates** (Landing, Login, Case Search)
- **10+ new components** required

### Effort Estimate:
- **Frontend Only:** 3-5 days
- **With Backend:** 2-3 weeks

---

## 📱 Screen-by-Screen Breakdown

### 🏠 Screen 1: Landing Page (dashboard.html)
**Current:** Generic landing with features/pricing  
**Required:** User persona-focused with updated pricing

**Changes:**
```
✏️ MODIFY EXISTING
├── Hero Section
│   ├── Update title: "STREAMLINED LEGAL CASE MANAGEMENT..."
│   ├── Add 4 user personas with icons
│   │   ├── Defense Personnel
│   │   ├── BSF, ITBP
│   │   ├── Central Gov Services
│   │   └── Individuals with Jawan
│   └── Update welcome message
├── Pricing Section
│   ├── Split into 2 categories:
│   │   ├── Individuals (~₹50/feature)
│   │   └── Legal Professionals (₹500-unlimited)
│   └── Update feature lists
└── Features Section
    ├── Emphasize SMS/WhatsApp alerts
    └── Add court calendar mention
```

**Effort:** 2-3 hours

---

### 🔐 Screen 2: Sign In Page (login.html)
**Current:** Simple email/password login  
**Required:** Email/Phone + OTP authentication

**Changes:**
```
✏️ MODIFY EXISTING + 🆕 ADD NEW
├── Login Form
│   ├── Change: Email OR Phone Number input
│   ├── Add: Captcha field
│   ├── Add: OTP input field
│   └── Update flow: Enter credentials → Verify OTP → Login
├── Registration Link
│   └── Add prominent "Register / Sign Up" button
└── 🆕 NEW: Registration Page (register.html)
    ├── User Type Selection
    │   ├── Radio: Individual
    │   └── Radio: Advocate
    ├── Basic Info
    │   ├── Name
    │   ├── Email
    │   ├── Phone
    │   └── Address
    ├── Plan Selection (3 visual boxes)
    └── Advocate-Only Fields (conditional)
        ├── Date of Enrollment
        └── Bar Council Dropdown
```

**Effort:** 4-6 hours (frontend), 1-2 days (with OTP backend)

---

### 👤 Screen 3: Personalized Dashboard (NEW: my-dashboard.html)
**Current:** Basic case search page  
**Required:** Full user dashboard with case management

**Changes:**
```
🆕 CREATE NEW PAGE
├── Header
│   └── Personalized greeting: "Hi, Mr. [Name]"
├── Section A: My Cases
│   ├── Form to add new case
│   │   ├── Case Number
│   │   ├── Title of Case
│   │   └── Court Selection: [AFT] [CAT] [HighCourt] [Supreme]
│   └── List of user's cases
├── Section B: Search My Cases
│   ├── Court filter buttons
│   ├── Case number search
│   ├── Case name search
│   └── Advocate name search
├── Section C: Orders/Judgements/Decree
│   ├── Case details display
│   └── Court selection tabs
└── Section D: Synopsis
    └── Judgement synopsis display area
```

**Effort:** 6-8 hours (frontend), 2-3 days (with backend CRUD)

---

### 📅 Screen 4: Case List & Calendar (NEW: calendar.html)
**Current:** Card-based case display only  
**Required:** Table view + Calendar view with filters

**Changes:**
```
🆕 CREATE NEW FEATURES
├── View Toggle
│   ├── List View (Table)
│   └── Calendar View
├── Section A: Cause List (Table View)
│   ├── Columns:
│   │   ├── S.No
│   │   ├── Court Name/No
│   │   ├── Case No
│   │   ├── Title of Case
│   │   ├── Advocate Names
│   │   ├── Orders of Case
│   │   ├── Penultimate Hearing
│   │   └── Next Date of Hearing
│   └── Sortable/Filterable
├── Section B: Calendar View
│   ├── Court Tabs: [AFT] [CAT] [HighCourt] [SC]
│   ├── Location Filters
│   │   ├── Delhi, Mumbai, Jaipur
│   │   └── Other cities
│   ├── Offbeat Benches filter
│   └── Calendar widget with hearing dates
└── Section C: News
    └── News ticker/feed component
```

**Effort:** 8-10 hours (frontend), 3-4 days (with backend integration)

---

## 🧩 New Components Required

### 1. Court Selector Component
```html
<div class="court-selector">
  <button class="court-btn" data-court="aft">AFT</button>
  <button class="court-btn" data-court="cat">CAT</button>
  <button class="court-btn" data-court="highcourt">High Court</button>
  <button class="court-btn" data-court="supreme">Supreme Court</button>
</div>
```
**Usage:** Dashboard, Calendar, Search pages  
**Effort:** 1 hour

### 2. OTP Input Component
```html
<div class="otp-input">
  <input type="text" maxlength="1" />
  <input type="text" maxlength="1" />
  <input type="text" maxlength="1" />
  <input type="text" maxlength="1" />
  <input type="text" maxlength="1" />
  <input type="text" maxlength="1" />
</div>
```
**Usage:** Login page  
**Effort:** 2 hours

### 3. User Type Selector
```html
<div class="user-type-selector">
  <label>
    <input type="radio" name="userType" value="individual" />
    <span>Individual</span>
  </label>
  <label>
    <input type="radio" name="userType" value="advocate" />
    <span>Legal Professional / Advocate</span>
  </label>
</div>
```
**Usage:** Registration page  
**Effort:** 1 hour

### 4. Case Table Component
```html
<table class="case-table">
  <thead>
    <tr>
      <th>S.No</th>
      <th>Court</th>
      <th>Case No</th>
      <th>Title</th>
      <th>Advocates</th>
      <th>Orders</th>
      <th>Last Hearing</th>
      <th>Next Date</th>
    </tr>
  </thead>
  <tbody>
    <!-- Dynamic rows -->
  </tbody>
</table>
```
**Usage:** Calendar page, Dashboard  
**Effort:** 3 hours

### 5. Calendar Widget
```html
<div class="calendar-widget">
  <div class="calendar-header">
    <button class="prev-month">←</button>
    <span class="month-year">February 2026</span>
    <button class="next-month">→</button>
  </div>
  <div class="calendar-grid">
    <!-- Days with hearing markers -->
  </div>
</div>
```
**Usage:** Calendar page  
**Effort:** 4-5 hours

### 6. News Ticker Component
```html
<div class="news-ticker">
  <div class="ticker-label">Latest News:</div>
  <div class="ticker-content">
    <marquee>News items scrolling...</marquee>
  </div>
</div>
```
**Usage:** Dashboard, Calendar page  
**Effort:** 1-2 hours

### 7. Plan Selection Component
```html
<div class="plan-selector">
  <div class="plan-box" data-plan="basic">
    <h4>Basic</h4>
    <p>₹50/month</p>
  </div>
  <div class="plan-box" data-plan="standard">
    <h4>Standard</h4>
    <p>₹360/month</p>
  </div>
  <div class="plan-box" data-plan="premium">
    <h4>Premium</h4>
    <p>₹1200/month</p>
  </div>
</div>
```
**Usage:** Registration page  
**Effort:** 2 hours

### 8. Case Add/Edit Form
```html
<form class="case-form">
  <input type="text" name="caseNo" placeholder="Case Number" />
  <input type="text" name="caseTitle" placeholder="Title of Case" />
  <div class="court-selector">
    <!-- Court buttons -->
  </div>
  <button type="submit">Add Case</button>
</form>
```
**Usage:** Dashboard  
**Effort:** 2 hours

### 9. Location Filter Component
```html
<div class="location-filter">
  <button class="location-btn" data-location="delhi">Delhi</button>
  <button class="location-btn" data-location="mumbai">Mumbai</button>
  <button class="location-btn" data-location="jaipur">Jaipur</button>
  <button class="location-btn" data-location="other">Other</button>
</div>
```
**Usage:** Calendar page  
**Effort:** 1 hour

### 10. Captcha Component
```html
<div class="captcha-container">
  <img src="/api/captcha" alt="Captcha" />
  <input type="text" name="captcha" placeholder="Enter captcha" />
  <button class="refresh-captcha">↻</button>
</div>
```
**Usage:** Login page  
**Effort:** 2 hours (frontend), 1 day (backend)

---

## 📊 File Structure Changes

### New Files to Create:
```
public/
├── register.html              🆕 Registration page
├── my-dashboard.html          🆕 Personalized dashboard
├── calendar.html              🆕 Calendar view
├── css/
│   ├── forms.css             🆕 Form styling
│   ├── tables.css            🆕 Table styling
│   ├── calendar.css          🆕 Calendar styling
│   └── news.css              🆕 News ticker styling
└── js/
    ├── otp.js                🆕 OTP handling
    ├── case-management.js    🆕 Case CRUD operations
    ├── calendar.js           🆕 Calendar logic
    ├── court-filter.js       🆕 Court filtering
    └── news-ticker.js        🆕 News ticker
```

### Files to Modify:
```
public/
├── dashboard.html            ✏️ Update hero, pricing, features
├── login.html                ✏️ Add OTP, captcha, phone option
├── index.html                ✏️ Convert to search or redirect
├── css/
│   ├── base.css             ✏️ Add new color variables
│   ├── components.css       ✏️ Add new component styles
│   └── tiers.css            ✏️ Update tier logic
└── js/
    ├── auth.js              ✏️ Add OTP, phone auth
    └── tier-renderer.js     ✏️ Add table view option
```

---

## ⏱️ Time Estimates

### Frontend Only (No Backend):
| Task | Time | Priority |
|------|------|----------|
| Update landing page | 2-3 hours | High |
| Update login page UI | 2 hours | High |
| Create registration page | 3-4 hours | High |
| Create dashboard page | 6-8 hours | High |
| Create calendar page | 6-8 hours | Medium |
| Build all components | 10-12 hours | High |
| Testing & polish | 4-6 hours | High |
| **TOTAL** | **33-43 hours** | **(4-5 days)** |

### With Backend Integration:
| Task | Time | Priority |
|------|------|----------|
| Frontend (above) | 4-5 days | High |
| OTP system | 1-2 days | High |
| User registration API | 1-2 days | High |
| Case management CRUD | 2-3 days | High |
| Court calendar API | 2-3 days | Medium |
| News feed integration | 1 day | Low |
| Testing & deployment | 2-3 days | High |
| **TOTAL** | **13-19 days** | **(2-3 weeks)** |

---

## 🎯 Recommended Approach

### Option 1: Quick Prototype (Frontend Only)
**Timeline:** 1 week  
**Deliverable:** Updated mockup with all UI changes, mock data  
**Good for:** Client approval before backend work

### Option 2: Full Implementation
**Timeline:** 3 weeks  
**Deliverable:** Fully functional system with backend  
**Good for:** Production-ready application

### Option 3: Phased Approach (Recommended)
**Phase 1 (Week 1):** Update landing, login, registration UI  
**Phase 2 (Week 2):** Build dashboard and case management  
**Phase 3 (Week 3):** Add calendar, news, and polish  
**Good for:** Iterative feedback and adjustments

---

## 🚦 Next Steps

1. **Review this analysis** with client
2. **Confirm priorities** (which features are must-have vs nice-to-have)
3. **Choose approach** (prototype vs full implementation)
4. **Get approval** on design direction
5. **Start implementation** based on priority order

---

## ❓ Questions for Client

1. **OTP Provider:** Which service for OTP? (Twilio, MSG91, AWS SNS?)
2. **Payment Gateway:** Which one? (Razorpay, Stripe, PayU?)
3. **Court Data:** Do you have API access or need scraping?
4. **News Source:** Where should news come from?
5. **Bar Council:** Need real validation or just dropdown?
6. **Timeline:** When do you need this live?
7. **Budget:** Frontend only or full backend too?

---

**Status:** ✅ Analysis Complete - Awaiting Client Approval  
**Prepared by:** Kiro AI Assistant  
**Date:** February 18, 2026

