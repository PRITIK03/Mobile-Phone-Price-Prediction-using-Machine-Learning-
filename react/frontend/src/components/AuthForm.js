
import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import { useNotification } from './NotificationProvider';
import CircularProgress from '@mui/material/CircularProgress';


  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const notify = useNotification();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const endpoint = mode === 'login' ? '/api/login' : '/api/register';
    try {
      const res = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (!res.ok) {
        notify(data.error || 'Something went wrong', 'error');
      } else {
        if (mode === 'login') {
          notify('Login successful!', 'success');
          localStorage.setItem('token', data.access_token);
          if (onAuthSuccess) onAuthSuccess();
        } else {
          notify('Registration successful! You can now log in.', 'success');
        }
      }
    } catch (err) {
      notify('Network error', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 360, mx: 'auto', mt: 6, p: 3, border: '1px solid #eee', borderRadius: 2, boxShadow: 1 }}>
      <Typography variant="h5" align="center" gutterBottom>{mode === 'login' ? 'Login' : 'Register'}</Typography>
      <TextField
        label="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
        required
        fullWidth
        margin="normal"
        disabled={loading}
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
        fullWidth
        margin="normal"
        disabled={loading}
      />
      <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }} disabled={loading}>
        {loading ? <CircularProgress size={24} color="inherit" /> : (mode === 'login' ? 'Login' : 'Register')}
      </Button>
    </Box>
  );
}

export default AuthForm;
