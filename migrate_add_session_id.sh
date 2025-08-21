#!/bin/bash

# Migration script to add session_id to negotiations table
# Usage: ./migrate_add_session_id.sh [database_file]

# Set database file (default to loads.db)
DB_FILE=${1:-loads.db}

echo "Running migration: Add session_id to negotiations table"
echo "Database: $DB_FILE"
echo "======================================================="

# Check if database file exists
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file '$DB_FILE' not found!"
    echo "Please make sure the database exists."
    exit 1
fi

# Create backup
BACKUP_FILE="${DB_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
echo "Creating backup: $BACKUP_FILE"
cp "$DB_FILE" "$BACKUP_FILE"

# Run migration
echo "Running migration..."
sqlite3 "$DB_FILE" < migrations/add_session_id_to_negotiations.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Migration completed successfully!"
    echo ""
    echo "Changes made:"
    echo "- Added session_id column to negotiations table"
    echo "- Created indexes for better performance"
    echo ""
    echo "Backup created at: $BACKUP_FILE"
    echo ""
    
    # Show updated table structure
    echo "Updated table structure:"
    echo "======================="
    sqlite3 "$DB_FILE" ".schema negotiations"
else
    echo ""
    echo "❌ Migration failed!"
    echo "Restoring from backup..."
    cp "$BACKUP_FILE" "$DB_FILE"
    echo "Database restored from backup."
    exit 1
fi
