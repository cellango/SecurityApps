import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function TeamList() {
  const navigate = useNavigate();
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${API_BASE_URL}/api/teams`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setTeams(response.data);
      } catch (err) {
        console.error('Error fetching teams:', err);
        setError(err.response?.data?.message || 'Failed to load teams');
        if (err.response?.status === 401) {
          // Redirect to login if unauthorized
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
  }, [navigate]);

  const handleTeamClick = (teamId) => {
    navigate(`/teams/${teamId}/applications`);
  };

  if (loading) {
    return (
      <Box 
        display="flex" 
        justifyContent="center" 
        alignItems="center" 
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 8 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Teams
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 4 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {teams.map((team) => (
            <Grid item xs={12} sm={6} md={4} key={team.id}>
              <Card 
                sx={{ 
                  height: '100%',
                  cursor: 'pointer',
                  transition: '0.3s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}
                onClick={() => handleTeamClick(team.id)}
              >
                <CardContent>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {team.name}
                  </Typography>
                  
                  <Typography 
                    color="text.secondary" 
                    sx={{ mb: 2 }}
                  >
                    {team.description}
                  </Typography>

                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip 
                      label={`${team.applicationCount} Applications`} 
                      color="primary" 
                      size="small" 
                      variant="outlined"
                    />
                    {team.averageScore > 0 && (
                      <Chip 
                        label={`Score: ${team.averageScore}`} 
                        color={team.averageScore >= 80 ? 'success' : team.averageScore >= 60 ? 'warning' : 'error'}
                        size="small"
                      />
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
}

export default TeamList;
