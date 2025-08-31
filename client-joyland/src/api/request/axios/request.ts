import {showNotification} from '@mantine/notifications';
import axios from 'axios';

import {refreshAccessToken} from '../../services/_auth.service';
import {AxiosRequestConfigWithRetry} from '../../../utils/constants/dataShapes';
import {axiosInstance} from './axiosInstance';

const query = axiosInstance;

// intercepting the request before it is sent to add the access token and content type
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

// intercepting the response for global error handling
query.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (axios.isAxiosError(error)) {
            const originalRequest = error.config;
            if (!originalRequest) return Promise.reject(error);

            const status = error.response?.status;
            const message = error?.response?.data?.error || error?.message || '';

            if (status === 401) {
                // cast to custom interface to include _retry

                const originalRequest = error.config as AxiosRequestConfigWithRetry;

                // try retrying if not already retried
                if (originalRequest && !originalRequest._retry) {
                    originalRequest._retry = true;
                    const {newAccessToken} = refreshAccessToken();

                    const newToken = await newAccessToken();

                    if (newToken) {
                        originalRequest.headers = originalRequest.headers || {};
                        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                        return query(originalRequest);
                    }
                }

                // show notification if retry failed or cannot retry
                showNotification({
                    title: 'Unauthorized! Please login again',
                    message,
                    color: 'red',
                });
            } else if (status == 500) {


                showNotification({
                    title: 'Server Error detected!',
                    message: message,
                    color: 'red',
                });
            } else if (status == 404) {


                showNotification({
                    title: 'Request not found',
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
        // components still can handle errors as the error is passed down to the caller
        return Promise.reject(error);
    }
);

export {query};
