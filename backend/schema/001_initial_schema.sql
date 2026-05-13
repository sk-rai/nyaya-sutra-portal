-- ============================================================
-- Nyaya Sutra Portal - Database Schema
-- Version: 1.0
-- Date: March 2026
-- Database: PostgreSQL 14+
-- 
-- Design Principles:
--   1. Lightweight storage (fetch-on-demand with smart caching)
--   2. Anti-fragile scraping (JSONB for raw data, structured for known fields)
--   3. Tier-based access control
--   4. Periodic cleanup of stale cache
-- ============================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- 1. COURTS (Reference table - static, manually maintained)
-- ============================================================
CREATE TABLE courts (
    code VARCHAR(30) PRIMARY KEY,          -- e.g., "sc", "hc_del", "aft_del", "cat_mum"
    name VARCHAR(255) NOT NULL,            -- e.g., "Armed Forces Tribunal - Delhi"
    short_name VARCHAR(50),                -- e.g., "AFT Delhi"
    court_type VARCHAR(20) NOT NULL,       -- sc, hc, aft, cat, district, appellate
    state VARCHAR(100),                    -- NULL for SC
    city VARCHAR(100),
    base_url VARCHAR(500),                 -- Court website URL
    cause_list_url VARCHAR(500),           -- Direct URL to cause list page
    scraper_key VARCHAR(50),              -- Which scraper module handles this court
    is_active BOOLEAN DEFAULT true,
    notes TEXT,                            -- Any special notes about this court's PDF format
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE courts IS 'Static reference table of all supported courts. Manually maintained.';
COMMENT ON COLUMN courts.scraper_key IS 'Maps to a scraper class/module. e.g., "aft_delhi", "cgat", "hc_generic"';

-- ============================================================
-- 2. USERS
-- ============================================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255),            -- bcrypt hash
    user_type VARCHAR(20) NOT NULL DEFAULT 'individual',  -- individual, advocate
    tier VARCHAR(30) NOT NULL DEFAULT 'free',             -- free, individual, advocate_normal, advocate_premium
    
    -- Advocate-specific fields
    enrollment_no VARCHAR(50),
    enrollment_date DATE,
    bar_council VARCHAR(100),
    
    -- Profile
    address TEXT,
    profile_image_url VARCHAR(500),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_tier ON users(tier);

-- ============================================================
-- 3. SUBSCRIPTIONS (Payment tracking)
-- ============================================================
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(30) NOT NULL,             -- individual, advocate_normal, advocate_premium
    amount_paise INTEGER NOT NULL,         -- Amount in paise (₹50 = 5000)
    currency VARCHAR(3) DEFAULT 'INR',
    
    -- Payment gateway details
    payment_gateway VARCHAR(20),           -- razorpay, stripe
    gateway_subscription_id VARCHAR(255),
    gateway_payment_id VARCHAR(255),
    
    -- Dates
    started_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    cancelled_at TIMESTAMP,
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- active, expired, cancelled, payment_failed
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_expires ON subscriptions(expires_at);

-- ============================================================
-- 4. CASE CACHE (The heart of the system)
--    
--    This is the "warm" cache. Cases are fetched on-demand from
--    court PDFs and stored here. Tracked cases persist; untracked
--    cases are purged after a configurable period.
--
--    ANTI-FRAGILITY: We store both structured fields (for queries)
--    AND the raw scraped data as JSONB. If PDF format changes and
--    our parser breaks, we still have the raw text. We can also
--    re-parse later with updated logic.
-- ============================================================
CREATE TABLE case_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    court_code VARCHAR(30) NOT NULL REFERENCES courts(code),
    case_number VARCHAR(150) NOT NULL,     -- As it appears in the PDF
    
    -- Structured fields (best-effort parsed from PDF)
    case_title VARCHAR(500),
    petitioner VARCHAR(500),
    respondent VARCHAR(500),
    advocate_petitioner VARCHAR(500),
    advocate_respondent VARCHAR(500),
    bench VARCHAR(255),
    item_number VARCHAR(20),
    case_type VARCHAR(50),                 -- OA, TA, MA, WP, SLP, etc.
    case_status VARCHAR(50),               -- pending, disposed, reserved, part_heard
    
    -- Hearing dates
    next_hearing_date DATE,
    last_hearing_date DATE,
    
    -- ANTI-FRAGILITY: Raw scraped data preserved as-is
    -- Even if parsing fails, we keep the raw text for manual review
    -- or re-parsing with updated logic
    raw_scraped_data JSONB,                -- Full raw text/data from PDF
    parse_confidence FLOAT DEFAULT 1.0,    -- 0.0 to 1.0, how confident the parser was
    parse_errors TEXT[],                   -- Any fields that failed to parse
    
    -- Flexible metadata (for fields we didn't anticipate)
    extra_fields JSONB DEFAULT '{}',       -- Catch-all for new/unknown fields
    
    -- Source tracking
    source_url VARCHAR(500),               -- URL of the PDF we scraped
    source_page_number INTEGER,            -- Which page in the PDF
    
    -- Cache management
    is_tracked BOOLEAN DEFAULT false,      -- true if any user is tracking this case
    tracked_by_count INTEGER DEFAULT 0,    -- How many users track this
    fetched_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_accessed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_refreshed_at TIMESTAMP,           -- When we last re-scraped
    refresh_count INTEGER DEFAULT 0,       -- How many times refreshed
    
    -- Scraper version (for re-parsing when scraper logic changes)
    scraper_version VARCHAR(20),
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- A case is unique per court + case_number
    UNIQUE(court_code, case_number)
);

