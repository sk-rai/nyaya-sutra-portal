# Advocate Pages Implementation Plan

**Date:** February 28, 2026  
**Status:** In Progress  
**Based on:** Whiteboard mockup analysis

---

## 📊 Overview

This document outlines the implementation plan for the new advocate-focused pages based on client mockups.

---

## 🎯 New Pages Created

### 1. ✅ Advocate Directory (`advocate-directory.html`)

**Purpose:** Search and browse advocates by name, court, and specialization

**Features:**
- Alphabetical board navigation (A-Z)
- Court-wise filtering (SC, HC, AFT, CAT, District)
- Search by name/specialization
- View advocate profiles
- e-Filing status lookup

**Access Levels:**
- Free Users: View only, limited results
- Individual (₹50): Full search, basic profiles
- Advocate Normal (₹199): Full access + own profile
- Advocate Premium (₹599): All features + analytics

**Status:** ✅ Basic structure created

---

### 2. ✅ Court Collection (`court-collection.html`)

**Purpose:** Hierarchical navigation of all courts in India

**Features:**
- Supreme Court section
- High Courts (State/UT wise)
- AFT (Armed Forces Tribunal) benches
- CAT (Central Administrative Tribunal) benches
- Appellate Tribunals (NCLAT, ITAT, CESTAT, TDSAT)
- District Courts (State/UT → District navigation)

**Hierarchy:**
```
Supreme Court
├── SC Registry
└── SC e-Filing

High Courts (by State/UT)
├── Delhi HC
├── Bombay HC
├── Calcutta HC
└── ...

AFT
├── Delhi (Principal Bench)
├── Mumbai
├── Chennai
└── ...

CAT
├── Delhi (Principal Bench)
├── Mumbai
├── Bangalore
└── ...

District Courts
├── State/UT Selection
└── District Selection
```

**Status:** ✅ Basic structure created

---

### 3. 🔄 Advocate Profile (`advocate-profile.html`)

**Purpose:** Detailed advocate information and case history

**Features:**
- Personal details (Name, Enrollment No, Bar Council)
- Specialization areas
- Courts of practice
- Cases handled (statistics)
- Recent appearances
- Contact information
- e-Filing status
- Professional achievements

**Status:** 🔄 To be created

---

### 4. 🔄 e-Filing Status (`efiling-status.html`)

**Purpose:** Track e-filing submissions across courts

**Features:**
- Court-wise filing lookup
- Filing status tracking
- Pending submissions
- Completed filings
- Document upload status
- Payment status
- Acknowledgment downloads

**Status:** 🔄 To be created

---

### 5. 🔄 Rare Acts (`rare-acts.html`)

**Purpose:** Collection of rare and important legal acts

**Features:**
- Browse acts by category
- Search functionality
- Act details and amendments
- Download PDF versions
- Bookmark favorite acts

**Status:** 🔄 To be created

---

## 🔗 Navigation Flow

### Current Site Structure:
```
Landing (dashboard.html)
    ↓
Register (register.html)
    ↓
Login (login.html)
    ↓
My Dashboard (my-dashboard.html)
    ↓
┌───────────────┼───────────────┐
↓               ↓               ↓
Calendar/       Case Search     [NEW PAGES]
Cause List      (index.html)
```

### Enhanced Structure with New Pages:
```
Landing (dashboard.html)
    ↓
Register (register.html)
    ↓
Login (login.html)
    ↓
My Dashboard (my-dashboard.html)
    ↓
┌───────────────┼───────────────┼───────────────┐
↓               ↓               ↓               ↓
Calendar/       Case Search     Advocate        Court
Cause List                      Directory       Collection
    ↓               ↓               ↓               ↓
Case Details    Case Details    Advocate        e-Filing
                                Profile         Status
                                    ↓
                                Rare Acts
```

---

## 🎨 Design Components

### Alphabetical Board Component
```html
<div class="alphabetical-board">
    <button class="alpha-btn">A</button>
    <button class="alpha-btn">B</button>
    ...
    <button class="alpha-btn">Z</button>
</div>
```

### Court Filter Component
```html
<div class="court-filters">
    <button class="court-filter-btn active">All Courts</button>
    <button class="court-filter-btn">Supreme Court</button>
    <button class="court-filter-btn">High Court</button>
    <button class="court-filter-btn">AFT</button>
    <button class="court-filter-btn">CAT</button>
    <button class="court-filter-btn">District Court</button>
</div>
```

