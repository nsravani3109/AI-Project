#!/bin/bash

# Script to populate the Inbound Sales AI Agent database with sample data
# Usage: ./populate_database.sh [database_file]

# Set database file (default to load_management.db)
DB_FILE=${1:-load_management.db}

echo "Populating database: $DB_FILE"
echo "================================"

# Check if database file exists
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file '$DB_FILE' not found!"
    echo "Please run the application first to create the database tables."
    exit 1
fi

# Run the SQL scripts in order
echo "1. Inserting carriers data..."
sqlite3 "$DB_FILE" < data/carriers_data.sql

echo "2. Inserting loads data..."
sqlite3 "$DB_FILE" < data/loads_data.sql

echo "3. Inserting calls data..."
sqlite3 "$DB_FILE" < data/calls_data.sql

echo "4. Inserting negotiations data..."
sqlite3 "$DB_FILE" < data/negotiations_data.sql

echo ""
echo "Database population completed!"
echo ""

# Show summary of inserted data
echo "Data Summary:"
echo "============="
sqlite3 "$DB_FILE" "SELECT 'Carriers: ' || COUNT(*) FROM carriers;"
sqlite3 "$DB_FILE" "SELECT 'Loads: ' || COUNT(*) FROM loads;"
sqlite3 "$DB_FILE" "SELECT 'Calls: ' || COUNT(*) FROM calls;"
sqlite3 "$DB_FILE" "SELECT 'Negotiations: ' || COUNT(*) FROM negotiations;"

echo ""
echo "You can now test the API endpoints with this sample data!"
echo "Example queries:"
echo "- GET /api/loads (view all loads)"
echo "- GET /api/carriers (view all carriers)" 
echo "- GET /api/calls (view all calls)"
echo "- GET /api/metrics/dashboard (view dashboard metrics)"
