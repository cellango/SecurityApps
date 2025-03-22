import React, { useState } from 'react';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Paper,
  Alert,
  CircularProgress
} from '@mui/material';
import api from '../utils/api';
import Layout from './Layout';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post('/auth/login', { username, password });
      const { access_token } = response.data;
      
      // Store the token
      localStorage.setItem('token', access_token);
      
      // Call onLogin with the response data
      onLogin(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to login. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <Container 
        maxWidth={false} 
        sx={{ 
          display: 'flex', 
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          bgcolor: 'background.default',
          p: 2
        }}
      >
        <Paper 
          elevation={3} 
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            maxWidth: 400,
            width: '100%'
          }}
        >
          <img
            src={`${process.env.PUBLIC_URL}/logo192.png`}
            alt="AppInventory Logo"
            style={{
              width: 'auto',
              height: '80px',
              marginBottom: '24px'
            }}
          />
          
          <Typography component="h1" variant="h5" gutterBottom>
            Welcome to AppInventory
          </Typography>
          
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 3 }}>
            Sign in to manage your applications
          </Typography>

          {error && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={loading}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2, py: 1.5 }}
              disabled={loading}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Sign In'
              )}
            </Button>
          </Box>
        </Paper>
      </Container>
    </Layout>
  );
}
