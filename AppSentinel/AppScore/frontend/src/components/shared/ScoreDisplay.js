/**
 * Shared security score display component
 * 
 * @authors Clement Ellango, Carolina Clement
 * @copyright Copyright (c) 2024. All rights reserved.
 */

import React from 'react';
import { Box, Typography, CircularProgress, Tooltip } from '@mui/material';
import { useTheme } from '@mui/material/styles';

const ScoreDisplay = ({ 
  score,
  size = 'medium',
  showLabel = true,
  tooltipText
}) => {
  const theme = useTheme();

  const getScoreColor = (score) => {
    if (score >= 80) return theme.palette.success.main;
    if (score >= 60) return theme.palette.warning.main;
    if (score >= 40) return theme.palette.warning.dark;
    return theme.palette.error.main;
  };

  const getSizeValues = (size) => {
    switch (size) {
      case 'small':
        return { width: 60, height: 60, fontSize: '1rem' };
      case 'large':
        return { width: 120, height: 120, fontSize: '2rem' };
      default: // medium
        return { width: 80, height: 80, fontSize: '1.5rem' };
    }
  };

  const { width, height, fontSize } = getSizeValues(size);
  const scoreColor = getScoreColor(score);

  const scoreDisplay = (
    <Box
      position="relative"
      display="inline-flex"
      flexDirection="column"
      alignItems="center"
    >
      <Box position="relative" display="inline-flex">
        <CircularProgress
          variant="determinate"
          value={100}
          size={width}
          sx={{ color: theme.palette.grey[200] }}
        />
        <CircularProgress
          variant="determinate"
          value={score}
          size={width}
          sx={{
            color: scoreColor,
            position: 'absolute',
            left: 0,
          }}
        />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography
            variant="h6"
            component="div"
            color="textPrimary"
            sx={{ fontSize }}
          >
            {Math.round(score)}
          </Typography>
        </Box>
      </Box>
      {showLabel && (
        <Typography
          variant="body2"
          color="textSecondary"
          sx={{ mt: 1 }}
        >
          Security Score
        </Typography>
      )}
    </Box>
  );

  if (tooltipText) {
    return (
      <Tooltip title={tooltipText} arrow>
        {scoreDisplay}
      </Tooltip>
    );
  }

  return scoreDisplay;
};

export default ScoreDisplay;
