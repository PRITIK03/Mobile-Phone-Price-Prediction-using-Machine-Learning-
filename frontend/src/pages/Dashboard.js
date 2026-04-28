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

  const marketTrends = [
    { quarter: 'Q1 2023', avgPrice: 28000, units: 450 },
    { quarter: 'Q2 2023', avgPrice: 29500, units: 480 },
    { quarter: 'Q3 2023', avgPrice: 31000, units: 520 },
    { quarter: 'Q4 2023', avgPrice: 32500, units: 580 },
    { quarter: 'Q1 2024', avgPrice: 34000, units: 620 }
  ];

  const featureComparison = [
    { feature: '5G', adoption: 78, satisfaction: 92 },
    { feature: 'AMOLED', adoption: 65, satisfaction: 88 },
    { feature: 'Fast Charging', adoption: 85, satisfaction: 95 },
    { feature: 'Multiple Cameras', adoption: 92, satisfaction: 87 },
    { feature: 'High Refresh Rate', adoption: 58, satisfaction: 90 }
  ];

  const confidenceData = [
    { range: '±5%', confidence: 95 },
    { range: '±10%', confidence: 88 },
    { range: '±15%', confidence: 76 },
    { range: '±20%', confidence: 62 },
    { range: '±25%', confidence: 48 }
  ];

  const userActivity = [
    { hour: '00', activity: 12 },
    { hour: '04', activity: 8 },
    { hour: '08', activity: 35 },
    { hour: '12', activity: 68 },
    { hour: '16', activity: 82 },
    { hour: '20', activity: 58 },
    { hour: '23', activity: 25 }
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

      {/* Additional Charts Row */}
      <Grid container spacing={3} sx={{ mt: 3 }}>
        {/* Market Trends Line Chart */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>Market Trends Analysis</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={marketTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="quarter" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="avgPrice" stroke="#2196f3" name="Avg Price (₹)" strokeWidth={2} />
                <Line yAxisId="right" type="monotone" dataKey="units" stroke="#4caf50" name="Units Sold" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Confidence Level Chart */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>Prediction Confidence</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={confidenceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="confidence" stroke="#9c27b0" fill="#e1bee7" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Feature Comparison and User Activity Row */}
      <Grid container spacing={3} sx={{ mt: 3 }}>
        {/* Feature Comparison Scatter Chart */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>Feature Adoption vs Satisfaction</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={featureComparison}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="feature" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="adoption" fill="#ff9800" name="Adoption %" />
                <Bar dataKey="satisfaction" fill="#4caf50" name="Satisfaction %" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* User Activity Heat Map */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, height: 350 }}>
            <Typography variant="h6" gutterBottom>User Activity by Hour</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={userActivity}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="activity" stroke="#607d8b" fill="#cfd8dc" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Additional Micro Stats */}
      <Grid container spacing={2} sx={{ mt: 3 }}>
        <Grid item xs={6} sm={3}>
          <Paper elevation={1} sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #fff9c4 0%, #fff 100%)' }}>
            <Typography variant="body2" color="text.secondary">Market Growth</Typography>
            <Typography variant="h6" fontWeight={700} color="#f57c00">+21.4%</Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper elevation={1} sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #f8bbd0 0%, #fff 100%)' }}>
            <Typography variant="body2" color="text.secondary">Avg Confidence</Typography>
            <Typography variant="h6" fontWeight={700} color="#c2185b">73.8%</Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper elevation={1} sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #c8e6c9 0%, #fff 100%)' }}>
            <Typography variant="body2" color="text.secondary">Peak Activity</Typography>
            <Typography variant="h6" fontWeight={700} color="#388e3c">4PM</Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper elevation={1} sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #bbdefb 0%, #fff 100%)' }}>
            <Typography variant="body2" color="text.secondary">Top Feature</Typography>
            <Typography variant="h6" fontWeight={700} color="#1976d2">5G</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
