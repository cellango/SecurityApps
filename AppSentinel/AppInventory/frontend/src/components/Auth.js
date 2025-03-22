import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';

const Auth = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if we have a token in localStorage
    const token = localStorage.getItem('token');
    if (token) {
      validateToken(token);
    } else {
      setLoading(false);
    }
  }, []);

  const validateToken = async (token) => {
    try {
      const response = await axios.get('http://localhost:5000/api/validate-token', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Token validation failed:', error);
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (method = 'oauth') => {
    if (method === 'oauth') {
      window.location.href = 'http://localhost:5000/auth/login';
    } else if (method === 'saml') {
      window.location.href = 'http://localhost:5000/saml/login';
    }
  };

  const logout = async () => {
    localStorage.removeItem('token');
    setUser(null);
    setIsAuthenticated(false);
    window.location.href = 'http://localhost:5000/auth/logout';
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      {!isAuthenticated ? (
        <div className="auth-buttons">
          <button onClick={() => login('oauth')}>Login with OAuth</button>
          <button onClick={() => login('saml')}>Login with SAML</button>
        </div>
      ) : (
        <div>
          <div className="user-info">
            Welcome, {user?.preferred_username}!
            <button onClick={logout}>Logout</button>
          </div>
          {children}
        </div>
      )}
    </div>
  );
};

export default Auth;
