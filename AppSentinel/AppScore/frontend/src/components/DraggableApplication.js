import React from 'react';
import { useDrag } from 'react-dnd';
import { Card, CardContent, Typography } from '@mui/material';

function DraggableApplication({ application, type }) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'application',
    item: { id: application.id, type },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  const getScoreColor = (score) => {
    if (score >= 90) return '#4caf50';
    if (score >= 70) return '#ff9800';
    return '#f44336';
  };

  return (
    <div ref={drag} style={{ opacity: isDragging ? 0.5 : 1, cursor: 'move' }}>
      <Card
        sx={{
          mb: 1,
          '&:hover': {
            boxShadow: 3,
          },
        }}
      >
        <CardContent>
          <Typography variant="subtitle1">{application.name}</Typography>
          <Typography
            variant="body2"
            style={{ color: getScoreColor(application.security_score) }}
          >
            Score: {application.security_score}
          </Typography>
        </CardContent>
      </Card>
    </div>
  );
}

export default DraggableApplication;
