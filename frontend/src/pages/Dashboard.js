import React from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';

const Dashboard = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          📊 Model Dashboard
        </Typography>
        <Box sx={{ mt: 2 }}>
          {/* Placeholder for model metrics and charts */}
          <Typography variant="body1">
            Model accuracy, RMSE, and other metrics will be displayed here.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Dashboard;
