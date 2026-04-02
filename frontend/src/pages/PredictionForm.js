
import React, { useState } from 'react';
import { Container, Typography, Paper, Box, TextField, Button, Grid, Alert, InputAdornment, CircularProgress, Fade } from '@mui/material';
import BatteryChargingFullIcon from '@mui/icons-material/BatteryChargingFull';
import MemoryIcon from '@mui/icons-material/Memory';

const initialForm = {
  battery_power: '',
  ram: '',
  px_height: '',
  px_width: '',
  mobile_wt: '',
  n_cores: '',
  clock_speed: '',
  int_memory: '',
  // Add more fields as needed
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
      // Replace with your backend API endpoint
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      if (response.ok) {
        setTimeout(() => setResult(data.prediction), 500); // Animation delay
      } else {
        setError(data.error || 'Prediction failed.');
      }
    } catch (err) {
      setError('Server error.');
    }
    setLoading(false);
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
                label="Battery Power (mAh)"
                name="battery_power"
                value={form.battery_power}
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
                label="RAM (MB)"
                name="ram"
                value={form.ram}
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
            {/* ...existing code... */}
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
