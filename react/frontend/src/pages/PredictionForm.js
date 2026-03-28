import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import { useNotification } from '../components/NotificationProvider';

function PredictionForm() {
  const [batterySize, setBatterySize] = useState('');
  const [brandName, setBrandName] = useState('');
  const [memorySize, setMemorySize] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const notify = useNotification();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          battery_size: batterySize,
          brand_name: brandName,
          memory_size: memorySize
        })
      });
      const data = await res.json();
      if (!res.ok) {
        notify(data.error || 'Prediction failed', 'error');
      } else {
        setResult(data.prediction);
        notify('Prediction successful!', 'success');
      }
    } catch (err) {
      notify('Network error', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 400, mx: 'auto', mt: 6, p: 3, border: '1px solid #eee', borderRadius: 2, boxShadow: 1 }}>
      <Typography variant="h5" align="center" gutterBottom>Predict Mobile Price</Typography>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField
          label="Battery Size (mAh)"
          value={batterySize}
          onChange={e => setBatterySize(e.target.value)}
          required
          fullWidth
          margin="normal"
          type="number"
          disabled={loading}
        />
        <TextField
          label="Brand Name"
          value={brandName}
          onChange={e => setBrandName(e.target.value)}
          required
          fullWidth
          margin="normal"
          disabled={loading}
        />
        <TextField
          label="Memory Size (GB)"
          value={memorySize}
          onChange={e => setMemorySize(e.target.value)}
          required
          fullWidth
          margin="normal"
          type="number"
          disabled={loading}
        />
        <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }} disabled={loading}>
          {loading ? <CircularProgress size={24} color="inherit" /> : 'Predict'}
        </Button>
      </Box>
      {result && (
        <Box mt={4}>
          <Typography variant="h6">Prediction Result:</Typography>
          <Typography>Model Name: {result.model_name}</Typography>
          <Typography>Lowest Price: ₹{result.lowest_price}</Typography>
          <Typography>Highest Price: ₹{result.highest_price}</Typography>
          <Typography>Release Date: {result.release_date}</Typography>
          <Typography>Screen Size: {result.screen_size} inches</Typography>
        </Box>
      )}
    </Box>
  );
}

export default PredictionForm;
