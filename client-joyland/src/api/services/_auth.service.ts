import { authEndpoints } from '../request/endpoints/auth.endpoints';
import query from '../request/request';

const refreshAccessToken = async (): Promise<string | null> => {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return null;

    const response = await query.post(authEndpoints.refreshAccessToken, {
      refreshToken,
    });

    const { accessToken } = response.data;
    localStorage.setItem('access_token', accessToken);
    return accessToken;
  } catch (err) {
    return null;
  }
};

export { refreshAccessToken };
