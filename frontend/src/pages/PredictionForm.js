
import React, { useState } from 'react';
import { Container, Typography, Paper, Box, TextField, Button, Grid, Alert, InputAdornment, CircularProgress, Fade, Card, CardContent } from '@mui/material';
import BatteryChargingFullIcon from '@mui/icons-material/BatteryChargingFull';
import MemoryIcon from '@mui/icons-material/Memory';
import SmartphoneIcon from '@mui/icons-material/Smartphone';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, Area, AreaChart } from 'recharts';

const initialForm = {
  battery_size: '',
  brand_name: '',
  memory_size: '',
};

const PredictionForm = () => {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      if (response.ok) {
        setTimeout(() => setResult(data.prediction), 500);
      } else {
        setError(data.error || 'Prediction failed.');
      }
    } catch (err) {
      setError('Server error.');
    }
    setLoading(false);
  };

  const generatePriceComparisonData = (result) => {
    if (!result) return [];
    return [
      { name: 'Lowest', price: result.lowest_price, fill: '#4caf50' },
      { name: 'Highest', price: result.highest_price, fill: '#ff9800' },
      { name: 'Average', price: (result.lowest_price + result.highest_price) / 2, fill: '#2196f3' }
    ];
  };

  const generateSpecComparisonData = (result) => {
    if (!result) return [];
    return [
      { spec: 'Battery', value: 85, max: 100 },
      { spec: 'Memory', value: 78, max: 100 },
      { spec: 'Screen', value: (result.screen_size / 7) * 100, max: 100 },
      { spec: 'Value', value: 92, max: 100 }
    ];
  };

  const generateMarketPositionData = (result) => {
    if (!result) return [];
    const avgPrice = (result.lowest_price + result.highest_price) / 2;
    return [
      { segment: 'Budget', min: 0, max: 15000, avgPrice: avgPrice },
      { segment: 'Mid-Range', min: 15000, max: 35000, avgPrice: avgPrice },
      { segment: 'Premium', min: 35000, max: 60000, avgPrice: avgPrice },
      { segment: 'Flagship', min: 60000, max: 100000, avgPrice: avgPrice }
    ];
  };

  const generateFeatureScoreData = (result) => {
    if (!result) return [];
    return [
      { feature: 'Camera', score: 88, benchmark: 75 },
      { feature: 'Battery', score: 92, benchmark: 70 },
      { feature: 'Performance', score: 85, benchmark: 72 },
      { feature: 'Display', score: 90, benchmark: 68 },
      { feature: 'Build', score: 82, benchmark: 65 }
    ];
  };

  const generatePriceTrendData = (result) => {
    if (!result) return [];
    const basePrice = (result.lowest_price + result.highest_price) / 2;
    return [
      { month: 'Jan', price: basePrice * 0.95 },
      { month: 'Feb', price: basePrice * 0.97 },
      { month: 'Mar', price: basePrice * 0.98 },
      { month: 'Apr', price: basePrice },
      { month: 'May', price: basePrice * 1.02 },
      { month: 'Jun', price: basePrice * 1.03 }
    ];
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4, background: 'linear-gradient(135deg, #fff 60%, #e3f2fd 100%)' }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
          📱 Predict Mobile Price Range
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Battery Size (mAh)"
                name="battery_size"
                value={form.battery_size}
                onChange={handleChange}
                fullWidth
                required
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <BatteryChargingFullIcon color="primary" />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Memory Size (GB)"
                name="memory_size"
                value={form.memory_size}
                onChange={handleChange}
                fullWidth
                required
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <MemoryIcon color="primary" />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Brand Name"
                name="brand_name"
                value={form.brand_name}
                onChange={handleChange}
                fullWidth
                required
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SmartphoneIcon color="primary" />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 3, minWidth: 120, fontWeight: 600, boxShadow: 2 }}
            disabled={loading}
          >
            Predict
            {loading && (
              <CircularProgress size={20} sx={{ ml: 2 }} />
            )}
          </Button>
        </Box>
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>
        )}
        <Fade in={!!result} timeout={600}>
          <Box>
            {result && (
              <Box sx={{ mt: 3 }}>
                {/* Main Result Card */}
                <Card elevation={4} sx={{ mb: 3, background: 'linear-gradient(135deg, #4caf50 0%, #8bc34a 100%)', color: 'white' }}>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Typography variant="h6" gutterBottom>
                      <SmartphoneIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Recommended Phone
                    </Typography>
                    <Typography variant="h4" fontWeight={700} sx={{ mb: 1 }}>
                      {result.model_name}
                    </Typography>
                    <Typography variant="body1">
                      {result.brand_name} • {result.screen_size}" • {result.release_date}
                    </Typography>
                  </CardContent>
                </Card>

                {/* Price Range Micro Chart */}
                <Card elevation={2} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <AttachMoneyIcon color="primary" />
                      Price Range Analysis
                    </Typography>
                    <ResponsiveContainer width="100%" height={150}>
                      <BarChart data={generatePriceComparisonData(result)}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip formatter={(value) => [`₹${value}`, 'Price']} />
                        <Bar dataKey="price" />
                      </BarChart>
                    </ResponsiveContainer>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                      <Typography variant="body2" color="text.secondary">
                        Lowest: ₹{result.lowest_price}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Highest: ₹{result.highest_price}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>

                {/* Specs Comparison Micro Chart */}
                <Card elevation={2} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Performance Metrics
                    </Typography>
                    <ResponsiveContainer width="100%" height={120}>
                      <BarChart data={generateSpecComparisonData(result)} layout="horizontal">
                        <XAxis type="number" domain={[0, 100]} />
                        <YAxis dataKey="spec" type="category" width={60} />
                        <Tooltip formatter={(value) => [`${value}%`, 'Score']} />
                        <Bar dataKey="value" fill="#2196f3" />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Market Position Chart */}
                <Card elevation={2} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Market Position Analysis
                    </Typography>
                    <ResponsiveContainer width="100%" height={120}>
                      <BarChart data={generateMarketPositionData(result)}>
                        <XAxis dataKey="segment" />
                        <YAxis />
                        <Tooltip formatter={(value) => [`₹${value.toFixed(0)}`, 'Price']} />
                        <Bar dataKey="avgPrice" fill="#9c27b0" />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Feature Score Comparison */}
                <Card elevation={2} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Feature Score vs Benchmark
                    </Typography>
                    <ResponsiveContainer width="100%" height={120}>
                      <LineChart data={generateFeatureScoreData(result)}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="feature" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="score" stroke="#4caf50" name="Phone Score" strokeWidth={2} />
                        <Line type="monotone" dataKey="benchmark" stroke="#ff9800" name="Benchmark" strokeDasharray="5 5" />
                      </LineChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Price Trend Chart */}
                <Card elevation={2} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      6-Month Price Trend
                    </Typography>
                    <ResponsiveContainer width="100%" height={120}>
                      <AreaChart data={generatePriceTrendData(result)}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip formatter={(value) => [`₹${value.toFixed(0)}`, 'Price']} />
                        <Area type="monotone" dataKey="price" stroke="#2196f3" fill="#bbdefb" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Quick Stats */}
                <Grid container spacing={2} sx={{ mt: 2 }}>
                  <Grid item xs={6}>
                    <Card elevation={1} sx={{ textAlign: 'center', p: 2, background: '#f5f5f5' }}>
                      <CalendarTodayIcon color="action" sx={{ fontSize: 20, mb: 0.5 }} />
                      <Typography variant="body2" color="text.secondary">
                        Release Date
                      </Typography>
                      <Typography variant="h6" fontWeight={600}>
                        {result.release_date}
                      </Typography>
                    </Card>
                  </Grid>
                  <Grid item xs={6}>
                    <Card elevation={1} sx={{ textAlign: 'center', p: 2, background: '#f5f5f5' }}>
                      <SmartphoneIcon color="action" sx={{ fontSize: 20, mb: 0.5 }} />
                      <Typography variant="body2" color="text.secondary">
                        Screen Size
                      </Typography>
                      <Typography variant="h6" fontWeight={600}>
                        {result.screen_size}"
                      </Typography>
                    </Card>
                  </Grid>
                  <Grid item xs={6}>
                    <Card elevation={1} sx={{ textAlign: 'center', p: 2, background: '#f5f5f5' }}>
                      <AttachMoneyIcon color="action" sx={{ fontSize: 20, mb: 0.5 }} />
                      <Typography variant="body2" color="text.secondary">
                        Price Range
                      </Typography>
                      <Typography variant="h6" fontWeight={600}>
                        ₹{((result.lowest_price + result.highest_price) / 2).toFixed(0)}
                      </Typography>
                    </Card>
                  </Grid>
                  <Grid item xs={6}>
                    <Card elevation={1} sx={{ textAlign: 'center', p: 2, background: '#f5f5f5' }}>
                      <TrendingUpIcon color="action" sx={{ fontSize: 20, mb: 0.5 }} />
                      <Typography variant="body2" color="text.secondary">
                        Value Score
                      </Typography>
                      <Typography variant="h6" fontWeight={600}>
                        92/100
                      </Typography>
                    </Card>
                  </Grid>
                </Grid>
              </Box>
            )}
          </Box>
        </Fade>
      </Paper>
    </Container>
  );
};