CREATE INDEX idx_case_cache_court ON case_cache(court_code);
CREATE INDEX idx_case_cache_number ON case_cache(case_number);
CREATE INDEX idx_case_cache_tracked ON case_cache(is_tracked);
CREATE INDEX idx_case_cache_next_hearing ON case_cache(next_hearing_date);
CREATE INDEX idx_case_cache_last_accessed ON case_cache(last_accessed_at);
CREATE INDEX idx_case_cache_fetched ON case_cache(fetched_at);

COMMENT ON TABLE case_cache IS 'On-demand case cache. Fetched from court PDFs when users search. Auto-purged when stale.';
COMMENT ON COLUMN case_cache.raw_scraped_data IS 'Raw text/data from PDF preserved for anti-fragility. Allows re-parsing if scraper logic changes.';
COMMENT ON COLUMN case_cache.parse_confidence IS '0.0-1.0 confidence score. Low confidence = PDF format may have changed.';
COMMENT ON COLUMN case_cache.extra_fields IS 'JSONB catch-all for fields not in the structured schema. Future-proofs against PDF changes.';

-- ============================================================
-- 5. CASE HEARINGS (Historical hearing records for tracked cases)
-- ============================================================
CREATE TABLE case_hearings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES case_cache(id) ON DELETE CASCADE,
    hearing_date DATE NOT NULL,
    bench VARCHAR(255),
    item_number VARCHAR(20),
    order_summary TEXT,
    order_pdf_url VARCHAR(500),
    raw_data JSONB,                        -- Raw scraped hearing data
    fetched_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(case_id, hearing_date)
);

CREATE INDEX idx_hearings_case ON case_hearings(case_id);
CREATE INDEX idx_hearings_date ON case_hearings(hearing_date);

-- ============================================================
-- 6. USER TRACKED CASES (HOT data - persists until user removes)
-- ============================================================
CREATE TABLE user_tracked_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    case_id UUID NOT NULL REFERENCES case_cache(id) ON DELETE CASCADE,
    
    -- User preferences for this case
    alert_enabled BOOLEAN DEFAULT true,
    alert_sms BOOLEAN DEFAULT false,
    alert_whatsapp BOOLEAN DEFAULT false,
    alert_email BOOLEAN DEFAULT true,
    notes TEXT,
    
    added_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, case_id)
);

CREATE INDEX idx_tracked_user ON user_tracked_cases(user_id);
CREATE INDEX idx_tracked_case ON user_tracked_cases(case_id);

-- ============================================================
-- 7. SCRAPER REGISTRY (Anti-fragility: track scraper health)
--    
--    Each court has a scraper. We track success/failure rates
--    so we can detect when a PDF format changes and alert admins.
-- ============================================================
CREATE TABLE scraper_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    court_code VARCHAR(30) NOT NULL REFERENCES courts(code),
    scraper_version VARCHAR(20) NOT NULL,
    
    -- Health metrics
    last_run_at TIMESTAMP,
    last_success_at TIMESTAMP,
    last_failure_at TIMESTAMP,
    consecutive_failures INTEGER DEFAULT 0,
    total_runs INTEGER DEFAULT 0,
    total_successes INTEGER DEFAULT 0,
    total_failures INTEGER DEFAULT 0,
    avg_parse_confidence FLOAT,
    
    -- Alert thresholds
    is_healthy BOOLEAN DEFAULT true,
    failure_threshold INTEGER DEFAULT 3,   -- Alert after N consecutive failures
    
    -- Last error details
    last_error_message TEXT,
    last_error_details JSONB,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(court_code, scraper_version)
);

