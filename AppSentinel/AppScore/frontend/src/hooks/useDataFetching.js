/**
 * Custom hook for data fetching with loading and error states
 * 
 * @authors Clement Ellango, Carolina Clement
 * @copyright Copyright (c) 2024. All rights reserved.
 */

import { useState, useEffect } from 'react';
import api from '../services/api';

const useDataFetching = (endpoint, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { 
    dependencies = [], 
    transform = (data) => data,
    autoFetch = true
  } = options;

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await api.get(endpoint);
      setData(transform(response.data));
      setError(null);
    } catch (err) {
      console.error(`Error fetching data from ${endpoint}:`, err);
      setError(err.message || 'An error occurred while fetching data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (autoFetch) {
      fetchData();
    }
  }, [...dependencies]);

  return {
    data,
    loading,
    error,
    refetch: fetchData,
    setData
  };
};

export default useDataFetching;
