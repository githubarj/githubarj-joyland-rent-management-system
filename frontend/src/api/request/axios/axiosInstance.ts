import axios from 'axios';

const baseUrl = import.meta.env.VITE_SERVER_BASE_URL;

export const axiosInstance = axios.create({
  baseURL: `${baseUrl}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
