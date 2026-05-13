# Implementation Plan: Nyaya Sutra Backend API

## Overview

This plan implements the Flask-based REST API for the Nyaya Sutra Legal Portal. The implementation follows a bottom-up approach: project scaffolding → data models → core services → API routes → middleware → background jobs → scrapers → tests. The existing PostgreSQL database (12 tables) is already provisioned; we only create SQLAlchemy models that map to the existing schema (no migrations).

**Language:** Python (Flask, SQLAlchemy, Hypothesis, pytest)

## Tasks

- [x] 1. Project setup and Flask app factory
  - [x] 1.1 Create project structure and install dependencies
    - Create `backend/` directory with the module structure defined in design (app/, models/, api/, services/, scrapers/, middleware/, utils/, jobs/)
    - Create `backend/requirements.txt` with: Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS, psycopg2-binary, APScheduler, hypothesis, pytest, razorpay, bcrypt, requests, pdfplumber
    - Create `backend/.env.example` with all required environment variables (DATABASE_URL, JWT_SECRET_KEY, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, OTP_EMAIL_SERVICE, OTP_SMS_SERVICE, CORS_ORIGIN, REDIS_URL)
    - Create `backend/run.py` entry point
    - _Requirements: 13, 14_

  - [x] 1.2 Implement Flask app factory and configuration
    - Create `backend/app/__init__.py` with `create_app()` factory function supporting test/dev/prod configs
    - Create `backend/app/config.py` with environment-based configuration classes (DevelopmentConfig, TestingConfig, ProductionConfig) including TIER_CONFIG dict from design
    - Create `backend/app/extensions.py` initializing SQLAlchemy, JWTManager, CORS
    - _Requirements: 13.1, 13.2, 13.3, 13.4_

  - [x] 1.3 Implement standard response envelope utility
    - Create `backend/app/utils/response.py` with `success_response(data)` and `error_response(code, message, details=None, status=400)` functions
    - Ensure all responses follow the envelope format: `{"success": bool, "data": obj|null, "error": obj|null}`
    - _Requirements: 14.1_

  - [x] 1.4 Implement global error handler
    - Create `backend/app/middleware/error_handler.py` with handlers for 400, 401, 403, 404, 429, 500 errors
    - Register error handlers in app factory
    - Ensure 500 errors log full traceback server-side but return only generic message to client
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [x] 2. Database models (mapping to existing schema)
  - [x] 2.1 Create Court and User models
    - Create `backend/app/models/court.py` with Court model mapping to `courts` table (all columns including scraper_key, is_active)
    - Create `backend/app/models/user.py` with User model mapping to `users` table and UserSession model mapping to `user_sessions` table
    - Include relationship definitions between User ↔ UserSession
    - _Requirements: 1, 2, 6_

  - [x] 2.2 Create Case and Hearing models
    - Create `backend/app/models/case.py` with CaseCache model mapping to `case_cache` table (including JSONB fields: raw_scraped_data, extra_fields, parse_errors)
    - Create CaseHearing model mapping to `case_hearings` table
    - Include relationship: CaseCache → CaseHearing (one-to-many)
    - _Requirements: 3, 5, 9_

  - [x] 2.3 Create Subscription, OTP, Tracking, and Scraper models
    - Create `backend/app/models/subscription.py` with Subscription model mapping to `subscriptions` table
    - Create `backend/app/models/otp.py` with OTPToken model mapping to `otp_tokens` table
    - Create `backend/app/models/tracking.py` with UserTrackedCase model mapping to `user_tracked_cases` table
    - Create `backend/app/models/scraper.py` with ScraperRegistry, ScrapeLog, and PdfFormatSignature models
    - _Requirements: 1, 5, 9, 10, 11_

  - [x] 2.4 Create models __init__.py and register all models
    - Create `backend/app/models/__init__.py` that imports and exposes all models
    - Verify all models load correctly with the app factory
    - _Requirements: All_

