import axios, {
  AxiosError,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios';
import { baseURL } from './apis';

const api = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

api.interceptors.request.use(
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
