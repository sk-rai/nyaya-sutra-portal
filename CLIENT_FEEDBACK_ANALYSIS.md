# Client Feedback Analysis - Change Requests

**Date:** February 19, 2026  
**Source:** Client handwritten feedback (3 pages)  
**Status:** Analysis Complete

---

## 📋 Overview of Feedback Documents

### Document 1 (Landing Page Changes)
- Updates to user personas
- Changes to pricing structure
- Key features modifications

### Document 2 (Dashboard/Registration Changes)
- Registration flow modifications
- Pricing plan changes
- Additional fields

### Document 3 (Calendar/Cause List Changes)
- Table column modifications
- Additional features

---

## 🔍 Detailed Analysis by Page

---

## PAGE 1: Landing Page (dashboard.html)

### Section: User Personas (Top of page)

**Current:** 4 personas displayed
1. Defence Personnel
2. BSF, ITBP
3. Central Gov Services
4. Individuals with Jawan

**Client Feedback - Changes Required:**

**Persona 1:** Defence Personnel
- Keep as: "Defence Personnel"
- Subtitle: "Army, Navy, Airforce"

**Persona 2:** CAPF
- Change from "BSF, ITBP" to: **"CAPF"**
- Subtitle: "BSF, ITBP, CRPF, etc."

**Persona 3:** Central Govt Services
- Keep as: "Central Govt Services"
- Subtitle: "CG" (Central Government)

**Persona 4:** Advocates
- Change from "Individuals with Jawan" to: **"Advocates"**
- Subtitle: "Service Matters"

### Section: Registration/Login Buttons

**Current:** "Register if New" and "Sign In"

**Client Feedback:**
- Keep "Register if New" button
- Keep "Sign In" button
- Add text: "email, or ph#" (indicating login options)

### Section: Search Cases

**Client Feedback:**
- Mark as: **"X not required"** (crossed out)
- **Action:** Remove or hide the Search Cases section from landing page

### Section: Key Features

**Current:** 4 feature cards
1. Hearing Alerts
2. Case Tracking
3. Audio Case Lists
4. Bare Acts & Forms

**Client Feedback - Keep but modify:**

**Feature 1:** Hearing Alerts
- Keep title
- Update description: "Get SMS/WhatsApp notifications from 2 days before hearing till due date of hearing"

**Feature 2:** Case Tracking
- Keep as is

**Feature 3:** Audio Case Lists
- Keep title
- Update description: "Audio case list"

**Feature 4:** Bare Acts & Forms
- Keep title
- Add additional text about forms

**Additional Notes on Features:**
- Client mentions: "For Individuals - Women Facing Domestic Violence, Pension Tracking, Case Lookup, Alerts, Judgments - 100 to unlimited, Case Search (100 to unlimited), Alerts, Counsel, Calendar, Updates on Court proceedings per their color, sizes, warnings, Timely for respective benches like phone, e-filing, Display boards, etc."

---

## PAGE 2: Registration & Dashboard Changes

### Section: Registration Flow

**Current:** User type selection (Individual/Advocate)

**Client Feedback - Changes Required:**

**For Registration Page (register.html):**

**Step 1: Create your account**
- Add field: "Rank/Designation"
- Add field: "Country"

**For Individuals Only:**
- Show: "Basic Plan ₹50 per month"
- Single plan option

**For Advocates:**
- Add field: "Address → Country"
- Show two plan options:
  - **Standard** box
  - **Premium** box

### Section: Dashboard Changes (my-dashboard.html)

**Client Feedback - Major Restructure:**

**Left Side:**
- "Let's Go" ✓
- "My Cases" ✓

**Main Area - Add Case Section:**
- Keep "Add Case" ✓

**Right Side - "My Case List" → @**
- Add columns:
  - Name (Counsel/Advocate/Petitioner/Respondent)
  - Previous date of hearing
  - Next Date of hearing
  - Orders till date

**Search My Cases Section:**
- Keep fields:
  - Case Number
  - Title of Case
  - Advocate Name

**Orders/Judgments/Decree Section:**
- Add dropdown for: "AFT / CAT / High Court / SC"
- Show fields:
  - Case No
  - Title of Case
  - Synopsis Required: Yes/No

---

## PAGE 3: Calendar/Cause List Changes

### Section: Cause List Table (calendar.html)

