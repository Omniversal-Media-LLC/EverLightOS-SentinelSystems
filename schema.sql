-- 🔥 THE ONE RING DATABASE SCHEMA 🔥
-- D1 Database: federation-logs

-- Knowledge Base for AutoRAG
CREATE TABLE knowledge_base (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  source TEXT,
  tags TEXT, -- JSON array
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- AI Conversations Log
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  model TEXT NOT NULL,
  prompt TEXT NOT NULL,
  response TEXT NOT NULL,
  session_id TEXT,
  context TEXT, -- JSON context for conversation continuity
  metadata TEXT -- JSON for additional data
);

-- Search Query Logs
CREATE TABLE search_logs (
  id TEXT PRIMARY KEY,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  query TEXT NOT NULL,
  results_count INTEGER,
  ai_response TEXT,
  session_id TEXT,
  response_time_ms INTEGER
);

-- Federation Experiments (Multi-AI Consensus)
CREATE TABLE federation_experiments (
  id TEXT PRIMARY KEY,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  query TEXT NOT NULL,
  models TEXT NOT NULL, -- JSON array of models used
  responses TEXT NOT NULL, -- JSON array of responses
  consensus TEXT, -- Final consensus response
  experiment_type TEXT,
  success BOOLEAN DEFAULT TRUE
);

-- User Sessions (for KV cache reference)
CREATE TABLE user_sessions (
  session_id TEXT PRIMARY KEY,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
  preferences TEXT, -- JSON user preferences
  conversation_count INTEGER DEFAULT 0
);

-- Guardian AI Monitoring Logs
CREATE TABLE guardian_logs (
  id TEXT PRIMARY KEY,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  event_type TEXT NOT NULL, -- 'policy_check', 'anomaly_detected', etc.
  severity TEXT NOT NULL, -- 'info', 'warning', 'critical'
  message TEXT NOT NULL,
  metadata TEXT, -- JSON additional context
  resolved BOOLEAN DEFAULT FALSE
);

-- Content Ingestion Tracking
CREATE TABLE ingestion_jobs (
  id TEXT PRIMARY KEY,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  source_type TEXT NOT NULL, -- 'github', 'manual', 'api'
  source_url TEXT,
  items_processed INTEGER DEFAULT 0,
  items_failed INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
  error_message TEXT
);

-- Indexes for performance
CREATE INDEX idx_knowledge_base_source ON knowledge_base(source);
CREATE INDEX idx_knowledge_base_created ON knowledge_base(created_at);
CREATE INDEX idx_conversations_session ON conversations(session_id);
CREATE INDEX idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX idx_search_logs_timestamp ON search_logs(timestamp);
CREATE INDEX idx_federation_experiments_timestamp ON federation_experiments(timestamp);
CREATE INDEX idx_guardian_logs_severity ON guardian_logs(severity);
CREATE INDEX idx_guardian_logs_timestamp ON guardian_logs(timestamp);