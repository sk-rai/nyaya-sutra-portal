# Implementation Plan - February 23, 2026

**Date Created:** February 22, 2026  
**Implementation Start:** February 23, 2026  
**Estimated Duration:** 8-10 hours (1-2 days)  
**Status:** Ready to Begin

---

## 📋 Executive Summary

Based on the new mockup analysis and client confirmations, we have a clear implementation plan with the following key changes:

### ✅ Confirmed Requirements:
1. **Pricing:** Individual plan = ₹59/month (FINAL)
2. **Synopsis:** Automatic scraping + gist
   - Advocates: Full access
   - Individuals: Blurred view (upgrade teaser)
   - Free users: Hidden/locked
3. **Advocate Columns:** "Please Amend" and "Please Add" (not buttons)
4. **Orders Enhancement:** Add Petitioner/Respondent field + popup modal

---

## 🎯 Implementation Priorities

### 🔴 CRITICAL (Must do first - 30 min)
1. Update pricing ₹50 → ₹59 in dashboard.html
2. Update pricing ₹50 → ₹59 in register.html

### 🟡 HIGH (Core features - 5-6 hrs)
3. Add "Petitioner/Respondent" field to Orders section
4. Create Orders/Judgement popup modal
5. Build Synopsis section with blur effect
6. Implement tier-based access control

### 🟢 MEDIUM (Advocate features - 2-3 hrs)
7. Add "Please Amend" column (advocate-only)
8. Add "Please Add" column (advocate-only)
9. Implement user type detection
10. Test advocate vs individual views

---


## 📊 Detailed Change Breakdown

### Change 1: Pricing Update (₹50 → ₹59)

**Files to Modify:**
- `public/dashboard.html`
- `public/register.html`

**What to Change:**
```html
<!-- BEFORE -->
<div class="price">₹50<span>/month</span></div>
<p>₹50 per month (up to 50 cases)</p>

<!-- AFTER -->
<div class="price">₹59<span>/month</span></div>
<p>₹59 per month (up to 50 cases)</p>
```

**Time Estimate:** 30 minutes  
**Priority:** 🔴 CRITICAL  
**Testing:** Verify all pricing displays show ₹59

---

### Change 2: Synopsis Section (NEW FEATURE)

**File:** `public/my-dashboard.html`

**Requirements:**
- Court selector buttons (AFT, CAT, High Court, SC)
- List of judgement summaries
- Automatic scraping + AI gist
- Tier-based access control:
  - **Advocates:** Full clear text
  - **Individuals:** Blurred text + upgrade CTA
  - **Free users:** Completely hidden/locked

**HTML Structure:**
```html
<!-- Section: Synopsis -->
<div class="dashboard-section synopsis-section" id="synopsisSection">
    <h2 class="section-title">📚 Synopsis of Judgements</h2>
    
    <!-- Tier notice for non-advocates -->
    <div class="tier-notice individual-only" style="display: none;">
        <p>🔒 Upgrade to Advocate plan for full access to synopsis</p>
    </div>
    
    <div class="court-selector">
        <button type="button" class="court-btn active" onclick="selectSynopsisCourt('aft')">AFT</button>
        <button type="button" class="court-btn" onclick="selectSynopsisCourt('cat')">CAT</button>
        <button type="button" class="court-btn" onclick="selectSynopsisCourt('highcourt')">High Court</button>
        <button type="button" class="court-btn" onclick="selectSynopsisCourt('supreme')">SC</button>
    </div>
    
    <div class="synopsis-list" id="synopsisList">
        <!-- Synopsis items will be rendered here -->
    </div>
</div>
```

