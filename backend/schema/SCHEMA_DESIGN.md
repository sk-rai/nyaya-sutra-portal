# Database Schema Design - Nyaya Sutra Portal

**Date:** March 2026  
**Database:** PostgreSQL 14+  
**Strategy:** Fetch-on-Demand with Smart Caching

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST FLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User selects Court → Enters Case Number → Clicks Search    │
│                              ↓                               │
│                   ┌──────────────────┐                       │
│                   │  Check case_cache │                       │
│                   └──────────────────┘                       │
│                     ↓              ↓                          │
│                  CACHE HIT      CACHE MISS                   │
│                     ↓              ↓                          │
│              Return data     ┌──────────────┐                │
│              (< 50ms)        │ Scrape Court │                │
│                              │   PDF/Site   │                │
│                              └──────────────┘                │
│                                    ↓                         │
│                              Parse PDF data                   │
│                              (structured + raw JSONB)         │
│                                    ↓                         │
│                              Store in case_cache             │
│                                    ↓                         │
│                              Return to user                   │
│                              (3-8 seconds)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Tiers

| Tier | Table | Lifetime | Purge Rule |
|------|-------|----------|------------|
| **HOT** | `user_tracked_cases` | Permanent (until user removes) | Never auto-deleted |
| **WARM** | `case_cache` (tracked) | Permanent | Refreshed every 12-24h |
| **COOL** | `case_cache` (untracked) | 24-48 hours | Purged if not accessed |
| **COLD** | Court website | Not stored | Fetched on-demand |

---

## Anti-Fragility Design

### Problem
Court PDFs can change format at any time without notice. We have no API access.
A rigid parser will break silently when formats change.

### Solution: Multi-Layer Defense

#### Layer 1: Raw Data Preservation
```
case_cache.raw_scraped_data (JSONB)
```
Every scrape stores the complete raw text/data from the PDF. Even if parsing
fails completely, we have the original data for manual review or re-parsing.

#### Layer 2: Confidence Scoring
```
case_cache.parse_confidence (FLOAT 0.0 - 1.0)
```
Each parse operation produces a confidence score:
- 1.0 = All expected fields found and validated
- 0.7-0.9 = Most fields found, some missing/uncertain
- 0.5-0.7 = Partial parse, format may have changed
- < 0.5 = Major issues, likely format change

When confidence drops below threshold → alert admin, flag for review.

#### Layer 3: Format Signatures
```
pdf_format_signatures table
```
We store "fingerprints" of known PDF formats (header patterns, column layouts).
Before parsing, we check if the PDF matches a known format. If not → new format
detected → use fallback parser → alert admin.

#### Layer 4: Flexible Schema
```
case_cache.extra_fields (JSONB)
```
Any fields the parser finds that don't map to known columns go into `extra_fields`.
This means new columns in PDFs don't break anything — they just get stored as JSON.

#### Layer 5: Scraper Health Monitoring
```
scraper_registry table + scrape_log table
```
Track success/failure rates per court. After N consecutive failures:
- Mark scraper as unhealthy
- Alert admin
- Return cached data with "stale" warning to users
- Never show broken/empty results

#### Layer 6: Versioned Scrapers
```
case_cache.scraper_version
```
Each case record knows which scraper version parsed it. When we update a scraper,
we can selectively re-parse old records with the new logic.

### Parsing Strategy (Per Court)

```python
class BaseScraper:
    def scrape(self, court_code, case_number):
        # 1. Fetch PDF/page
        raw_content = self.fetch(url)
        
        # 2. Try primary parser
        result, confidence = self.parse_primary(raw_content)
        
        # 3. If confidence low, try fallback parser
        if confidence < 0.7:
            result2, confidence2 = self.parse_fallback(raw_content)
            if confidence2 > confidence:
                result, confidence = result2, confidence2
        
        # 4. Store BOTH structured result AND raw content
        return {
            'structured': result,
            'raw': raw_content,
            'confidence': confidence,
            'errors': self.get_parse_errors()
        }
```

---

## Storage Estimates

### Per Case Record
| Field | Avg Size |
|-------|----------|
| Structured fields | ~500 bytes |
| raw_scraped_data (JSONB) | ~2 KB |
| extra_fields | ~200 bytes |
| Indexes | ~300 bytes |
| **Total per case** | **~3 KB** |

