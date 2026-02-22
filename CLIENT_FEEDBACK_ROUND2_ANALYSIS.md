# Client Feedback Round 2 - UI Fine-tuning Analysis

**Date:** February 19, 2026  
**Source:** Client handwritten feedback (4 pages)  
**Type:** UI refinements and feature clarifications

---

## 📋 Overview of Feedback Documents

### Document 1: Pricing Structure Clarification
- Detailed breakdown for Individuals vs Legal Professionals
- Specific pricing tiers and features

### Document 2: Dashboard Structure ("Hi, Mr ABC Singh")
- My Cases section layout
- Add Case button placement
- Case list format changes

### Document 3: Calendar/Cause List Changes
- Format changes for Individual vs Advocate views
- Item No field removal
- Print preview functionality

### Document 4: Create New Account Flow
- Individual vs Advocate selection
- Field requirements
- Plan selection logic

---

## 🔍 Detailed Analysis by Document

---

## DOCUMENT 1: Pricing Structure & Features

### For Individuals:
**Checkmarks indicate included features:**
- ✓ Own case tracking (upto 50 cases)
- ✓ Orders/Judgements (upto 50) ✓✓✓
- ✓ Case search (upto 50)
- ✓ SMS/WhatsApp alerts

### For Legal Professionals:

**Two Tiers Shown:**

**Tier 1: Advocate (Normal Plan)**
- Price: ₹199/month
- Case tracking (upto 300 cases)
- Judgements (upto 300)
- Orders/Judgements (upto 300)
- Case search (upto 300)
- SMS/WhatsApp alert
- Court proceedings update ©

**Tier 2: Advocate (Premium Plan)**  
- Price: ₹599/month
- Case tracking (unlimited)
- Orders/Judgements (upto 500)
- Case search (upto 2000)
- Priority alerts
- Advanced Analytics
- Dedicated support

**Additional Note:**
"Advocate (Super Premium Plan)"
- Case tracking (unlimited)
- Orders/Judgements (unlimited)
- Case search (unlimited)
- Priority alerts
- Advanced Analytics
- Dedicated support

### Key Changes Required:
1. Update pricing on landing page
2. Update pricing in registration page
3. Change limits displayed

---

## DOCUMENT 2: Dashboard Structure Changes

### Header:
"Hi, Mr ABC Singh"

### Section: My Cases

**Current Issue:** Client notes that cases should be displayed differently

**New Structure Required:**

**Top Section:**
- Case Number — Title of Case — ✓
- Court selector boxes: [AFT] [CAT] [High Court] [Supreme Court]
- [Add Case] button ✓

**Important Note:**
"⇒ All the cases which are added by an Individual or Advocate should be added in different page & not shown on this page."

**Key Change:** Cases added by user should NOT appear on main dashboard page

**Next Button:**
"After [Add Case] button, next should be → [My Case List]"

**My Case List Format:**
"⇒ Here all the cases added by user in this format:"

**Table Structure:**
| Name | Case Number | Title of Case | Advocate Name | Previous Date of Hearing | Next Date of Hearing | Orders Till Date |

### Section: Orders/Judgement/Decree

**Court selector:** [AFT] [CAT] [High Court] [SC]

**Search Fields:**
- Case Number
- Title of Case
- Name of Petitioner/Respondent

**Display:** Synopsis/Judgments ✓

### Key Changes Required:
1. Separate "Add Case" from case display
2. Create new "My Case List" page/section
3. Add table with all specified columns
4. Update Orders/Judgement search fields

---

## DOCUMENT 3: Calendar/Cause List Changes

### Calendar View ✓ (Keep as is)

### Cause List Format Changes:

**For Individual View:**
"Cause list format (for individual view)"
- **Remove:** Item No: X (crossed out)

**For Advocate View:**
"Cause list format (for Advocates)"
- **Add:** Print Preview for [Date]

**Table Structure for Advocates:**
| S.No | Item Found No | Case No | Title of Case | Orders/Case | Previous Date of Hearing | Next Date of Hearing |

### News ✓ (Keep as is)

### Key Changes Required:
1. Remove "Item No" field from Individual view
2. Add "Print Preview for Date" button for Advocate view
3. Add "Item Found No" column to advocate table
4. Simplify table for individual view

---

## DOCUMENT 4: Create New Account (Registration)

