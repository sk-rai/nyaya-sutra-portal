# Requirements Document

## Introduction

This document defines the requirements for the Nyaya Sutra Legal Portal Backend API — a Flask-based REST API that serves the existing frontend (11 HTML pages deployed on GitHub Pages). The backend provides user authentication, case search with on-demand scraping and smart caching, tier-based access control, subscription management via Razorpay, background case refresh jobs, and scraper health monitoring. The system connects to an existing PostgreSQL database (12 tables already created) and must handle court PDF scraping with anti-fragile design patterns.

## Glossary

- **API_Server**: The Flask-based backend application that exposes REST endpoints and handles all business logic
- **Auth_Service**: The module responsible for OTP generation, verification, JWT issuance, and session management
- **Case_Cache_Service**: The module responsible for checking the case_cache table, returning cached data, or triggering a scrape on cache miss
- **Scraper_Framework**: The pluggable scraper system that fetches and parses court PDFs, producing structured data with confidence scores
- **Rate_Limiter**: The middleware that enforces per-tier search and API call limits
- **Refresh_Scheduler**: The background job system that periodically refreshes tracked cases and purges stale cache
- **Payment_Service**: The module that integrates with Razorpay for subscription creation, verification, and webhook handling
- **Court_Registry**: The reference data service that provides the list of supported courts and their metadata
- **User**: A registered person (individual or advocate) who interacts with the portal
- **Tier**: The subscription level of a user (free, individual, advocate_normal, advocate_premium) that determines access limits
- **Tracked_Case**: A case that a user has added to their "My Cases" list, which persists and is auto-refreshed
- **Cache_Hit**: When a requested case already exists in the case_cache table and is fresh enough to return directly
- **Cache_Miss**: When a requested case does not exist in case_cache, requiring an on-demand scrape from the court source
- **Parse_Confidence**: A float (0.0–1.0) indicating how reliably the scraper extracted structured data from a PDF
- **OTP**: One-Time Password sent via email or SMS for passwordless authentication
- **JWT**: JSON Web Token used for stateless session authentication after OTP verification

## Requirements

### Requirement 1: User Authentication via OTP

**User Story:** As a user, I want to log in using an OTP sent to my email or phone, so that I can securely access the portal without remembering a password.

#### Acceptance Criteria

1. WHEN a user submits their email or phone number, THE Auth_Service SHALL generate a 6-digit OTP, hash it, store it in the otp_tokens table with a 10-minute expiry, and dispatch it to the user via the configured channel
2. WHEN a user submits a valid OTP within the expiry window, THE Auth_Service SHALL issue a JWT token, create a record in user_sessions, and return the token to the client
3. IF an OTP verification attempt exceeds 3 failed tries, THEN THE Auth_Service SHALL invalidate the OTP token and require the user to request a new one
4. IF an expired or already-used OTP is submitted, THEN THE Auth_Service SHALL return an error indicating the OTP is no longer valid
5. WHEN a user requests a logout, THE Auth_Service SHALL revoke the session by setting revoked_at on the user_sessions record

### Requirement 2: User Registration with Tier Selection

**User Story:** As a new user, I want to register with my details and select a subscription plan, so that I can start tracking cases according to my chosen tier.

#### Acceptance Criteria

1. WHEN a user submits registration details (name, email, phone, user_type), THE API_Server SHALL create a new user record with tier set to "free" and is_verified set to false
2. WHEN a user completes OTP verification during registration, THE Auth_Service SHALL set is_verified to true on the user record
3. WHEN an advocate registers, THE API_Server SHALL accept and store enrollment_no, enrollment_date, and bar_council fields
4. IF a registration request contains an email or phone already in use, THEN THE API_Server SHALL return an error indicating the identifier is already registered
5. THE API_Server SHALL validate that email follows a valid format and phone is a 10-digit Indian mobile number

### Requirement 3: Case Search with On-Demand Caching

**User Story:** As a user, I want to search for a case by selecting a court and entering a case number, so that I can view case details fetched from the court source.

#### Acceptance Criteria

1. WHEN a user searches for a case that exists in case_cache and was fetched within 24 hours, THE Case_Cache_Service SHALL return the cached data and update last_accessed_at
2. WHEN a user searches for a case that does not exist in case_cache, THE Case_Cache_Service SHALL trigger the Scraper_Framework to fetch the case from the court source, store the result in case_cache, and return it to the user
3. WHEN a user searches for a case that exists in cache but is older than 24 hours and untracked, THE Case_Cache_Service SHALL trigger a re-scrape, update the cache, and return fresh data
4. THE Case_Cache_Service SHALL return both structured fields and a freshness indicator (fresh, recent, stale) based on the fetched_at timestamp
5. IF the Scraper_Framework fails to fetch or parse the case, THEN THE Case_Cache_Service SHALL return an error with the court source URL so the user can check manually
6. WHEN a case is fetched from cache, THE Case_Cache_Service SHALL call the touch_case function to update last_accessed_at

