
import React, { useState } from 'react';
import { Container, Typography, Paper, Box, TextField, Button, Grid, Alert, InputAdornment, CircularProgress, Fade, Card, CardContent } from '@mui/material';
import BatteryChargingFullIcon from '@mui/icons-material/BatteryChargingFull';
import MemoryIcon from '@mui/icons-material/Memory';
import SmartphoneIcon from '@mui/icons-material/Smartphone';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
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
              <Alert severity="success" sx={{ mt: 2, fontSize: 18, fontWeight: 500 }}>
                Predicted Price Range: <b>{result}</b>
              </Alert>
            )}
          </Box>
        </Fade>
      </Paper>
    </Container>
  );
