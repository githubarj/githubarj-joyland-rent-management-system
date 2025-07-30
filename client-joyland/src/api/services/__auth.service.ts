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

import { request } from '../request';
import { auth } from '../endpoints';

const handleLogin = (data: { username: string; password: string }) => {
  return request.post(auth.LOGIN, data);
};

const handleRegister = (data: {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
}) => {
  return request.post(auth.SIGN_UP, data);
};

export { handleLogin, handleRegister };