### Requirement 4: Tier-Based Rate Limiting

**User Story:** As a platform operator, I want to enforce search and tracking limits per subscription tier, so that the system remains sustainable and premium users get better service.

#### Acceptance Criteria

1. THE Rate_Limiter SHALL enforce the following daily search limits: free=10, individual=50, advocate_normal=200, advocate_premium=unlimited
2. WHEN a user exceeds their daily search limit, THE Rate_Limiter SHALL return a 429 status with a message indicating the limit and time until reset
3. THE Rate_Limiter SHALL track search counts per user per calendar day (IST timezone) and reset at midnight IST
4. WHILE a user has an active JWT session, THE Rate_Limiter SHALL identify the user's tier from the token claims to apply the correct limits

### Requirement 5: Case Tracking Management

**User Story:** As a user, I want to add and remove cases from my tracked list, so that I receive automatic updates on cases I care about.

#### Acceptance Criteria

1. WHEN a user adds a case to their tracked list, THE API_Server SHALL create a record in user_tracked_cases and update the case_cache tracked_by_count via the database trigger
2. WHEN a user attempts to add a case beyond their tier limit, THE API_Server SHALL return an error indicating the maximum tracked cases for their tier (free=5, individual=50, advocate_normal=300, advocate_premium=2000)
3. WHEN a user removes a case from their tracked list, THE API_Server SHALL delete the user_tracked_cases record and decrement tracked_by_count via the database trigger
4. THE API_Server SHALL provide an endpoint to list all tracked cases for a user, including case details, next hearing date, and freshness indicator
5. WHEN a user adds a case to tracking, THE API_Server SHALL accept optional alert preferences (email, SMS, WhatsApp)

### Requirement 6: Court Listing API

**User Story:** As a user, I want to see the list of supported courts, so that I can select the correct court when searching for a case.

#### Acceptance Criteria

1. THE API_Server SHALL provide an endpoint that returns all active courts from the courts table, including code, name, short_name, court_type, state, and city
2. WHEN a court_type filter parameter is provided, THE API_Server SHALL return only courts matching that type (sc, hc, aft, cat, appellate)
3. THE Court_Registry SHALL return courts sorted by court_type and then alphabetically by short_name

### Requirement 7: Background Case Refresh

**User Story:** As a user with tracked cases, I want my cases to be automatically refreshed in the background, so that I always see up-to-date hearing information.

#### Acceptance Criteria

1. THE Refresh_Scheduler SHALL run periodically and invoke get_cases_needing_refresh to identify cases due for re-scraping (12 hours for advocate_premium users, 24 hours for all other tiers)
2. WHEN a tracked case is refreshed, THE Refresh_Scheduler SHALL update the case_cache record with new data, increment refresh_count, and set last_refreshed_at to the current timestamp
3. IF a background refresh fails for a case, THEN THE Refresh_Scheduler SHALL log the failure in scrape_log and increment consecutive_failures in scraper_registry without removing the existing cached data
4. THE Refresh_Scheduler SHALL process cases in batches to avoid overwhelming court servers, with a configurable delay between requests

### Requirement 8: Cache Cleanup

**User Story:** As a platform operator, I want stale untracked cases to be automatically purged, so that storage remains lightweight.

#### Acceptance Criteria

1. THE Refresh_Scheduler SHALL invoke the purge_stale_cache function every 6 hours to remove untracked cases older than 48 hours or inactive for 24 hours
2. THE purge_stale_cache function SHALL delete associated case_hearings records before deleting case_cache records
3. THE purge_stale_cache function SHALL also remove expired OTP tokens and expired or revoked user sessions
4. THE Refresh_Scheduler SHALL log the count of purged records for monitoring purposes

### Requirement 9: Scraper Framework with Anti-Fragile Design

**User Story:** As a platform operator, I want a pluggable scraper system that gracefully handles PDF format changes, so that the system remains operational even when courts change their document formats.

#### Acceptance Criteria

1. THE Scraper_Framework SHALL store both structured parsed data and raw scraped content (in raw_scraped_data JSONB field) for every scrape operation
2. THE Scraper_Framework SHALL produce a parse_confidence score (0.0–1.0) for each scrape, reflecting how many expected fields were successfully extracted
3. WHEN parse_confidence falls below 0.7, THE Scraper_Framework SHALL store the result with a low-confidence flag and log a warning in scrape_log
4. THE Scraper_Framework SHALL support pluggable parser modules keyed by court scraper_key, allowing new court parsers to be added without modifying existing code
5. WHEN a PDF does not match any known format signature in pdf_format_signatures, THE Scraper_Framework SHALL attempt a fallback generic parser and flag the result for admin review
6. THE Scraper_Framework SHALL store any fields not matching the structured schema in the extra_fields JSONB column
7. THE Scraper_Framework SHALL record every scrape operation in the scrape_log table with timing, status, and confidence metrics

