import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Applications from './pages/Applications';
import { AuthProvider } from './contexts/AuthContext';
import api from './utils/api';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976D2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token and get user data
      api.get('/auth/verify')
        .then(response => {
          setUser(response.data);
        })
        .catch(() => {
          localStorage.removeItem('token');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AuthProvider>
          {loading ? (
            <div>Loading...</div>
          ) : user ? (
            <Routes>
              <Route path="/dashboard" element={<Dashboard user={user} onLogout={handleLogout} />} />
              <Route path="/applications" element={<Applications />} />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          ) : (
            <Login onLogin={handleLogin} />
          )}
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;
