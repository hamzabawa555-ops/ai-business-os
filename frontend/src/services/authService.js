/**
 * Authentication API Service
 */

import apiClient from '../config/apiClient';

const authService = {
  // User login
  login: async (email, password) => {
    const response = await apiClient.post('/api/v1/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  // User registration
  register: async (userData) => {
    const response = await apiClient.post('/api/v1/auth/register', userData);
    return response.data;
  },

  // User logout
  logout: async () => {
    await apiClient.post('/api/v1/auth/logout');
    localStorage.removeItem('access_token');
  },

  // Refresh token
  refreshToken: async (refreshToken) => {
    const response = await apiClient.post('/api/v1/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await apiClient.get('/api/v1/users/me');
    return response.data;
  },
};

export default authService;
