import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  CircularProgress,
  Box,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Tooltip,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import api from '../services/api';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';
import DragIndicatorIcon from '@mui/icons-material/DragIndicator';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend
);

function TeamScore({ score, previousScore }) {
  const getScoreColor = (score) => {
    if (score >= 90) return '#4caf50';
    if (score >= 70) return '#ff9800';
    return '#f44336';
  };

  const getTrendIcon = () => {
    if (!previousScore) return null;
    const difference = score - previousScore;
    const threshold = 1;

    if (Math.abs(difference) < threshold) {
      return (
        <Tooltip title={`Score stable (${difference.toFixed(1)}% change)`}>
          <TrendingFlatIcon sx={{ ml: 1, color: '#757575' }} />
        </Tooltip>
      );
    }
    
    if (difference > 0) {
      return (
        <Tooltip title={`Score improved by ${difference.toFixed(1)}%`}>
          <TrendingUpIcon sx={{ ml: 1, color: '#4caf50' }} />
        </Tooltip>
      );
    }
    
    return (
      <Tooltip title={`Score decreased by ${Math.abs(difference).toFixed(1)}%`}>
        <TrendingDownIcon sx={{ ml: 1, color: '#f44336' }} />
      </Tooltip>
    );
  };

  const scoreTooltip = `
    Team Security Score: ${Math.round(score)}%
    
    This score is calculated as the average of all application scores in the team.
    
    Score Ratings:
    • ≥90%: Good security posture
    • 70-89%: Moderate security concerns
    • <70%: Needs immediate attention
    
    The trend indicator shows score changes compared to the previous period.
  `;

  return (
    <Box sx={{ display: 'inline-flex', alignItems: 'center', ml: 2 }}>
      <Tooltip 
        title={scoreTooltip}
        placement="bottom-start"
        sx={{ whiteSpace: 'pre-line' }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="h6" component="span" sx={{ mr: 1 }}>
            Team Score:
          </Typography>
          <Chip
            label={`${Math.round(score)}%`}
            sx={{
              backgroundColor: getScoreColor(score),
              color: 'white',
              fontWeight: 'bold',
              fontSize: '1.1rem',
              height: '32px',
            }}
          />
          {getTrendIcon()}
        </Box>
      </Tooltip>
    </Box>
  );
}

function TeamApplications() {
  const { teamId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [team, setTeam] = useState(null);
  const [applications, setApplications] = useState([]);
  const [unassignedApplications, setUnassignedApplications] = useState([]);
  const [scoreHistory, setScoreHistory] = useState([]);

  useEffect(() => {
    fetchTeamData();
    fetchUnassignedApplications();
  }, [teamId]);

  const fetchTeamData = async () => {
    try {
      const [teamResponse, appsResponse, historyResponse] = await Promise.all([
        api.get(`/api/teams/${teamId}`),
        api.get(`/api/teams/${teamId}/applications`),
        api.get(`/api/teams/${teamId}/score-history`)
      ]);

      setTeam(teamResponse.data);
      setApplications(appsResponse.data);
      setScoreHistory(historyResponse.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch team data');
      setLoading(false);
    }
  };

  const fetchUnassignedApplications = async () => {
    try {
      const response = await api.get('/api/applications?unassigned=true');
      setUnassignedApplications(response.data);
    } catch (err) {
      console.error('Failed to fetch unassigned applications:', err);
    }
  };

  const handleDragEnd = async (result) => {
    if (!result.destination) return;

    const { draggableId, source, destination } = result;
    const appId = parseInt(draggableId.replace('app-', ''));

    // If dropping in the same place, do nothing
    if (source.droppableId === destination.droppableId) return;

    try {
      // Update the application's team
      const newTeamId = destination.droppableId === 'team-applications' ? parseInt(teamId) : null;
      await api.put(`/api/applications/${appId}/team`, { team_id: newTeamId });

      // Optimistically update the UI
      if (destination.droppableId === 'team-applications') {
        const app = unassignedApplications.find(a => a.id === appId);
        setUnassignedApplications(prev => prev.filter(a => a.id !== appId));
        setApplications(prev => [...prev, app]);
      } else {
        const app = applications.find(a => a.id === appId);
        setApplications(prev => prev.filter(a => a.id !== appId));
        setUnassignedApplications(prev => [...prev, app]);
      }
    } catch (err) {
      console.error('Failed to update application team:', err);
      // Revert the UI on error
      fetchTeamData();
      fetchUnassignedApplications();
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!team) return <Alert severity="error">Team not found</Alert>;

  return (
    <Container>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1">
          {team.name}
          {team.security_score && (
            <TeamScore
              score={team.security_score}
              previousScore={team.previous_score}
            />
          )}
        </Typography>
        <Typography color="textSecondary">{team.description}</Typography>
      </Box>

      <DragDropContext onDragEnd={handleDragEnd}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Typography variant="h6" sx={{ mb: 2 }}>Team Applications</Typography>
            <Droppable droppableId="team-applications">
              {(provided) => (
                <Box
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  sx={{ minHeight: '200px' }}
                >
                  {applications.map((app, index) => (
                    <Draggable
                      key={app.id}
                      draggableId={`app-${app.id}`}
                      index={index}
                    >
                      {(provided) => (
                        <Card
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          sx={{ mb: 2 }}
                        >
                          <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
                            <Box {...provided.dragHandleProps} sx={{ mr: 2 }}>
                              <DragIndicatorIcon />
                            </Box>
                            <Box sx={{ flexGrow: 1 }}>
                              <Typography variant="h6">{app.name}</Typography>
                              <Typography color="textSecondary">
                                {app.description}
                              </Typography>
                            </Box>
                            <Chip
                              label={`${app.security_score}%`}
                              color={app.security_score >= 90 ? 'success' : app.security_score >= 70 ? 'warning' : 'error'}
                              sx={{ ml: 2 }}
                            />
                            <Tooltip title="View Details">
                              <IconButton
                                onClick={() => navigate(`/applications/${app.id}`)}
                                sx={{ ml: 1 }}
                              >
                                <VisibilityIcon />
                              </IconButton>
                            </Tooltip>
                          </CardContent>
                        </Card>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </Box>
              )}
            </Droppable>
          </Grid>

          <Grid item xs={12} md={4}>
            <Typography variant="h6" sx={{ mb: 2 }}>Unassigned Applications</Typography>
            <Droppable droppableId="unassigned-applications">
              {(provided) => (
                <Box
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  sx={{
                    minHeight: '200px',
                    p: 2,
                    bgcolor: 'grey.100',
                    borderRadius: 1
                  }}
                >
                  {unassignedApplications.map((app, index) => (
                    <Draggable
                      key={app.id}
                      draggableId={`app-${app.id}`}
                      index={index}
                    >
                      {(provided) => (
                        <Card
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          sx={{ mb: 2 }}
                        >
                          <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
                            <Box {...provided.dragHandleProps} sx={{ mr: 2 }}>
                              <DragIndicatorIcon />
                            </Box>
                            <Box sx={{ flexGrow: 1 }}>
                              <Typography variant="h6">{app.name}</Typography>
                              <Typography color="textSecondary">
                                {app.description}
                              </Typography>
                            </Box>
                          </CardContent>
                        </Card>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </Box>
              )}
            </Droppable>
          </Grid>
        </Grid>
      </DragDropContext>

      {scoreHistory.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>Score History</Typography>
          <Paper sx={{ p: 2 }}>
            <Line
              data={{
                labels: scoreHistory.map(h => new Date(h.timestamp).toLocaleDateString()),
                datasets: [{
                  label: 'Team Security Score',
                  data: scoreHistory.map(h => h.score),
                  borderColor: '#1976d2',
                  tension: 0.1
                }]
              }}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                  },
                  title: {
                    display: true,
                    text: 'Team Security Score Trend'
                  }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100
                  }
                }
              }}
            />
          </Paper>
        </Box>
      )}
    </Container>
  );
}

export default TeamApplications;