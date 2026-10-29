-- Keep table and column order compatible with the original local databases.
CREATE TABLE IF NOT EXISTS inbox (
    key TEXT PRIMARY KEY,
    cid TEXT NOT NULL,
    body TEXT NOT NULL,
    received REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS threads (
    cid TEXT PRIMARY KEY,
    thread_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drafts (
    id TEXT PRIMARY KEY,
    message_key TEXT NOT NULL,
    summary TEXT NOT NULL,
    text TEXT NOT NULL,
    thread_id TEXT,
    status TEXT NOT NULL,
    version INTEGER NOT NULL,
    idem TEXT NOT NULL,
    receipt TEXT,
    created REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS handled (
    message_key TEXT PRIMARY KEY,
    updated REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS todos (
    id TEXT PRIMARY KEY,
    message_key TEXT NOT NULL,
    title TEXT NOT NULL,
    evidence TEXT NOT NULL,
    status TEXT NOT NULL,
    task_id TEXT,
    receipt TEXT,
    created REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    body TEXT NOT NULL
);
