import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import PredictionForm from './pages/PredictionForm';
import Dashboard from './pages/Dashboard';
import History from './pages/History';

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/predict" />} />
        <Route path="/predict" element={<PredictionForm />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Router>
  );
};

export default App;
