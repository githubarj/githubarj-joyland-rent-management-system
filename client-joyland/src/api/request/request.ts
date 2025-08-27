import { showNotification } from '@mantine/notifications';
import axios from 'axios';

const query = axios.create({
  baseURL: 'http://localhost:3000/',
  timeout: 10000,
});

query.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
      config.headers['Content-Type'] = 'application/json';
      config.headers['Accept'] = 'application/json';
    }
    return config;
  },
  (error) => Promise.reject(error)
);

query.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const message = error?.response?.data?.message || error.message || '';
      if (status == 401) {
        showNotification({
          title: 'Unauthorized! Redirecting to login',
          message: message,
          color: 'red',
        });
      } else if (status == 500) {
        showNotification({
          title: 'Server Error detected!',
          message: message,
          color: 'red',
        });
      } else {
        showNotification({
          title: `An error occurred ${status}`,
          message: message,
          color: 'red',
        });
      }
    }
    return Promise.reject(error);
  }
);

export default query;
