import React, { useState, useEffect } from 'react';
import {
  Container,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Autocomplete,
  CircularProgress,
} from '@mui/material';
import api from '../utils/api';

export default function DepartmentTeams() {
  const [departments, setDepartments] = useState([]);
  const [teams, setTeams] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState({
    departments: true,
    teams: false,
    applications: false
  });
  const [error, setError] = useState({
    departments: null,
    teams: null,
    applications: null
  });

  // Fetch departments on component mount
  useEffect(() => {
    fetchDepartments();
  }, []);

  // Fetch teams when department is selected
  useEffect(() => {
    if (selectedDepartment) {
      fetchTeams(selectedDepartment.id);
    } else {
      setTeams([]);
      setSelectedTeam('');
    }
  }, [selectedDepartment]);

  // Fetch applications when team is selected
  useEffect(() => {
    if (selectedTeam) {
      fetchApplications(selectedTeam);
    } else {
      setApplications([]);
    }
  }, [selectedTeam]);

  const fetchDepartments = async () => {
    setLoading(prev => ({ ...prev, departments: true }));
    setError(prev => ({ ...prev, departments: null }));
    try {
      const response = await api.get('/departments');
      const sortedDepartments = response.data.sort((a, b) => 
        a.name.localeCompare(b.name)
      );
      setDepartments(sortedDepartments);
    } catch (err) {
      console.error('Error fetching departments:', err);
      setError(prev => ({ 
        ...prev, 
        departments: 'Failed to load departments. Please try again.' 
      }));
    } finally {
      setLoading(prev => ({ ...prev, departments: false }));
    }
  };

  const fetchTeams = async (departmentId) => {
    setLoading(prev => ({ ...prev, teams: true }));
    setError(prev => ({ ...prev, teams: null }));
    try {
      const response = await api.get(`/departments/${departmentId}/teams`);
      const sortedTeams = response.data.sort((a, b) => 
        a.name.localeCompare(b.name)
      );
      setTeams(sortedTeams);
    } catch (err) {
      console.error('Error fetching teams:', err);
      setError(prev => ({ 
        ...prev, 
        teams: 'Failed to load teams. Please try again.' 
      }));
    } finally {
      setLoading(prev => ({ ...prev, teams: false }));
    }
  };

  const fetchApplications = async (teamId) => {
    setLoading(prev => ({ ...prev, applications: true }));
    setError(prev => ({ ...prev, applications: null }));
    try {
      const response = await api.get(`/teams/${teamId}/applications`);
      setApplications(response.data);
    } catch (err) {
      console.error('Error fetching applications:', err);
      setError(prev => ({ 
        ...prev, 
        applications: 'Failed to load applications. Please try again.' 
      }));
    } finally {
      setLoading(prev => ({ ...prev, applications: false }));
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Departments & Teams
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
          <FormControl fullWidth>
            <Autocomplete
              value={selectedDepartment}
              onChange={(event, newValue) => {
                setSelectedDepartment(newValue);
              }}
              options={departments}
              getOptionLabel={(option) => option.name}
              loading={loading.departments}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Department"
                  error={!!error.departments}
                  helperText={error.departments}
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {loading.departments ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
            />
          </FormControl>

          <FormControl fullWidth>
            <Autocomplete
              value={selectedTeam}
              onChange={(event, newValue) => {
                setSelectedTeam(newValue ? newValue.id : '');
              }}
              options={teams}
              getOptionLabel={(option) => option.name}
              loading={loading.teams}
              disabled={!selectedDepartment}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Team"
                  error={!!error.teams}
                  helperText={error.teams}
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {loading.teams ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
            />
          </FormControl>
        </Box>

        {error.applications && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error.applications}
          </Typography>
        )}

        {loading.applications ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : applications.length > 0 ? (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Last Updated</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {applications.map((app) => (
                  <TableRow key={app.id}>
                    <TableCell>{app.name}</TableCell>
                    <TableCell>{app.application_type}</TableCell>
                    <TableCell>{app.status}</TableCell>
                    <TableCell>{new Date(app.updated_at).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        ) : selectedTeam ? (
          <Typography variant="body1" color="text.secondary" align="center">
            No applications found for this team.
          </Typography>
        ) : null}
      </Paper>
    </Container>
  );
}
