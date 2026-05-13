# Court Data Sources & Case Linkage Analysis

**Date:** March 2026  
**Purpose:** Understand how each court publishes data, PDF formats, and how cases link across courts

---

## 1. Data Sources Per Court

### Supreme Court of India (sci.gov.in)

**Data Access Methods:**
- **Cause List:** HTML page at `/cause-list/` shows daily index (court number, judges, session)
- **Published Cause List:** PDF downloads at `/published-cause-list/` (by court number, type: Miscellaneous/Regular/Advance)
- **Case Status:** Web form at `/case-status-case-no/` (requires Case Type + Number + Year + CAPTCHA)
- **Judgments:** Searchable by case number at `/judgements-case-no/`
- **Daily Orders:** Available online

**Case Number Format:**
```
[Case Type] No. [Number] / [Year]
Examples:
  SLP(C) No. 12345/2025       (Special Leave Petition - Civil)
  CA No. 6789/2024            (Civil Appeal)
  WP(C) No. 234/2026          (Writ Petition - Civil)
  TC(C) No. 56/2025           (Transfer Case - Civil)
```

**Case Types (key ones for service matters):**
- SLP(C) - Special Leave Petition (Civil)
- SLP(Crl) - Special Leave Petition (Criminal)
- CA - Civil Appeal
- WP(C) - Writ Petition (Civil)
- TC(C) - Transfer Case (Civil)
- CONMT.PET.(C) - Contempt Petition (Civil)
- CURATIVE PET. - Curative Petition

**PDF Cause List Format (typical):**
```
COURT NO. [X] - HON'BLE [JUDGE NAMES]
[Date] AT [Time]

ITEM NO. | CASE NO. | PARTIES | ADVOCATE(S)
---------|----------|---------|------------
1        | SLP(C).. | X vs Y  | Adv. A / Adv. B
```

**Scraping Approach:** 
- Cause list PDFs are downloadable (court-number wise)
- Case status requires CAPTCHA solving (harder to automate)
- Best approach: Scrape cause list PDFs for hearing dates, use case status form for detailed info

---

### High Courts (via eCourts - hcservices.ecourts.gov.in)

**Data Access Methods:**
- **eCourts Portal:** Unified portal for ALL High Courts
- **Search by:** Case Number, FIR Number, Party Name, Advocate Name, CNR Number
- **Case Status:** Web form with CAPTCHA
- **Cause Lists:** Each HC also publishes its own PDF cause lists

**Case Number Format (Delhi HC example):**
```
W.P.(C) 2342/2026             (Writ Petition Civil)
CRL.A. 456/2025              (Criminal Appeal)
FAO(OS) 123/2024             (First Appeal from Order - Original Side)
LPA 789/2025                 (Letters Patent Appeal)
CM APPL. 11291/2026          (Civil Miscellaneous Application)
```

**Delhi HC Specific:**
- URL: delhihighcourt.nic.in
- Cause lists: PDF downloads (Regular + Advance lists)
- PDF sizes: 4-6 MB (large, multi-bench)
- Format: Bench-wise listing with case details

**PDF Cause List Format (Delhi HC typical):**
```
HON'BLE [JUDGE NAME(S)]
COURT NO. [X]

S.No | Case No. | Title | Advocate(s) | Remarks
-----|----------|-------|-------------|--------
1    | W.P.(C) | X v Y | Adv. A      | Fresh/Hearing
```

**Scraping Approach:**
- eCourts portal has CAPTCHA (harder)
- PDF cause lists are freely downloadable from each HC website
- Delhi HC: Regular + Advance cause lists published daily

---

### AFT - Armed Forces Tribunal (aftdelhi.nic.in)

**Data Access Methods:**
- **Cause Lists:** PDF downloads from website
- **Case Status:** Not available online (must check cause list)
- **Orders:** Some available as PDFs

