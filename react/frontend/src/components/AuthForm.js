import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';

function AuthForm({ mode = 'login', onAuthSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    const endpoint = mode === 'login' ? '/api/login' : '/api/register';
    try {
      const res = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || 'Something went wrong');
      } else {
        if (mode === 'login') {
          setMessage('Login successful!');
          localStorage.setItem('token', data.access_token);
          if (onAuthSuccess) onAuthSuccess();
        } else {
          setMessage('Registration successful! You can now log in.');
        }
      }
    } catch (err) {
      setError('Network error');
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
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}
    </Box>
  );
}

export default AuthForm;
