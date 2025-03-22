import api from '../api/axios';

const TOKEN_KEY = 'auth_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

class AuthService {
  setTokens(token, refreshToken) {
    localStorage.setItem(TOKEN_KEY, token);
    if (refreshToken) {
      localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    }
  }

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  }

  removeTokens() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  }

  async login(email, password) {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { token, refreshToken } = response.data;
      this.setTokens(token, refreshToken);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async refreshToken() {
    try {
      const refreshToken = this.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await api.post('/auth/refresh', {
        refreshToken: refreshToken
      });
      
      const { token, newRefreshToken } = response.data;
      this.setTokens(token, newRefreshToken);
      return token;
    } catch (error) {
      this.removeTokens();
      throw error;
    }
  }

  async logout() {
    try {
      await api.post('/auth/logout');
    } finally {
      this.removeTokens();
    }
  }

  isAuthenticated() {
    return !!this.getToken();
  }
}

export default new AuthService();