**Case Number Format:**
```
OA [Number]/[Year]/[Bench]    (Original Application)
TA [Number]/[Year]/[Bench]    (Transfer Application)
MA [Number]/[Year]/[Bench]    (Miscellaneous Application)
RA [Number]/[Year]/[Bench]    (Review Application)
WP(C) [Number]/[Year]         (Writ Petition - when transferred from HC)

Examples:
  OA 123/2024/DEL             (Original Application, Delhi bench)
  TA 456/2025/MUM             (Transfer Application, Mumbai bench)
  MA 789/2024/CHD             (Misc Application, Chandigarh bench)
```

**PDF Cause List Format (AFT typical):**
```
ARMED FORCES TRIBUNAL, [BENCH NAME]
CAUSE LIST FOR [DATE]
BENCH: HON'BLE [JUDGE NAMES]

S.No | Case No.      | Parties              | Advocate(s)    | Remarks
-----|---------------|----------------------|----------------|--------
1    | OA 123/2024   | Ex-Hav X vs UOI     | Adv. A         | For hearing
2    | TA 456/2025   | Nb Sub Y vs UOI     | Adv. B         | For orders
```

**Key Characteristics:**
- Relatively simple tabular format
- Bench-specific PDFs
- Daily publication
- Smaller PDFs (fewer cases per bench)

---

### CAT - Central Administrative Tribunal (cis.cgat.gov.in)

**Data Access Methods:**
- **Case Status:** Online at `cis.cgat.gov.in/catlive/case_status.php`
  - Search by: Case No, Diary No, Party Name, Advocate Name
  - Bench selection required
- **Cause Lists:** PDF downloads at `/catlive/pdf/`
- **Display Board:** Live at `/catlive/Displayboard.php`
- **e-Filing:** Available at `efiling.cgat.gov.in`

**Case Number Format:**
```
OA [Number]/[Year]/[Bench Code]     (Original Application)
MA [Number]/[Year]/[Bench Code]     (Miscellaneous Application)
TA [Number]/[Year]/[Bench Code]     (Transfer Application)
CP [Number]/[Year]/[Bench Code]     (Contempt Petition)

Examples:
  OA 1234/2024/PB-DEL              (Original Application, Principal Bench Delhi)
  MA 567/2025/MUM                  (Misc Application, Mumbai)
  OA 890/2024/CHE                  (Original Application, Chennai)
```

**PDF Cause List Format (CAT typical):**
```
CENTRAL ADMINISTRATIVE TRIBUNAL
[BENCH NAME]
CAUSE LIST FOR [DATE]
COURT NO. [X] - HON'BLE [MEMBER NAMES]

S.No | Case No.        | Applicant vs Respondent | Advocate | For
-----|-----------------|------------------------|----------|----
1    | OA/1234/2024    | X vs Union of India    | Adv. A   | Hearing
```

**Key Characteristics:**
- Online case status available (advantage over AFT)
- Bench-specific cause lists
- Relatively structured format
- Multiple benches across India

---

## 2. Appeal Hierarchy & Case Linkages

### The Legal Appeal Chain (Service Matters)

```
                    ┌─────────────────────┐
                    │   SUPREME COURT     │
                    │   (Final Appeal)    │
                    │   SLP(C), CA        │
                    └─────────┬───────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
    │  HIGH COURT │  │  HIGH COURT  │  │  HIGH COURT  │
    │  (Art. 226) │  │  (Art. 226)  │  │  (Art. 226)  │
    │  WP(C)      │  │  WP(C)       │  │  WP(C)       │
    └──────┬──────┘  └──────┬───────┘  └──────┬───────┘
           │                │                  │
           ▼                ▼                  ▼
    ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
    │     AFT     │  │     CAT      │  │   District   │
    │  (OA, TA)   │  │  (OA, TA)    │  │   Court      │
    └─────────────┘  └──────────────┘  └──────────────┘
```

### How Cases Link Across Courts:

**1. AFT → High Court (Writ Petition under Art. 226)**
- After 2023 SC ruling, High Courts CAN hear challenges to AFT orders
- A case `OA 123/2024/DEL` at AFT Delhi can become `WP(C) 5678/2025` at Delhi HC
- The HC writ petition will reference the AFT case number in its title/body

