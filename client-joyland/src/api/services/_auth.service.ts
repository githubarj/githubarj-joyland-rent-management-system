import { CanceledError } from 'axios';
import { authEndpoints } from '../request/endpoints/auth.endpoints';
import { ApiResponse } from '../../utils/constants/dataShapes';
import { query } from '../request/axios/request';
import { useLoadingStore } from '../../store/useLoadingStore';
import { useUserStore } from '../../store/useUserContext';

const { setLoading } = useLoadingStore.getState();

const register = async (data: {
  email: string;
  full_name: string;
  password: string;
}): Promise<ApiResponse | null> => {
  setLoading('register', true);
  try {
    const response = await query.post(authEndpoints.register, data);
    return response.data;
  } catch (error) {
    console.error('Registration Error', error);
    return null;
  } finally {
    setLoading('register', false);
  }
};

const verifyEmail = async (
  uid?: string,
  token?: string
): Promise<ApiResponse | null> => {
  setLoading('verify-email', true);
  try {
    const response = await query.get(
      `${authEndpoints.verifyEmail}${uid}/${token}/`
    );
    return response.data;
  } catch (error) {
    console.error('Verification Error', error);
    return null;
  } finally {
    setLoading('verify-email', false);
  }
};

const login = async (data: {
  email: string;
  password: string;
}): Promise<ApiResponse | null> => {
  setLoading('login', true);
  try {
    const response = await query.post(authEndpoints.login, data);
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    return response.data;
  } catch (error) {
    console.error('Login Error', error);
    return null;
  } finally {
    setLoading('login', false);
  }
};

const fetchCurrentUser = async (): Promise<ApiResponse | null> => {
  setLoading('user', true);
  try {
    const response = await query.get(authEndpoints.fetchCurrentUser);
    const user = response.data;

    useUserStore.getState().setUser(user);
    return user;
  } catch (error) {
    console.error('Fetch Current User Error', error);
    useUserStore.getState().clearUser();
    return null;
  } finally {
    setLoading('user', false);
  }
};

const refreshAccessToken = (): {
  newAccessToken: () => Promise<string | null>;
  cancel: () => void;
} => {
  const controller = new AbortController();

  const newAccessToken = async (): Promise<string | null> => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) return null;

      const response = await query.post(
        authEndpoints.refreshAccessToken,
        { refreshToken },
        { signal: controller.signal }
      );

      const { accessToken } = response.data;
      localStorage.setItem('access_token', accessToken);
      return accessToken;
    } catch (err) {
      if (err instanceof CanceledError) {
        console.log('Request was canceled');
        return null;
      }
      return null;
    }
  };

  return {
    newAccessToken,
    cancel: () => controller.abort(),
  };
};

const logout = async (data: {
  refresh?: string;
}): Promise<ApiResponse | null> => {
  setLoading('logout', true);
  try {
    const response = await query.post(authEndpoints.logout, data);
    localStorage.removeItem('access_token');
    return response.data;
  } catch (error) {
    console.error('Logout Error', error);
    return null;
  } finally {
    setLoading('logout', false);
  }
};

export {
  register,
  refreshAccessToken,
  login,
  verifyEmail,
  fetchCurrentUser,
  logout,
};