- [x] 3. Checkpoint - Verify project structure and models
  - Ensure the Flask app starts without errors, all models are importable, and the database connection works. Ask the user if questions arise.

- [x] 4. Core services - Authentication
  - [x] 4.1 Implement OTP utility functions
    - Create `backend/app/utils/otp.py` with `generate_otp()` (6-digit), `hash_otp(code)` (bcrypt), `verify_otp_hash(code, hash)` functions
    - Create `backend/app/utils/validators.py` with `validate_email(email)` and `validate_phone(phone)` (10-digit Indian mobile starting with 6-9)
    - _Requirements: 1.1, 2.5_

  - [x] 4.2 Implement AuthService
    - Create `backend/app/services/auth_service.py` with the AuthService class
    - Implement `request_otp(identifier, purpose)`: generate OTP, hash it, store in otp_tokens with 10-min expiry, dispatch via configured channel
    - Implement `verify_otp(identifier, otp_code)`: check hash, check expiry, check attempts < 3, issue JWT with user_id and tier claims, create user_sessions record
    - Implement `register_user(data)`: create user with tier="free", is_verified=false, validate inputs
    - Implement `logout(session_id)`: set revoked_at on user_sessions record
    - Implement `refresh_token(token)`: issue new JWT if current is valid but near expiry
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_

  - [ ]* 4.3 Write property tests for Auth (Properties 1-6)
    - **Property 1: OTP Generation Invariants** — verify 6-digit, bcrypt-hashed, 10-min expiry
    - **Property 2: JWT Issuance on Valid OTP** — verify JWT contains correct user_id and tier claims
    - **Property 3: Session Revocation** — verify revoked_at is set to non-null
    - **Property 4: Registration Defaults** — verify tier="free" and is_verified=false for all inputs
    - **Property 5: Input Validation Correctness** — verify email/phone validators accept/reject correctly
    - **Property 6: Duplicate Registration Prevention** — verify error on duplicate email/phone
    - Create `backend/tests/properties/test_props_auth.py`
    - **Validates: Requirements 1.1, 1.2, 1.5, 2.1, 2.4, 2.5**

- [x] 5. Core services - Case Cache and Rate Limiter
  - [x] 5.1 Implement CaseCacheService
    - Create `backend/app/services/cache_service.py` with the CaseCacheService class
    - Implement `search_case(court_code, case_number)`: check cache → return if fresh (<24h) → trigger scrape on miss → store result → return with freshness
    - Implement `get_freshness(fetched_at)`: deterministic calculation (fresh <6h, recent <24h, stale <48h, very_stale)
    - Implement `track_case(user_id, case_id, alerts)`: check tier limit via check_case_limit(), create user_tracked_cases record
    - Implement `untrack_case(user_id, case_id)`: delete user_tracked_cases record
    - Implement `get_tracked_cases(user_id)`: return all tracked cases with details and freshness
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 5.2 Implement RateLimiter service
    - Create `backend/app/services/rate_limiter.py` with the RateLimiter class
    - Implement `check_limit(user_id, tier)`: check daily count against TIER_LIMITS (free=10, individual=50, advocate_normal=200, advocate_premium=None)
    - Implement `increment(user_id)`: increment daily search count
    - Implement `get_reset_time()`: return next midnight IST (UTC+5:30)
    - Implement `get_remaining(user_id, tier)`: return remaining searches for today
    - Use in-memory dict with daily key (date-based) for single-instance; support Redis fallback via config
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ]* 5.3 Write property tests for Cache and Rate Limiter (Properties 7-13)
    - **Property 7: Cache Freshness Calculation** — deterministic freshness for any timestamp
    - **Property 8: Cache Hit Behavior** — fresh cache returns data without scrape
    - **Property 9: Stale Cache Triggers Re-scrape** — stale untracked cases trigger scrape
    - **Property 10: Rate Limit Tier Mapping** — correct limits per tier
    - **Property 11: Rate Limit Daily Reset** — counter resets at midnight IST
    - **Property 12: Tracking Round-Trip** — add then remove leaves count unchanged
    - **Property 13: Tracking Tier Limit Enforcement** — reject when at max
    - Create `backend/tests/properties/test_props_cache.py` and `backend/tests/properties/test_props_rate_limit.py`
    - **Validates: Requirements 3.1, 3.3, 3.4, 3.6, 4.1, 4.3, 4.4, 5.1, 5.2, 5.3**

