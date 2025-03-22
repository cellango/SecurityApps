import React, { useState, useEffect } from 'react';
import { useDrop } from 'react-dnd';
import {
  Card,
  CardContent,
  Typography,
  IconButton,
  CircularProgress,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import DraggableApplication from './DraggableApplication';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function GroupDropZone({ group, onAddApplication, onRemoveApplication }) {
  const [groupScore, setGroupScore] = useState(null);
  const [loading, setLoading] = useState(true);

  const [{ isOver }, drop] = useDrop(() => ({
    accept: 'application',
    drop: (item) => {
      if (item.type === 'available') {
        onAddApplication(group.id, item.id);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  }));

  useEffect(() => {
    fetchGroupScore();
  }, [group.applications]);

  const fetchGroupScore = async () => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/groups/${group.id}/score`
      );
      setGroupScore(response.data);
    } catch (error) {
      console.error('Error fetching group score:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return '#4caf50';
    if (score >= 70) return '#ff9800';
    return '#f44336';
  };

  return (
    <div
      ref={drop}
      style={{
        minHeight: '200px',
        backgroundColor: isOver ? 'rgba(0, 0, 0, 0.05)' : 'transparent',
      }}
    >
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            {group.name}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {group.description}
          </Typography>

          {loading ? (
            <CircularProgress size={20} />
          ) : (
            groupScore && (
              <Typography
                variant="h5"
                style={{
                  color: getScoreColor(groupScore.average_score),
                  marginTop: '1rem',
                }}
              >
                Average Score: {groupScore.average_score}
              </Typography>
            )
          )}

          <div style={{ marginTop: '1rem' }}>
            {group.applications.map((app) => (
              <div
                key={app.id}
                style={{ display: 'flex', alignItems: 'center' }}
              >
                <div style={{ flexGrow: 1 }}>
                  <DraggableApplication
                    application={app}
                    type="grouped"
                  />
                </div>
                <IconButton
                  size="small"
                  onClick={() => onRemoveApplication(group.id, app.id)}
                >
                  <DeleteIcon />
                </IconButton>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default GroupDropZone;
