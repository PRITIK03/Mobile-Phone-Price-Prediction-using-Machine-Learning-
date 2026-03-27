import React from 'react';
import AuthForm from '../components/AuthForm';

function LoginPage({ onAuthSuccess }) {
  return <AuthForm mode="login" onAuthSuccess={onAuthSuccess} />;
}

export default LoginPage;