- [x] 6. Core services - Payment and Refresh
  - [x] 6.1 Implement PaymentService
    - Create `backend/app/services/payment_service.py` with the PaymentService class
    - Implement `create_order(user_id, tier)`: create Razorpay order with correct amount (individual=5000, advocate_normal=19900, advocate_premium=59900 paise)
    - Implement `verify_payment(payment_data)`: verify Razorpay signature using HMAC-SHA256
    - Implement `handle_webhook(payload, signature)`: process payment.captured and payment.failed events, create subscription record, update user tier
    - Implement `check_expiry()`: find expired subscriptions, downgrade user tier to "free"
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [x] 6.2 Implement RefreshService
    - Create `backend/app/services/refresh_service.py` with the RefreshService class
    - Implement `refresh_tracked_cases(batch_size, delay_sec)`: call get_cases_needing_refresh DB function, scrape each in batches with delay, update cache
    - Implement `purge_stale_cache()`: call purge_stale_cache() DB function, log results
    - Implement `get_cases_needing_refresh()`: execute the DB function and return results
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3, 8.4_

  - [ ]* 6.3 Write property tests for Payment and Refresh (Properties 15-16, 22-24)
    - **Property 15: Background Refresh Preserves Data on Failure** — existing data unchanged on failure
    - **Property 16: Purge Respects Tracked Cases** — tracked cases never deleted
    - **Property 22: Subscription Tier-Amount Mapping** — correct amounts per tier
    - **Property 23: Failed Payment Preserves Tier** — tier unchanged on failure
    - **Property 24: Subscription Expiry Downgrade** — expired subscription → tier="free"
    - Create `backend/tests/properties/test_props_payments.py` and `backend/tests/properties/test_props_refresh.py`
    - **Validates: Requirements 7.3, 8.1, 8.2, 11.1, 11.3, 11.4**

- [x] 7. Checkpoint - Verify core services
  - Ensure all services instantiate correctly, unit tests for auth/cache/rate-limiter/payment pass. Ask the user if questions arise.

- [x] 8. API routes - Auth and Courts
  - [x] 8.1 Implement auth blueprint
    - Create `backend/app/api/auth.py` with Flask Blueprint
    - `POST /api/auth/otp/request` — accept identifier (email or phone), call AuthService.request_otp()
    - `POST /api/auth/otp/verify` — accept identifier + otp_code, call AuthService.verify_otp()
    - `POST /api/auth/register` — accept registration data, call AuthService.register_user()
    - `POST /api/auth/logout` — require JWT, call AuthService.logout()
    - All responses use standard envelope format
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 8.2 Implement courts blueprint
    - Create `backend/app/api/courts.py` with Flask Blueprint
    - `GET /api/courts` — return all active courts, support `court_type` filter parameter
    - Sort results by court_type then alphabetically by short_name
    - No authentication required
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ]* 8.3 Write property test for Court Filtering (Property 14)
    - **Property 14: Court Filtering** — only matching court_type returned, sorted correctly
    - Create `backend/tests/properties/test_props_courts.py`
    - **Validates: Requirements 6.2, 6.3**

