/**
 * Shared loading state component
 * 
 * @authors Clement Ellango, Carolina Clement
 * @copyright Copyright (c) 2024. All rights reserved.
 */

import React from 'react';
import { CircularProgress, Box, Typography } from '@mui/material';

const LoadingState = ({ message = 'Loading...' }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="200px"
    >
      <CircularProgress size={40} />
      <Typography
        variant="body1"
        color="textSecondary"
        sx={{ mt: 2 }}
      >
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingState;
