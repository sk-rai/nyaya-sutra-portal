# Quick Start Guide - February 23, 2026

**Ready to implement?** Follow this checklist!

---

## ⚡ Quick Reference

### What's Changing?
1. ✅ Pricing: ₹50 → ₹59 (Individual plan)
2. ✅ Synopsis: New section with blur for individuals
3. ✅ Orders: Add field + popup modal
4. ✅ Advocate Columns: "Please Amend" & "Please Add"

### Time Required
- **Day 1:** 7 hours (Pricing + Orders + Synopsis)
- **Day 2:** 6 hours (Advocate columns + Testing)
- **Total:** 13 hours over 2 days

---

## 🚀 Start Here (30 seconds)

### Step 1: Open Your Editor
```bash
cd ~/Documents/POC/nyaya-sutra-portal
code .
```

### Step 2: Read the Plan
Open: `IMPLEMENTATION_PLAN_FEB23.md`

### Step 3: Start with Pricing (15 min)
Files to edit:
- `public/dashboard.html` (line ~250)
- `public/register.html` (line ~180)

Change: `₹50` → `₹59`

---

## 📋 Day 1 Checklist

### Morning (3 hours)
- [ ] ☕ Coffee first!
- [ ] Update pricing in dashboard.html
- [ ] Update pricing in register.html
- [ ] Add Petitioner/Respondent field
- [ ] Create Orders modal HTML
- [ ] Add modal CSS
- [ ] Add modal JavaScript
- [ ] Test modal

### Afternoon (4 hours)
- [ ] Create Synopsis section HTML
- [ ] Add Synopsis CSS (blur effect)
- [ ] Add Synopsis JavaScript
- [ ] Test advocate view (clear)
- [ ] Test individual view (blurred)
- [ ] Test free user view (hidden)
- [ ] Commit all changes

---

## 📋 Day 2 Checklist

### Morning (3 hours)
- [ ] Update calendar.html table
- [ ] Add advocate-only columns
- [ ] Add CSS for columns
- [ ] Implement user type detection
- [ ] Test column visibility

### Afternoon (3 hours)
- [ ] Add amendment function
- [ ] Add addition function
- [ ] Final testing (all features)
- [ ] Mobile testing
- [ ] Bug fixes
- [ ] Commit and celebrate! 🎉

---

## 🎯 Key Code Snippets

### Pricing Update
```html
<!-- Change this -->
<div class="price">₹50<span>/month</span></div>

<!-- To this -->
<div class="price">₹59<span>/month</span></div>
```

### Synopsis Blur Effect
```css
.synopsis-text.blurred {
    filter: blur(5px);
    user-select: none;
}
```

### User Type Detection
```javascript
const userType = localStorage.getItem('userType');
if (userType === 'advocate') {
    // Show advocate features
}
```

---

## ✅ Testing Quick Check

After each feature:
1. Open in browser
2. Test as advocate
3. Test as individual
4. Check mobile view
5. Fix any issues
6. Commit changes

---

## 📞 Need Help?

**Detailed docs:**
- Full plan: `IMPLEMENTATION_PLAN_FEB23.md`
- Analysis: `NEW_MOCKUP_ANALYSIS_FEB22.md`
- Visual guide: `VISUAL_CHANGES_DIAGRAM.txt`

**Stuck?** Check the detailed plan for complete code examples!

---

## 🎉 You Got This!

Start with the pricing update - it's quick and builds momentum!

**Good luck! 🚀**
