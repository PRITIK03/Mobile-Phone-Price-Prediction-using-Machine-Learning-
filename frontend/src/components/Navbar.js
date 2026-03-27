import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          📱 Mobile Price Predictor
        </Typography>
        <Box>
          <Button color="inherit" component={RouterLink} to="/predict">
            Predict
          </Button>
          <Button color="inherit" component={RouterLink} to="/dashboard">
            Dashboard
          </Button>
          <Button color="inherit" component={RouterLink} to="/history">
            History
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
