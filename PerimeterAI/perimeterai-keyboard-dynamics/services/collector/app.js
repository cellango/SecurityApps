const express = require('express');
const Redis = require('redis');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const redisClient = Redis.createClient(process.env.REDIS_URL);

app.post('/collect', async (req, res) => {
    try {
        const { userId, typingData } = req.body;
        
        // Forward the data to analytics service
        const response = await axios.post(process.env.ANALYTICS_SERVICE_URL + '/analyze', {
            userId,
            typingData
        });

        res.json(response.data);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Collector service listening on port ${port}`);
});
