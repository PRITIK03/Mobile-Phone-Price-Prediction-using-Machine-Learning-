import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { motion } from 'framer-motion';
import FeatureImportanceChart from '../components/FeatureImportanceChart';

function Dashboard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Box mt={4} textAlign="center">
        <Typography variant="h4" gutterBottom>Dashboard</Typography>
        <Typography variant="body1">Welcome! You are logged in.</Typography>
        <FeatureImportanceChart />
      </Box>
    </motion.div>
  );
}

export default Dashboard;
