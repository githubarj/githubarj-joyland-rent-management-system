import { showNotification } from '@mantine/notifications';
import axios, {
  AxiosError,
  AxiosRequestConfig,
  InternalAxiosRequestConfig,
  Method,
} from 'axios';
import { baseURL } from './endpoints';

export const request = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

request.interceptors.request.use(
  (response: InternalAxiosRequestConfig) => response,
  (error: AxiosError) => {
    if (error.response) {
      if (error.response.status === 401) {
        console.warn('Unauthorized! Redirecting to login...');
        window.location.href = '/login';
      }
      if (error.response.status === 500) {
        console.error('Server error!');
      }
    }
    return Promise.reject(error);
  }
);

