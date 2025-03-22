#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up local development environment...${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    
    # Generate random secret keys
    SECRET_KEY=$(openssl rand -hex 32)
    JWT_SECRET_KEY=$(openssl rand -hex 32)
    
    # Update secrets in .env file
    sed -i '' "s/your-secret-key-here/$SECRET_KEY/" .env
    sed -i '' "s/your-jwt-secret-key/$JWT_SECRET_KEY/" .env
    
    echo -e "${GREEN}Created .env file with secure random keys${NC}"
else
    echo -e "${YELLOW}.env file already exists, skipping...${NC}"
fi

# Create Python virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Created virtual environment${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists, skipping...${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r backend/requirements.txt
pip install -r tests/requirements-test.txt

# Install Node.js dependencies
echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
cd frontend
npm install
cd ..

# Setup database
echo -e "${YELLOW}Setting up database...${NC}"
if ! psql -lqt | cut -d \| -f 1 | grep -qw appsentinel; then
    echo -e "${YELLOW}Creating database...${NC}"
    createdb appsentinel
    echo -e "${GREEN}Database created${NC}"
else
    echo -e "${YELLOW}Database already exists, skipping...${NC}"
fi

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
cd backend
flask db upgrade

# Seed database with sample data (if available)
if [ -f "seed_data.py" ]; then
    echo -e "${YELLOW}Seeding database with sample data...${NC}"
    python seed_data.py
fi

echo -e "${GREEN}Local development environment setup complete!${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Review and update .env file with your local settings"
echo "2. Start the backend server: cd backend && flask run"
echo "3. Start the frontend server: cd frontend && npm start"
echo -e "\n${YELLOW}Happy coding!${NC}"