**CSS for Blur Effect:**
```css
.synopsis-item {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid var(--gold);
    margin-bottom: 1.5rem;
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
    font-size: 1.1rem;
}

.synopsis-text {
    color: var(--gray-dark);
    line-height: 1.6;
    margin-bottom: 1rem;
}

/* Blur effect for individuals */
.synopsis-text.blurred {
    filter: blur(5px);
    user-select: none;
    pointer-events: none;
    position: relative;
}

.synopsis-item.individual-view {
    position: relative;
}

.synopsis-item.individual-view::after {
    content: "🔓 Upgrade to Advocate Plan to View";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.85);
    color: white;
    padding: 1rem 2rem;
    border-radius: 8px;
    font-weight: 600;
    white-space: nowrap;
    z-index: 10;
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

**JavaScript for Access Control:**
```javascript
function renderSynopsis(court = 'aft') {
    const userType = localStorage.getItem('userType') || 'individual';
    const synopsisList = document.getElementById('synopsisList');
    
    // Sample data (will be replaced with API call)
    const synopsisData = [
        {
            caseNo: 'AFT/DEL/2023/1234',
            date: '15 Feb 2026',
            title: 'Rajesh Kumar vs. Union of India',
            synopsis: 'The tribunal held that the petitioner\'s claim for pension benefits was valid and directed the respondent to release the arrears within 60 days. The court emphasized the importance of timely pension disbursement for retired personnel.'
        },
        {
            caseNo: 'AFT/DEL/2023/5678',
            date: '10 Feb 2026',
            title: 'Meena Devi vs. Indian Army',
            synopsis: 'The court ruled in favor of the petitioner regarding service benefits and ordered reinstatement with back wages. The judgment highlighted procedural irregularities in the dismissal process.'
        }
    ];
    
    synopsisList.innerHTML = '';
    
    synopsisData.forEach(item => {
        const synopsisItem = document.createElement('div');
        synopsisItem.className = 'synopsis-item';
        
        if (userType === 'individual') {
            synopsisItem.classList.add('individual-view');
        }
        
        synopsisItem.innerHTML = `
            <div class="synopsis-header">
                <span class="synopsis-case-no">${item.caseNo}</span>
                <span class="synopsis-date">${item.date}</span>
            </div>
            <h4 class="synopsis-title">${item.title}</h4>
            <p class="synopsis-text ${userType === 'individual' ? 'blurred' : ''}">
                ${item.synopsis}
            </p>
            <button class="btn btn-sm ${userType === 'advocate' ? 'btn-secondary' : 'btn-primary'}" 
                    onclick="${userType === 'advocate' ? 'viewFullJudgement(\'' + item.caseNo + '\')' : 'showUpgradeModal()'}">
                ${userType === 'advocate' ? 'View Full Judgement' : '🔓 Upgrade to View'}
            </button>
        `;
        
        synopsisList.appendChild(synopsisItem);
    });
    
    // Show/hide tier notice
    const tierNotice = document.querySelector('.tier-notice.individual-only');
    if (userType === 'individual') {
        tierNotice.style.display = 'block';
    } else {
        tierNotice.style.display = 'none';
    }
}

