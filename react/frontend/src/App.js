
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import { NotificationProvider } from './components/NotificationProvider';
import { useState, useEffect } from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    setIsLoggedIn(!!localStorage.getItem('token'));
  }, []);

  const handleAuthSuccess = () => setIsLoggedIn(true);
  const handleLogout = () => setIsLoggedIn(false);

  return (
    <NotificationProvider>
      <Router>
        <Navbar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
        <Container maxWidth="sm">
          <Box mt={4}>
            <Routes>
              <Route path="/login" element={<LoginPage onAuthSuccess={handleAuthSuccess} />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/dashboard" element={
                <ProtectedRoute isLoggedIn={isLoggedIn}>
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="*" element={
                <Box textAlign="center" mt={8}>
                  <Typography variant="h4" gutterBottom>Welcome to Mobile Price Prediction</Typography>
                  <Typography variant="body1">Select Login or Register to continue.</Typography>
                </Box>
              } />
            </Routes>
          </Box>
        </Container>
      </Router>
    </NotificationProvider>
  );
}

export default App;
