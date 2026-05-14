# Nyaya Sutra Portal — Client Testing Guide

## 🌐 Live URLs

- **Frontend (Web App):** https://sk-rai.github.io/nyaya-sutra-portal/
- **Backend API:** https://nyaya-sutra-api.onrender.com
- **Health Check:** https://nyaya-sutra-api.onrender.com/api/health

> **Note:** The backend is on Render free tier. If idle for 15 minutes, the first request may take 30-60 seconds to wake up. Subsequent requests are fast.

---

## 📱 Test Accounts (Pre-created)

All test accounts use OTP code: **`111111`**

| Account Type | Email | Phone | Tier |
|---|---|---|---|
| Admin (Full Access) | admin@nyayasutra.test | 9900000001 | Advocate Premium |
| Premium Advocate | premium@nyayasutra.test | 9900000002 | Advocate Premium |
| Normal Advocate | advocate@nyayasutra.test | 9900000003 | Advocate Normal |
| Individual (Paid) | individual@nyayasutra.test | 9900000004 | Individual |
| Free User | free@nyayasutra.test | 9900000005 | Free |

---

## 🧪 Testing Steps

### Step 1: Login
1. Go to https://sk-rai.github.io/nyaya-sutra-portal/login.html
2. Enter email: `admin@nyayasutra.test`
3. Enter the captcha shown on screen
4. Click **Send OTP**
5. Enter OTP: `111111`
6. Click **Verify & Sign In**
7. You will be redirected to the Dashboard

### Step 2: Search & Track a Case
1. On the Dashboard, in the **"Add Case"** section
2. Enter any case number from the list below
3. Select the correct court tab (AFT / CAT / HC / SC)
4. Click **Add Case**
5. The case will appear in **"My Case List"** below

### Step 3: View Tracked Cases
- All tracked cases appear in the **"My Case List"** section
- Each case shows: Case Number, Title, Advocate, Next Hearing, Status, Freshness
- Click **Untrack** to remove a case from your list

### Step 4: Search My Cases
- Use the **"Search My Cases"** section to filter your tracked cases
- Filter by court type (AFT / CAT / HC / SC)
- Search by case number or case name

### Step 5: Court Collection
1. Go to https://sk-rai.github.io/nyaya-sutra-portal/court-collection.html
2. Browse courts by category (Supreme Court, High Courts, AFT, CAT)
3. Click any court to navigate to case search

### Step 6: Test Different Tiers
1. Logout (click Logout button)
2. Login with `free@nyayasutra.test` / OTP `111111`
3. Try searching — free tier has 10 searches/day limit
4. Login with `premium@nyayasutra.test` to see Synopsis section

---

## 📋 Sample Case Numbers for Testing

### AFT Delhi (select AFT tab)
| Case Number | Title | Next Hearing |
|---|---|---|
| OA 234/2025 | Ex Sub Maj Rajesh Kumar vs Union of India | 10 Jun 2026 |
| OA 567/2024 | Col (Retd) Vikram Singh vs Chief of Army Staff | 12 Jun 2026 |
| TA 89/2026 | Nb Sub Mohan Lal vs Union of India | 17 Jun 2026 |
| MA 45/2026 | Wg Cdr (Retd) Amit Sharma vs Union of India | 19 Jun 2026 |
| OA 890/2025 | Hav Suresh Yadav vs Union of India | 24 Jun 2026 |

### AFT Mumbai (select AFT tab)
| Case Number | Title | Next Hearing |
|---|---|---|
| OA 112/2025 | Ex Sgt Ramesh Patil vs Union of India | 5 Jun 2026 |
| OA 345/2026 | Cdr (Retd) Anil Joshi vs Chief of Naval Staff | 11 Jun 2026 |
| TA 23/2026 | Sep Dinesh More vs Union of India | 18 Jun 2026 |

### CAT Delhi (select CAT tab)
| Case Number | Title | Next Hearing |
|---|---|---|
| OA 1234/2025 | Sh. Arvind Mishra vs Union of India | 3 Jun 2026 |
| OA 2567/2024 | Smt. Sunita Devi vs UPSC | 9 Jun 2026 |
| OA 789/2026 | Sh. Manoj Kumar vs Ministry of Railways | 16 Jun 2026 |
| MA 456/2026 | Sh. Ravi Shankar vs DoPT | 23 Jun 2026 |

### CAT Mumbai (select CAT tab)
| Case Number | Title | Next Hearing |
|---|---|---|
| OA 678/2025 | Sh. Prakash Jadhav vs Western Railway | 4 Jun 2026 |
| OA 901/2026 | Smt. Kavita Sawant vs CGDA | 13 Jun 2026 |
| TA 67/2026 | Sh. Vijay Bhosale vs Customs Dept | 20 Jun 2026 |

### Delhi High Court (select High Court tab)
| Case Number | Title | Next Hearing |
|---|---|---|
| WP(C) 4567/2025 | Ex Maj Gen A.K. Singh vs Union of India | 6 Jun 2026 |
| WP(C) 8901/2024 | All India Defence Employees Federation vs UOI | 15 Jun 2026 |
| LPA 234/2026 | Union of India vs Ex Col Deepak Rao | 25 Jun 2026 |

### Supreme Court (select Supreme Court tab)
| Case Number | Title | Next Hearing |
|---|---|---|
| SLP(C) 12345/2025 | Union of India vs Ex Lt Gen P.K. Sehgal | 2 Jun 2026 |
| CA 7890/2024 | Ex Brig Harinder Singh vs Chief of Army Staff | 26 Jun 2026 |

---

## ✅ What's Working (Backend Complete)

- ✅ User Registration (Email + Phone)
- ✅ OTP-based Login (Passwordless)
- ✅ JWT Authentication with session management
- ✅ Court listing (23 courts across SC, HC, AFT, CAT)
- ✅ Case search by court + case number
- ✅ Case tracking (add/remove from personal list)
- ✅ Tier-based access control (Free / Individual / Advocate Normal / Advocate Premium)
- ✅ Rate limiting (10/50/200/unlimited searches per day based on tier)
- ✅ Data freshness indicators (fresh/recent/stale)
- ✅ Case relationships (appeal/writ/SLP linkages)
- ✅ Subscription order creation (Razorpay integration ready)
- ✅ Background jobs (auto-refresh tracked cases, cleanup stale data)
- ✅ Scraper framework (AFT, CAT, HC, SC parsers ready)

## 🔜 Next Steps

- Android app development (starting tomorrow)
- Razorpay payment testing with real test keys
- Twilio OTP integration (currently OTP is logged server-side)
- Admin dashboard UI
- Real court PDF scraping (currently using seeded test data)

---

## 💡 Feedback Requested

Please test the above flows and share feedback on:
1. Is the login/registration flow clear?
2. Is the case search and tracking intuitive?
3. Any additional fields needed in case display?
4. Preferred layout for the dashboard?
5. Any court or case type missing?
