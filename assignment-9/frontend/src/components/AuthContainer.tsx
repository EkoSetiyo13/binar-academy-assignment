import React, { useState } from 'react';
import { Login } from './Login';
import { Register } from './Register';

interface AuthContainerProps {
  onAuthSuccess: () => void;
}

export function AuthContainer({ onAuthSuccess }: AuthContainerProps) {
  const [isLogin, setIsLogin] = useState(true);

  const handleSwitchToRegister = () => {
    setIsLogin(false);
  };

  const handleSwitchToLogin = () => {
    setIsLogin(true);
  };

  const handleAuthSuccess = () => {
    onAuthSuccess();
  };

  return (
    <div>
      {isLogin ? (
        <Login
          onSwitchToRegister={handleSwitchToRegister}
          onLoginSuccess={handleAuthSuccess}
        />
      ) : (
        <Register
          onSwitchToLogin={handleSwitchToLogin}
          onRegisterSuccess={handleAuthSuccess}
        />
      )}
    </div>
  );
} 