/**
 * Application-wide constants
 * 
 * @authors Clement Ellango, Carolina Clement
 * @copyright Copyright (c) 2024. All rights reserved.
 */

export const SCORE_RANGES = {
  CRITICAL: { min: 0, max: 30, color: '#d32f2f' },
  HIGH: { min: 31, max: 60, color: '#f57c00' },
  MEDIUM: { min: 61, max: 80, color: '#ffa726' },
  LOW: { min: 81, max: 100, color: '#2e7d32' }
};

export const SEVERITY_LEVELS = {
  CRITICAL: { label: 'Critical', color: '#d32f2f' },
  HIGH: { label: 'High', color: '#f57c00' },
  MEDIUM: { label: 'Medium', color: '#ffa726' },
  LOW: { label: 'Low', color: '#2e7d32' },
  INFO: { label: 'Info', color: '#1976d2' }
};

export const APPLICATION_TYPES = {
  INTERNAL: 'Internal',
  VENDOR: 'Vendor',
  OPEN_SOURCE: 'Open Source'
};

export const PAGINATION_OPTIONS = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [5, 10, 25, 50],
  MAX_PAGE_SIZE: 100
};

export const DATE_FORMATS = {
  DISPLAY: 'MMM DD, YYYY',
  API: 'YYYY-MM-DD',
  FULL: 'MMMM DD, YYYY HH:mm:ss'
};

export const API_ENDPOINTS = {
  APPLICATIONS: '/api/applications',
  TEAMS: '/api/teams',
  FINDINGS: '/api/findings',
  SCORES: '/api/scores',
  REPORTS: '/api/reports'
};

export const ERROR_MESSAGES = {
  FETCH_ERROR: 'Failed to fetch data. Please try again.',
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  SERVER_ERROR: 'An internal server error occurred.'
};