function selectSynopsisCourt(court) {
    // Update active button
    document.querySelectorAll('.synopsis-section .court-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load synopsis for selected court
    renderSynopsis(court);
}

function viewFullJudgement(caseNo) {
    alert(`Opening full judgement for case: ${caseNo}\n\nThis will open the complete judgement document.`);
    // Will be implemented with backend integration
}

function showUpgradeModal() {
    alert('Upgrade to Advocate Plan\n\nGet full access to:\n• Complete synopsis of all judgements\n• Unlimited case tracking\n• Advanced advocate features\n\nPrice: ₹199/month onwards');
    // Will be replaced with proper modal
}

// Initialize synopsis on page load
document.addEventListener('DOMContentLoaded', () => {
    const userType = localStorage.getItem('userType');
    if (userType === 'advocate' || userType === 'individual') {
        renderSynopsis();
    } else {
        // Hide synopsis section for free users
        document.getElementById('synopsisSection').style.display = 'none';
    }
});
```

**Time Estimate:** 3-4 hours  
**Priority:** 🟡 HIGH  
**Testing:** 
- Test as advocate (full access)
- Test as individual (blurred view)
- Test as free user (hidden)

---


### Change 3: Orders/Judgements Enhancement

**File:** `public/my-dashboard.html`

**Requirements:**
- Add "Name of Petitioner/Respondent" field
- Create popup modal to display orders
- Add Download PDF button

**Add Field to Orders Section:**
```html
<!-- In Orders/Judgements section, after Title field -->
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

**Add Modal HTML (before closing </body>):**
```html
<!-- Orders/Judgement Modal -->
<div id="ordersModal" class="modal" style="display: none;">
    <div class="modal-overlay" onclick="closeOrdersModal()"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h2>Orders / Judgement</h2>
            <button class="modal-close" onclick="closeOrdersModal()">&times;</button>
        </div>
        <div class="modal-body">
            <div class="order-details">
                <div class="order-meta">
                    <h3 id="modalCaseNo"></h3>
                    <span id="modalCourtBadge" class="court-badge"></span>
                </div>
                <h4 id="modalCaseTitle"></h4>
                <div class="order-content" id="modalOrderContent">
                    <!-- Order/Judgement content will be loaded here -->
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeOrdersModal()">Close</button>
            <button class="btn btn-primary" onclick="downloadOrder()">
                📥 Download PDF
            </button>
        </div>
    </div>
</div>
```

**Modal CSS:**
```css
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
}

.modal-content {
    position: relative;
    background: white;
    border-radius: 12px;
    max-width: 800px;
    width: 90%;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    z-index: 1001;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
    margin: 0;
    color: var(--navy-dark);
}

.modal-close {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: #666;
    line-height: 1;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    transition: background 0.2s;
}

.modal-close:hover {
    background: #f0f0f0;
}

.modal-body {
    padding: 2rem;
    overflow-y: auto;
    flex: 1;
}

.order-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.order-meta h3 {
    margin: 0;
    color: var(--navy-dark);
}

.court-badge {
    background: var(--navy-dark);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-size: 0.85rem;
    font-weight: 600;
}

.order-content {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    line-height: 1.8;
    color: var(--gray-dark);
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid #e0e0e0;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .modal-content {
        width: 95%;
        max-height: 90vh;
    }
    
    .modal-body {
        padding: 1rem;
    }
    
    .modal-header,
    .modal-footer {
        padding: 1rem;
    }
}
```

**Modal JavaScript:**
```javascript
function showOrdersModal(caseNo, caseTitle, court, orderContent) {
    document.getElementById('modalCaseNo').textContent = caseNo;
    document.getElementById('modalCaseTitle').textContent = caseTitle;
    document.getElementById('modalCourtBadge').textContent = court.toUpperCase();
    document.getElementById('modalOrderContent').innerHTML = orderContent;
    document.getElementById('ordersModal').style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent background scroll
}

function closeOrdersModal() {
    document.getElementById('ordersModal').style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore scroll
}

function downloadOrder() {
    const caseNo = document.getElementById('modalCaseNo').textContent;
    alert(`Downloading order for case: ${caseNo}\n\nPDF download will be implemented with backend integration.`);
    // Will be implemented with backend
}

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeOrdersModal();
    }
});

// Example usage - update search button to open modal
function searchOrders() {
    const caseNo = document.getElementById('orderCaseNo').value;
    const title = document.getElementById('orderTitle').value;
    const petitioner = document.getElementById('petitionerRespondent').value;
    
    if (!caseNo && !title && !petitioner) {
        alert('Please enter at least one search criteria');
        return;
    }
    
    // Sample order content (will be fetched from backend)
    const sampleOrder = `
        <h4>Order dated: 15 February 2026</h4>
        <p><strong>Before:</strong> Hon'ble Justice R.K. Sharma</p>
        <p><strong>Petitioner:</strong> ${petitioner || 'Rajesh Kumar'}</p>
        <p><strong>Respondent:</strong> Union of India</p>
        <br>
        <p>The tribunal, after hearing both parties and examining the evidence on record, 
        is of the opinion that the petitioner's claim for pension benefits is valid and 
        well-founded. The respondent is hereby directed to release the arrears of pension 
        within a period of 60 days from the date of this order.</p>
        <br>
        <p>The case is disposed of accordingly.</p>
        <br>
        <p><strong>Signed:</strong> Justice R.K. Sharma<br>
        <strong>Date:</strong> 15 February 2026</p>
    `;
    
    showOrdersModal(
        caseNo || 'AFT/DEL/2023/1234',
        title || 'Rajesh Kumar vs. Union of India',
        'aft',
        sampleOrder
    );
}
```

**Time Estimate:** 2 hours  
**Priority:** 🟡 HIGH  
**Testing:**
- Test modal open/close
- Test ESC key close
- Test overlay click close
- Test mobile responsiveness

---


### Change 4: Advocate-Specific Cause List Columns

**File:** `public/calendar.html`

**Requirements:**
- Add "Please Amend" column (advocate-only)
- Add "Please Add" column (advocate-only)
- Show these columns only for advocates
- Hide for individual users

**Updated Table Structure:**
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
            <th class="advocate-only">Please Amend</th>
            <th class="advocate-only">Please Add</th>
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
            <td class="advocate-only">Special note for advocate</td>
            <td class="advocate-only">
                <span class="status-badge status-active">Active</span>
            </td>
            <td class="advocate-only">
                <button class="btn-icon" onclick="requestAmendment(1)" title="Request Amendment">
                    ✏️
                </button>
            </td>
            <td class="advocate-only">
                <button class="btn-icon" onclick="requestAddition(1)" title="Request Addition">
                    ➕
                </button>
            </td>
            <td>10 Feb 2026</td>
            <td>20 Feb 2026</td>
        </tr>
        <tr>
            <td>2</td>
            <td>CAT/DEL/2024/5678</td>
            <td>Suresh Patel vs. Ministry of Defence</td>
            <td>Adv. R. Singh</td>
            <td class="advocate-only">Follow-up required</td>
            <td class="advocate-only">
                <span class="status-badge status-pending">Pending</span>
            </td>
            <td class="advocate-only">
                <button class="btn-icon" onclick="requestAmendment(2)" title="Request Amendment">
                    ✏️
                </button>
            </td>
            <td class="advocate-only">
                <button class="btn-icon" onclick="requestAddition(2)" title="Request Addition">
                    ➕
                </button>
            </td>
            <td>15 Feb 2026</td>
            <td>-</td>
        </tr>
    </tbody>
</table>
```

**CSS for Advocate Columns:**
```css
/* Advocate-only columns styling */
.advocate-only {
    background-color: #e3f2fd;
    display: none; /* Hidden by default */
}

/* Show for advocates */
body.user-advocate .advocate-only {
    display: table-cell;
}

/* Status badges */
.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
}

