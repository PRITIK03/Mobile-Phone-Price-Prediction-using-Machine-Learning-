import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import InputAdornment from '@mui/material/InputAdornment';
import BatteryChargingFullIcon from '@mui/icons-material/BatteryChargingFull';
import MemoryIcon from '@mui/icons-material/Memory';
import { useNotification } from '../components/NotificationProvider';
import { motion, AnimatePresence } from 'framer-motion';

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
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
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
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <BatteryChargingFullIcon color="primary" />
                </InputAdornment>
              ),
            }}
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
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <MemoryIcon color="primary" />
                </InputAdornment>
              ),
            }}
          />
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }} disabled={loading}>
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Predict'}
          </Button>
        </Box>
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4 }}
            >
              <Box mt={4}>
                <Typography variant="h6">Prediction Result:</Typography>
                <Typography>Model Name: {result.model_name}</Typography>
                <Typography>Lowest Price: ₹{result.lowest_price}</Typography>
                <Typography>Highest Price: ₹{result.highest_price}</Typography>
                <Typography>Release Date: {result.release_date}</Typography>
                <Typography>Screen Size: {result.screen_size} inches</Typography>
              </Box>
            </motion.div>
          )}
        </AnimatePresence>
      </Box>
    </motion.div>
  );
}

export default PredictionForm;
