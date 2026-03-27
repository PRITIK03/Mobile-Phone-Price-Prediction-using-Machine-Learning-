import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

function App() {
  return (
    <Router>
      <nav style={{ display: 'flex', gap: 16, padding: 16, justifyContent: 'center' }}>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </nav>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="*" element={<div style={{textAlign:'center',marginTop:40}}><h2>Welcome to Mobile Price Prediction</h2><p>Select Login or Register to continue.</p></div>} />
      </Routes>
    </Router>
  );
}

export default App;
