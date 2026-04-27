import React from 'react';
import { Container, Typography, Box, Paper, Grid } from '@mui/material';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import BarChartIcon from '@mui/icons-material/BarChart';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PieChartIcon from '@mui/icons-material/PieChart';

const Dashboard = () => {
  // Sample data for charts
  const brandData = [
    { name: 'Samsung', value: 35, color: '#1976d2' },
    { name: 'Apple', value: 28, color: '#2e7d32' },
    { name: 'Xiaomi', value: 18, color: '#ed6c02' },
    { name: 'OnePlus', value: 12, color: '#9c27b0' },
    { name: 'Others', value: 7, color: '#757575' }
  ];

  const priceRangeData = [
    { range: '0-10k', count: 45 },
    { range: '10-25k', count: 78 },
    { range: '25-40k', count: 92 },
    { range: '40-60k', count: 65 },
    { range: '60k+', count: 38 }
  ];

  const performanceData = [
    { month: 'Jan', predictions: 120, accuracy: 88 },
    { month: 'Feb', predictions: 145, accuracy: 90 },
    { month: 'Mar', predictions: 168, accuracy: 91 },
    { month: 'Apr', predictions: 192, accuracy: 92 },
    { month: 'May', predictions: 210, accuracy: 93 }
  ];

  const batteryPerformance = [
    { battery: '3000', efficiency: 75 },
    { battery: '4000', efficiency: 82 },
    { battery: '5000', efficiency: 89 },
    { battery: '6000', efficiency: 94 },
    { battery: '7000', efficiency: 96 }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 4 }}>
        <BarChartIcon color="primary" /> Analytics Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 3, textAlign: 'center', background: 'linear-gradient(135deg, #e3f2fd 0%, #fff 100%)' }}>
            <Typography variant="h6" color="primary">Model Accuracy</Typography>
            <Typography variant="h4" fontWeight={700} color="#2e7d32">92%</Typography>
            <TrendingUpIcon sx={{ color: '#2e7d32', mt: 1 }} />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 3, textAlign: 'center', background: 'linear-gradient(135deg, #fff3e0 0%, #fff 100%)' }}>
            <Typography variant="h6" color="primary">RMSE Score</Typography>
            <Typography variant="h4" fontWeight={700} color="#ed6c02">0.18</Typography>
            <PieChartIcon sx={{ color: '#ed6c02', mt: 1 }} />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 3, textAlign: 'center', background: 'linear-gradient(135deg, #f3e5f5 0%, #fff 100%)' }}>
            <Typography variant="h6" color="primary">Total Predictions</Typography>
            <Typography variant="h4" fontWeight={700} color="#9c27b0">1.2K</Typography>
            <BarChartIcon sx={{ color: '#9c27b0', mt: 1 }} />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 3, textAlign: 'center', background: 'linear-gradient(135deg, #e8f5e8 0%, #fff 100%)' }}>
            <Typography variant="h6" color="primary">Active Users</Typography>
            <Typography variant="h4" fontWeight={700} color="#1976d2">348</Typography>
            <TrendingUpIcon sx={{ color: '#1976d2', mt: 1 }} />
          </Paper>
        </Grid>
      </Grid>

      {/* Charts Grid */}
      <Grid container spacing={3}>
        {/* Brand Distribution Pie Chart */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>Brand Distribution</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={brandData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {brandData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Price Range Bar Chart */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>Price Range Distribution</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={priceRangeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#1976d2" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Performance Trend Line Chart */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>Model Performance Trend</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="left" dataKey="predictions" fill="#8884d8" name="Predictions" />
                <Line yAxisId="right" type="monotone" dataKey="accuracy" stroke="#2e7d32" name="Accuracy %" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Battery Efficiency Area Chart */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>Battery vs Efficiency</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={batteryPerformance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="battery" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="efficiency" stroke="#ed6c02" fill="#ffcc80" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
