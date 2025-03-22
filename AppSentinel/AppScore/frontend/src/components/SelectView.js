import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  CircularProgress,
  Alert,
  Divider,
  Grid,
  Card,
  CardContent,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function SelectView() {
  const navigate = useNavigate();
  const [teams, setTeams] = useState([]);
  const [applications, setApplications] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [selectedApp, setSelectedApp] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch teams
        const teamsResponse = await api.get('/api/teams');
        // Filter out duplicate teams and sort by name
        const uniqueTeams = Array.from(new Map(teamsResponse.data.map(team => [team.id, team])).values())
          .sort((a, b) => a.name.localeCompare(b.name));
        setTeams(uniqueTeams);

        // Fetch applications
        const appsResponse = await api.get('/api/applications');
        // Filter out duplicate applications and sort by name
        const uniqueApps = Array.from(new Map(appsResponse.data.map(app => [app.id, app])).values())
          .sort((a, b) => a.name.localeCompare(b.name));
        setApplications(uniqueApps);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.response?.data?.message || 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleTeamChange = (event) => {
    setSelectedTeam(event.target.value);
    setSelectedApp(''); // Reset application selection when team changes
  };

  const handleAppChange = (event) => {
    setSelectedApp(event.target.value);
    setSelectedTeam(''); // Reset team selection when application changes
  };

  const handleViewTeam = () => {
    if (selectedTeam) {
      navigate(`/teams/${selectedTeam}/applications`);
    }
  };

  const handleViewApp = () => {
    if (selectedApp) {
      navigate(`/applications/${selectedApp}`);
    }
  };

  if (loading) {
    return (
      <Box 
        sx={{ 
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="sm">
      <Box sx={{ minHeight: '100vh', py: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" align="center" gutterBottom>
            Security Score Card
          </Typography>
          
          <Typography 
            variant="subtitle1" 
            color="text.secondary" 
            align="center" 
            sx={{ mb: 4 }}
          >
            Select a team or application to view security scores
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <Box sx={{ mb: 4 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Select Team</InputLabel>
              <Select
                value={selectedTeam}
                onChange={handleTeamChange}
                disabled={!!selectedApp}
                label="Select Team"
              >
                {teams.map((team) => (
                  <MenuItem key={team.id} value={team.id}>
                    {team.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Button
              variant="contained"
              fullWidth
              onClick={handleViewTeam}
              disabled={!selectedTeam}
              sx={{ mt: 1 }}
            >
              View Team Security Scores
            </Button>
          </Box>

          <Divider sx={{ my: 4 }}>OR</Divider>

          <Box>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Select Application</InputLabel>
              <Select
                value={selectedApp}
                onChange={handleAppChange}
                disabled={!!selectedTeam}
                label="Select Application"
              >
                {applications.map((app) => (
                  <MenuItem key={app.id} value={app.id}>
                    {app.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Button
              variant="contained"
              fullWidth
              onClick={handleViewApp}
              disabled={!selectedApp}
              sx={{ mt: 1 }}
            >
              View Application Security Score
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default SelectView;