- [x] 9. API routes - Cases, Tracking, and Relationships
  - [x] 9.1 Implement cases blueprint
    - Create `backend/app/api/cases.py` with Flask Blueprint
    - `GET /api/cases/search` — require JWT, accept court_code + case_number params, call CaseCacheService.search_case(), apply rate limiting
    - Return case data with freshness indicator in standard envelope
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2_

  - [x] 9.2 Implement tracking blueprint
    - Create `backend/app/api/tracking.py` with Flask Blueprint
    - `GET /api/tracking` — require JWT, call CaseCacheService.get_tracked_cases()
    - `POST /api/tracking` — require JWT, accept case_id + alert preferences, call CaseCacheService.track_case()
    - `DELETE /api/tracking/{case_id}` — require JWT, call CaseCacheService.untrack_case()
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 9.3 Implement relationships blueprint
    - Create `backend/app/api/relationships.py` with Flask Blueprint
    - `POST /api/cases/relationships` — require JWT, accept case_id + related_case_id + relationship_type, validate type is one of 6 valid values, set detected_by="user" and confidence=1.0
    - `GET /api/cases/{case_id}/relationships` — require JWT, return all related cases (both directions)
    - Prevent duplicate relationships (same case_id, related_case_id, relationship_type)
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [ ]* 9.4 Write property tests for Relationships (Properties 25-26)
    - **Property 25: Case Relationship Invariants** — detected_by="user", confidence=1.0, valid type
    - **Property 26: Bidirectional Relationship Retrieval** — both directions returned
    - Create `backend/tests/properties/test_props_relationships.py`
    - **Validates: Requirements 12.1, 12.2, 12.3**

- [x] 10. API routes - Subscriptions, Synopsis, and Admin
  - [x] 10.1 Implement subscriptions blueprint
    - Create `backend/app/api/subscriptions.py` with Flask Blueprint
    - `POST /api/subscriptions/create-order` — require JWT, accept tier, call PaymentService.create_order()
    - `POST /api/subscriptions/webhook` — no JWT (use Razorpay signature verification), call PaymentService.handle_webhook()
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [x] 10.2 Implement synopsis blueprint
    - Create `backend/app/api/synopsis.py` with Flask Blueprint
    - `GET /api/synopsis/{case_id}` — require JWT, check tier is advocate_premium, return 403 for other tiers
    - Return synopsis data (placeholder implementation for now)
    - _Requirements: 15.1, 15.2, 15.3_

  - [x] 10.3 Implement admin blueprint
    - Create `backend/app/api/admin.py` with Flask Blueprint
    - `GET /api/admin/scraper-health` — require JWT + admin check, call check_scraper_health() DB function
    - Return scraper health data in standard envelope
    - _Requirements: 10.4_

  - [ ]* 10.4 Write property tests for API format and Synopsis (Properties 27-29)
    - **Property 27: Response Envelope Format** — all responses have success, data, error fields
    - **Property 28: Error Response Safety** — 500 errors never expose internals
    - **Property 29: Synopsis Tier Gate** — only advocate_premium gets access, others get 403
    - Create `backend/tests/properties/test_props_api.py`
    - **Validates: Requirements 14.1, 14.5, 15.1, 15.2**

- [x] 11. Middleware - Auth, Rate Limiting, CORS
  - [x] 11.1 Implement auth middleware (JWT verification decorator)
    - Create `backend/app/middleware/auth_middleware.py` with `@require_auth` decorator
    - Extract JWT from Authorization header, verify signature and expiry
    - Check session not revoked (lookup user_sessions by token_hash)
    - Attach user_id and tier to Flask `g` object for downstream use
    - Return 401 for missing/invalid/expired tokens, 401 for revoked sessions
    - _Requirements: 1.2, 1.5, 4.4, 14.2_

  - [x] 11.2 Implement rate limit middleware
    - Create `backend/app/middleware/rate_limit.py` with `@rate_limited` decorator
    - Read tier from `g.user_tier`, call RateLimiter.check_limit()
    - On limit exceeded: return 429 with reset time
    - On success: call RateLimiter.increment()
    - _Requirements: 4.1, 4.2, 4.3, 14.3_

  - [x] 11.3 Register all blueprints and middleware in app factory
    - Update `backend/app/__init__.py` to register all API blueprints (auth, courts, cases, tracking, relationships, subscriptions, synopsis, admin)
    - Configure CORS to allow origin https://sk-rai.github.io, allow Authorization header, support OPTIONS preflight
    - Register global error handlers
    - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [x] 12. Checkpoint - Verify API routes and middleware
  - Ensure all endpoints respond correctly, auth middleware blocks unauthenticated requests, rate limiter returns 429 when exceeded, CORS headers are present. Ask the user if questions arise.

