import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api, { setAuthToken } from '../services/api';

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Check if user is already logged in
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    console.log('[Login] Checking existing token:', !!token);
    if (token) {
      console.log('[Login] User already logged in, redirecting to /select');
      navigate('/select');
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Attempting login with:', { username, password: '********' });
      
      const response = await api.post('/api/auth/login', {
        username,
        password
      });

      console.log('[Login] Login response:', {
        status: response.status,
        hasAccessToken: !!response.data.access_token,
        hasRefreshToken: !!response.data.refresh_token,
        hasUser: !!response.data.user
      });
      
      const { access_token, refresh_token, user } = response.data;
      
      // Set up authentication
      console.log('[Login] Setting up authentication...');
      console.log('[Login] Access token:', access_token.substring(0, 20) + '...');
      
      // Store tokens and user data in localStorage
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      localStorage.setItem('user', JSON.stringify(user));
      
      // Set the Authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Verify everything is set up correctly
      console.log('[Login] Verifying setup:', {
        localStorage: {
          access_token: localStorage.getItem('access_token')?.substring(0, 20) + '...',
          refresh_token: localStorage.getItem('refresh_token')?.substring(0, 20) + '...',
          hasUser: !!localStorage.getItem('user')
        },
        apiHeaders: {
          authorization: api.defaults.headers.common['Authorization']?.substring(0, 30) + '...'
        }
      });

      // Validate token immediately
      console.log('[Login] Validating token...');
      try {
        const validationResponse = await api.post('/api/auth/validate');
        console.log('[Login] Token validation response:', validationResponse.data);
        
        if (validationResponse.data.valid) {
          console.log('[Login] Token is valid, navigating to /select');
          navigate('/select', { replace: true });
        } else {
          console.error('[Login] Token validation failed:', validationResponse.data);
          setError('Authentication failed. Please try again.');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          delete api.defaults.headers.common['Authorization'];
        }
      } catch (validationError) {
        console.error('[Login] Token validation error:', validationError);
        setError('Authentication failed. Please try again.');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        delete api.defaults.headers.common['Authorization'];
      }
      
    } catch (err) {
      console.error('[Login] Login error:', err);
      setError(
        err.response?.data?.message || 
        'Login failed. Please check your credentials and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 4,
            width: '100%',
            maxWidth: 400,
            textAlign: 'center'
          }}
        >
          <Typography variant="h4" component="h1" gutterBottom>
            Security Score Card
          </Typography>
          
          <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 4 }}>
            Sign in to access your security dashboard
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Username"
              variant="outlined"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={loading}
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Password"
              type="password"
              variant="outlined"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              sx={{ mb: 3 }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              disabled={loading}
              sx={{ py: 1.5 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Sign In'}
            </Button>
          </form>
        </Paper>
      </Box>
    </Container>
  );
}

export default Login;
