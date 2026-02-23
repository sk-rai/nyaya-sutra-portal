# Quick Summary: New Mockup Changes (Feb 22, 2026)

## 🎯 TL;DR - What Changed?

### 🔴 CRITICAL CHANGE
**Individual Plan Pricing: ₹50 → ₹59/month**
- Must update in: dashboard.html, register.html
- 18% price increase
- Update ALL references

---

## 📋 New Features Required

### 1. Orders/Judgements Section Enhancements
✅ Already Have:
- Court selector buttons (AFT, CAT, HC, SC)
- Case No and Title fields

➕ Need to Add:
- **"Name of Petitioner/Respondent"** field
- **Popup modal** to display orders/judgements
- **Download PDF** button in modal

---

### 2. Synopsis Section (NEW!)
➕ Completely New Feature:
- Court selector (AFT, CAT, HC, SC)
- List of archived judgements with synopsis
- "View Full Judgement" button
- **Tier Restriction:** Premium & Advocate users only
- Show notice for free users

---

### 3. Advocate-Specific Cause List View
➕ New Columns (Advocates Only):
- "Only for Adv" column (special notes)
- "Status" column
- "Actions" column with buttons:
  - **[Planned]** button
  - **[RCAST]** button

🔒 Access Control:
- Show these columns ONLY for advocates
- Hide for individual users

---

### 4. Case List Enhancements
⚠️ Verify These Columns Exist:
- S.No ✅
- Case No ✅
- Title of Case ✅
- Court Number/Name ✅
- Previous Date of Hearing ⚠️ (check)
- Next Date of Hearing ✅
- **Orders Till Date** ➕ (add if missing)

---

## 📊 Changes by Page

### Page 1: Landing (dashboard.html)
```
CHANGE: ₹50 → ₹59
WHERE: Pricing section, Individual plan
TIME: 15 minutes
```

### Page 2: Registration (register.html)
```
CHANGE: ₹50 → ₹59
WHERE: Plan selection, Individual option
TIME: 15 minutes
```

### Page 3: My Dashboard (my-dashboard.html)
```
CHANGES:
1. Add "Petitioner/Respondent" field
2. Create Orders/Judgement popup modal
3. Add Synopsis section (new)
4. Add tier-based access control

TIME: 3-4 hours
```

### Page 4: Calendar (calendar.html)
```
CHANGES:
1. Add advocate-only columns
2. Add Planned/RCAST buttons
3. Implement user type detection
4. Conditional column display

TIME: 2-3 hours
```

---

## ⏱️ Time Estimates

| Task | Time | Priority |
|------|------|----------|
| Update pricing (₹50→₹59) | 30 min | 🔴 CRITICAL |
| Add Petitioner field | 15 min | 🔴 HIGH |
| Create Orders popup | 1.5 hrs | 🔴 HIGH |
| Add Synopsis section | 2 hrs | 🔴 HIGH |
| Advocate cause list view | 2 hrs | 🟡 MEDIUM |
| Planned/RCAST buttons | 1 hr | 🟡 MEDIUM |
| Testing & polish | 1 hr | 🟢 LOW |

**TOTAL: 8-10 hours (1-2 days)**

---

## 🎨 Visual Changes

### Before vs After

#### Orders Section:
```
BEFORE:
[AFT] [CAT] [HC] [SC]
Case No: _____
Title: _____
[Search]

AFTER:
[AFT] [CAT] [HC] [SC]
Case No: _____
Title: _____
Petitioner/Respondent: _____ ← NEW
[Search] → Opens Popup Modal ← NEW
```

#### Synopsis Section:
```
BEFORE:
(Doesn't exist)

AFTER:
📚 Synopsis of Judgements
⭐ Premium & Advocate Only

[AFT] [CAT] [HC] [SC]

┌─────────────────────────────┐
│ AFT/DEL/2023/1234  15 Feb   │
│ Rajesh Kumar vs. UOI        │
│ Synopsis text here...       │
│ [View Full Judgement]       │
└─────────────────────────────┘
```

#### Advocate Cause List:
```
BEFORE (All Users):
S.No | Case No | Title | Adv Name | Prev Date | Next Date

AFTER (Advocates Only):
S.No | Case No | Title | Adv Name | Only for Adv | Status | [Planned][RCAST] | Prev Date | Next Date
                                    ↑ NEW COLUMNS ↑
```

---

## 🔐 Access Control Matrix

| Feature | Free User | Individual (₹59) | Advocate (₹199+) |
|---------|-----------|------------------|------------------|
| Basic case search | ✅ | ✅ | ✅ |
| Add cases | ❌ | ✅ | ✅ |
| Orders/Judgements | ❌ | ✅ | ✅ |
| **Synopsis** | ❌ | ✅ | ✅ |
| Advocate columns | ❌ | ❌ | ✅ |
| Planned/RCAST | ❌ | ❌ | ✅ |

---

## 📝 Implementation Checklist

### Phase 1: Critical (30 min)
- [ ] Update ₹50 → ₹59 in dashboard.html
- [ ] Update ₹50 → ₹59 in register.html
- [ ] Test pricing display

### Phase 2: High Priority (3-4 hrs)
- [ ] Add Petitioner/Respondent field
- [ ] Create popup modal HTML
- [ ] Add modal CSS styling
- [ ] Add modal JavaScript
- [ ] Create Synopsis section HTML
- [ ] Add Synopsis CSS
- [ ] Add Synopsis JavaScript
- [ ] Implement tier checking

### Phase 3: Advocate Features (2-3 hrs)
- [ ] Add advocate-only table columns
- [ ] Add Planned button
- [ ] Add RCAST button
- [ ] Add user type detection
- [ ] Test advocate vs individual views

### Phase 4: Testing (1 hr)
- [ ] Test all new features
- [ ] Test tier restrictions
- [ ] Test mobile responsiveness
- [ ] Fix any bugs

---

## 🚨 Important Notes

1. **Pricing Change is CRITICAL**
   - Must be done first
   - Update everywhere ₹50 appears
   - Check for hardcoded values

2. **Synopsis is Premium Feature**
   - Must check user tier before showing
   - Show upgrade message for free users
   - Don't just hide - encourage upgrade

3. **Advocate Features are Exclusive**
   - Only show to advocates
   - Don't show to individuals at all
   - Use localStorage.getItem('userType')

4. **Modal Must Be Accessible**
   - Close on ESC key
   - Close on outside click
   - Proper focus management
   - Mobile-friendly

---

## 🎯 Success Criteria

✅ Individual pricing shows ₹59 everywhere  
✅ Petitioner/Respondent field works  
✅ Orders popup opens and closes smoothly  
✅ Synopsis section displays for Premium users  
✅ Synopsis hidden for Free users  
✅ Advocate columns show only for advocates  
✅ Planned/RCAST buttons work  
✅ All features work on mobile  
✅ No console errors  
✅ Tier restrictions enforced  

---

## 📞 Questions to Ask Client

1. **What does "RCAST" mean?** (Recast? Reassign?)
2. **What should "Planned" button do?** (Mark case? Change status?)
3. **Should free users see blurred synopsis?** (Or completely hidden?)
4. **Confirm ₹59 is final price?** (Not ₹60 or back to ₹50?)
5. **Where does synopsis data come from?** (Manual entry? Scraping?)

---

**Created:** February 22, 2026  
**Status:** Ready for Implementation  
**Next Step:** Get client confirmation, then start with pricing update

