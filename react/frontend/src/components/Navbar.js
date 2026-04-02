import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

function Navbar({ isLoggedIn, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    if (onLogout) onLogout();
    navigate('/login');
  };

  return (
    <AppBar
      position="static"
      color="primary"
      sx={{
        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
      }}
    >
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{ flexGrow: 1, color: 'inherit', textDecoration: 'none', fontWeight: 600 }}
        >
          Mobile Price Predictor
        </Typography>
        <Button
          color="inherit"
          component={RouterLink}
          to="/predict"
          sx={{
            mx: 1,
            transition: 'background 0.2s',
            '&:hover': { background: 'rgba(255,255,255,0.12)' },
          }}
        >
          Predict
        </Button>
        <Box>
          {isLoggedIn ? (
            <>
              <Button
                color="inherit"
                component={RouterLink}
                to="/dashboard"
                sx={{
                  mx: 1,
                  transition: 'background 0.2s',
                  '&:hover': { background: 'rgba(255,255,255,0.12)' },
                }}
              >
                Dashboard
              </Button>
              <Button
                color="inherit"
                onClick={handleLogout}
                sx={{
                  mx: 1,
                  transition: 'background 0.2s',
                  '&:hover': { background: 'rgba(255,255,255,0.12)' },
                }}
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button
                color="inherit"
                component={RouterLink}
                to="/login"
                sx={{
                  mx: 1,
                  transition: 'background 0.2s',
                  '&:hover': { background: 'rgba(255,255,255,0.12)' },
                }}
              >
                Login
              </Button>
              <Button
                color="inherit"
                component={RouterLink}
                to="/register"
                sx={{
                  mx: 1,
                  transition: 'background 0.2s',
                  '&:hover': { background: 'rgba(255,255,255,0.12)' },
                }}
              >
                Register
              </Button>
            </>
          )}
        </Box>
        <Box sx={{ ml: 3 }}>
          <AccountCircleIcon fontSize="large" />
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