### User Type Selection:
Two boxes at top:
- [Individual]
- [Advocate]

**Checkmarks for fields:**
- ✓ (multiple checkmarks - indicating required fields)
- Name/Designation ✓
- Country ✓
- Select Plan:

**For Individual:**
- Individual: ₹50/month

**For Advocate:**
- Advocate (Normal Plan): ₹199/month
- Advocate (Premium): ₹599/month
- Advocate (Super Premium): ₹679/month

**Additional Fields:**
- [Track Court] ✓ (appears to be a new field)

**Note at bottom:**
"Only to be kept for Advocates"

### Key Changes Required:
1. Update plan pricing in registration
2. Add "Track Court" field (for advocates only)
3. Show correct plans based on user type
4. Update pricing display

---

## 📊 Summary of Changes by File

---

### 1. **dashboard.html (Landing Page)** - MODIFY

**Changes:**
- ✏️ Update pricing for Individuals: "₹50/month" (keep as is)
- ✏️ Update pricing for Advocates:
  - Normal Plan: ₹199/month (was ₹360)
  - Premium Plan: ₹599/month (was ₹1,200)
  - Add Super Premium: ₹679/month (new tier)
- ✏️ Update feature limits:
  - Individuals: up to 50 cases
  - Advocate Normal: up to 300 cases
  - Advocate Premium: unlimited cases, up to 500 judgements, up to 2000 searches
  - Advocate Super Premium: unlimited everything

**Effort:** 1-2 hours

---

### 2. **register.html (Registration Page)** - MODIFY

**Changes:**
- ✏️ Update plan pricing:
  - Individual: ₹50/month (keep)
  - Advocate Normal: ₹199/month (change from ₹360)
  - Advocate Premium: ₹599/month (change from ₹1,200)
  - Add Advocate Super Premium: ₹679/month (new)
- ➕ Add "Track Court" field (for advocates only)
- ✏️ Update plan display to show 3 advocate tiers

**Effort:** 2-3 hours

---

### 3. **my-dashboard.html (Dashboard)** - MAJOR RESTRUCTURE

**Changes:**
- ✏️ Separate "Add Case" section from case display
- ➕ Create "My Case List" button/link
- 🆕 Create new page/section for "My Case List" with table:
  - Columns: Name, Case Number, Title of Case, Advocate Name, Previous Date of Hearing, Next Date of Hearing, Orders Till Date
- ✏️ Update Orders/Judgement search fields:
  - Add: Name of Petitioner/Respondent
- ✏️ Main dashboard should NOT show added cases (move to separate list)

**Effort:** 4-5 hours

---

### 4. **calendar.html (Calendar Page)** - MODIFY

**Changes:**
- ❌ Remove "Item No" dropdown (for individual view)
- ➕ Add "Print Preview for Date" button (for advocate view)
- ➕ Add "Item Found No" column to table (for advocate view)
- ✏️ Create different table views for Individual vs Advocate
- ✏️ Simplify table for individual users

**Effort:** 2-3 hours

---

## 🎯 Priority Implementation Order

### Phase 1 (High Priority - Pricing Updates):
1. ✅ Update landing page pricing
2. ✅ Update registration page pricing
3. ✅ Add Super Premium tier

### Phase 2 (High Priority - Dashboard Restructure):
4. ✅ Separate Add Case from case display
5. ✅ Create "My Case List" page/section
6. ✅ Add table with all required columns
7. ✅ Update Orders/Judgement search

### Phase 3 (Medium Priority - Calendar Updates):
8. ✅ Remove Item No for individuals
9. ✅ Add Print Preview for advocates
10. ✅ Add Item Found No column
11. ✅ Create tier-specific views

### Phase 4 (Low Priority - Registration Fields):
12. ✅ Add Track Court field
13. ✅ Update plan selection logic

---

## 💡 Key Insights

### 1. Pricing Structure Changed:
**Old:**
- Individual: ₹50
- Advocate: ₹360
- Premium: ₹1,200

**New:**
- Individual: ₹50 (same)
- Advocate Normal: ₹199 (reduced)
- Advocate Premium: ₹599 (reduced)
- Advocate Super Premium: ₹679 (new)

### 2. Dashboard Philosophy Change:
- **Old:** Show all cases on main dashboard
- **New:** Separate "Add Case" from "My Case List"
- Cases should be in a different page/section

