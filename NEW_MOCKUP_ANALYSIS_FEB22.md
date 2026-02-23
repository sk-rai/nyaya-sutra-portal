# New Mockup Analysis - February 22, 2026

**Date:** February 22, 2026  
**Source:** 2 new handwritten mockup pages  
**Focus:** Advocate-specific features and enhancements  
**Status:** Analysis in Progress

---

## 📋 Overview

These mockups appear to focus on **advocate-specific features** and enhancements to existing screens. The mockups show:

1. **Mockup 1 (Page 1):** Search My Cases + Orders/Judgements/Decree + Synopsis sections
2. **Mockup 2 (Page 2):** Advocate Cause List View + Pricing Plans

---

## 🔍 MOCKUP 1 - Detailed Analysis

### Section ① - Search My Cases

**Layout Structure:**
```
Search My Cases
[  ] [  ] [  ] ✓ [Search] ✓

[AFT] [CAT] [HC] [SC]
↓
S.No | Case No | Title of Case | Court Number/Name | Previous Date of Hearing | Next Date of Hearing | Orders Till Date
```

**Key Features Identified:**

1. **Search Filters (Top Row):**
   - 3 empty checkboxes/input fields
   - 1 checked checkbox (✓)
   - "Search" button (✓)

2. **Court Selection Buttons:**
   - AFT (Armed Forces Tribunal)
   - CAT (Central Administrative Tribunal)
   - HC (High Court)
   - SC (Supreme Court)

3. **Results Table Columns:**
   - S.No
   - Case No
   - Title of Case
   - Court Number/Name
   - Previous Date of Hearing
   - Next Date of Hearing
   - Orders Till Date

**Changes from Current Implementation:**
- ✅ Already have court selector buttons
- ✅ Already have search functionality
- ⚠️ Need to add "Orders Till Date" column
- ⚠️ Need to ensure "Previous Date of Hearing" is included

---

### Section ② - Add to My Case List / News Section

**Text visible:**
```
② Add to my Case List / News Section
```

**Interpretation:**
- This appears to be a button or action to add cases to a personal case list
- May also include a news section component
- Possibly a dual-purpose section

**Implementation Notes:**
- Need to create "Add to My Case List" functionality
- Consider adding a news ticker or news section
- May need to integrate with case management system

---

### Section ③ - Orders/Judgements/Decree

**Layout Structure:**
```
③ Orders/Judgements/Decree

[AFT] [CAT] [HC] [SC]
↓
Case No: _______
Title of Case: _______  → Orders/Judgement Pops up
Name of Petitioner/Respondent: _______
```

**Additional Features:**
```
③ Synopsis → [AFT] [CAT] [HC] [SC]
                ↓
                Archived
                Judgement
```

**Right Side Note:**
```
→ only for
   work purposes
   for individuals
   - available for
     Premium &
     Advocate
```

**Key Features Identified:**

1. **Court Selection:** AFT, CAT, HC, SC buttons

2. **Search Fields:**
   - Case No
   - Title of Case
   - Name of Petitioner/Respondent

3. **Action:** "Orders/Judgement Pops up" (modal or popup)

4. **Synopsis Section:**
   - Court selection (AFT, CAT, HC, SC)
   - Shows "Archived Judgement"

5. **Access Control:**
   - Only for work purposes
   - For individuals: Available for Premium & Advocate tiers only

**Changes Required:**
- ✅ Already have court selector
- ✅ Already have search fields (Case No, Title)
- ➕ Need to add "Name of Petitioner/Respondent" field
- ➕ Need to implement popup/modal for Orders/Judgement display
- ➕ Need to add Synopsis section with archived judgements
- ➕ Need to implement tier-based access control (Premium & Advocate only)

---

## 🔍 MOCKUP 2 - Detailed Analysis

### Section ⑧ - For Advocates in Cause List View

**Layout Structure:**
```
⑧ For Advocates in Cause List View:

S.No | Case No | Title of Case | Adv Name | Only for Adv (Not from Orders) | Adv | No | [Planned] [RCAST]
```

**Key Features Identified:**

1. **Table Columns:**
   - S.No
   - Case No
   - Title of Case
   - Adv Name (Advocate Name)
   - "Only for Adv (Not from Orders)" - Special column for advocates only
   - Adv (possibly advocate status)
   - No (possibly item number)

2. **Action Buttons:**
   - [Planned] button
   - [RCAST] button (possibly "Recast" or similar action)

**Interpretation:**
- This is an **advocate-specific view** of the cause list
- Contains columns that are NOT visible to individuals
- Has special action buttons for advocates to manage cases
- "Not from Orders" suggests this data comes from a different source