**2. AFT → Supreme Court (SLP under Art. 136)**
- Direct appeal from AFT to SC via Special Leave Petition
- `OA 123/2024/DEL` at AFT → `SLP(C) 9999/2025` at SC
- SC case title will mention "arising out of order of AFT in OA 123/2024"

**3. CAT → High Court (Writ Petition under Art. 226)**
- CAT orders can be challenged in the HC of the state where the bench sits
- `OA 456/2024/PB-DEL` at CAT → `WP(C) 7890/2025` at Delhi HC

**4. CAT → Supreme Court (SLP)**
- Direct appeal possible but less common
- Usually goes through HC first

**5. High Court → Supreme Court (SLP/Appeal)**
- `WP(C) 5678/2025` at Delhi HC → `SLP(C) 1111/2026` at SC

### How to Detect Linkages:

**Method 1: Case Title Parsing**
- SC/HC cases often mention the lower court case in their title:
  - "X vs Union of India (Arising out of OA 123/2024 before AFT Delhi)"
  - "In the matter of: OA No. 456/2024 decided by CAT Delhi"

**Method 2: Impugned Order Reference**
- The petition/appeal document references the order being challenged
- This is in the case details, not always in the cause list

**Method 3: Party Name Matching**
- Same parties appearing in AFT/CAT and HC/SC = likely linked
- Combined with subject matter matching

**Method 4: User-Provided Linkage**
- Most reliable: Let users manually link their cases across courts
- User adds OA at AFT + WP at HC + SLP at SC as related cases

---

## 3. Schema Enhancement for Case Linkages

```sql
-- Add to the schema: Case relationships table
CREATE TABLE case_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- The two linked cases
    case_id UUID NOT NULL REFERENCES case_cache(id) ON DELETE CASCADE,
    related_case_id UUID NOT NULL REFERENCES case_cache(id) ON DELETE CASCADE,
    
    -- Relationship type
    relationship_type VARCHAR(30) NOT NULL,
    -- Types: 'appeal_of', 'writ_against', 'slp_against', 
    --        'transfer_from', 'connected_with', 'contempt_of'
    
    -- Direction: case_id [relationship] related_case_id
    -- e.g., SLP at SC [is appeal_of] OA at AFT
    
    -- How was this linkage detected?
    detected_by VARCHAR(20) NOT NULL DEFAULT 'user',
    -- Values: 'user', 'title_parse', 'party_match', 'auto'
    
    confidence FLOAT DEFAULT 1.0,  -- 1.0 for user-provided, lower for auto-detected
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(case_id, related_case_id, relationship_type)
);

CREATE INDEX idx_case_rel_case ON case_relationships(case_id);
CREATE INDEX idx_case_rel_related ON case_relationships(related_case_id);
```

---

## 4. Comparison of PDF Formats Across Courts

| Aspect | AFT | CAT | High Court | Supreme Court |
|--------|-----|-----|------------|---------------|
| **Format** | PDF (text-based) | PDF (text-based) | PDF (text-based) | PDF (text-based) |
| **Size** | Small (50-200 KB) | Medium (100-500 KB) | Large (2-6 MB) | Medium (200KB-1MB) |
| **Structure** | Simple table | Simple table | Complex multi-bench | Court-number wise |
| **Columns** | S.No, Case No, Parties, Advocate, Remarks | S.No, Case No, Parties, Advocate, For | S.No, Case No, Title, Advocate, Remarks | Item No, Case No, Parties, Advocate |
| **Frequency** | Daily | Daily | Daily (Regular + Advance) | Daily (per court) |
| **Online Status** | No | Yes (web form) | Yes (eCourts) | Yes (web form + CAPTCHA) |
| **CAPTCHA** | No | No | Yes (eCourts) | Yes |
| **Bench-wise** | Yes | Yes | Yes | Yes (court number) |

---

## 5. Anti-Fragility Considerations Per Court

### AFT PDFs
- **Risk:** Low complexity, but format varies between benches
- **Strategy:** One parser per bench type, fallback to generic
- **Signature:** Look for "ARMED FORCES TRIBUNAL" header + bench name

