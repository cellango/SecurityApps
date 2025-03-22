/**
 * Security Score Card - Frontend Application
 * 
 * A comprehensive security scoring and monitoring system for applications.
 * 
 * @authors Clement Ellango, Carolina Clement
 * @copyright Copyright (c) 2024. All rights reserved.
 */

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './components/Navbar';
import ApplicationRiskSearch from './components/ApplicationRiskSearch';
import ApplicationList from './components/ApplicationList';
import SecurityDashboard from './components/SecurityDashboard';
import Login from './components/Login';
import SelectView from './components/SelectView';
import TeamList from './components/TeamList';
import TeamApplications from './components/TeamApplications';
import ApplicationDetails from './components/ApplicationDetails';
import api from './services/api';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});

function PrivateRoute({ children }) {
  const [isValidating, setIsValidating] = useState(true);
  const [isValid, setIsValid] = useState(false);
  const navigate = useNavigate();
  
  useEffect(() => {
    const validateToken = async () => {
      try {
        console.log('[PrivateRoute] Starting token validation...');
        const token = localStorage.getItem('access_token');
        
        if (!token) {
          console.log('[PrivateRoute] No token in localStorage, redirecting to login');
          setIsValidating(false);
          navigate('/login');
          return;
        }

        console.log('[PrivateRoute] Found token:', token.substring(0, 20) + '...');
        console.log('[PrivateRoute] Current API headers:', api.defaults.headers.common);

        // Ensure the token is set in the API headers
        if (!api.defaults.headers.common['Authorization']) {
          console.log('[PrivateRoute] Setting Authorization header');
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }

        console.log('[PrivateRoute] Making validation request...');
        const response = await api.post('/api/auth/validate');
        console.log('[PrivateRoute] Validation response:', response.data);
        
        if (response.data.valid) {
          console.log('[PrivateRoute] Token is valid, proceeding');
          setIsValid(true);
        } else {
          console.log('[PrivateRoute] Server says token is invalid:', response.data);
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          delete api.defaults.headers.common['Authorization'];
          navigate('/login');
        }
      } catch (error) {
        console.error('[PrivateRoute] Validation error:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        delete api.defaults.headers.common['Authorization'];
        navigate('/login');
      } finally {
        setIsValidating(false);
      }
    };
    
    validateToken();
  }, [navigate]);
  
  if (isValidating) {
    console.log('[PrivateRoute] Still validating token...');
    return <div>Validating authentication...</div>;
  }
  
  if (!isValid) {
    console.log('[PrivateRoute] Token is invalid, not rendering protected route');
    return null;
  }
  
  console.log('[PrivateRoute] Token is valid, rendering protected route:', window.location.pathname);
  return children;
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          
          {/* Protected Routes */}
          <Route
            path="/select"
            element={
              <PrivateRoute>
                <Navbar />
                <SelectView />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/teams"
            element={
              <PrivateRoute>
                <Navbar />
                <TeamList />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/teams/:teamId/applications"
            element={
              <PrivateRoute>
                <Navbar />
                <TeamApplications />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/applications"
            element={
              <PrivateRoute>
                <Navbar />
                <ApplicationList />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/applications/:id"
            element={
              <PrivateRoute>
                <Navbar />
                <ApplicationDetails />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Navbar />
                <SecurityDashboard />
              </PrivateRoute>
            }
          />
          
          <Route
            path="/search"
            element={
              <PrivateRoute>
                <Navbar />
                <ApplicationRiskSearch />
              </PrivateRoute>
            }
          />
          
          {/* Default Route */}
          <Route
            path="/"
            element={<Navigate to="/select" />}
          />

          {/* 404 Route */}
          <Route
            path="*"
            element={<Navigate to="/select" />}
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
