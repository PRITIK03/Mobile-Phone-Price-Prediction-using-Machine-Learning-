
import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import { useNotification } from './NotificationProvider';


function AuthForm({ mode = 'login', onAuthSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const notify = useNotification();

  const handleSubmit = async (e) => {
    e.preventDefault();
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
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
        fullWidth
        margin="normal"
      />
      <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
        {mode === 'login' ? 'Login' : 'Register'}
      </Button>
    </Box>
  );
}

export default AuthForm;