**Changes Required:**
- ➕ Create advocate-specific cause list view
- ➕ Add conditional columns based on user type (advocate vs individual)
- ➕ Add "Planned" button functionality
- ➕ Add "RCAST" button functionality
- ➕ Implement data source differentiation (orders vs other sources)

---

### Section ⑧ - Individual/Advocate Plans (Pricing)

**Layout Structure:**
```
⑧ Individual | Advocate | Advocate | Advocate
   Plan      | Normal   | (Premium)| (Super Premium)
   ₹59/mon   | ₹199/mon | ₹599/mon | ₹679/mon
             | (Currently
             | ₹48,000
             | Cases)
```

**Additional Note:**
```
"Reset all plans"
```

**Key Features Identified:**

1. **Pricing Tiers:**
   - **Individual Plan:** ₹59/month (changed from ₹50!)
   - **Advocate Normal:** ₹199/month
   - **Advocate Premium:** ₹599/month (currently ₹48,000 cases)
   - **Advocate Super Premium:** ₹679/month

2. **Case Limits:**
   - Note shows "Currently ₹48,000 Cases" for Premium tier
   - This seems to indicate current usage or limit

3. **Action:**
   - "Reset all plans" button/link

**IMPORTANT PRICING CHANGE:**
- Individual plan changed from ₹50/month to **₹59/month**
- This is a NEW change not in previous feedback!

**Changes Required:**
- ⚠️ Update Individual plan pricing: ₹50 → ₹59
- ✅ Advocate pricing already updated (₹199, ₹599, ₹679)
- ➕ Add "Reset all plans" functionality
- ➕ Display current case count/usage for users
- ➕ Update all pricing displays across the application

---

## 📊 Summary of Changes by Screen

### 1. My Dashboard (my-dashboard.html) - ENHANCEMENTS

**Search My Cases Section:**
- ✅ Court selector buttons (already implemented)
- ✅ Search functionality (already implemented)
- ⚠️ Ensure "Orders Till Date" column is present
- ⚠️ Verify "Previous Date of Hearing" column

**Add to My Case List:**
- ➕ Create "Add to My Case List" button/action
- ➕ Consider adding news section integration

**Orders/Judgements Section:**
- ✅ Court selector (already implemented)
- ✅ Case No and Title fields (already implemented)
- ➕ Add "Name of Petitioner/Respondent" field
- ➕ Implement popup/modal for displaying orders/judgements
- ➕ Add Synopsis section with archived judgements
- ➕ Implement tier-based access (Premium & Advocate only)

**Effort:** 3-4 hours

---

### 2. Calendar/Cause List (calendar.html) - ADVOCATE-SPECIFIC VIEW

**New Advocate View:**
- ➕ Create separate table view for advocates
- ➕ Add advocate-only columns
- ➕ Add "Planned" button
- ➕ Add "RCAST" button
- ➕ Implement conditional rendering based on user type
- ➕ Add data source differentiation logic

**Effort:** 4-5 hours

---

### 3. Pricing Updates (dashboard.html, register.html) - CRITICAL

**Pricing Changes:**
- ⚠️ **URGENT:** Update Individual plan: ₹50 → ₹59
- ✅ Advocate pricing already correct (₹199, ₹599, ₹679)
- ➕ Add "Reset all plans" functionality
- ➕ Display current usage/case count

**Files to Update:**
- `public/dashboard.html` (landing page pricing)
- `public/register.html` (registration pricing)
- Any other files displaying pricing

**Effort:** 1-2 hours

---

## 🎯 Priority Implementation Order

### CRITICAL (Must Do Immediately):
1. ⚠️ **Update Individual pricing: ₹50 → ₹59** (all pages)
2. ➕ Add "Name of Petitioner/Respondent" field to Orders section
3. ➕ Implement tier-based access for Synopsis (Premium & Advocate only)

### HIGH PRIORITY:
4. ➕ Create advocate-specific cause list view
5. ➕ Add "Orders Till Date" column to case list
6. ➕ Implement Orders/Judgement popup modal
7. ➕ Add Synopsis section with archived judgements

### MEDIUM PRIORITY:
8. ➕ Add "Planned" and "RCAST" buttons for advocates
9. ➕ Create "Add to My Case List" functionality
10. ➕ Add current usage/case count display

### LOW PRIORITY:
11. ➕ Add "Reset all plans" functionality
12. ➕ Integrate news section
13. ➕ Polish advocate-specific UI elements

---

## 📝 Detailed Implementation Specifications

### Change 1: Update Individual Pricing (CRITICAL)

**Files to Update:**
1. `public/dashboard.html`
2. `public/register.html`