- [x] 13. Background jobs - Scheduler, Refresh, Cleanup
  - [x] 13.1 Implement APScheduler setup
    - Create `backend/app/jobs/scheduler.py` with scheduler initialization
    - Configure interval jobs: refresh_tracked_cases (every 6 hours), purge_stale_cache (every 6 hours), check_expiry (every 1 hour)
    - Integrate scheduler start/stop with Flask app lifecycle
    - _Requirements: 7.1, 8.1_

  - [x] 13.2 Implement refresh job
    - Create `backend/app/jobs/refresh_job.py` wrapping RefreshService.refresh_tracked_cases()
    - Process in batches of 10 with 2-second delay between requests
    - Log results (refreshed, failed, skipped counts)
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [x] 13.3 Implement cleanup job
    - Create `backend/app/jobs/cleanup_job.py` wrapping RefreshService.purge_stale_cache()
    - Log purge results (deleted_cases, deleted_hearings, deleted_otps, deleted_sessions)
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 14. Scraper framework - Base and Registry
  - [x] 14.1 Implement BaseScraper abstract class
    - Create `backend/app/scrapers/base.py` with BaseScraper ABC
    - Define abstract methods: `fetch_pdf(court_code, source_url)`, `parse(raw_content)`
    - Implement concrete methods: `scrape(court_code, case_number)` (full pipeline), `detect_format(raw_content)`, `update_health(court_code, success, confidence)`
    - Define ScrapeResult dataclass with: structured, raw_data, confidence, parse_errors, extra_fields, source_url, source_page
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.6, 9.7_

  - [x] 14.2 Implement scraper registry/factory
    - Create `backend/app/scrapers/registry.py` with ScraperFactory class
    - Map scraper_key values to scraper classes (aft_delhi → AftDelhiScraper, etc.)
    - Implement `get_scraper(scraper_key)` factory method
    - Implement fallback to generic parser when no specific scraper exists
    - _Requirements: 9.4, 9.5_

  - [x] 14.3 Implement scraper health update logic
    - In BaseScraper.update_health(): on success → reset consecutive_failures to 0, update last_success_at, update avg_parse_confidence (rolling average)
    - On failure → increment consecutive_failures, update last_failure_at, store error details
    - When consecutive_failures >= failure_threshold → set is_healthy=false
    - _Requirements: 10.1, 10.2, 10.3, 10.5_

  - [ ]* 14.4 Write property tests for Scraper (Properties 17-21)
    - **Property 17: Scraper Data Preservation** — both structured and raw data stored
    - **Property 18: Parse Confidence Bounds** — confidence in [0.0, 1.0], warning logged when < 0.7
    - **Property 19: Scrape Logging Completeness** — every scrape has a scrape_log record
    - **Property 20: Scraper Health State Machine** — success resets failures, failure increments, threshold triggers unhealthy
    - **Property 21: Rolling Average Confidence** — avg equals arithmetic mean of scores
    - Create `backend/tests/properties/test_props_scraper.py`
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.6, 9.7, 10.1, 10.2, 10.3, 10.5**

