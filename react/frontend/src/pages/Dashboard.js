import React from 'react';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import { motion } from 'framer-motion';
import FeatureImportanceChart from '../components/FeatureImportanceChart';
import BarChartIcon from '@mui/icons-material/BarChart';


function Dashboard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Box mt={4} textAlign="center">
        <Paper elevation={3} sx={{ p: 4, background: 'linear-gradient(135deg, #e3f2fd 0%, #fff 100%)' }}>
          <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, justifyContent: 'center' }}>
            <BarChartIcon color="primary" /> Dashboard
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
        <Box mt={4}>
          <FeatureImportanceChart />
        </Box>
      </Box>
    </motion.div>
  );
}

export default Dashboard;