**Current:**
```html
<div class="price">₹50<span>/month</span></div>
```

**New:**
```html
<div class="price">₹59<span>/month</span></div>
```

**Also update any text references:**
- "₹50/month" → "₹59/month"
- "₹50 per month" → "₹59 per month"

---

### Change 2: Add Petitioner/Respondent Field

**File:** `public/my-dashboard.html`

**Location:** Orders/Judgements section

**Add after "Title of Case" field:**
```html
<div class="form-group">
    <label for="petitionerRespondent" class="form-label">Name of Petitioner/Respondent</label>
    <input 
        type="text" 
        id="petitionerRespondent" 
        name="petitionerRespondent" 
        class="form-input" 
        placeholder="Enter petitioner or respondent name"
    >
</div>
```

---

### Change 3: Implement Orders/Judgement Popup

**File:** `public/my-dashboard.html`

**Add modal HTML:**
```html
<!-- Orders/Judgement Modal -->
<div id="ordersModal" class="modal" style="display: none;">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Orders / Judgement</h2>
            <button class="modal-close" onclick="closeOrdersModal()">&times;</button>
        </div>
        <div class="modal-body">
            <div class="order-details">
                <h3 id="modalCaseNo"></h3>
                <h4 id="modalCaseTitle"></h4>
                <div class="order-content" id="modalOrderContent">
                    <!-- Order/Judgement content will be loaded here -->
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeOrdersModal()">Close</button>
            <button class="btn btn-primary" onclick="downloadOrder()">Download PDF</button>
        </div>
    </div>
</div>
```

**Add JavaScript:**
```javascript
function showOrdersModal(caseNo, caseTitle, orderContent) {
    document.getElementById('modalCaseNo').textContent = caseNo;
    document.getElementById('modalCaseTitle').textContent = caseTitle;
    document.getElementById('modalOrderContent').innerHTML = orderContent;
    document.getElementById('ordersModal').style.display = 'block';
}

function closeOrdersModal() {
    document.getElementById('ordersModal').style.display = 'none';
}

function downloadOrder() {
    alert('Download functionality will be implemented with backend integration');
}
```

**Add CSS:**
```css
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    border-radius: 12px;
    max-width: 800px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e0e0e0;
}

.modal-close {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: #666;
}

.modal-body {
    padding: 2rem;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid #e0e0e0;
}
```

---

### Change 4: Add Synopsis Section

**File:** `public/my-dashboard.html`

**Add new section after Orders/Judgements:**
```html
<!-- Section: Synopsis -->
<div class="dashboard-section tier-paid-only">
    <h2 class="section-title">📚 Synopsis of Judgements</h2>
    
    <div class="tier-notice">
        <p>⭐ Available for Premium and Advocate users only</p>
    </div>
    
    <div class="court-selector">
        <button type="button" class="court-btn active" onclick="selectSynopsisCourt('aft')">AFT</button>
        <button type="button" class="court-btn" onclick="selectSynopsisCourt('cat')">CAT</button>
        <button type="button" class="court-btn" onclick="selectSynopsisCourt('highcourt')">High Court</button>
        <button type="button" class="court-btn" onclick="selectSynopsisCourt('supreme')">SC</button>
    </div>
    
    <div class="synopsis-list" id="synopsisList">
        <div class="synopsis-item">
            <div class="synopsis-header">
                <span class="synopsis-case-no">AFT/DEL/2023/1234</span>
                <span class="synopsis-date">15 Feb 2026</span>
            </div>
            <h4 class="synopsis-title">Rajesh Kumar vs. Union of India</h4>
            <p class="synopsis-text">
                The tribunal held that the petitioner's claim for pension benefits was valid 
                and directed the respondent to release the arrears within 60 days...
            </p>
            <button class="btn btn-sm btn-secondary" onclick="viewFullJudgement('AFT/DEL/2023/1234')">
                View Full Judgement
            </button>
        </div>
        
        <div class="synopsis-item">
            <div class="synopsis-header">
                <span class="synopsis-case-no">AFT/DEL/2023/5678</span>
                <span class="synopsis-date">10 Feb 2026</span>
            </div>
            <h4 class="synopsis-title">Meena Devi vs. Indian Army</h4>
            <p class="synopsis-text">
                The court ruled in favor of the petitioner regarding service benefits 
                and ordered reinstatement with back wages...
            </p>
            <button class="btn btn-sm btn-secondary" onclick="viewFullJudgement('AFT/DEL/2023/5678')">
                View Full Judgement
            </button>
        </div>
    </div>
</div>
```