COMMENT ON TABLE scraper_registry IS 'Tracks scraper health per court. Detects PDF format changes via failure patterns.';

-- ============================================================
-- 8. SCRAPE LOG (Audit trail of all scrape operations)
-- ============================================================
CREATE TABLE scrape_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    court_code VARCHAR(30) NOT NULL REFERENCES courts(code),
    triggered_by VARCHAR(50),              -- "user_search", "background_refresh", "manual"
    triggered_by_user_id UUID REFERENCES users(id),
    
    -- What was scraped
    source_url VARCHAR(500),
    pdf_page_count INTEGER,
    cases_found INTEGER DEFAULT 0,
    cases_parsed_ok INTEGER DEFAULT 0,
    cases_parse_failed INTEGER DEFAULT 0,
    
    -- Timing
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    
    -- Result
    status VARCHAR(20) NOT NULL DEFAULT 'running',  -- running, success, partial, failed
    error_message TEXT,
    error_details JSONB,
    
    -- Confidence
    avg_parse_confidence FLOAT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scrape_log_court ON scrape_log(court_code);
CREATE INDEX idx_scrape_log_status ON scrape_log(status);
CREATE INDEX idx_scrape_log_started ON scrape_log(started_at);

COMMENT ON TABLE scrape_log IS 'Audit trail of every scrape operation. Useful for debugging and monitoring.';

-- ============================================================
-- 9. PDF FORMAT SIGNATURES (Anti-fragility: detect format changes)
--    
--    We store "signatures" of known PDF formats. When a new PDF
--    doesn't match any known signature, we flag it for review.
--    This lets us detect format changes BEFORE they break parsing.
-- ============================================================
CREATE TABLE pdf_format_signatures (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    court_code VARCHAR(30) NOT NULL REFERENCES courts(code),
    
    -- Format identification
    format_name VARCHAR(100),              -- e.g., "AFT Delhi Standard 2024"
    format_version VARCHAR(20),
    
    -- Signature characteristics
    header_pattern TEXT,                   -- Regex/text pattern for PDF header
    column_pattern TEXT[],                 -- Expected column headers
    row_pattern TEXT,                      -- Regex for data rows
    page_layout VARCHAR(20),              -- portrait, landscape
    expected_columns INTEGER,
    
    -- Sample data for validation
    sample_raw_text TEXT,                  -- A sample of what this format looks like
    
    -- Status
    is_current BOOLEAN DEFAULT true,       -- Is this the current format?
    first_seen_at TIMESTAMP DEFAULT NOW(),
    last_seen_at TIMESTAMP DEFAULT NOW(),
    
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE pdf_format_signatures IS 'Known PDF format patterns per court. Detects when format changes.';

-- ============================================================
-- 10. OTP TOKENS (Short-lived, for authentication)
-- ============================================================
CREATE TABLE otp_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    identifier VARCHAR(255) NOT NULL,      -- email or phone
    otp_hash VARCHAR(255) NOT NULL,        -- hashed OTP
    purpose VARCHAR(20) DEFAULT 'login',   -- login, register, reset
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_otp_identifier ON otp_tokens(identifier);
CREATE INDEX idx_otp_expires ON otp_tokens(expires_at);

-- ============================================================
-- 11. USER SESSIONS (JWT tracking)
-- ============================================================
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    device_info VARCHAR(500),
    ip_address VARCHAR(45),
    expires_at TIMESTAMP NOT NULL,
    revoked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);

-- ============================================================
-- SEED DATA: Courts
-- ============================================================
INSERT INTO courts (code, name, short_name, court_type, state, city, base_url, cause_list_url, scraper_key) VALUES
-- Supreme Court
('sc', 'Supreme Court of India', 'Supreme Court', 'sc', NULL, 'New Delhi', 'https://www.sci.gov.in', 'https://www.sci.gov.in/cause-list', 'sc_india'),

