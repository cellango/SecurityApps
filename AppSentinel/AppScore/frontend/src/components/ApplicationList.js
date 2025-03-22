import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  TextField,
  Box,
  Typography,
  Chip,
  IconButton,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Pagination,
  Stack,
  Alert,
  CircularProgress,
  Tooltip,
} from '@mui/material';
import {
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';

function ApplicationList() {
  const { teamId: urlTeamId } = useParams();
  const navigate = useNavigate();
  const [applications, setApplications] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedTeam, setSelectedTeam] = useState(urlTeamId || '');
  const [page, setPage] = useState(1);
  const [rowsPerPage] = useState(10);

  useEffect(() => {
    fetchTeams();
  }, []);

  useEffect(() => {
    fetchApplications();
  }, [selectedTeam]);

  const fetchTeams = async () => {
    try {
      const response = await api.get('/api/teams');
      setTeams(response.data);
      
      // If we have a teamId from URL and it exists in the teams list, select it
      if (urlTeamId && response.data.some(team => team.id.toString() === urlTeamId)) {
        setSelectedTeam(urlTeamId);
      }
    } catch (error) {
      console.error('Error fetching teams:', error);
      setError('Failed to load teams');
    }
  };

  const fetchApplications = async () => {
    setLoading(true);
    try {
      let url = '/api/applications';
      if (selectedTeam) {
        url = `/api/teams/${selectedTeam}/applications`;
      }
      const response = await api.get(url);
      setApplications(response.data);
      setError('');
    } catch (error) {
      console.error('Error fetching applications:', error);
      setError('Failed to load applications');
    } finally {
      setLoading(false);
    }
  };

  const handleTeamChange = (event) => {
    const teamId = event.target.value;
    setSelectedTeam(teamId);
    if (teamId) {
      navigate(`/teams/${teamId}/applications`);
    } else {
      navigate('/applications');
    }
  };

  const handleViewApplication = (appId) => {
    navigate(`/applications/${appId}`);
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL':
        return '#d32f2f';
      case 'HIGH':
        return '#f44336';
      case 'MEDIUM':
        return '#ff9800';
      case 'LOW':
        return '#4caf50';
      default:
        return '#757575';
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toUpperCase()) {
      case 'OPEN':
        return 'error';
      case 'IN_PROGRESS':
        return 'warning';
      case 'CLOSED':
        return 'success';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Applications
        </Typography>
        
        <FormControl sx={{ minWidth: 200, mb: 3 }}>
          <InputLabel id="team-select-label">Filter by Team</InputLabel>
          <Select
            labelId="team-select-label"
            id="team-select"
            value={selectedTeam}
            label="Filter by Team"
            onChange={handleTeamChange}
          >
            <MenuItem value="">
              <em>All Teams</em>
            </MenuItem>
            {teams.map((team) => (
              <MenuItem key={team.id} value={team.id}>
                {team.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Application Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Team</TableCell>
                <TableCell>Security Score</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {applications
                .slice((page - 1) * rowsPerPage, page * rowsPerPage)
                .map((app) => (
                  <TableRow
                    key={app.id}
                    hover
                    sx={{ '&:hover': { backgroundColor: 'rgba(0, 0, 0, 0.04)' } }}
                  >
                    <TableCell>{app.name}</TableCell>
                    <TableCell>{app.app_type}</TableCell>
                    <TableCell>{app.team?.name || 'Unassigned'}</TableCell>
                    <TableCell>
                      <Chip
                        label={`${Math.round(app.security_score || 0)}%`}
                        sx={{
                          backgroundColor: getSeverityColor(app.severity),
                          color: 'white'
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={app.status || 'N/A'}
                        color={getStatusColor(app.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="View Details">
                        <IconButton
                          size="small"
                          onClick={() => handleViewApplication(app.id)}
                        >
                          <VisibilityIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>

        {applications.length > rowsPerPage && (
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
            <Pagination
              count={Math.ceil(applications.length / rowsPerPage)}
              page={page}
              onChange={(e, newPage) => setPage(newPage)}
              color="primary"
            />
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default ApplicationList;
