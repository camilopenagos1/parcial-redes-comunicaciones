
CREATE TABLE IF NOT EXISTS nginx_requests (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    client_ip TEXT NOT NULL,
    method TEXT NOT NULL,
    path TEXT NOT NULL,
    status INTEGER NOT NULL,
    bytes_sent BIGINT NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_nginx_requests_ts
    ON nginx_requests (ts);

CREATE INDEX IF NOT EXISTS idx_nginx_requests_status
    ON nginx_requests (status);