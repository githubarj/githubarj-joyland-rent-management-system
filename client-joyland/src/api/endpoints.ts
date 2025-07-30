/**
 * The base URL for all API requests.
 * @constant {string}
 */
export const baseURL = 'http://localhost:8000/api';

/**
 * Apis are grouped according to their categories using objects
 * Named in capital letters to mark them as constants and as apis
 * Paths are relative to the `baseURL`.
 *
 * for example 
 * @namespace auth
 * @property {string} login - Endpoint for user login.
 * @property {string} signUp - Endpoint for user signup.
 */


export const auth = {
  LOGIN: '/login',
  SIGN_UP: '/signup',
  // ...
};

