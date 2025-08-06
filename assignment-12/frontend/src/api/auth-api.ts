import api from './axios-config';
import { PerformanceMonitor } from '../utils/performance';
import type { User, LoginRequest, RegisterRequest, AuthResponse } from '../types';

export const authApi = {
  // Register a new user
  register: async (data: RegisterRequest): Promise<User> => {
    return PerformanceMonitor.measureAsync('auth-register', async () => {
      const response = await api.post('/auth/register', data);
      return response.data;
    });
  },

  // Login user
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    return PerformanceMonitor.measureAsync('auth-login', async () => {
      const response = await api.post('/auth/login', data);
      return response.data;
    });
  },

  // Get current user info
  getCurrentUser: async (): Promise<User> => {
    return PerformanceMonitor.measureAsync('auth-get-current-user', async () => {
      const response = await api.get('/auth/me');
      return response.data;
    });
  },

  // Logout user
  logout: () => {
    PerformanceMonitor.measureSync('auth-logout', () => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    });
  },
}; 