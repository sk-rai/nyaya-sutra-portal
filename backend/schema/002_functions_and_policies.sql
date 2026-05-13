-- ============================================================
-- Nyaya Sutra Portal - Functions, Triggers & Cleanup Policies
-- Version: 1.0
-- ============================================================

-- ============================================================
-- FUNCTION: Update timestamp trigger
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to relevant tables
CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_case_cache_updated_at
    BEFORE UPDATE ON case_cache
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_courts_updated_at
    BEFORE UPDATE ON courts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_scraper_registry_updated_at
    BEFORE UPDATE ON scraper_registry
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- FUNCTION: Update tracked_by_count when users track/untrack
-- ============================================================
CREATE OR REPLACE FUNCTION update_tracked_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE case_cache 
        SET tracked_by_count = tracked_by_count + 1,
            is_tracked = true
        WHERE id = NEW.case_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE case_cache 
        SET tracked_by_count = GREATEST(tracked_by_count - 1, 0),
            is_tracked = (tracked_by_count - 1 > 0)
        WHERE id = OLD.case_id;
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_tracked_count_insert
    AFTER INSERT ON user_tracked_cases
    FOR EACH ROW EXECUTE FUNCTION update_tracked_count();

CREATE TRIGGER trg_tracked_count_delete
    AFTER DELETE ON user_tracked_cases
    FOR EACH ROW EXECUTE FUNCTION update_tracked_count();

-- ============================================================
-- FUNCTION: Purge stale cache (called by periodic job)
--
-- Rules:
--   - Untracked cases older than 48 hours: DELETE
--   - Untracked cases not accessed in 24 hours: DELETE
--   - Tracked cases: NEVER delete (only refresh)
--   - OTP tokens older than 10 minutes: DELETE
--   - Expired sessions: DELETE
-- ============================================================
CREATE OR REPLACE FUNCTION purge_stale_cache(
    max_age_hours INTEGER DEFAULT 48,
    inactive_hours INTEGER DEFAULT 24
)
RETURNS TABLE(
    deleted_cases INTEGER,
    deleted_hearings INTEGER,
    deleted_otps INTEGER,
    deleted_sessions INTEGER
) AS $$
DECLARE
    v_deleted_cases INTEGER := 0;
    v_deleted_hearings INTEGER := 0;
    v_deleted_otps INTEGER := 0;
    v_deleted_sessions INTEGER := 0;
BEGIN
    -- Delete hearings for cases about to be purged
    WITH stale_cases AS (
        SELECT id FROM case_cache
        WHERE is_tracked = false
        AND (
            fetched_at < NOW() - (max_age_hours || ' hours')::INTERVAL
            OR last_accessed_at < NOW() - (inactive_hours || ' hours')::INTERVAL
        )
    )
    DELETE FROM case_hearings
    WHERE case_id IN (SELECT id FROM stale_cases);
    GET DIAGNOSTICS v_deleted_hearings = ROW_COUNT;

    -- Delete stale untracked cases
    DELETE FROM case_cache
    WHERE is_tracked = false
    AND (
        fetched_at < NOW() - (max_age_hours || ' hours')::INTERVAL
        OR last_accessed_at < NOW() - (inactive_hours || ' hours')::INTERVAL
    );
    GET DIAGNOSTICS v_deleted_cases = ROW_COUNT;

    -- Delete expired OTPs
    DELETE FROM otp_tokens
    WHERE expires_at < NOW();
    GET DIAGNOSTICS v_deleted_otps = ROW_COUNT;

    -- Delete expired/revoked sessions
    DELETE FROM user_sessions
    WHERE expires_at < NOW() OR revoked_at IS NOT NULL;
    GET DIAGNOSTICS v_deleted_sessions = ROW_COUNT;

    RETURN QUERY SELECT v_deleted_cases, v_deleted_hearings, v_deleted_otps, v_deleted_sessions;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION purge_stale_cache IS 'Periodic cleanup. Call every 6 hours via cron/scheduler.';

