import React, { useState } from 'react';

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
    <form onSubmit={handleSubmit} style={{ maxWidth: 320, margin: '2rem auto', padding: 24, border: '1px solid #ccc', borderRadius: 8 }}>
      <h2 style={{ textAlign: 'center' }}>{mode === 'login' ? 'Login' : 'Register'}</h2>
      <div style={{ marginBottom: 12 }}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
          style={{ width: '100%', padding: 8 }}
        />
      </div>
      <div style={{ marginBottom: 12 }}>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          style={{ width: '100%', padding: 8 }}
        />
      </div>
      <button type="submit" style={{ width: '100%', padding: 10, background: '#1976d2', color: '#fff', border: 'none', borderRadius: 4 }}>
        {mode === 'login' ? 'Login' : 'Register'}
      </button>
      {error && <div style={{ color: 'red', marginTop: 10 }}>{error}</div>}
      {message && <div style={{ color: 'green', marginTop: 10 }}>{message}</div>}
    </form>
  );
}

export default AuthForm;