### Requirement 10: Scraper Health Monitoring

**User Story:** As a platform operator, I want to monitor scraper health per court, so that I can detect and respond to PDF format changes quickly.

#### Acceptance Criteria

1. WHEN a scraper succeeds, THE Scraper_Framework SHALL reset consecutive_failures to 0 and update last_success_at in scraper_registry
2. WHEN a scraper fails, THE Scraper_Framework SHALL increment consecutive_failures, update last_failure_at, and store the error details in scraper_registry
3. WHEN consecutive_failures reaches the failure_threshold, THE Scraper_Framework SHALL set is_healthy to false in scraper_registry
4. THE API_Server SHALL provide an admin endpoint that returns the output of check_scraper_health() for monitoring dashboards
5. THE Scraper_Framework SHALL update avg_parse_confidence as a rolling average in scraper_registry after each successful scrape

### Requirement 11: Subscription and Payment Integration

**User Story:** As a user, I want to subscribe to a paid plan via Razorpay, so that I can unlock higher case tracking limits and premium features.

#### Acceptance Criteria

1. WHEN a user initiates a subscription, THE Payment_Service SHALL create a Razorpay order with the correct amount (individual=5000 paise, advocate_normal=19900 paise, advocate_premium=59900 paise) and return the order details to the client
2. WHEN Razorpay sends a payment success webhook, THE Payment_Service SHALL verify the signature, create a subscription record, and update the user's tier
3. IF Razorpay sends a payment failure webhook, THEN THE Payment_Service SHALL log the failure and keep the user's current tier unchanged
4. WHEN a subscription expires, THE Payment_Service SHALL downgrade the user's tier to "free" and enforce the free-tier limits on subsequent requests
5. THE Payment_Service SHALL store gateway_subscription_id and gateway_payment_id in the subscriptions table for reconciliation

### Requirement 12: Case Relationships and Cross-Court Linkages

**User Story:** As a user tracking a case across multiple courts (e.g., AFT order appealed at High Court), I want to link related cases, so that I can see the full litigation history in one place.

#### Acceptance Criteria

1. WHEN a user links two cases, THE API_Server SHALL create a record in case_relationships with the specified relationship_type and detected_by set to "user" with confidence 1.0
2. THE API_Server SHALL support the following relationship types: appeal_of, writ_against, slp_against, transfer_from, connected_with, contempt_of
3. WHEN a user views a case, THE API_Server SHALL return all related cases from case_relationships (both directions: case_id and related_case_id)
4. THE API_Server SHALL prevent duplicate relationships (same case_id, related_case_id, and relationship_type combination)

### Requirement 13: CORS and Frontend Integration

**User Story:** As a frontend developer, I want the backend API to support cross-origin requests from GitHub Pages, so that the deployed frontend can communicate with the backend.

#### Acceptance Criteria

1. THE API_Server SHALL include CORS headers allowing requests from the GitHub Pages domain (https://sk-rai.github.io)
2. THE API_Server SHALL support preflight OPTIONS requests for all API endpoints
3. THE API_Server SHALL allow the Authorization header in CORS configuration for JWT-based authentication
4. THE API_Server SHALL return JSON responses with appropriate Content-Type headers for all API endpoints

### Requirement 14: API Error Handling and Response Format

**User Story:** As a frontend developer, I want consistent error responses from the API, so that I can handle errors uniformly in the client application.

#### Acceptance Criteria

1. THE API_Server SHALL return all responses in a consistent JSON envelope format containing "success" (boolean), "data" (object or null), and "error" (object or null with "code" and "message" fields)
2. WHEN an authentication error occurs, THE API_Server SHALL return HTTP 401 with an appropriate error code
3. WHEN a rate limit is exceeded, THE API_Server SHALL return HTTP 429 with the reset time in the response
4. WHEN a validation error occurs, THE API_Server SHALL return HTTP 400 with field-level error details
5. IF an unexpected server error occurs, THEN THE API_Server SHALL return HTTP 500 with a generic message and log the full error details server-side without exposing internals to the client

### Requirement 15: Synopsis Access for Premium Users

**User Story:** As an advocate premium subscriber, I want to access case synopsis (AI-generated summaries of judgments), so that I can quickly understand case outcomes without reading full orders.

#### Acceptance Criteria

1. WHILE a user has the advocate_premium tier, THE API_Server SHALL allow access to the synopsis endpoint for any case
2. WHEN a non-premium user requests a synopsis, THE API_Server SHALL return HTTP 403 with a message indicating this feature requires the advocate_premium subscription
3. THE API_Server SHALL return synopsis data as a PDF-compatible response with print permission metadata based on the user's tier