- [x] 15. Scraper implementations - Court-specific parsers
  - [x] 15.1 Implement AFT Delhi scraper
    - Create `backend/app/scrapers/aft_delhi.py` extending BaseScraper
    - Implement PDF fetching from AFT Delhi cause list URL
    - Implement parsing logic for AFT Delhi PDF format (table-based cause list)
    - Extract: case_number, case_title, petitioner, respondent, advocate_petitioner, bench, item_number, next_hearing_date
    - Calculate parse_confidence based on fields successfully extracted
    - _Requirements: 9.1, 9.2, 9.3_

  - [x] 15.2 Implement generic AFT and CAT scrapers
    - Create `backend/app/scrapers/aft_generic.py` for other AFT benches (Mumbai, Chennai, Kolkata, etc.)
    - Create `backend/app/scrapers/cat_delhi.py` for CAT Delhi
    - Create `backend/app/scrapers/cat_generic.py` for other CAT benches
    - Each extends BaseScraper with court-specific PDF parsing logic
    - _Requirements: 9.1, 9.4_

  - [x] 15.3 Implement fallback generic parser
    - Create `backend/app/scrapers/fallback.py` extending BaseScraper
    - Attempt generic PDF text extraction using pdfplumber
    - Use regex patterns to extract common fields (case number, parties, dates)
    - Set lower parse_confidence (0.3-0.5) for fallback results
    - Flag result for admin review when fallback is used
    - _Requirements: 9.5, 9.6_

- [x] 16. Checkpoint - Verify scrapers and background jobs
  - Ensure scraper framework loads all parsers, health tracking works, background scheduler starts and stops cleanly. Ask the user if questions arise.

- [x] 17. Integration tests and test configuration
  - [x] 17.1 Set up test configuration and fixtures
    - Create `backend/tests/conftest.py` with pytest fixtures: test app, test client, test database session, authenticated user fixture, sample court/case data
    - Configure test database (separate from production)
    - Create fixture for mocking external services (Razorpay, court PDFs, email/SMS)
    - _Requirements: All_

  - [ ]* 17.2 Write integration tests for auth flow
    - Test full flow: register → request OTP → verify OTP → get JWT → access protected endpoint → logout
    - Test OTP expiry and max attempts
    - Test duplicate registration rejection
    - Create `backend/tests/integration/test_auth_flow.py`
    - _Requirements: 1, 2_

  - [ ]* 17.3 Write integration tests for case search and tracking
    - Test cache miss → scrape → cache hit flow
    - Test tracking add/remove with tier limits
    - Test rate limiting across multiple requests
    - Create `backend/tests/integration/test_cases_flow.py`
    - _Requirements: 3, 4, 5_

  - [ ]* 17.4 Write integration tests for subscriptions and webhooks
    - Test create order → mock Razorpay webhook → tier upgrade
    - Test payment failure → tier unchanged
    - Test subscription expiry → downgrade to free
    - Create `backend/tests/integration/test_subscription_flow.py`
    - _Requirements: 11_

- [x] 18. Final wiring and deployment configuration
  - [x] 18.1 Wire all components in app factory
    - Ensure `create_app()` initializes all extensions, registers all blueprints, sets up error handlers, configures CORS, and optionally starts scheduler
    - Add health check endpoint `GET /api/health` returning app status
    - Verify the complete app starts and all routes are registered
    - _Requirements: 13, 14_

  - [x] 18.2 Create deployment configuration files
    - Create `backend/Dockerfile` for containerized deployment
    - Create `backend/docker-compose.yml` with app + PostgreSQL + Redis services
    - Create `backend/gunicorn.conf.py` for production WSGI server
    - _Requirements: All (deployment support)_

- [x] 19. Final checkpoint - Full system verification
  - Ensure all tests pass, the app starts cleanly, all endpoints respond correctly, CORS works, and the scheduler runs. Ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties (29 total across 7 test files)
- The PostgreSQL database already exists — models only map to existing tables, no migrations needed
- External services (Razorpay, email, SMS) should be mocked in tests
- Court-specific scrapers (task 15) can be expanded incrementally as new courts are onboarded
