import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

// Example static data for feature importance
const data = [
  { name: 'Battery', importance: 0.35 },
  { name: 'Brand', importance: 0.25 },
  { name: 'Memory', importance: 0.20 },
  { name: 'Screen', importance: 0.12 },
  { name: 'Release', importance: 0.08 }
];

export default function FeatureImportanceChart() {
  return (
    <Box mt={4}>
      <Typography variant="h6" gutterBottom>Feature Importance (Example)</Typography>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="importance" fill="#1976d2" />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
}
