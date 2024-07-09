import axios, { AxiosResponse, AxiosRequestConfig } from 'axios';

interface Request {
  get: <T = any>(
    url: string,
    config?: AxiosRequestConfig
  ) => Promise<AxiosResponse<T>>;
  post: <T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ) => Promise<AxiosResponse<T>>;
  put: <T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ) => Promise<AxiosResponse<T>>;
  delete: <T = any>(
    url: string,
    config?: AxiosRequestConfig
  ) => Promise<AxiosResponse<T>>;
}

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000/',
  timeout: 10000,
//   headers: {
//     'Content-Type': 'application/json',
//   },
});

const request : Request = {
  get: async (url, config) => {
    try {
      const response = await axiosInstance.get(url, config);
      return response;
    } catch (error) {
      handleRequestError(error);
      throw error;
    }
  },
  post: async (url, data, config) => {
    try {
      const response = await axiosInstance.post(url, data, config);
      return response;
    } catch (error) {
      handleRequestError(error);
      throw error;
    }
  },
  put: async (url, data, config) => {
    try {
      const response = await axiosInstance.put(url, data, config);
      return response;
    } catch (error) {
      handleRequestError(error);
      throw error;
    }
  },
  delete: async (url, config) => {
    try {
      const response = await axiosInstance.delete(url, config);
      return response;
    } catch (error) {
      handleRequestError(error);
      throw error;
    }
  },
};

const handleRequestError = (error: any) => {
  if (axios.isAxiosError(error)) {
    console.error('Axios error:', error.response?.data || error.message);
  } else {
    console.error('Unexpected error:', error);
  }

  throw error;
};

export default request;
