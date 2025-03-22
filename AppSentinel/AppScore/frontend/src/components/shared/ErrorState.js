/**
 * Shared error state component
 * 
 * @authors Clement Ellango, Carolina Clement
 * @copyright Copyright (c) 2024. All rights reserved.
 */

import React from 'react';
import { Alert, Box, Button } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const ErrorState = ({ 
  error, 
  onRetry,
  severity = 'error'
}) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      p={2}
    >
      <Alert
        severity={severity}
        icon={<ErrorOutlineIcon />}
        action={
          onRetry && (
            <Button 
              color="inherit" 
              size="small"
              onClick={onRetry}
            >
              Retry
            </Button>
          )
        }
      >
        {error}
      </Alert>
    </Box>
  );
};

export default ErrorState;