### 3. Tier-Specific Features:
- Individual view: Simpler, no Item No field
- Advocate view: More features, Print Preview, Item Found No

### 4. New Fields:
- Track Court (for advocates in registration)
- Item Found No (in advocate cause list)
- Name of Petitioner/Respondent (in Orders/Judgement search)

---

## 📝 Detailed Change Specifications

### Change 1: Update Pricing (dashboard.html)

**Current Pricing Section:**
```
For Individuals: ₹50/feature/month
For Legal Professionals:
  - Advocate: ₹360/month
  - Premium: ₹1,200/month
```

**New Pricing Section:**
```
For Individuals: ₹50/month (up to 50 cases)

For Legal Professionals:
  - Advocate (Normal): ₹199/month (up to 300 cases)
  - Advocate (Premium): ₹599/month (unlimited cases, up to 500 judgements)
  - Advocate (Super Premium): ₹679/month (unlimited everything)
```

---

### Change 2: Dashboard Restructure (my-dashboard.html)

**Current Structure:**
```
My Cases
  - Add Case Form
  - Case List (shows added cases)
```

**New Structure:**
```
My Cases
  - Add Case Form
  - [Add Case] Button
  
[My Case List] Button/Link

Separate Page/Section: My Case List
  - Table with columns:
    | Name | Case No | Title | Advocate | Prev Hearing | Next Hearing | Orders |
```

---

### Change 3: Calendar Tier-Specific Views (calendar.html)

**For Individuals:**
```
Cause List Table:
  - S.No
  - Court Name/No
  - Case No
  - Title of Case
  - Advocate Name
  - Orders/Case
  - Previous Date of Hearing
  - Next Date of Hearing
  
NO Item No field
```

**For Advocates:**
```
[Print Preview for Date] Button

Cause List Table:
  - S.No
  - Item Found No (NEW)
  - Case No
  - Title of Case
  - Orders/Case
  - Previous Date of Hearing
  - Next Date of Hearing
```

---

### Change 4: Registration Updates (register.html)

**Add Track Court Field (Advocates Only):**
```html
<div class="form-group" id="trackCourtField" style="display: none;">
  <label for="trackCourt" class="form-label">Track Court</label>
  <select id="trackCourt" name="trackCourt" class="form-select">
    <option value="">Select Court</option>
    <option value="aft">AFT</option>
    <option value="cat">CAT</option>
    <option value="highcourt">High Court</option>
    <option value="supreme">Supreme Court</option>
  </select>
</div>
```

**Update Plan Selector:**
```
For Individuals:
  - Basic: ₹50/month

For Advocates:
  - Normal: ₹199/month
  - Premium: ₹599/month
  - Super Premium: ₹679/month
```

---

## ✅ Testing Checklist After Changes

- [ ] Landing page shows correct pricing (₹50, ₹199, ₹599, ₹679)
- [ ] Registration shows correct plans based on user type
- [ ] Track Court field appears for advocates only
- [ ] Dashboard Add Case section is separate from case list
- [ ] My Case List button/link works
- [ ] My Case List table shows all required columns
- [ ] Calendar shows different views for Individual vs Advocate
- [ ] Item No removed for individuals
- [ ] Print Preview button appears for advocates
- [ ] Item Found No column appears for advocates
- [ ] All existing functionality still works

---

## 📊 Effort Estimate

**Total Estimated Time:** 9-13 hours

**Breakdown:**
- Landing page pricing: 1-2 hours
- Registration updates: 2-3 hours
- Dashboard restructure: 4-5 hours
- Calendar tier-specific views: 2-3 hours

**Recommended Approach:** Implement in priority order, test after each phase.

---

## 🎯 Summary

**Files to Modify:** 4
1. ✏️ dashboard.html - Pricing updates
2. ✏️ register.html - Pricing, Track Court field, 3 advocate tiers
3. ✏️ my-dashboard.html - Major restructure (separate Add Case from list)
4. ✏️ calendar.html - Tier-specific views

**New Concepts:**
- Separate "My Case List" page/section
- Tier-specific calendar views
- Track Court field for advocates
- Super Premium tier (₹679/month)

**Key Philosophy Change:**
- Cases added by users should NOT appear on main dashboard
- Should be in separate "My Case List" section

---

**Analysis Complete:** February 19, 2026  
**Status:** ✅ Ready for Implementation  
**Next Step:** Implement changes in priority order

