/**
 * Authentication Service for Task Management Application
 * 
 * Author: Eon (Himanshu Shekhar)
 * Email: eonhimanshu@gmail.com
 * 
 * This service handles user authentication and token management.
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

interface LoginResponse {
  user: {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
  };
  tokens: {
    access: string;
    refresh: string;
  };
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}

class AuthService {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  removeToken() {
    this.token = null;
    delete api.defaults.headers.common['Authorization'];
  }

  async login(username: string, password: string): Promise<LoginResponse> {
    const response = await api.post('/users/login/', {
      username,
      password,
    });
    return response.data;
  }

  async register(userData: RegisterData): Promise<LoginResponse> {
    const response = await api.post('/users/register/', userData);
    return response.data;
  }

  async getProfile() {
    const response = await api.get('/users/profile/');
    return response.data;
  }

  async refreshToken(refreshToken: string) {
    const response = await api.post('/auth/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  }
}

export const authService = new AuthService(); 