-- ============================================================
-- FUNCTION: Get cases needing refresh (for background job)
--
-- Returns tracked cases that haven't been refreshed recently.
-- Premium users' cases get refreshed more frequently.
-- ============================================================
CREATE OR REPLACE FUNCTION get_cases_needing_refresh(
    normal_refresh_hours INTEGER DEFAULT 24,
    premium_refresh_hours INTEGER DEFAULT 12
)
RETURNS TABLE(
    case_id UUID,
    court_code VARCHAR,
    case_number VARCHAR,
    source_url VARCHAR,
    max_tier VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        cc.id AS case_id,
        cc.court_code,
        cc.case_number,
        cc.source_url,
        -- Get the highest tier among users tracking this case
        MAX(u.tier) AS max_tier
    FROM case_cache cc
    JOIN user_tracked_cases utc ON utc.case_id = cc.id
    JOIN users u ON u.id = utc.user_id
    WHERE cc.is_tracked = true
    AND (
        -- Premium users' cases: refresh every premium_refresh_hours
        (u.tier = 'advocate_premium' AND 
         (cc.last_refreshed_at IS NULL OR cc.last_refreshed_at < NOW() - (premium_refresh_hours || ' hours')::INTERVAL))
        OR
        -- Normal users' cases: refresh every normal_refresh_hours
        (u.tier != 'advocate_premium' AND 
         (cc.last_refreshed_at IS NULL OR cc.last_refreshed_at < NOW() - (normal_refresh_hours || ' hours')::INTERVAL))
    )
    GROUP BY cc.id, cc.court_code, cc.case_number, cc.source_url;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: Record a case access (updates last_accessed_at)
-- ============================================================
CREATE OR REPLACE FUNCTION touch_case(p_case_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE case_cache
    SET last_accessed_at = NOW()
    WHERE id = p_case_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: Check user case limits based on tier
-- ============================================================
CREATE OR REPLACE FUNCTION check_case_limit(p_user_id UUID)
RETURNS TABLE(
    current_count INTEGER,
    max_allowed INTEGER,
    can_add BOOLEAN
) AS $$
DECLARE
    v_tier VARCHAR;
    v_count INTEGER;
    v_max INTEGER;
BEGIN
    SELECT tier INTO v_tier FROM users WHERE id = p_user_id;
    SELECT COUNT(*) INTO v_count FROM user_tracked_cases WHERE user_id = p_user_id;
    
    v_max := CASE v_tier
        WHEN 'free' THEN 5
        WHEN 'individual' THEN 50
        WHEN 'advocate_normal' THEN 300
        WHEN 'advocate_premium' THEN 2000
        ELSE 5
    END;
    
    RETURN QUERY SELECT v_count, v_max, (v_count < v_max);
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: Detect scraper health issues
-- ============================================================
CREATE OR REPLACE FUNCTION check_scraper_health()
RETURNS TABLE(
    court_code VARCHAR,
    court_name VARCHAR,
    consecutive_failures INTEGER,
    last_success TIMESTAMP,
    last_failure TIMESTAMP,
    avg_confidence FLOAT,
    needs_attention BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sr.court_code,
        c.name AS court_name,
        sr.consecutive_failures,
        sr.last_success_at AS last_success,
        sr.last_failure_at AS last_failure,
        sr.avg_parse_confidence AS avg_confidence,
        (sr.consecutive_failures >= sr.failure_threshold 
         OR sr.avg_parse_confidence < 0.7) AS needs_attention
    FROM scraper_registry sr
    JOIN courts c ON c.code = sr.court_code
    WHERE sr.is_healthy = false
       OR sr.consecutive_failures >= sr.failure_threshold
       OR sr.avg_parse_confidence < 0.7
    ORDER BY sr.consecutive_failures DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION check_scraper_health IS 'Returns courts where scrapers are failing. Use for monitoring/alerting.';

-- ============================================================
-- VIEW: Active subscriptions with user info
-- ============================================================
CREATE OR REPLACE VIEW v_active_subscriptions AS
SELECT 
    u.id AS user_id,
    u.name,
    u.email,
    u.tier,
    s.started_at,
    s.expires_at,
    s.amount_paise,
    CASE 
        WHEN s.expires_at > NOW() THEN 'active'
        ELSE 'expired'
    END AS computed_status
FROM users u
LEFT JOIN subscriptions s ON s.user_id = u.id AND s.status = 'active'
WHERE u.is_active = true;

-- ============================================================
-- VIEW: Case cache with tracking info
-- ============================================================
CREATE OR REPLACE VIEW v_case_summary AS
SELECT 
    cc.id,
    cc.court_code,
    c.short_name AS court_name,
    c.court_type,
    cc.case_number,
    cc.case_title,
    cc.petitioner,
    cc.respondent,
    cc.advocate_petitioner,
    cc.next_hearing_date,
    cc.last_hearing_date,
    cc.case_status,
    cc.is_tracked,
    cc.tracked_by_count,
    cc.parse_confidence,
    cc.fetched_at,
    cc.last_accessed_at,
    -- Staleness indicator
    CASE 
        WHEN cc.fetched_at > NOW() - INTERVAL '6 hours' THEN 'fresh'
        WHEN cc.fetched_at > NOW() - INTERVAL '24 hours' THEN 'recent'
        WHEN cc.fetched_at > NOW() - INTERVAL '48 hours' THEN 'stale'
        ELSE 'very_stale'
    END AS freshness
FROM case_cache cc
JOIN courts c ON c.code = cc.court_code;