**Current Columns:**
1. S.No
2. Court Name/No
3. Case No
4. Title of Case
5. Advocate Names
6. Orders of Case
7. Penultimate Hearing
8. Next Date of Hearing

**Client Feedback - Changes Required:**

**New Column Structure:**
1. **S/No** (keep)
2. **Court Name/No** (keep)
3. **Case No** (keep)
4. **Title of Case** (keep)
5. **Advocate Name** (keep - singular)
6. **Orders/Case** (keep)
7. **Previous date of hearing** (rename from "Penultimate Hearing")
8. **Next Date of hearing** (keep)

**Additional Elements:**

**Below table:**
- Add: "Item No: [Present/Not/No]" (dropdown or status indicator)

**Sections to Add:**
1. **News** section (keep as is)
2. **Calendar View** section (keep as is)

---

## 📊 Summary of Changes by Screen

### 1. Landing Page (dashboard.html) - MODIFY

**Changes:**
- ✏️ Update Persona 2: "BSF, ITBP" → "CAPF (BSF, ITBP, CRPF, etc.)"
- ✏️ Update Persona 4: "Individuals with Jawan" → "Advocates (Service Matters)"
- ✏️ Update Persona 1 subtitle: Add "Army, Navy, Airforce"
- ✏️ Update Persona 3 subtitle: Add "CG"
- ❌ Remove "Search Cases" section (marked as not required)
- ✏️ Update Hearing Alerts description
- ✏️ Add "email, or ph#" text near login buttons

**Effort:** 1-2 hours

---

### 2. Registration Page (register.html) - MODIFY

**Changes:**
- ➕ Add "Rank/Designation" field
- ➕ Add "Country" field
- ✏️ For Individuals: Show only "Basic Plan ₹50/month"
- ✏️ For Advocates: Show "Standard" and "Premium" boxes only
- ✏️ Update "Address" to "Address → Country"

**Effort:** 2-3 hours

---

### 3. My Dashboard (my-dashboard.html) - MAJOR CHANGES

