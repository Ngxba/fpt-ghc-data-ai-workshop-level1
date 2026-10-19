-- Instructor-managed DDL reference. Students inspect but DO NOT run CREATE TABLE.
-- The extension is provisioned as extensions.vector(1536).
CREATE SCHEMA IF NOT EXISTS shared;
CREATE TABLE shared.ticket_types (
    ticket_type TEXT PRIMARY KEY,
    notes TEXT NOT NULL DEFAULT ''
);
CREATE TABLE shared.raw_tickets (
    ticket_id INTEGER PRIMARY KEY,
    ticket_type TEXT,
    ticket_subject TEXT,
    ticket_description TEXT,
    status TEXT,
    priority TEXT,
    channel TEXT,
    product TEXT,
    first_response_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    satisfaction_rating NUMERIC(4,2),
    resolution_text TEXT
);
CREATE TABLE shared.knowledge_articles (
    article_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding extensions.vector(1536) NOT NULL
);
-- Repeat for team_01, team_02, etc. with separate roles.
CREATE TABLE team_01.clean_tickets (
    ticket_id INTEGER PRIMARY KEY,
    ticket_type TEXT NOT NULL REFERENCES shared.ticket_types(ticket_type),
    ticket_subject TEXT,
    status TEXT NOT NULL,
    priority TEXT,
    channel TEXT,
    product TEXT,
    first_response_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    satisfaction_rating NUMERIC(4,2),
    response_to_resolution_hours NUMERIC(12,2),
    CHECK (response_to_resolution_hours IS NULL OR response_to_resolution_hours >= 0)
);
CREATE TABLE team_01.knowledge_articles (
    article_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding extensions.vector(1536) NOT NULL
);
