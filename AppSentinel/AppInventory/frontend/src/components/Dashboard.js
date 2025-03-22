import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AppBar,
  Box,
  Container,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Divider,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  AccountTree as DepartmentIcon,
  Apps as ApplicationIcon,
  AccountCircle as AccountIcon,
} from '@mui/icons-material';
import DepartmentTeams from './DepartmentTeams';

const drawerWidth = 240;

export default function Dashboard({ user, onLogout }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleClose();
    onLogout();
  };

  const handleNavigation = (view) => {
    if (view === 'applications') {
      navigate('/applications');
    } else {
      setCurrentView(view);
    }
    setMobileOpen(false);
  };

  const drawer = (
    <div>
      <Toolbar sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
        <img 
          src={`${process.env.PUBLIC_URL}/logo192.png`}
          alt="AppInventory Logo" 
          style={{ 
            height: '40px', 
            width: 'auto',
            marginRight: '8px'
          }} 
        />
        <Typography variant="h6" noWrap component="div">
          AppInventory
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        <ListItem button onClick={() => handleNavigation('dashboard')}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button onClick={() => handleNavigation('departments')}>
          <ListItemIcon>
            <DepartmentIcon />
          </ListItemIcon>
          <ListItemText primary="Departments/Teams" />
        </ListItem>
        <ListItem button onClick={() => handleNavigation('applications')}>
          <ListItemIcon>
            <ApplicationIcon />
          </ListItemIcon>
          <ListItemText primary="Applications" />
        </ListItem>
      </List>
    </div>
  );

  const renderContent = () => {
    switch (currentView) {
      case 'departments':
        return <DepartmentTeams />;
      case 'applications':
        return <Typography>Applications View</Typography>;
      default:
        return (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <img 
              src={`${process.env.PUBLIC_URL}/logo192.png`}
              alt="AppInventory Logo" 
              style={{ 
                height: '80px', 
                width: 'auto',
                marginBottom: '24px'
              }} 
            />
            <Typography variant="h4" gutterBottom>
              Welcome to AppInventory
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Manage your applications, teams, and departments all in one place.
            </Typography>
          </Box>
        );
    }
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <img 
              src={`${process.env.PUBLIC_URL}/logo192.png`}
              alt="AppInventory Logo" 
              style={{ 
                height: '32px', 
                width: 'auto',
                marginRight: '12px',
                display: { xs: 'none', sm: 'block' }
              }} 
            />
            <Typography variant="h6" noWrap component="div">
              {currentView.charAt(0).toUpperCase() + currentView.slice(1)}
            </Typography>
          </Box>
          <div>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
            >
              <AccountIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem>
                <Typography>
                  {user?.username || 'User'}
                </Typography>
              </MenuItem>
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </div>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {renderContent()}
      </Box>
    </Box>
  );
}
