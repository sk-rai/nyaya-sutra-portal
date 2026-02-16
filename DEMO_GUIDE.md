# 🎯 Nyaya Sutra - Client Demo Guide

## Quick Demo Flow (5 minutes)

### Step 1: Show Unregistered View
1. Open `index.html` in browser
2. Point out: "This is what visitors see without logging in"
3. Show limited case information (only number and date)
4. Click on "Login to View Details" button

### Step 2: Login as Free User
1. On login page, use: `unpaid@example.com` / `demo123`
2. After login, show the enhanced view:
   - ✅ Case number & date
   - ✅ Bench information
   - ✅ Case type
   - ✅ Status (For Hearing/Disposed)
   - ❌ Counsel names (locked)
   - ❌ Venue details (locked)
3. Point out the "Unlock Full Access" button
4. Show the user menu with tier badge

### Step 3: Logout and Login as Premium User
1. Click "Logout" button
2. Login again with: `paid@example.com` / `demo123`
3. Show the complete view:
   - ✅ All previous fields
   - ✅ Counsel names
   - ✅ Venue information
   - ✅ Print button (functional)
   - ✅ Copy button (functional)
4. Demonstrate print functionality
5. Demonstrate copy to clipboard

### Step 4: Show Landing Page
1. Open `dashboard.html`
2. Walk through:
   - Hero section with value proposition
   - Features section (alerts, tracking, accessibility)
   - Pricing tiers (₹110, ₹360, ₹1,200)
   - Professional navy/gold design

## 🎨 Key Selling Points

### 1. Tier-Based Access Control
"The system intelligently shows different content based on subscription level - no need for separate pages"

### 2. Professional Design
"Clean, modern interface specifically designed for legal professionals with navy and gold color scheme"

### 3. Security Features
"Print and copy restrictions ensure content protection for premium features"

### 4. Scalable Architecture
"Frontend is ready - backend integration is straightforward with clear API requirements"

## 📊 Pricing Tiers to Highlight

| Feature | Personal (₹110) | Advocate (₹360) | Premium (₹1,200) |
|---------|----------------|-----------------|------------------|
| Cases | 50 | 500 | Unlimited |
| Basic Details | ✅ | ✅ | ✅ |
| Full Details | ❌ | ✅ | ✅ |
| Print/Copy | ❌ | ✅ | ✅ |
| Analytics | ❌ | ❌ | ✅ |

## 🚀 Next Phase Preview

"Once approved, we'll build:
1. Backend API with Flask/FastAPI
2. PDF scraping for AFT Delhi & CGAT
3. SMS/WhatsApp alert system
4. Payment gateway integration
5. Mobile app (Phase 2)"

## 💡 Demo Tips

- **Start with unregistered view** to show the progression
- **Emphasize the tier system** - it's the core differentiator
- **Show the professional design** - navy/gold theme for legal sector
- **Mention scalability** - easy to add more courts/features
- **Highlight security** - content protection for paid users

## 📱 Browser Testing

Works best in:
- Chrome/Edge (recommended)
- Firefox
- Safari

## 🔧 Troubleshooting

**If login doesn't work:**
- Check browser console (F12)
- Ensure localStorage is enabled
- Try clearing browser cache

**If styles look broken:**
- Verify all CSS files are in `css/` folder
- Check file paths are correct
- Ensure fonts are loading from Google Fonts

---

**Ready to impress!** 🎉
