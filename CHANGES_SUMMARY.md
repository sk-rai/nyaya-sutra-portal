# Quick Changes Summary - Client Mockups

**Date:** February 18, 2026

---

## 🎯 At a Glance

### Screens Analysis:
- **1 New Screen:** Registration page
- **2 New Features:** Personalized Dashboard, Calendar View
- **3 Modified Screens:** Landing, Login, Case Search

---

## 📋 Screen-by-Screen Changes

### 1️⃣ Landing Page (dashboard.html) - MODIFY ✏️

**What Changes:**
- Hero title → More specific for legal professionals
- Add 4 user personas with icons (Defense, BSF, Central Gov, Individuals)
- Pricing → Split into "Individuals" vs "Legal Professionals"
- Features → Emphasize SMS/WhatsApp alerts

**Why:**
Client wants to target specific user groups clearly

**Effort:** 2-3 hours

---

### 2️⃣ Login Page (login.html) - MAJOR CHANGES ✏️

**What Changes:**
- Email/Password → Email OR Phone + OTP
- Add Captcha field
- Add "Register" link
- Create NEW registration page with:
  - User type (Individual/Advocate)
  - Full contact details
  - Plan selection (3 boxes)
  - Advocate fields (enrollment, bar council)

**Why:**
Client wants OTP-based authentication and proper registration

**Effort:** 4-6 hours (UI), 1-2 days (with backend)

---

### 3️⃣ User Dashboard - NEW PAGE 🆕

**What's New:**
- Personalized greeting: "Hi, Mr. [Name]"
- "My Cases" section to add/manage cases
- Court selector buttons (AFT, CAT, High Court, Supreme)
- Search within user's cases
- Orders/Judgements display
- Synopsis section

**Why:**
Client wants users to manage their own case portfolio

**Effort:** 6-8 hours (UI), 2-3 days (with backend)

---

### 4️⃣ Calendar & List View - NEW FEATURE 🆕

**What's New:**
- Table view for cases (not just cards)
- Calendar view with hearing dates
- Court filter tabs
- Location filters (Delhi, Mumbai, Jaipur)
- "Offbeat Benches" filter
- News ticker section

**Why:**
Client wants advanced case tracking and calendar features

**Effort:** 8-10 hours (UI), 3-4 days (with backend)

---

## 🔄 Key Functional Changes

### Authentication Flow:
```
BEFORE:
Login → Email + Password → Dashboard

AFTER:
Login → Email/Phone + Captcha → OTP → Personalized Dashboard
Register → User Type → Details → Plan Selection → OTP → Dashboard
```

### User Journey:
```
BEFORE:
Visitor → Login → Search Cases → View (based on tier)

AFTER:
Visitor → Register (with user type) → Login (OTP) → My Dashboard → 
  → Add My Cases → Search My Cases → View Calendar → Read News
```

### Pricing Structure:
```
BEFORE:
- Personal: ₹110/month
- Advocate: ₹360/month  
- Premium: ₹1,200/month

AFTER:
INDIVIDUALS:
- Own case tracking: ~₹50
- Orders/Judgements: ~₹50
- Case search & alerts: ~₹50

LEGAL PROFESSIONALS:
- 500 cases: ₹360/month
- Unlimited cases: ₹1,200/month
- Includes: tracking, judgements, search, alerts, calendar
```

---

## 🆕 New Components Needed

1. **Court Selector Buttons** - [AFT] [CAT] [HighCourt] [Supreme]
2. **OTP Input** - 6-digit code entry
3. **Captcha** - Image + input field
4. **User Type Radio** - Individual / Advocate
5. **Plan Selection Boxes** - 3 visual boxes
6. **Case Add Form** - Quick add case to "My Cases"
7. **Table View** - Alternative to card view
8. **Calendar Widget** - Monthly view with hearing dates
9. **Location Filters** - City-based filtering
10. **News Ticker** - Scrolling news feed
11. **Bar Council Dropdown** - For advocates only
12. **Advocate Fields** - Conditional form fields

---

## 📊 Comparison Table

| Feature | Current | Required | Change Type |
|---------|---------|----------|-------------|
| **Landing Page** | Generic | User persona-focused | ✏️ Modify |
| **Login Method** | Email/Password | Email/Phone + OTP | ✏️ Major |
| **Registration** | None | Full form with user type | 🆕 New |
| **User Dashboard** | Generic search | Personalized "My Cases" | 🆕 New |
| **Case View** | Cards only | Cards + Table | ✏️ Add |
| **Court Filters** | None | AFT/CAT/HC/SC buttons | 🆕 New |
| **Calendar** | None | Monthly view with dates | 🆕 New |
| **Location Filter** | None | Delhi/Mumbai/Jaipur | 🆕 New |
| **News** | None | News ticker | 🆕 New |
| **User Types** | Generic tiers | Individual vs Advocate | ✏️ Major |
| **Pricing** | 3 tiers | Per-feature for individuals | ✏️ Modify |
| **Case Management** | View only | Add/Edit/Delete | 🆕 New |
| **Orders/Judgements** | None | Dedicated section | 🆕 New |
| **Synopsis** | None | Judgement synopsis | 🆕 New |

