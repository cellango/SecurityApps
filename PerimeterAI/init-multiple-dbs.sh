#!/bin/bash

set -e
set -u

function create_database() {
    local database=$1
    echo "Creating database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL
}

function create_keyboard_dynamics_tables() {
    echo "Creating keyboard dynamics tables in perimeterai database"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d perimeterai <<-EOSQL
        CREATE TABLE IF NOT EXISTS keyboard_dynamics_profiles (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            typing_pattern JSONB NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS keyboard_dynamics_sessions (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            session_data JSONB NOT NULL,
            risk_score FLOAT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_keyboard_dynamics_profiles_user_id ON keyboard_dynamics_profiles(user_id);
        CREATE INDEX IF NOT EXISTS idx_keyboard_dynamics_sessions_user_id ON keyboard_dynamics_sessions(user_id);
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        create_database $db
    done
    echo "Multiple databases created"
    
    # Create keyboard dynamics tables in perimeterai database
    create_keyboard_dynamics_tables
fi
