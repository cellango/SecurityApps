-- Initial database schema

-- Teams table
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    team_id INTEGER REFERENCES teams(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Applications table
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255),
    team_id INTEGER REFERENCES teams(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Score History table
CREATE TABLE IF NOT EXISTS score_history (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    score FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ML Model Versions table
CREATE TABLE IF NOT EXISTS ml_model_versions (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL,
    model_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Findings table
CREATE TABLE IF NOT EXISTS findings (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    finding_type VARCHAR(100) NOT NULL,
    description TEXT,
    severity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk Parameters table
CREATE TABLE IF NOT EXISTS risk_parameters (
    id SERIAL PRIMARY KEY,
    parameter_name VARCHAR(100) NOT NULL,
    weight FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