### State/District Selector
```html
<select class="state-dropdown">
    <option value="">-- Select State/UT --</option>
    <option value="delhi">Delhi</option>
    <option value="maharashtra">Maharashtra</option>
    ...
</select>
<div class="district-list">
    <!-- Districts populated dynamically -->
</div>
```

---

## 📋 Implementation Checklist

### Phase 1: Core Pages (Week 1)
- [x] Create advocate-directory.html
- [x] Create court-collection.html
- [ ] Create advocate-profile.html
- [ ] Create efiling-status.html
- [ ] Create rare-acts.html

### Phase 2: Backend Integration (Week 2)
- [ ] Advocate database schema
- [ ] Court hierarchy database
- [ ] e-Filing API integration
- [ ] Search functionality backend
- [ ] Filtering and sorting APIs

### Phase 3: Features & Polish (Week 3)
- [ ] Advanced search filters
- [ ] Advocate profile management
- [ ] e-Filing status tracking
- [ ] Rare acts database
- [ ] Mobile responsiveness
- [ ] Performance optimization

---

## 🗄️ Database Schema

### Advocates Table
```sql
CREATE TABLE advocates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    enrollment_no VARCHAR(50) UNIQUE NOT NULL,
    bar_council VARCHAR(100),
    enrollment_date DATE,
    email VARCHAR(255),
    phone VARCHAR(20),
    specialization TEXT[],
    courts TEXT[],
    experience_years INT,
    profile_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Courts Table
```sql
CREATE TABLE courts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50), -- SC, HC, AFT, CAT, District
    state VARCHAR(100),
    district VARCHAR(100),
    address TEXT,
    website VARCHAR(255),
    efiling_url VARCHAR(255),
    parent_court_id INT REFERENCES courts(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### e-Filing Table
```sql
CREATE TABLE efilings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    court_id INT REFERENCES courts(id),
    case_number VARCHAR(100),
    filing_type VARCHAR(50),
    status VARCHAR(50), -- pending, submitted, accepted, rejected
    submission_date TIMESTAMP,
    acknowledgment_no VARCHAR(100),
    documents JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 Access Control

### Tier-Based Features

**Unregistered Users:**
- View advocate directory (limited results)
- Browse court collection
- No profile access

**Individual (₹50/month):**
- Full advocate search
- View basic advocate profiles
- Court collection access
- Limited e-filing status

**Advocate Normal (₹199/month):**
- All Individual features
- Manage own profile
- Full e-filing status
- Case tracking

**Advocate Premium (₹599/month):**
- All Normal features
- Advanced analytics
- Priority support
- Bulk operations
- API access

---

## 🚀 Next Steps

### Immediate (Today):
1. ✅ Create advocate-directory.html
2. ✅ Create court-collection.html
3. ⏳ Create advocate-profile.html
4. ⏳ Create efiling-status.html
5. ⏳ Create rare-acts.html

### Short Term (This Week):
1. Add navigation links to all pages
2. Implement mock data for testing
3. Create CSS components for new elements
4. Test responsive design
5. Get client feedback

### Medium Term (Next Week):
1. Set up backend APIs
2. Create database schemas
3. Implement search functionality
4. Add authentication checks
5. Integrate with existing pages

### Long Term (Next 2 Weeks):
1. Real data integration
2. e-Filing API connections
3. Payment gateway for premium features
4. Performance optimization
5. Production deployment

---

## 📞 Questions for Client

1. **Advocate Data Source:** Where will advocate data come from? Bar Council APIs?
2. **e-Filing Integration:** Which courts have e-filing APIs we can integrate?
3. **Rare Acts:** What acts should be included? Any specific categories?
4. **Verification:** Should advocate profiles be verified? How?
5. **Premium Features:** What additional features for premium advocates?
6. **Timeline:** When do you need these pages live?

---

## 💡 Technical Notes

### Frontend:
- Using existing CSS framework (base.css, components.css)
- Vanilla JavaScript for interactivity
- Responsive design (mobile-first)
- Consistent with existing pages

### Backend (To be implemented):
- Flask/FastAPI for APIs
- PostgreSQL for database
- Redis for caching
- Elasticsearch for search (optional)

### Integration Points:
- Existing auth system (auth.js)
- Tier checking (tier-renderer.js)
- Navigation menu (add new links)
- User dashboard (add quick links)

---

**Status:** ✅ Phase 1 Started - 2/5 pages created  
**Next:** Complete remaining 3 pages  
**Timeline:** 1 week for frontend, 2 weeks for full integration

---

**Prepared by:** Kiro AI Assistant  
**Last Updated:** February 28, 2026