---

## 🎨 Design Changes

### Color Scheme:
- Keep existing navy (#0a192f) + gold (#ffd700)
- Add court-specific colors (optional):
  - AFT: Blue
  - CAT: Green
  - High Court: Purple
  - Supreme Court: Red/Maroon

### Layout Changes:
- Landing: Add persona icons section
- Login: Vertical form with OTP flow
- Dashboard: Multi-section layout (My Cases, Search, Orders, Synopsis)
- Calendar: Tabbed interface with filters

### Typography:
- Keep Inter + Merriweather
- Add emphasis on user greeting (larger, bold)

---

## 🔧 Technical Changes

### Frontend:
- Add 4 new HTML pages
- Add 4 new CSS files
- Add 5 new JS files
- Update 3 existing pages
- Create 12 new components

### Backend (Required):
- OTP generation/verification API
- User registration with type validation
- Case CRUD operations
- Court calendar data
- News feed integration
- Bar Council validation (optional)
- Phone number verification

### Third-Party Services:
- OTP provider (Twilio/MSG91)
- Captcha service (Google reCAPTCHA)
- Payment gateway (Razorpay/Stripe)
- News API (optional)

---

## ⚠️ Important Notes

### Must-Have Features (Phase 1):
1. ✅ Updated landing page
2. ✅ OTP-based login
3. ✅ Registration with user type
4. ✅ Personalized dashboard
5. ✅ "My Cases" management
6. ✅ Court selector buttons

### Nice-to-Have Features (Phase 2):
7. ⭐ Calendar view
8. ⭐ Table view for cases
9. ⭐ Location filters
10. ⭐ News ticker
11. ⭐ Orders/Judgements section
12. ⭐ Synopsis display

### Backend-Dependent:
- OTP authentication (can't demo without backend)
- Case management (can use mock data initially)
- Calendar data (can use mock data initially)
- News feed (can use static content initially)

---

## 💰 Cost Implications

### Development:
- Frontend only: 4-5 days
- With backend: 2-3 weeks

### Third-Party Services (Monthly):
- OTP service: ₹500-2,000 (based on volume)
- Captcha: Free (Google reCAPTCHA)
- Payment gateway: 2% transaction fee
- Hosting: ₹500-2,000 (Netlify/Vercel/AWS)

### Maintenance:
- Court data updates: Manual or automated scraping
- News feed: Manual or API integration
- User support: Based on user base

---

## 🚀 Recommended Next Steps

### Immediate (This Week):
1. ✅ Get client approval on this analysis
2. ✅ Clarify must-have vs nice-to-have features
3. ✅ Decide: Prototype or full implementation?
4. ✅ Choose OTP provider and payment gateway

### Short-term (Next 2 Weeks):
5. ✅ Update landing page with new content
6. ✅ Build registration page
7. ✅ Update login with OTP flow (UI only)
8. ✅ Create personalized dashboard
9. ✅ Add court selector buttons

### Medium-term (Next Month):
10. ✅ Integrate backend APIs
11. ✅ Add calendar view
12. ✅ Add table view
13. ✅ Add news section
14. ✅ Testing and deployment

---

## 📞 Questions to Ask Client

1. **Priority:** Which features are must-have for launch?
2. **Timeline:** When do you need this live?
3. **Budget:** Frontend mockup or full implementation?
4. **OTP:** Which provider? (Twilio, MSG91, other?)
5. **Payment:** Which gateway? (Razorpay, Stripe, PayU?)
6. **Court Data:** Do you have API access or need scraping?
7. **Bar Council:** Real validation needed or just dropdown?
8. **News:** Where should news come from?
9. **Hosting:** Any preference? (AWS, Netlify, Vercel?)
10. **Mobile App:** Is this planned for future?

---

## ✅ Summary

**Total Changes:**
- 1 new registration page
- 2 new major features (dashboard, calendar)
- 3 modified existing pages
- 12 new UI components
- Backend integration required for full functionality

**Effort:**
- Frontend prototype: 1 week
- Full implementation: 3 weeks

**Status:** Ready to start once priorities are confirmed

---

**Prepared by:** Kiro AI Assistant  
**Date:** February 18, 2026  
**Status:** ✅ Analysis Complete - Awaiting Client Approval

