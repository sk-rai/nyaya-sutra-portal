-- Track uploaded cause list files to prevent duplicate processing
CREATE TABLE IF NOT EXISTS upload_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_hash VARCHAR(64) NOT NULL UNIQUE,  -- SHA256 hash of file content
    filename VARCHAR(255) NOT NULL,
    court_code VARCHAR(30) NOT NULL REFERENCES courts(code),
    hearing_date DATE,
    file_size_bytes INTEGER,
    cases_parsed INTEGER DEFAULT 0,
    cases_new INTEGER DEFAULT 0,
    cases_updated INTEGER DEFAULT 0,
    uploaded_by UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'success',  -- success, failed, duplicate
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_upload_log_hash ON upload_log(file_hash);
CREATE INDEX IF NOT EXISTS idx_upload_log_court ON upload_log(court_code);
