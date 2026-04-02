import React from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';


import BarChartIcon from '@mui/icons-material/BarChart';

const Dashboard = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4, background: 'linear-gradient(135deg, #e3f2fd 0%, #fff 100%)' }}>
        <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <BarChartIcon color="primary" /> Model Dashboard
        </Typography>
        <Box sx={{ mt: 3, display: 'flex', gap: 4, justifyContent: 'center' }}>
          <Paper elevation={1} sx={{ p: 2, minWidth: 120, textAlign: 'center', background: '#f5faff' }}>
            <Typography variant="h6" color="primary">Accuracy</Typography>
            <Typography variant="h5" fontWeight={700}>92%</Typography>
          </Paper>
          <Paper elevation={1} sx={{ p: 2, minWidth: 120, textAlign: 'center', background: '#f5faff' }}>
            <Typography variant="h6" color="primary">RMSE</Typography>
            <Typography variant="h5" fontWeight={700}>0.18</Typography>
          </Paper>
        </Box>
        <Box sx={{ mt: 5, textAlign: 'center' }}>
          {/* Placeholder for chart */}
          <Box sx={{ width: '100%', height: 220, background: '#e3f2fd', borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#90caf9', fontSize: 32, fontWeight: 500 }}>
            [Sample Chart Placeholder]
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Dashboard;
