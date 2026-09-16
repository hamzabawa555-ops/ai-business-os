/**
 * Authentication Store (Zustand)
 */

import { create } from 'zustand';
import authService from '../services/authService';

const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  isLoading: false,
  error: null,

  // Login
  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.login(email, password);
      localStorage.setItem('access_token', response.access_token);
      set({ isAuthenticated: true, isLoading: false });
      return response;
    } catch (error) {
      set({
        isLoading: false,
        error: error.response?.data?.detail || 'Login failed',
      });
      throw error;
    }
  },

  // Register
  register: async (userData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.register(userData);
      set({ isLoading: false });
      return response;
    } catch (error) {
      set({
        isLoading: false,
        error: error.response?.data?.detail || 'Registration failed',
      });
      throw error;
    }
  },

  // Logout
  logout: async () => {
    try {
      await authService.logout();
      set({ user: null, isAuthenticated: false });
    } catch (error) {
      console.error('Logout error:', error);
    }
  },

  // Get current user
  fetchCurrentUser: async () => {
    set({ isLoading: true });
    try {
      const user = await authService.getCurrentUser();
      set({ user, isLoading: false });
    } catch (error) {
      set({ isLoading: false, error: 'Failed to fetch user' });
    }
  },

  // Clear error
  clearError: () => set({ error: null }),
}));

export default useAuthStore;
