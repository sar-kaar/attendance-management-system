import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000/api';

export const ACCESS_TOKEN_KEY = 'access_token';
export const REFRESH_TOKEN_KEY = 'refresh_token';

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = await SecureStore.getItemAsync(REFRESH_TOKEN_KEY);
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, res.data.access);
          if (res.data.refresh) {
            await SecureStore.setItemAsync(REFRESH_TOKEN_KEY, res.data.refresh);
          }
          originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
          return api(originalRequest);
        } catch (refreshError) {
          await SecureStore.deleteItemAsync(ACCESS_TOKEN_KEY);
          await SecureStore.deleteItemAsync(REFRESH_TOKEN_KEY);
          return Promise.reject(refreshError);
        }
      }
    }
    return Promise.reject(error);
  },
);

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

export const authAPI = {
  me: () => api.get('/auth/me/'),
  login: (username: string, password: string) =>
    api.post<{ access: string; refresh: string }>('/auth/login/', { username, password }),
  register: (payload: RegisterPayload) => api.post('/auth/register/', payload),
};

export const otpAPI = {
  send: (email: string) =>
    api.post('/auth/otp/send/', { email, purpose: 'email_verification' }),
  verify: (email: string, code: string) =>
    api.post('/auth/otp/verify/', { email, code, purpose: 'email_verification' }),
};

export default api;
