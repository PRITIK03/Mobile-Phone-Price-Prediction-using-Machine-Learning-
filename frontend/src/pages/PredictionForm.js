import React, { useState } from 'react';
import { Container, Typography, Paper, Box, TextField, Button, Grid, Alert } from '@mui/material';

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
        setResult(data.prediction);
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
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          📱 Mobile Price Prediction
        </Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            {Object.keys(initialForm).map((key) => (
              <Grid item xs={12} sm={6} key={key}>
                <TextField
                  label={key.replace('_', ' ').toUpperCase()}
                  name={key}
                  value={form[key]}
                  onChange={handleChange}
                  fullWidth
                  required
                  type="number"
                />
              </Grid>
            ))}
          </Grid>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 3 }}
            fullWidth
            disabled={loading}
          >
            {loading ? 'Predicting...' : 'Predict'}
          </Button>
        </Box>
        {result && (
          <Alert severity="success" sx={{ mt: 3 }}>
            Predicted Price Range: <strong>{result}</strong>
          </Alert>
        )}
        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {error}
          </Alert>
        )}
      </Paper>
    </Container>
  );
};

export default PredictionForm;
