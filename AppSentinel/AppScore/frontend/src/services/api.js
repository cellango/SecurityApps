 /**
 * API service for making HTTP requests
 * 
 * @authors Clement Ellango, Carolina Clement
 * @copyright Copyright (c) 2024. All rights reserved.
 */

import axios from 'axios';
import { ERROR_MESSAGES } from '../utils/constants';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          return Promise.reject(new Error(ERROR_MESSAGES.UNAUTHORIZED));
        case 404:
          return Promise.reject(new Error(ERROR_MESSAGES.NOT_FOUND));
        case 500:
          return Promise.reject(new Error(ERROR_MESSAGES.SERVER_ERROR));
        default:
          return Promise.reject(new Error(error.response.data.message || ERROR_MESSAGES.FETCH_ERROR));
      }
    }
    if (error.request) {
      return Promise.reject(new Error(ERROR_MESSAGES.NETWORK_ERROR));
    }
    return Promise.reject(error);
  }
);

export default api;