.status-active {
    background: #d4edda;
    color: #155724;
}

.status-pending {
    background: #fff3cd;
    color: #856404;
}

.status-disposed {
    background: #d1ecf1;
    color: #0c5460;
}

/* Icon buttons */
.btn-icon {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: background 0.2s;
}

.btn-icon:hover {
    background: rgba(0, 0, 0, 0.05);
}

/* Table responsive */
@media (max-width: 1200px) {
    .cause-list-table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
}
```

**JavaScript for User Type Detection:**
```javascript
// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const { isLoggedIn, userTier } = checkAuth();

    if (!isLoggedIn) {
        window.location.href = 'login.html';
        return;
    }

    // Update user menu
    const userMenu = document.getElementById('userMenu');
    const tierLabel = userTier === 'unpaid' ? 'Free User' : 'Premium User';
    userMenu.innerHTML = `
        <div class="user-info">
            <span style="color: var(--white); font-size: 0.9rem;">${localStorage.getItem('userEmail')}</span>
            <span class="user-tier-badge tier-${userTier}">${tierLabel}</span>
        </div>
        <button class="btn btn-logout" onclick="logout()">Logout</button>
    `;

    // Check user type and show/hide advocate columns
    const userType = localStorage.getItem('userType') || 'individual';
    
    if (userType === 'advocate') {
        // Add class to body to show advocate columns
        document.body.classList.add('user-advocate');
        
        // Show advocate-only features
        document.querySelectorAll('.advocate-only').forEach(el => {
            el.style.display = 'table-cell';
        });
        
        console.log('Advocate view enabled');
    } else {
        // Individual view - hide advocate columns
        document.body.classList.add('user-individual');
        
        document.querySelectorAll('.advocate-only').forEach(el => {
            el.style.display = 'none';
        });
        
        console.log('Individual view enabled');
    }

    renderCalendar();
});