**Add JavaScript:**
```javascript
function selectSynopsisCourt(court) {
    // Update active button
    document.querySelectorAll('.court-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load synopsis for selected court
    loadSynopsis(court);
}

function loadSynopsis(court) {
    console.log('Loading synopsis for court:', court);
    // This will be implemented with backend integration
    alert(`Loading synopsis for ${court.toUpperCase()}...`);
}

function viewFullJudgement(caseNo) {
    alert(`Viewing full judgement for case: ${caseNo}\n\nThis will open the complete judgement document.`);
}
```

**Add CSS:**
```css
.synopsis-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.synopsis-item {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid var(--gold);
}

.synopsis-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.synopsis-case-no {
    font-weight: 600;
    color: var(--navy-dark);
}

.synopsis-date {
    color: var(--gray-medium);
    font-size: 0.9rem;
}

.synopsis-title {
    color: var(--navy-dark);
    margin-bottom: 0.75rem;
}

.synopsis-text {
    color: var(--gray-dark);
    line-height: 1.6;
    margin-bottom: 1rem;
}

.tier-notice {
    background: #fff3cd;
    border: 1px solid #ffc107;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}

.tier-notice p {
    margin: 0;
    color: #856404;
    font-weight: 500;
}
```

---

### Change 5: Create Advocate-Specific Cause List View

**File:** `public/calendar.html`

**Add advocate-only columns to table:**
```html
<table class="cause-list-table">
    <thead>
        <tr>
            <th>S.No</th>
            <th>Case No</th>
            <th>Title of Case</th>
            <th>Adv Name</th>
            <th class="advocate-only">Only for Adv</th>
            <th class="advocate-only">Status</th>
            <th class="advocate-only">Actions</th>
            <th>Previous Date</th>
            <th>Next Date</th>
        </tr>
    </thead>
    <tbody id="causeListBody">
        <tr>
            <td>1</td>
            <td>AFT/DEL/2023/1234</td>
            <td>Rajesh Kumar vs. Union of India</td>
            <td>Adv. S. Patel</td>
            <td class="advocate-only">Special Note</td>
            <td class="advocate-only">Active</td>
            <td class="advocate-only">
                <button class="btn-sm btn-primary" onclick="markPlanned(1)">Planned</button>
                <button class="btn-sm btn-secondary" onclick="recast(1)">RCAST</button>
            </td>
            <td>10 Feb 2026</td>
            <td>20 Feb 2026</td>
        </tr>
    </tbody>
</table>
```

**Add JavaScript for advocate detection:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
    const userType = localStorage.getItem('userType') || 'individual';
    
    if (userType === 'advocate') {
        // Show advocate-only columns
        document.querySelectorAll('.advocate-only').forEach(el => {
            el.style.display = 'table-cell';
        });
    } else {
        // Hide advocate-only columns
        document.querySelectorAll('.advocate-only').forEach(el => {
            el.style.display = 'none';
        });
    }
});

function markPlanned(caseId) {
    alert(`Marking case ${caseId} as planned`);
    // Backend integration needed
}

function recast(caseId) {
    alert(`Recasting case ${caseId}`);
    // Backend integration needed
}
```

**Add CSS:**
```css
.advocate-only {
    background-color: #e3f2fd;
}

.btn-sm {
    padding: 0.25rem 0.75rem;
    font-size: 0.85rem;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    margin-right: 0.5rem;
}

.btn-sm.btn-primary {
    background: var(--navy-dark);
    color: white;
}