**Changes:**
- ✏️ Rename section to "My Case List"
- ➕ Add "Name" column (Counsel/Advocate/Petitioner/Respondent)
- ➕ Add "Previous date of hearing" column
- ➕ Add "Next Date of hearing" column
- ➕ Add "Orders till date" column
- ✏️ Restructure layout (Left: Let's Go, My Cases | Main: Add Case | Right: Case List)
- ➕ Add dropdown in Orders/Judgments section: AFT/CAT/High Court/SC
- ➕ Add "Synopsis Required: Yes/No" field

**Effort:** 3-4 hours

---

### 4. Calendar Page (calendar.html) - MODIFY

**Changes:**
- ✏️ Rename column: "Penultimate Hearing" → "Previous date of hearing"
- ✏️ Change "Advocate Names" → "Advocate Name" (singular)
- ➕ Add "Item No: [Present/Not/No]" below table
- ✅ Keep News section
- ✅ Keep Calendar View section

**Effort:** 1-2 hours

---

## 🎯 Priority Implementation Order

### High Priority (Must Do):
1. ✅ Update landing page personas (quick fix)
2. ✅ Remove Search Cases section from landing
3. ✅ Add fields to registration (Rank/Designation, Country)
4. ✅ Update dashboard case list columns

### Medium Priority (Should Do):
5. ✅ Update calendar table columns
6. ✅ Add Orders/Judgments dropdown
7. ✅ Update pricing display logic

### Low Priority (Nice to Have):
8. ✅ Add Item No indicator
9. ✅ Update feature descriptions
10. ✅ Polish UI based on new structure

---

## 📝 Detailed Change Specifications

### Change 1: Landing Page Personas

**File:** `public/dashboard.html`

**Current Code:**
```html
<div class="persona">
  <div class="persona-icon">🛡️</div>
  <h3>BSF, ITBP</h3>
  <p>Border Security Forces</p>
</div>
<div class="persona">
  <div class="persona-icon">👨‍👩‍👦</div>
  <h3>Individuals with Jawan</h3>
  <p>Family Members</p>
</div>
```

**New Code:**
```html
<div class="persona">
  <div class="persona-icon">🛡️</div>
  <h3>CAPF</h3>
  <p>BSF, ITBP, CRPF, etc.</p>
</div>
<div class="persona">
  <div class="persona-icon">⚖️</div>
  <h3>Advocates</h3>
  <p>Service Matters</p>
</div>
```

Also update Persona 1:
```html
<div class="persona">
  <div class="persona-icon">🎖️</div>
  <h3>Defence Personnel</h3>
  <p>Army, Navy, Airforce</p>
</div>
```

And Persona 3:
```html
<div class="persona">
  <div class="persona-icon">🏛️</div>
  <h3>Central Gov Services</h3>
  <p>CG</p>
</div>
```

---

### Change 2: Remove Search Cases Section

**File:** `public/dashboard.html`

**Action:** Comment out or remove the entire `<section class="case-search">` block

---

### Change 3: Registration Fields

**File:** `public/register.html`

**Add after Address field:**
```html
<div class="form-group">
  <label for="rank" class="form-label">Rank/Designation</label>
  <input type="text" id="rank" name="rank" class="form-input" placeholder="Your rank or designation">
</div>

<div class="form-group">
  <label for="country" class="form-label">Country</label>
  <select id="country" name="country" class="form-select" required>
    <option value="">Select Country</option>
    <option value="india" selected>India</option>
    <option value="usa">United States</option>
    <option value="uk">United Kingdom</option>
    <option value="other">Other</option>
  </select>
</div>
```

**Update Plan Display Logic:**
- For Individuals: Show only Basic plan
- For Advocates: Show Standard and Premium only

---

### Change 4: Dashboard Case List Columns

**File:** `public/my-dashboard.html`

**Add to case list table:**
```html
<div class="case-item-header">
  <span class="case-number">${caseItem.caseNo}</span>
  <span class="case-court-badge court-${caseItem.court}">${caseItem.court.toUpperCase()}</span>
</div>
<div class="case-details">
  <div class="case-title">${caseItem.caseTitle}</div>
  <div class="case-meta">
    <span><strong>Name:</strong> ${caseItem.counselName || 'N/A'}</span>
    <span><strong>Previous Hearing:</strong> ${caseItem.previousHearing || 'N/A'}</span>
    <span><strong>Next Hearing:</strong> ${caseItem.nextHearing || 'N/A'}</span>
    <span><strong>Orders:</strong> ${caseItem.orders || 'N/A'}</span>
  </div>
</div>
```

---

### Change 5: Calendar Table Columns

**File:** `public/calendar.html`

**Update table headers:**
```html
<thead>
  <tr>
    <th>S.No</th>
    <th>Court Name/No</th>
    <th>Case No</th>
    <th>Title of Case</th>
    <th>Advocate Name</th>
    <th>Orders/Case</th>
    <th>Previous Date of Hearing</th>
    <th>Next Date of Hearing</th>
  </tr>
</thead>
```

**Add below table:**
```html
<div class="item-status">
  <label>Item No:</label>
  <select class="status-select">
    <option value="present">Present</option>
    <option value="not">Not</option>
    <option value="no">No</option>
  </select>
</div>
```

---

## ✅ Testing Checklist After Changes

- [ ] Landing page personas display correctly
- [ ] Search Cases section removed
- [ ] Registration shows Rank/Designation field
- [ ] Registration shows Country dropdown
- [ ] Plan display logic works (Individual vs Advocate)
- [ ] Dashboard case list shows all new columns
- [ ] Calendar table columns renamed correctly
- [ ] Item No dropdown appears below calendar table
- [ ] All existing functionality still works
- [ ] Mobile responsiveness maintained

---

## 📊 Effort Estimate

**Total Estimated Time:** 7-11 hours

**Breakdown:**
- Landing page updates: 1-2 hours
- Registration page updates: 2-3 hours
- Dashboard restructure: 3-4 hours
- Calendar page updates: 1-2 hours

**Recommended Approach:** Implement in priority order, test after each change.

---

## 🎯 Summary

**Screens Affected:** 4 out of 7
1. ✏️ Landing Page (dashboard.html) - Moderate changes
2. ✏️ Registration (register.html) - Minor additions
3. ✏️ My Dashboard (my-dashboard.html) - Major restructure
4. ✏️ Calendar (calendar.html) - Minor changes

**Screens Unchanged:** 3
- Login page (login.html) - No changes
- Search page (index.html) - No changes
- Demo guide (START_HERE.html) - No changes

**Overall Impact:** Medium - Most changes are additions/modifications, not complete rewrites.

---

**Analysis Complete:** February 19, 2026  
**Status:** ✅ Ready for Implementation  
**Next Step:** Implement changes in priority order