-- High Courts
('hc_del', 'Delhi High Court', 'Delhi HC', 'hc', 'Delhi', 'New Delhi', 'https://delhihighcourt.nic.in', NULL, 'hc_delhi'),
('hc_bom', 'Bombay High Court', 'Bombay HC', 'hc', 'Maharashtra', 'Mumbai', 'https://bombayhighcourt.nic.in', NULL, 'hc_bombay'),
('hc_cal', 'Calcutta High Court', 'Calcutta HC', 'hc', 'West Bengal', 'Kolkata', 'https://calcuttahighcourt.gov.in', NULL, 'hc_calcutta'),
('hc_mad', 'Madras High Court', 'Madras HC', 'hc', 'Tamil Nadu', 'Chennai', 'https://www.mhc.tn.gov.in', NULL, 'hc_madras'),
('hc_kar', 'Karnataka High Court', 'Karnataka HC', 'hc', 'Karnataka', 'Bangalore', 'https://karnatakajudiciary.kar.nic.in', NULL, 'hc_karnataka'),
('hc_raj', 'Rajasthan High Court', 'Rajasthan HC', 'hc', 'Rajasthan', 'Jaipur', 'https://hcraj.nic.in', NULL, 'hc_rajasthan'),

-- AFT (Armed Forces Tribunal)
('aft_del', 'Armed Forces Tribunal - Principal Bench Delhi', 'AFT Delhi', 'aft', 'Delhi', 'New Delhi', 'https://aftdelhi.nic.in', 'https://aftdelhi.nic.in/index.php/reg-benches/mumbai/mumbai-cause-list', 'aft_delhi'),
('aft_mum', 'Armed Forces Tribunal - Mumbai Bench', 'AFT Mumbai', 'aft', 'Maharashtra', 'Mumbai', 'https://aftdelhi.nic.in', NULL, 'aft_mumbai'),
('aft_che', 'Armed Forces Tribunal - Chennai Bench', 'AFT Chennai', 'aft', 'Tamil Nadu', 'Chennai', 'https://aftdelhi.nic.in', NULL, 'aft_chennai'),
('aft_kol', 'Armed Forces Tribunal - Kolkata Bench', 'AFT Kolkata', 'aft', 'West Bengal', 'Kolkata', 'https://aftdelhi.nic.in', NULL, 'aft_kolkata'),
('aft_chd', 'Armed Forces Tribunal - Chandigarh Bench', 'AFT Chandigarh', 'aft', 'Chandigarh', 'Chandigarh', 'https://aftdelhi.nic.in', NULL, 'aft_chandigarh'),
('aft_lko', 'Armed Forces Tribunal - Lucknow Bench', 'AFT Lucknow', 'aft', 'Uttar Pradesh', 'Lucknow', 'https://aftdelhi.nic.in', NULL, 'aft_lucknow'),
('aft_jai', 'Armed Forces Tribunal - Jaipur Bench', 'AFT Jaipur', 'aft', 'Rajasthan', 'Jaipur', 'https://aftdelhi.nic.in', NULL, 'aft_jaipur'),

-- CAT (Central Administrative Tribunal)
('cat_del', 'Central Administrative Tribunal - Principal Bench Delhi', 'CAT Delhi', 'cat', 'Delhi', 'New Delhi', 'https://cis.cgat.gov.in', 'https://cis.cgat.gov.in/catlive/pdf/', 'cat_delhi'),
('cat_mum', 'Central Administrative Tribunal - Mumbai Bench', 'CAT Mumbai', 'cat', 'Maharashtra', 'Mumbai', 'https://cis.cgat.gov.in', NULL, 'cat_mumbai'),
('cat_che', 'Central Administrative Tribunal - Chennai Bench', 'CAT Chennai', 'cat', 'Tamil Nadu', 'Chennai', 'https://cis.cgat.gov.in', NULL, 'cat_chennai'),
('cat_kol', 'Central Administrative Tribunal - Kolkata Bench', 'CAT Kolkata', 'cat', 'West Bengal', 'Kolkata', 'https://cis.cgat.gov.in', NULL, 'cat_kolkata'),
('cat_blr', 'Central Administrative Tribunal - Bangalore Bench', 'CAT Bangalore', 'cat', 'Karnataka', 'Bangalore', 'https://cis.cgat.gov.in', NULL, 'cat_bangalore'),

-- Appellate Tribunals
('nclat', 'National Company Law Appellate Tribunal', 'NCLAT', 'appellate', NULL, 'New Delhi', 'https://nclat.nic.in', NULL, 'nclat'),
('itat_del', 'Income Tax Appellate Tribunal - Delhi', 'ITAT Delhi', 'appellate', 'Delhi', 'New Delhi', 'https://itat.gov.in', NULL, 'itat_delhi'),
('cestat', 'Customs Excise and Service Tax Appellate Tribunal', 'CESTAT', 'appellate', NULL, 'New Delhi', 'https://cestat.gov.in', NULL, 'cestat'),
('tdsat', 'Telecom Disputes Settlement Appellate Tribunal', 'TDSAT', 'appellate', NULL, 'New Delhi', 'https://tdsat.gov.in', NULL, 'tdsat');
