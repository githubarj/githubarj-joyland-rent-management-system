/**
 * Auth Service
 *
 * Provides functions for calling authentication-related API endpoints such as login, signup, and password management.
 *
 * To add a new auth method:
 * - Import the endpoint from `../endpoints`
 * - Use the `request` utility to call the API
 *
 * Example:
 * ```ts
 * const handleSignup = (data) => request.post(auth.SIGN_UP, data);
 * ```
 */

import { AxiosRequestConfig } from 'axios';
import { request } from '../request';
import { auth } from '../endpoints';

const handleLogin = (data?: AxiosRequestConfig<any>) => {
  return request.get(auth.LOGIN, data);
};

export { handleLogin };
