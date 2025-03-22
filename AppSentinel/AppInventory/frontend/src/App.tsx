import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/auth/Login';
import Dashboard from './components/Dashboard';

const RequireAuth = ({ children }: { children: React.ReactNode }) => {
  const { user } = useAuth();
  return user ? <>{children}</> : <Navigate to="/login" replace />;
};

const RequireGuest = ({ children }: { children: React.ReactNode }) => {
  const { user } = useAuth();
  return !user ? <>{children}</> : <Navigate to="/" replace />;
};

const AppRoutes = () => (
  <Routes>
    <Route path="/login" element={
      <RequireGuest>
        <Login />
      </RequireGuest>
    } />
    <Route path="/" element={
      <RequireAuth>
        <Dashboard />
      </RequireAuth>
    } />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
);

const App = () => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  </ThemeProvider>
);

export default App;