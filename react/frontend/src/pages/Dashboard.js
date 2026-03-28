import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

function Dashboard() {
  return (
    <Box mt={4} textAlign="center">
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Typography variant="body1">Welcome! You are logged in.</Typography>
    </Box>
  );
}

export default Dashboard;
