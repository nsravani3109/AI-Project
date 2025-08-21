-- Migration script to add session_id column to negotiations table
-- Run this in SQLite to update existing database structure

-- Add session_id column to negotiations table
ALTER TABLE negotiations ADD COLUMN session_id TEXT;

-- Create index on session_id for better performance
CREATE INDEX IF NOT EXISTS idx_negotiations_session_id ON negotiations(session_id);

-- Create index on call_id + session_id combination for efficient queries
CREATE INDEX IF NOT EXISTS idx_negotiations_call_session ON negotiations(call_id, session_id);

-- Verify the change
.schema negotiations

-- Show sample data structure
SELECT 'Migration completed successfully!' as message;
