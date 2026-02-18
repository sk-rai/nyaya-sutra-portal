# Nyaya Sutra Portal - Client Mockup Analysis

**Date:** February 18, 2026  
**Source:** Paper mockups received from client  
**Total Mockups:** 4 screens

---

## 📋 Overview of Mockups

### Mockup 1: Home/Landing Page (Register/New)
**Status:** 🆕 NEW - Significant changes to existing dashboard

### Mockup 2: Sign In Page  
**Status:** ✏️ MODIFY - Enhance existing login.html

### Mockup 3: Personalized Page (Individual/Legal Agent)
**Status:** 🆕 NEW - User dashboard with case management

### Mockup 4: Case List & Calendar Views
**Status:** 🆕 NEW - Advanced features not in current prototype

---

## 🔍 Detailed Analysis

---

## MOCKUP 1: Home/Landing Page ✨

### Current State:
- We have `dashboard.html` with basic hero, features, and pricing sections
- Generic landing page for all visitors

### Client Requirements (from mockup):

#### Header Section:
- "Register if New" button (top left)
- "Sign In" button (top right)

#### Hero Section:
**Title:** "STREAMLINED LEGAL CASE MANAGEMENT FOR LEGAL PROFESSIONALS & INDIVIDUALS"

**User Types (4 personas with icons):**
1. **Defense Personnel** - "As Yourself (Any My Agent)"
2. **BSF, ITBP** - (Border Security Forces)
3. **Central Gov Services** - (Government employees)
4. **Individuals with Jawan** - (Family members)

**Welcome Message:**
"Welcome to Nyaya Sutra, a platform for personalized updation and information on cases related to service matters at Hon'ble A Supreme Court, Hon'ble High Court, Hon'ble CATs and Hon'ble AFTs."

#### Subscription Tiers (NEW structure):

**Individuals:**
- Own case tracking (~₹50)
- Orders/Judgements (~₹50)
- Case search (~₹50) & alerts

**Advocate/Legal Professionals:**
- Case tracking (500 to unlimited)
- Judgements (100 to unlimited)
- Case search (100 to unlimited)
- Alerts, Court Calendar, Updation on Court proceedings as per their color changes
- Open, reply, roster purposes etc.

**Key Features Section:**
- Hearing alerts
- Get SMS/WhatsApp notifications from days before hearing till on day of hearing
- Case tracking
- Auto alarm live

### Changes Required:
1. ✅ Update hero title to be more specific
2. ✅ Add 4 user persona icons with descriptions
3. ✅ Rewrite welcome message to match client's text
4. ✅ Restructure pricing tiers (Individuals vs Legal Professionals)
5. ✅ Update pricing amounts and features
6. ✅ Add court calendar mention
7. ✅ Emphasize SMS/WhatsApp alerts more prominently

---

## MOCKUP 2: Sign In Page 🔐

### Current State:
- We have `login.html` with email/password form
- Demo credentials displayed
- Simple login flow

### Client Requirements (from mockup):

**Title:** "Sign In"  
**Subtitle:** "For entry to Personalized Page"

**Form Fields:**
1. Email ID / Phone No
2. Captcha
3. OTP

**Action Flow:**
- "If new, Pl. register / Sign Up" link

**Sign-Up Form Fields (NEW):**
- Name
- Contact
- Know Type: Individual / Advocate
- Email ID
- Ph. No
- Address
- Plan Options: [3 boxes shown]
- "For advocates only: Dt. of enrollment"
- "Member of Bar Council of ___" [Delhi/Pune dropdown]

### Changes Required:
1. ✅ Add phone number option (Email ID / Phone No)
2. ✅ Add Captcha field
3. ✅ Implement OTP-based authentication
4. 🆕 Create separate registration form with:
   - User type selection (Individual / Advocate)
   - Contact details (Name, Email, Phone, Address)
   - Plan selection with visual boxes
   - Advocate-specific fields (enrollment date, bar council)
5. ✅ Update flow: Sign In → OTP verification
6. ✅ Add "Register / Sign Up" link prominently

---

## MOCKUP 3: Personalized Page (User Dashboard) 👤

### Current State:
- We have `index.html` with case search and results
- Basic tier-based content display
- No personalized dashboard

### Client Requirements (from mockup):

**Header:** "Hi, Mr. ABC Singh" (Personalized greeting)

**Section A: My Cases**
Form to add cases:
- Case No
- Title of Case
- Name of Hon'ble Court: [AFT] [CAT] [HighCourt] [Supreme] (buttons)

**Section B: Search My Cases**
Search form with:
- Name of Hon'ble Court: [AFT] [CAT] [HighCourt] [Supreme]
- Name of in case
- Case No
- Advocate Name

**Section C: Orders/Judgements/Decree**
Display section for:
- Case No
- Case Title
- Name of Hon'ble Court: [AFT] [CAT] [HighCourt] [SC]

**Section D: ANJ (Judgement/Decree)**
- Synopsis
- Synopsis of Judgement

**Right Sidebar (Sign-Up form visible):**
- Name
- Contact
- Know Type
- Email ID
- Ph. No
- Address
- Plan Options
- For advocates only: Dt. of enrollment
- Member of Bar Council of ___

### Changes Required:
1. 🆕 Create new personalized dashboard page
2. ✅ Add personalized greeting with user name
3. 🆕 Add "My Cases" section with form to add cases
4. 🆕 Add court selection buttons (AFT, CAT, High Court, Supreme Court)
5. 🆕 Add "Search My Cases" functionality
6. 🆕 Add "Orders/Judgements/Decree" section
7. 🆕 Add synopsis/judgement display area
8. ✅ Integrate with existing tier system
9. 🆕 Add case management (add/edit/delete cases)

---