// Request amendment function
function requestAmendment(caseId) {
    const caseRow = event.target.closest('tr');
    const caseNo = caseRow.cells[1].textContent;
    const caseTitle = caseRow.cells[2].textContent;
    
    const amendment = prompt(`Request Amendment for:\n${caseNo}\n${caseTitle}\n\nPlease describe the amendment needed:`);
    
    if (amendment && amendment.trim()) {
        alert(`Amendment request submitted for case ${caseNo}:\n\n"${amendment}"\n\nThe court administrator will be notified.`);
        // Will be implemented with backend API
        console.log('Amendment request:', { caseId, caseNo, amendment });
    }
}

// Request addition function
function requestAddition(caseId) {
    const caseRow = event.target.closest('tr');
    const caseNo = caseRow.cells[1].textContent;
    const caseTitle = caseRow.cells[2].textContent;
    
    const addition = prompt(`Request Addition for:\n${caseNo}\n${caseTitle}\n\nPlease describe what needs to be added:`);
    
    if (addition && addition.trim()) {
        alert(`Addition request submitted for case ${caseNo}:\n\n"${addition}"\n\nThe court administrator will be notified.`);
        // Will be implemented with backend API
        console.log('Addition request:', { caseId, caseNo, addition });
    }
}
```

**Time Estimate:** 2-3 hours  
**Priority:** 🟢 MEDIUM  
**Testing:**
- Test as advocate (columns visible)
- Test as individual (columns hidden)
- Test amendment request
- Test addition request
- Test mobile responsiveness

---


## 📅 Day-by-Day Implementation Schedule

### Day 1 - February 23, 2026

#### Morning Session (9:00 AM - 12:00 PM) - 3 hours

**9:00 - 9:30 AM: Pricing Update (CRITICAL)**
- [ ] Update `public/dashboard.html`: Change ₹50 → ₹59
- [ ] Update `public/register.html`: Change ₹50 → ₹59
- [ ] Search for any other ₹50 references
- [ ] Test pricing display on both pages
- [ ] Commit changes: "Update Individual plan pricing to ₹59"

**9:30 - 10:00 AM: Orders Enhancement - Part 1**
- [ ] Add "Petitioner/Respondent" field to Orders section
- [ ] Update form layout
- [ ] Test field display
- [ ] Commit changes: "Add Petitioner/Respondent field to Orders"

**10:00 - 12:00 PM: Orders Enhancement - Part 2**
- [ ] Create modal HTML structure
- [ ] Add modal CSS styling
- [ ] Implement modal JavaScript functions
- [ ] Test modal open/close
- [ ] Test ESC key and overlay click
- [ ] Commit changes: "Add Orders/Judgement popup modal"

#### Afternoon Session (1:00 PM - 5:00 PM) - 4 hours

**1:00 - 4:00 PM: Synopsis Section**
- [ ] Create Synopsis section HTML
- [ ] Add court selector buttons
- [ ] Create synopsis item cards
- [ ] Add blur effect CSS
- [ ] Implement tier-based access control
- [ ] Add sample synopsis data
- [ ] Test advocate view (full access)
- [ ] Test individual view (blurred)
- [ ] Test free user view (hidden)
- [ ] Commit changes: "Add Synopsis section with tier-based access"

**4:00 - 5:00 PM: Testing & Bug Fixes**
- [ ] Test all Day 1 changes
- [ ] Fix any issues found
- [ ] Test mobile responsiveness
- [ ] Update documentation

**End of Day 1 Status:**
- ✅ Pricing updated
- ✅ Orders enhancement complete
- ✅ Synopsis section complete
- ⏳ Advocate columns (Day 2)

---

### Day 2 - February 24, 2026

#### Morning Session (9:00 AM - 12:00 PM) - 3 hours

**9:00 - 11:00 AM: Advocate Cause List Columns**
- [ ] Update calendar.html table structure
- [ ] Add "Please Amend" column
- [ ] Add "Please Add" column
- [ ] Add "Only for Adv" column
- [ ] Add "Status" column
- [ ] Add CSS for advocate columns
- [ ] Add status badge styling
- [ ] Commit changes: "Add advocate-specific columns to cause list"

**11:00 AM - 12:00 PM: User Type Detection**
- [ ] Implement user type detection logic
- [ ] Add body class based on user type
- [ ] Show/hide columns based on user type
- [ ] Test advocate view
- [ ] Test individual view
- [ ] Commit changes: "Implement user type detection for cause list"

#### Afternoon Session (1:00 PM - 4:00 PM) - 3 hours

**1:00 - 2:30 PM: Amendment/Addition Functions**
- [ ] Implement requestAmendment() function
- [ ] Implement requestAddition() function
- [ ] Add icon buttons to table
- [ ] Test amendment request flow
- [ ] Test addition request flow
- [ ] Commit changes: "Add amendment and addition request functions"

**2:30 - 4:00 PM: Final Testing & Polish**
- [ ] Comprehensive testing of all features
- [ ] Test all user types (free, individual, advocate)
- [ ] Test all tier levels (unpaid, paid)
- [ ] Mobile responsiveness check
- [ ] Cross-browser testing
- [ ] Fix any bugs found
- [ ] Update documentation
- [ ] Final commit: "Complete Feb 23 mockup implementation"

**End of Day 2 Status:**
- ✅ All features implemented
- ✅ All testing complete
- ✅ Ready for client review

---

## ✅ Testing Checklist

### Pricing Update
- [ ] Landing page shows ₹59 for Individual plan
- [ ] Registration page shows ₹59 for Individual plan
- [ ] No references to ₹50 remain
- [ ] Advocate pricing unchanged (₹199, ₹599, ₹679)
- [ ] Mobile view displays correctly

### Synopsis Section
- [ ] Section visible for advocates
- [ ] Section visible for individuals (blurred)
- [ ] Section hidden for free users
- [ ] Court selector buttons work
- [ ] Synopsis items display correctly
- [ ] Blur effect works for individuals
- [ ] Upgrade CTA shows for individuals
- [ ] "View Full Judgement" works for advocates
- [ ] Mobile responsive

### Orders Modal
- [ ] Petitioner/Respondent field added
- [ ] Modal opens on search
- [ ] Modal displays case details
- [ ] Modal closes on X button
- [ ] Modal closes on ESC key
- [ ] Modal closes on overlay click
- [ ] Download PDF button present
- [ ] Mobile full-screen works

### Advocate Columns
- [ ] Columns visible for advocates
- [ ] Columns hidden for individuals
- [ ] "Please Amend" button works
- [ ] "Please Add" button works
- [ ] Status badges display correctly
- [ ] User type detection works
- [ ] Mobile horizontal scroll works

### Cross-Browser Testing
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (if available)
- [ ] Mobile browsers

---

## 📊 Files Modified Summary

| File | Changes | Lines Changed | Priority |
|------|---------|---------------|----------|
| public/dashboard.html | Pricing ₹50→₹59 | ~5 | 🔴 CRITICAL |
| public/register.html | Pricing ₹50→₹59 | ~5 | 🔴 CRITICAL |
| public/my-dashboard.html | Petitioner field, Modal, Synopsis | ~200 | 🟡 HIGH |
| public/calendar.html | Advocate columns, User detection | ~100 | 🟢 MEDIUM |
| public/css/components.css | Modal, Synopsis, Advocate styles | ~150 | 🟡 HIGH |

**Total Estimated Changes:** ~460 lines of code

---

## 🎯 Success Criteria

### Must Have (Critical)
- ✅ Individual pricing shows ₹59 everywhere
- ✅ Synopsis section works with tier-based access
- ✅ Orders modal opens and closes properly
- ✅ Advocate columns show/hide based on user type

### Should Have (Important)
- ✅ Blur effect works smoothly for individuals
- ✅ Amendment/Addition requests work
- ✅ Mobile responsiveness maintained
- ✅ No console errors

### Nice to Have (Polish)
- ✅ Smooth animations
- ✅ Proper loading states
- ✅ Helpful error messages
- ✅ Tooltips on buttons

---

## 🚨 Known Limitations (Backend Required)

These features are mocked and will need backend implementation:

1. **Synopsis Data:** Currently using sample data
   - Need: API endpoint for synopsis scraping
   - Need: AI gist generation service

2. **Orders/Judgement Content:** Currently using sample data
   - Need: API endpoint to fetch actual orders
   - Need: PDF generation/download service

3. **Amendment/Addition Requests:** Currently using alerts
   - Need: API endpoint to submit requests
   - Need: Notification system for court admins

4. **User Type Detection:** Currently using localStorage
   - Need: Backend authentication with user roles
   - Need: JWT token with user type claim

---

## 📝 Post-Implementation Tasks

### Immediate (After Day 2)
- [ ] Create demo video showing new features
- [ ] Update user documentation
- [ ] Prepare client presentation
- [ ] Deploy to staging environment

### Short Term (Next Week)
- [ ] Gather client feedback
- [ ] Make any requested adjustments
- [ ] Deploy to production
- [ ] Monitor for issues

### Medium Term (Next Month)
- [ ] Implement backend APIs
- [ ] Replace mock data with real data
- [ ] Add analytics tracking
- [ ] Optimize performance

---

## 💡 Tips for Implementation

### Best Practices
1. **Commit Often:** Commit after each major feature
2. **Test Incrementally:** Test each feature before moving to next
3. **Mobile First:** Check mobile view after each change
4. **Console Clean:** Fix console errors immediately
5. **Code Comments:** Add comments for complex logic

### Common Pitfalls to Avoid
1. ❌ Don't forget to update both dashboard.html and register.html for pricing
2. ❌ Don't hardcode user types - use localStorage
3. ❌ Don't forget mobile responsiveness
4. ❌ Don't skip testing tier-based access
5. ❌ Don't forget to prevent body scroll when modal is open

### Debugging Tips
1. Use browser DevTools to inspect elements
2. Check localStorage for user type and tier
3. Use console.log to verify user detection
4. Test with different screen sizes
5. Clear cache if changes don't appear

---

## 📞 Support & Resources

### Documentation References
- **Detailed Analysis:** NEW_MOCKUP_ANALYSIS_FEB22.md
- **Quick Reference:** MOCKUP_CHANGES_SUMMARY.md
- **Visual Guide:** VISUAL_CHANGES_DIAGRAM.txt
- **Previous Work:** CLIENT_FEEDBACK_ANALYSIS.md

### Code Examples
All code examples are provided in this document and can be copied directly.

### Testing Credentials
- **Free User:** unpaid@example.com / demo123
- **Individual User:** paid@example.com / demo123
- **Advocate User:** (need to add) advocate@example.com / demo123

### Questions During Implementation
If you encounter issues:
1. Check the detailed analysis documents
2. Review code examples in this plan
3. Test with different user types
4. Check browser console for errors

---

## 🎉 Ready to Begin!

**Status:** ✅ All planning complete  
**Start Date:** February 23, 2026  
**Estimated Completion:** February 24, 2026  
**Total Effort:** 8-10 hours over 2 days

**Next Step:** Begin with pricing update tomorrow morning at 9:00 AM

Good luck with the implementation! 🚀

---

**Document Created:** February 22, 2026  
**Last Updated:** February 22, 2026  
**Version:** 1.0  
**Status:** Ready for Implementation