.btn-sm.btn-secondary {
    background: var(--gray-medium);
    color: white;
}
```

---

## 🔄 Comparison: Current vs New Requirements

| Feature | Current Status | New Requirement | Priority |
|---------|---------------|-----------------|----------|
| Individual Pricing | ₹50/month | ₹59/month | 🔴 CRITICAL |
| Petitioner/Respondent Field | Not present | Add to Orders section | 🔴 HIGH |
| Orders Popup | Not implemented | Modal popup | 🔴 HIGH |
| Synopsis Section | Not present | Add with tier restriction | 🔴 HIGH |
| Advocate Cause List | Basic view | Enhanced with special columns | 🟡 MEDIUM |
| Planned/RCAST Buttons | Not present | Add for advocates | 🟡 MEDIUM |
| Add to Case List | Basic | Enhanced functionality | 🟢 LOW |
| Reset Plans | Not present | Add functionality | 🟢 LOW |
| Current Usage Display | Not present | Show case count | 🟢 LOW |

---

## 📊 Files to Modify

| File | Changes | Effort | Priority |
|------|---------|--------|----------|
| `public/dashboard.html` | Update pricing ₹50→₹59 | 30 min | 🔴 CRITICAL |
| `public/register.html` | Update pricing ₹50→₹59 | 30 min | 🔴 CRITICAL |
| `public/my-dashboard.html` | Add fields, popup, synopsis | 3-4 hrs | 🔴 HIGH |
| `public/calendar.html` | Advocate-specific view | 2-3 hrs | 🟡 MEDIUM |
| `public/css/components.css` | Modal, synopsis styles | 1 hr | 🔴 HIGH |
| `public/js/auth.js` | User type detection | 30 min | 🟡 MEDIUM |

**Total Estimated Effort:** 8-10 hours

---

## ✅ Implementation Checklist

### Phase 1: Critical Updates (2-3 hours)
- [ ] Update Individual pricing to ₹59 in dashboard.html
- [ ] Update Individual pricing to ₹59 in register.html
- [ ] Add "Name of Petitioner/Respondent" field
- [ ] Implement Orders/Judgement popup modal
- [ ] Add modal CSS styling

### Phase 2: High Priority Features (3-4 hours)
- [ ] Create Synopsis section
- [ ] Add tier-based access control for Synopsis
- [ ] Implement court selector for Synopsis
- [ ] Add sample synopsis data
- [ ] Style synopsis items

### Phase 3: Advocate Features (2-3 hours)
- [ ] Add advocate-only columns to cause list
- [ ] Implement "Planned" button
- [ ] Implement "RCAST" button
- [ ] Add user type detection logic
- [ ] Style advocate-specific elements

### Phase 4: Additional Features (1-2 hours)
- [ ] Add "Add to My Case List" functionality
- [ ] Add current usage/case count display
- [ ] Add "Reset all plans" button
- [ ] Test all new features
- [ ] Mobile responsiveness check

---

## 💡 Key Insights from New Mockups

### 1. Pricing Adjustment
- **Individual plan increased from ₹50 to ₹59** (18% increase)
- This is a significant change that must be updated everywhere
- Suggests market research or cost analysis was done

### 2. Advocate-Centric Features
- Strong focus on advocate-specific functionality
- Separate views and columns for advocates
- Special action buttons (Planned, RCAST)
- Indicates target market is legal professionals

### 3. Enhanced Case Management
- More detailed case information
- Popup modals for better UX
- Synopsis feature for quick judgement review
- Tier-based access to premium features

### 4. Data Source Differentiation
- "Not from Orders" note suggests multiple data sources
- May need to track data origin
- Important for data integrity and user trust

### 5. Tier-Based Access Control
- Synopsis only for Premium & Advocate users
- Clear monetization strategy
- Need to implement proper access restrictions

---

## 🚀 Recommended Implementation Approach

### Step 1: Quick Wins (Day 1 - 2 hours)
1. Update pricing to ₹59 across all pages
2. Add Petitioner/Respondent field
3. Test and verify changes

### Step 2: Core Features (Day 2 - 4 hours)
1. Implement Orders/Judgement popup
2. Create Synopsis section
3. Add tier-based access control
4. Test modal functionality

### Step 3: Advocate Features (Day 3 - 3 hours)
1. Add advocate-only columns
2. Implement Planned/RCAST buttons
3. Add user type detection
4. Test advocate vs individual views

### Step 4: Polish & Test (Day 4 - 2 hours)
1. Add remaining features
2. Comprehensive testing
3. Mobile responsiveness
4. Bug fixes

**Total Timeline:** 3-4 days for complete implementation

---

## 📞 Questions for Client

Before implementation, clarify:

1. **Pricing Change:**
   - Confirm ₹59 is the final price for Individual plan
   - Should existing users be grandfathered at ₹50?

2. **RCAST Button:**
   - What does "RCAST" stand for?
   - What action should it perform?

3. **Synopsis Access:**
   - Should Basic/Free users see synopsis at all (blurred/locked)?
   - Or completely hidden?

4. **Data Sources:**
   - What are the different data sources?
   - How should "Not from Orders" data be displayed differently?

5. **Planned Button:**
   - What does marking a case as "Planned" do?
   - Should it change case status or appearance?

---

## 📝 Next Steps

1. **Review this analysis** with client
2. **Get clarifications** on questions above
3. **Prioritize features** based on client feedback
4. **Begin implementation** starting with critical pricing update
5. **Test incrementally** after each phase
6. **Deploy to staging** for client review
7. **Iterate based on feedback**

---

**Analysis Status:** ✅ Complete  
**Ready for Implementation:** ⏳ Pending Client Confirmation  
**Estimated Timeline:** 3-4 days  
**Risk Level:** 🟢 Low (mostly UI enhancements)