### CAT PDFs  
- **Risk:** Medium - multiple benches with slightly different formats
- **Strategy:** Bench-specific parsers with shared base logic
- **Advantage:** Online case status available as backup data source
- **Signature:** Look for "CENTRAL ADMINISTRATIVE TRIBUNAL" header

### High Court PDFs
- **Risk:** HIGH - large files, complex multi-bench layouts, frequent format changes
- **Strategy:** 
  - Use eCourts web portal as PRIMARY source (more structured)
  - PDF as fallback/supplement
  - Separate parser per HC (Delhi, Bombay, etc.)
- **Signature:** Court-specific headers and layouts

### Supreme Court PDFs
- **Risk:** Medium - well-structured but CAPTCHA-protected web access
- **Strategy:**
  - Cause list PDFs are freely downloadable (use these)
  - Case status requires CAPTCHA (defer to user-triggered lookup)
  - Court-number-wise parsing
- **Signature:** "SUPREME COURT OF INDIA" header, court number format

---

## 6. Recommended Scraping Priority

### Phase 1 (Immediate - Simplest)
1. **AFT Delhi** - Simple PDFs, your client's primary use case
2. **CAT Delhi** - Online case status available, good fallback

### Phase 2 (Next)
3. **AFT Other Benches** - Same format as Delhi, just different URLs
4. **CAT Other Benches** - Same system, different bench codes

### Phase 3 (Complex)
5. **Delhi High Court** - Large PDFs, complex format
6. **Supreme Court** - Cause list PDFs (avoid CAPTCHA-protected pages)

### Phase 4 (Future)
7. **Other High Courts** - Via eCourts portal
8. **Appellate Tribunals** - NCLAT, ITAT, etc.

---

## 7. Key Design Decisions

### Decision 1: PDF vs Web Scraping
- **AFT:** PDF only (no web case status)
- **CAT:** Web case status preferred (structured), PDF as supplement
- **HC:** eCourts web portal preferred, HC-specific PDFs as supplement
- **SC:** Cause list PDFs (free), case status web form (CAPTCHA - user-triggered only)

### Decision 2: Case Linkage Strategy
- **Primary:** User-provided linkages (most reliable)
- **Secondary:** Title parsing (look for "arising out of" patterns)
- **Tertiary:** Party name + court matching (fuzzy, lower confidence)
- **Store all linkages** with confidence scores

### Decision 3: What to Store from PDFs
- **Always store:** Case number, parties, advocate names, hearing date, bench
- **Store if available:** Item number, remarks/status, order references
- **Always preserve:** Raw text (for re-parsing)
- **Flexible fields:** JSONB for anything else found

### Decision 4: Handling CAPTCHA-Protected Sources
- **Don't auto-solve CAPTCHAs** (legal/ethical concerns)
- **User-triggered lookups:** User enters case number → we check cache first → if miss, show them the court's own search page or use PDF cause lists
- **For SC/HC case status:** Provide direct links to court websites for detailed info we can't scrape

---

## 8. Updated Schema Addition

Based on this analysis, we need to add the `case_relationships` table to track cross-court linkages. Run this in your WSL terminal:

```bash
PGPASSWORD='NyayaSutra2026!' psql -U nyaya_app -d nyaya_sutra -h localhost <<'EOF'
CREATE TABLE case_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES case_cache(id) ON DELETE CASCADE,
    related_case_id UUID NOT NULL REFERENCES case_cache(id) ON DELETE CASCADE,
    relationship_type VARCHAR(30) NOT NULL,
    detected_by VARCHAR(20) NOT NULL DEFAULT 'user',
    confidence FLOAT DEFAULT 1.0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(case_id, related_case_id, relationship_type)
);
CREATE INDEX idx_case_rel_case ON case_relationships(case_id);
CREATE INDEX idx_case_rel_related ON case_relationships(related_case_id);
COMMENT ON TABLE case_relationships IS 'Tracks linkages between cases across courts (e.g., AFT OA appealed as SLP at SC)';
EOF
```

---

**Document Status:** Complete  
**Next:** Set up Flask project structure with scraper framework