## MOCKUP 4: Case List & Calendar Views 📅

### Current State:
- Basic case cards with limited information
- No calendar view
- No filtering by court

### Client Requirements (from mockup):

**Section A: Cause List**
Table view with columns:
- S.No
- Court Name/No
- Case No
- Title of Case
- Advocate Names

**Additional columns:**
- Orders of Case
- Penultimate of hearing
- Next Date of hearing

**Section B: Calendar View**
Court selection tabs:
- [AFT] [CAT] [HighCourt] [SC]

Below each:
- "Delhi, Mum, Jaipur" (location filters)
- "Offbeat Benches" (special benches)

**Section C: News**
- News ticker/display area

### Changes Required:
1. 🆕 Create table view for case list (replace card view option)
2. ✅ Add columns: S.No, Court Name, Case No, Title, Advocates
3. 🆕 Add "Orders of Case" column
4. 🆕 Add "Penultimate hearing" and "Next Date" columns
5. 🆕 Create calendar view component
6. 🆕 Add court filter tabs (AFT, CAT, High Court, SC)
7. 🆕 Add location filters (Delhi, Mumbai, Jaipur, etc.)
8. 🆕 Add "Offbeat Benches" filter
9. 🆕 Add News section/ticker
10. ✅ Make views switchable (List view / Calendar view)

---

## 📊 Summary of Changes

### New Pages Required:
1. ✅ **Register/Sign-Up Page** - Complete registration form with user type selection
2. ✅ **Personalized Dashboard** - User-specific case management page
3. ✅ **Calendar View Page** - Court calendar with filters
4. ✅ **News Section** - Legal news ticker/feed

### Existing Pages to Modify:
1. ✅ **dashboard.html** (Landing Page)
   - Update hero content
   - Add 4 user personas
   - Restructure pricing tiers
   - Update feature descriptions

2. ✅ **login.html** (Sign In Page)
   - Add phone number option
   - Add Captcha
   - Implement OTP flow
   - Add link to registration

3. ✅ **index.html** (Case Search)
   - Convert to personalized dashboard
   - Add "My Cases" management
   - Add court filter buttons
   - Add table view option
   - Add Orders/Judgements section

### New Components Required:
1. ✅ Court selector buttons (AFT, CAT, High Court, Supreme Court)
2. ✅ Location filters (Delhi, Mumbai, Jaipur, etc.)
3. ✅ Calendar widget
4. ✅ Table view for cases
5. ✅ News ticker component
6. ✅ Case add/edit form
7. ✅ OTP input component
8. ✅ Captcha component
9. ✅ User type selector (Individual/Advocate)
10. ✅ Bar Council dropdown

### Backend Requirements (for Phase 2):
1. ✅ OTP generation and verification
2. ✅ User registration with type (Individual/Advocate)
3. ✅ Case management CRUD operations
4. ✅ Court calendar data integration
5. ✅ News feed integration
6. ✅ Orders/Judgements storage and retrieval
7. ✅ Bar Council validation for advocates
8. ✅ Phone number verification

---

## 🎯 Priority Implementation Order

### Phase 1 (High Priority - Core Flow):
1. Update landing page (dashboard.html) with new content
2. Enhance login page with OTP flow
3. Create registration page with user type selection
4. Create personalized dashboard with "My Cases"

### Phase 2 (Medium Priority - Features):
5. Add court filter buttons across pages
6. Implement table view for case list
7. Add Orders/Judgements section
8. Create calendar view component

### Phase 3 (Low Priority - Enhancements):
9. Add news ticker/section
10. Add location filters
11. Add "Offbeat Benches" filter
12. Polish UI/UX based on feedback

---

## 🔄 Comparison: Current vs Required

| Feature | Current | Required | Status |
|---------|---------|----------|--------|
| Landing Page | Generic | 4 user personas | ✏️ Modify |
| Login | Email/Password | Email/Phone + OTP | ✏️ Modify |
| Registration | None | Full form with user type | 🆕 New |
| User Dashboard | Basic search | Personalized "My Cases" | 🆕 New |
| Case View | Card view only | Card + Table view | ✏️ Modify |
| Court Filters | None | AFT/CAT/HC/SC buttons | 🆕 New |
| Calendar | None | Court calendar view | 🆕 New |
| Orders/Judgements | None | Dedicated section | 🆕 New |
| News | None | News ticker | 🆕 New |
| Pricing Tiers | 3 generic | Individual vs Advocate | ✏️ Modify |

---

## 💡 Key Insights

### User Segmentation:
Client wants clear distinction between:
- **Individuals** (defense personnel, BSF, ITBP, families)
- **Legal Professionals** (advocates with bar council membership)

### Authentication:
- Move from simple email/password to **OTP-based authentication**
- Support both email and phone number login

### Personalization:
- Each user should have their own **"My Cases"** dashboard
- Ability to add, track, and manage personal cases

### Court-Specific Features:
- Strong emphasis on **multiple courts** (AFT, CAT, High Court, Supreme Court)
- Need for **location-based filtering** (Delhi, Mumbai, Jaipur)
- **Calendar view** for hearing dates

### Professional Features:
- **Bar Council membership** validation for advocates
- **Enrollment date** tracking
- Higher limits for advocates (500-unlimited cases)

---

## 📝 Next Steps

1. Review and approve this analysis
2. Prioritize features for implementation
3. Create detailed wireframes/mockups for new pages
4. Update existing pages with new content
5. Implement new components and pages
6. Test user flows
7. Deploy updated prototype

---

**Status:** ✅ Analysis Complete - Ready for Implementation  
**Estimated Effort:** 3-5 days for Phase 1 (frontend only)  
**Backend Required:** Yes, for OTP, user management, and case CRUD

