import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Divider
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = React.useState(null);
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
    handleClose();
  };

  const handleBack = () => {
    if (location.pathname.includes('/applications/')) {
      navigate('/applications');
    } else if (location.pathname.includes('/teams/')) {
      navigate('/teams');
    } else {
      navigate('/select');
    }
  };

  // Don't show navbar on login page
  if (location.pathname === '/login') {
    return null;
  }

  return (
    <AppBar position="static">
      <Toolbar>
        {location.pathname !== '/select' && (
          <IconButton
            edge="start"
            color="inherit"
            onClick={handleBack}
            sx={{ mr: 2 }}
          >
            <ArrowBackIcon />
          </IconButton>
        )}

        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Security Score Card
        </Typography>

        {user.username && (
          <Box>
            <IconButton
              size="large"
              onClick={handleMenu}
              color="inherit"
            >
              <AccountCircleIcon />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleClose}
              transformOrigin={{ horizontal: 'right', vertical: 'top' }}
              anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
            >
              <MenuItem disabled>
                <Typography variant="body2" color="text.secondary">
                  Signed in as {user.username}
                </Typography>
              </MenuItem>
              <Divider />
              <MenuItem onClick={() => { navigate('/select'); handleClose(); }}>
                Home
              </MenuItem>
              <MenuItem onClick={handleLogout}>
                Sign Out
              </MenuItem>
            </Menu>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
