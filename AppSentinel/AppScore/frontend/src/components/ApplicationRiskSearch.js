import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Autocomplete,
  TextField,
  Button,
  CircularProgress,
  Stack,
  Divider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function ApplicationRiskSearch() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [catalogApps, setCatalogApps] = useState([]);
  const [teams, setTeams] = useState([]);
  const [selectedApp, setSelectedApp] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [appInputValue, setAppInputValue] = useState('');
  const [teamInputValue, setTeamInputValue] = useState('');
  const [syncingCatalog, setSyncingCatalog] = useState(false);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      // First sync with catalog to ensure we have latest data
      await syncWithCatalog();
      
      // Then fetch teams
      const teamsResponse = await axios.get('http://localhost:5000/api/teams');
      setTeams(teamsResponse.data);
    } catch (error) {
      console.error('Error fetching initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const syncWithCatalog = async () => {
    setSyncingCatalog(true);
    try {
      await axios.post('http://localhost:5000/api/applications/sync-catalog');
    } catch (error) {
      console.error('Error syncing with catalog:', error);
    } finally {
      setSyncingCatalog(false);
    }
  };

  const handleAppSearch = async (searchValue) => {
    if (!searchValue) {
      setCatalogApps([]);
      return;
    }

    try {
      const response = await axios.get(`http://localhost:5000/api/catalog/applications/search?q=${searchValue}`);
      setCatalogApps(response.data);
    } catch (error) {
      console.error('Error searching applications:', error);
    }
  };

  const handleTeamSearch = async (searchValue) => {
    if (!searchValue) return;

    try {
      const response = await axios.get(`http://localhost:5000/api/teams?search=${searchValue}`);
      setTeams(response.data);
    } catch (error) {
      console.error('Error searching teams:', error);
    }
  };

  const handleViewResults = async () => {
    if (selectedApp) {
      try {
        // Get or create local application record
        const appResponse = await axios.post('http://localhost:5000/api/applications', {
          catalog_id: selectedApp.id,
          name: selectedApp.name,
          description: selectedApp.description,
          app_type: selectedApp.vendor ? 'vendor' : 'built'
        });
        
        navigate(`/applications/${appResponse.data.id}`);
      } catch (error) {
        console.error('Error processing application:', error);
      }
    } else if (selectedTeam) {
      try {
        // Fetch team's applications
        const appsResponse = await axios.get(`http://localhost:5000/api/teams/${selectedTeam.id}/applications`);
        
        if (appsResponse.data.length === 1) {
          // If team has only one application, go directly to it
          navigate(`/applications/${appsResponse.data[0].id}`);
        } else {
          // Otherwise, show filtered list
          navigate(`/applications?team=${selectedTeam.id}`);
        }
      } catch (error) {
        console.error('Error fetching team applications:', error);
      }
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 8 }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 6,
          textAlign: 'center',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderRadius: 2
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography 
            variant="h2" 
            component="h1"
            sx={{ 
              fontWeight: 'bold',
              color: 'primary.main'
            }}
          >
            Application Risk Score
          </Typography>
          
          {syncingCatalog && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CircularProgress size={20} />
              <Typography variant="body2" color="text.secondary">
                Syncing with App Catalog...
              </Typography>
            </Box>
          )}
        </Box>

        <Box sx={{ maxWidth: 600, mx: 'auto' }}>
          <Stack spacing={4}>
            <Box>
              <Typography variant="h6" gutterBottom sx={{ textAlign: 'left' }}>
                Search by Application
              </Typography>
              <Autocomplete
                value={selectedApp}
                onChange={(event, newValue) => {
                  setSelectedApp(newValue);
                  setSelectedTeam(null); // Clear team selection
                }}
                inputValue={appInputValue}
                onInputChange={(event, newInputValue) => {
                  setAppInputValue(newInputValue);
                  handleAppSearch(newInputValue);
                }}
                options={catalogApps}
                getOptionLabel={(option) => `${option.name}${option.vendor ? ' (Vendor)' : ''}`}
                renderOption={(props, option) => (
                  <Box component="li" {...props}>
                    <Box>
                      <Typography variant="body1">
                        {option.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {option.vendor ? `Vendor: ${option.vendor.name}` : 'Built Application'}
                      </Typography>
                    </Box>
                  </Box>
                )}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    placeholder="Search application catalog..."
                    InputProps={{
                      ...params.InputProps,
                      endAdornment: (
                        <>
                          {loading && <CircularProgress color="inherit" size={20} />}
                          {params.InputProps.endAdornment}
                        </>
                      ),
                    }}
                  />
                )}
              />
            </Box>

            <Divider>
              <Typography variant="body1" color="text.secondary">
                OR
              </Typography>
            </Divider>

            <Box>
              <Typography variant="h6" gutterBottom sx={{ textAlign: 'left' }}>
                Search by Team
              </Typography>
              <Autocomplete
                value={selectedTeam}
                onChange={(event, newValue) => {
                  setSelectedTeam(newValue);
                  setSelectedApp(null); // Clear application selection
                }}
                inputValue={teamInputValue}
                onInputChange={(event, newInputValue) => {
                  setTeamInputValue(newInputValue);
                  handleTeamSearch(newInputValue);
                }}
                options={teams}
                getOptionLabel={(option) => option.name}
                renderOption={(props, option) => (
                  <Box component="li" {...props}>
                    <Typography variant="body1">
                      {option.name}
                    </Typography>
                    {option.description && (
                      <Typography variant="body2" color="text.secondary">
                        {option.description}
                      </Typography>
                    )}
                  </Box>
                )}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    placeholder="Search teams..."
                    InputProps={{
                      ...params.InputProps,
                      endAdornment: (
                        <>
                          {loading && <CircularProgress color="inherit" size={20} />}
                          {params.InputProps.endAdornment}
                        </>
                      ),
                    }}
                  />
                )}
              />
            </Box>

            <Button
              variant="contained"
              size="large"
              onClick={handleViewResults}
              disabled={!selectedApp && !selectedTeam || loading || syncingCatalog}
              sx={{ 
                mt: 4,
                py: 2,
                fontSize: '1.1rem',
                width: '100%'
              }}
            >
              {loading || syncingCatalog ? 'Loading...' : 'View Risk Score'}
            </Button>
          </Stack>
        </Box>
      </Paper>
    </Container>
  );
}

export default ApplicationRiskSearch;
