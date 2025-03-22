-- Create users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    oauth_provider VARCHAR(20),
    oauth_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert admin user with password hash for 'admin123'
INSERT INTO users (
    username,
    email,
    password_hash,
    first_name,
    last_name,
    role,
    is_active,
    created_at,
    updated_at
) VALUES (
    'admin',
    'admin@appsentinel.com',
    'pbkdf2:sha256:260000$gEMqxHLJ$4cb059492f6796dd50fe0d5faa6684011af8915b46ab995cdf3c9b9f0d39558d',
    'Admin',
    'User',
    'admin',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) ON CONFLICT (username) DO NOTHING;
