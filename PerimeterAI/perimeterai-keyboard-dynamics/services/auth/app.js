const express = require('express');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
const Redis = require('redis');
require('dotenv').config();

const app = express();
app.use(express.json());

const pool = new Pool({
    connectionString: process.env.DATABASE_URL
});

const redisClient = Redis.createClient(process.env.REDIS_URL);

app.post('/auth/verify', async (req, res) => {
    try {
        const { token, typingPattern } = req.body;
        // Add your authentication verification logic here
        res.json({ status: 'success', verified: true });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Auth service listening on port ${port}`);
});
