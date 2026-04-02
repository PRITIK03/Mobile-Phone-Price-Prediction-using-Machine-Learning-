import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';


import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const Navbar = () => {
  return (
    <AppBar
      position="static"
      color="primary"
      sx={{
        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
      }}
    >
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 600 }}>
          📱 Mobile Price Predictor
        </Typography>
        <Box>
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
            component={RouterLink}
            to="/history"
            sx={{
              mx: 1,
              transition: 'background 0.2s',
              '&:hover': { background: 'rgba(255,255,255,0.12)' },
            }}
          >
            History
          </Button>
        </Box>
        <Box sx={{ ml: 3 }}>
          <AccountCircleIcon fontSize="large" />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