### Projected Usage (500 users)
| Category | Count | Size |
|----------|-------|------|
| Tracked cases (HOT) | 5,000 | 15 MB |
| Warm cache (COOL) | 2,000 | 6 MB |
| Hearings history | 20,000 | 10 MB |
| Users + subscriptions | 500 | 1 MB |
| Scrape logs (30 days) | 5,000 | 5 MB |
| **Total** | | **~37 MB** |

This is extremely lightweight. Even at 5,000 users, we'd be under 500 MB.

---

## Periodic Jobs

### Every 6 Hours: Cache Cleanup
```sql
SELECT * FROM purge_stale_cache(48, 24);
-- Deletes untracked cases older than 48h or inactive for 24h
```

### Every 12 Hours: Refresh Tracked Cases
```sql
SELECT * FROM get_cases_needing_refresh(24, 12);
-- Returns cases that need re-scraping
-- Premium users: refresh every 12h
-- Normal users: refresh every 24h
```

### Every Hour: Health Check
```sql
SELECT * FROM check_scraper_health();
-- Returns courts with failing scrapers
```

---

## Latency Budget

| Operation | Target | Strategy |
|-----------|--------|----------|
| Cache hit (case exists) | < 100ms | Direct DB query |
| Cache miss (new scrape) | 3-8 sec | Show loading UI, async scrape |
| Tracked case refresh | Background | User never waits |
| Search within cache | < 200ms | Indexed queries |

### User Experience for Cache Miss:
```
1. User clicks "Search"
2. UI shows: "Fetching from [Court Name]..." with spinner
3. Backend scrapes PDF (3-8 seconds)
4. Result appears
5. Subsequent searches for same case: instant
```

---

## Tier Limits

| Tier | Tracked Cases | Search/Day | Refresh Rate | Synopsis |
|------|--------------|------------|--------------|----------|
| Free | 5 | 10 | 48h | No |
| Individual (₹50) | 50 | 50 | 24h | No |
| Advocate Normal (₹199) | 300 | 200 | 24h | No |
| Advocate Premium (₹599) | 2000 | Unlimited | 12h | Yes |

---

## Court PDF Formats (Known)

### AFT Delhi (aftdelhi.nic.in)
- **Format:** PDF cause list
- **Layout:** Tabular, landscape
- **Columns observed:** S.No, Case No, Parties, Advocate, Bench, Item No
- **Update frequency:** Daily (new cause list each day)
- **Challenges:** 
  - PDF structure varies between benches
  - Sometimes scanned images instead of text PDFs
  - Column alignment can shift

### CGAT (cis.cgat.gov.in)
- **Format:** PDF cause list
- **Layout:** Tabular
- **Columns observed:** S.No, Case No, Case Title, Advocate, Date
- **Update frequency:** Daily
- **Challenges:**
  - Multiple bench PDFs per day
  - Format differs between benches (Delhi vs Mumbai vs Chennai)

### General Challenges (All Courts):
1. No standard format across courts
2. PDFs may be text-based OR scanned images
3. Column headers may change without notice
4. Special characters and Hindi text in party names
5. Date formats vary (DD/MM/YYYY, DD-Mon-YYYY, etc.)
6. Case number formats vary per court

---

## Files

```
backend/schema/
├── 001_initial_schema.sql      -- Tables, indexes, seed data
├── 002_functions_and_policies.sql  -- Functions, triggers, views
└── SCHEMA_DESIGN.md            -- This document
```

---

## Setup Instructions

### Create Database
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE nyaya_sutra;
CREATE USER nyaya_app WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE nyaya_sutra TO nyaya_app;

# Connect to the new database
\c nyaya_sutra

# Run schema files in order
\i backend/schema/001_initial_schema.sql
\i backend/schema/002_functions_and_policies.sql
```

### Verify
```sql
-- Check tables created
\dt

-- Check courts seeded
SELECT code, short_name, court_type FROM courts ORDER BY court_type, code;

-- Test cleanup function
SELECT * FROM purge_stale_cache(48, 24);
```

---

## Next Steps

1. ✅ Schema design (this document)
2. ⏳ Create database in PostgreSQL
3. ⏳ Flask project structure with API routes
4. ⏳ Scraper framework (pluggable per court)
5. ⏳ Authentication (JWT + OTP)
6. ⏳ Payment integration (Razorpay)
7. ⏳ Background job scheduler
8. ⏳ Connect frontend to APIs
