import React, { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { authApi } from './api';
import { AuthContainer } from './components/AuthContainer';
import { Header } from './components/Header';
import { TodoApp } from './components/TodoApp';
import { PerformanceMonitor } from './utils/performance';

const queryClient = new QueryClient();

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    PerformanceMonitor.measureSync('app-initialization', () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        setIsAuthenticated(true);
      }
    });
  }, []);

  const handleAuthSuccess = () => {
    PerformanceMonitor.measureSync('auth-success-handler', () => {
      setIsAuthenticated(true);
    });
  };

  const handleLogout = () => {
    PerformanceMonitor.measureSync('logout-handler', () => {
      authApi.logout();
      setIsAuthenticated(false);
    });
  };

  if (!isAuthenticated) {
    return (
      <QueryClientProvider client={queryClient}>
        <AuthContainer onAuthSuccess={handleAuthSuccess} />
      </QueryClientProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gradient-to-br from-blue-100 to-green-50">
        <Header onLogout={handleLogout} />
        <div className="py-6">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <TodoApp />
          </div>
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App; 