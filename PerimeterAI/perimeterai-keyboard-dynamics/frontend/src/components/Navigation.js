import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authService from '../services/authService';

const Navigation = () => {
  const navigate = useNavigate();
  const isAuthenticated = authService.isAuthenticated();

  const handleLogout = async () => {
    try {
      await authService.logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="navigation">
      <div className="nav-brand">
        <Link to="/">PerimeterAI</Link>
      </div>
      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link to="/applications">Applications</Link>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
