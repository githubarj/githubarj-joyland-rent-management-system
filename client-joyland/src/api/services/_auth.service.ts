import { CanceledError } from 'axios';
import { authEndpoints } from '../request/endpoints/auth.endpoints';
import { ApiResponse } from '../../utils/constants/dataShapes';
import { query } from '../request/axios/axiosInstance';
import { useLoadingStore } from '../../store/useLoadingStore';

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
    console.error('Registration error:', error);
    return null;
  } finally {
    setLoading('register', false);
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

export { register, refreshAccessToken };
