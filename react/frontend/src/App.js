
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

import Dashboard from './pages/Dashboard';
import PredictionForm from './pages/PredictionForm';
import History from './pages/History';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import { NotificationProvider } from './components/NotificationProvider';

import { useState, useEffect } from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import SampleChart from './components/SampleChart';
import PieChart from './components/PieChart';
import LineChart from './components/LineChart';
import AreaChart from './components/AreaChart';
import DonutChart from './components/DonutChart';
import RandomTip from './components/RandomTip';
import FunFact from './components/FunFact';


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
              <Route path="/predict" element={<PredictionForm />} />
              <Route path="*" element={
                <Box textAlign="center" mt={8} sx={{ minHeight: '100vh', background: 'linear-gradient(135deg, #e3f2fd 0%, #fff 100%)' }}>
                  <Typography variant="h3" gutterBottom sx={{ fontWeight: 700, color: '#1976d2', letterSpacing: 1 }}>
                    Welcome to Mobile Price Prediction
                  </Typography>
                  <Typography variant="h6" sx={{ color: '#1565c0', mb: 2 }}>
                    Select Login or Register to continue.
                  </Typography>
                  <Card sx={{ mt: 4, mb: 2, borderRadius: 3, boxShadow: 3, maxWidth: 350, mx: 'auto', background: '#fff', transition: 'transform 0.2s, box-shadow 0.2s', ':hover': { transform: 'scale(1.03)', boxShadow: 6 } }}>
                    <CardContent>
                      <SampleChart />
                    </CardContent>
                  </Card>
                  <Card sx={{ mt: 4, mb: 2, borderRadius: 3, boxShadow: 3, maxWidth: 350, mx: 'auto', background: '#fff', transition: 'transform 0.2s, box-shadow 0.2s', ':hover': { transform: 'scale(1.03)', boxShadow: 6 } }}>
                    <CardContent>
                      <PieChart />
                    </CardContent>
                  </Card>
                  <Card sx={{ mt: 4, mb: 2, borderRadius: 3, boxShadow: 3, maxWidth: 350, mx: 'auto', background: '#fff', transition: 'transform 0.2s, box-shadow 0.2s', ':hover': { transform: 'scale(1.03)', boxShadow: 6 } }}>
                    <CardContent>
                      <LineChart />
                    </CardContent>
                  </Card>
                  <Card sx={{ mt: 4, mb: 2, borderRadius: 3, boxShadow: 3, maxWidth: 350, mx: 'auto', background: '#fff', transition: 'transform 0.2s, box-shadow 0.2s', ':hover': { transform: 'scale(1.03)', boxShadow: 6 } }}>
                    <CardContent>
                      <AreaChart />
                    </CardContent>
                  </Card>
                  <Card sx={{ mt: 4, mb: 2, borderRadius: 3, boxShadow: 3, maxWidth: 350, mx: 'auto', background: '#fff', transition: 'transform 0.2s, box-shadow 0.2s', ':hover': { transform: 'scale(1.03)', boxShadow: 6 } }}>
                    <CardContent>
                      <DonutChart />
                    </CardContent>
                  </Card>
                  <RandomTip />
                  <FunFact />
                </Box>
              } />
            </Routes>
          </Box>
        </Container>
            <Routes>
              <Route path="/login" element={<LoginPage onAuthSuccess={handleAuthSuccess} />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/predict" element={<PredictionForm />} />
              <Route path="/dashboard" element={<ProtectedRoute isLoggedIn={isLoggedIn}><Dashboard /></ProtectedRoute>} />
              <Route path="/history" element={<ProtectedRoute isLoggedIn={isLoggedIn}><History /></ProtectedRoute>} />
            </Routes>
