import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  CircularProgress,
  LinearProgress,
  Alert,
  Box,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Tabs,
  Tab,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Security as SecurityIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Timeline as TimelineIcon
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import VulnerabilityFindings from './VulnerabilityFindings';
import useDataFetching from '../hooks/useDataFetching';
import LoadingState from './shared/LoadingState';
import ErrorState from './shared/ErrorState';
import ScoreDisplay from './shared/ScoreDisplay';
import { API_ENDPOINTS, ERROR_MESSAGES } from '../utils/constants';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

const severityColors = {
  critical: '#d32f2f',
  high: '#f44336',
  medium: '#ff9800',
  low: '#4caf50'
};

const RemediationItem = ({ title, description, severity, effort }) => (
  <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
      <Typography variant="h6">{title}</Typography>
      <Chip
        label={severity.toUpperCase()}
        sx={{ 
          bgcolor: severityColors[severity.toLowerCase()],
          color: 'white'
        }}
      />
    </Box>
    <Typography variant="body1" paragraph>
      {description}
    </Typography>
    <Typography variant="body2" color="text.secondary">
      Estimated effort: {effort}
    </Typography>
  </Paper>
);

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index} style={{ padding: '20px 0' }}>
      {value === index && children}
    </div>
  );
}

function ApplicationDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [scores, setScores] = useState([]);
  const [findings, setFindings] = useState([]);
  const [remediations, setRemediations] = useState([]);
  const [tabValue, setTabValue] = useState(0);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  const {
    data: application,
    loading,
    error,
    refetch
  } = useDataFetching(`${API_ENDPOINTS.APPLICATIONS}/${id}`);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [scoresResponse, findingsResponse, remediationsResponse] = await Promise.all([
          api.get(`/api/applications/${id}/scores`),
          api.get(`/api/applications/${id}/findings`),
          api.get(`/api/applications/${id}/remediations`)
        ]);

        setScores(scoresResponse.data);
        setFindings(findingsResponse.data);
        setRemediations(remediationsResponse.data);
      } catch (err) {
        console.error('[ApplicationDetails] Error fetching data:', err);
      }
    };

    fetchData();
  }, [id]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    const newRowsPerPage = parseInt(event.target.value, 10);
    setRowsPerPage(newRowsPerPage);
    setPage(0);
  };

  const getScoreColor = (score) => {
    if (!score && score !== 0) return 'default';
    score = Number(score);
    if (score >= 90) return 'success';
    if (score >= 70) return 'warning';
    return 'error';
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL':
        return 'error';
      case 'HIGH':
        return 'error';
      case 'MEDIUM':
        return 'warning';
      case 'LOW':
        return 'success';
      default:
        return 'default';
    }
  };

  if (loading) {
    return <LoadingState message="Loading application details..." />;
  }

  if (error) {
    return (
      <ErrorState 
        error={error || ERROR_MESSAGES.FETCH_ERROR}
        onRetry={refetch}
      />
    );
  }

  return (
    <Container>
      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          {application.name}
        </Typography>
        <Box display="flex" gap={1} mb={2}>
          <Chip 
            label={application.app_type} 
            color={application.app_type === 'BUILT' ? 'primary' : 'secondary'}
          />
          <Chip 
            label={`Team: ${application.team?.name || 'Unassigned'}`}
            variant="outlined"
          />
          {application.archer?.details?.business_unit && (
            <Chip 
              label={`Business Unit: ${application.archer.details.business_unit}`}
              variant="outlined"
            />
          )}
        </Box>
      </Box>

      <Paper>
        <Tabs value={tabValue} onChange={handleTabChange} variant="scrollable">
          <Tab label="Overview" />
          <Tab label="Risk & Compliance" />
          <Tab label="Vulnerabilities" />
          <Tab label="Remediation" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            {/* Application Details */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2, mb: 3 }}>
                <Typography variant="h6" gutterBottom>Application Details</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={3}>
                    <Typography variant="subtitle2">Name</Typography>
                    <Typography>{application.name}</Typography>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Typography variant="subtitle2">Type</Typography>
                    <Typography>{application.app_type}</Typography>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Typography variant="subtitle2">Team</Typography>
                    <Typography>{application.team_name || 'N/A'}</Typography>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Typography variant="subtitle2">Security Score</Typography>
                    <Chip
                      label={`${Math.round(application.security_score || 0)}%`}
                      color={getScoreColor(application.security_score)}
                      size="small"
                    />
                  </Grid>
                </Grid>
              </Paper>
            </Grid>

            {/* Score History */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>Score History</Typography>
                <Box sx={{ height: 300 }}>
                  <Line data={{
                    labels: scores.map(score => {
                      const date = new Date(score.date);
                      return `${date.getMonth() + 1}/${date.getDate()}`;
                    }),
                    datasets: [{
                      label: 'Security Score',
                      data: scores.map(score => score.score),
                      fill: false,
                      borderColor: '#1976d2',
                      tension: 0.1,
                    }]
                  }} options={{
                    responsive: true,
                    plugins: {
                      legend: { position: 'top' },
                      title: { display: true, text: 'Security Score History' }
                    },
                    scales: {
                      y: { beginAtZero: true, max: 100 }
                    }
                  }} />
                </Box>
              </Paper>
            </Grid>

            {/* Remediations */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>Recommended Remediations</Typography>
                {remediations.length > 0 ? (
                  <Grid container spacing={2}>
                    {remediations.map((remediation, index) => (
                      <Grid item xs={12} key={index}>
                        <RemediationItem
                          title={remediation.title}
                          description={remediation.description}
                          severity={remediation.severity}
                          effort={remediation.effort}
                        />
                      </Grid>
                    ))}
                  </Grid>
                ) : (
                  <Typography color="textSecondary">No remediation suggestions available</Typography>
                )}
              </Paper>
            </Grid>

            {/* Score Breakdown */}
            <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 3 }}>
              Score Breakdown
            </Typography>
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Rules Score
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={application.latest_score?.rules_score || 0}
                    sx={{ mb: 1, height: 10 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    Based on security rules evaluation
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    ML Score
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={application.latest_score?.ml_score || 0}
                    sx={{ mb: 1, height: 10 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    Based on machine learning prediction
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Final Score
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={application.latest_score?.final_score || 0}
                    sx={{ mb: 1, height: 10 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    Weighted combination of rules and ML
                  </Typography>
                </Paper>
              </Grid>
            </Grid>

            {/* Score Gauge */}
            <Grid item xs={12} sx={{ textAlign: 'center' }}>
              <ScoreDisplay 
                score={application.latest_score?.final_score || 0}
                size="large"
                tooltipText="Overall security score based on findings and compliance"
              />
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            {/* Vulnerability Findings Table */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2, mb: 3 }}>
                <Typography variant="h6" gutterBottom>Application Findings</Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell>Team</TableCell>
                        <TableCell>Security Score</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {findings
                        .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                        .map((finding) => (
                          <TableRow key={finding.id}>
                            <TableCell>{finding.name}</TableCell>
                            <TableCell>{finding.type || 'N/A'}</TableCell>
                            <TableCell>{finding.team || 'N/A'}</TableCell>
                            <TableCell>
                              <Chip
                                label={finding.score || 'N/A'}
                                color={getSeverityColor(finding.score)}
                                size="small"
                              />
                            </TableCell>
                            <TableCell>
                              <Typography variant="body2" color="textSecondary">
                                {new Date(finding.first_found).toLocaleDateString()}
                              </Typography>
                            </TableCell>
                          </TableRow>
                        ))}
                    </TableBody>
                  </Table>
                </TableContainer>
                <TablePagination
                  rowsPerPageOptions={[5, 10, 25]}
                  component="div"
                  count={findings.length}
                  rowsPerPage={rowsPerPage}
                  page={page}
                  onPageChange={handleChangePage}
                  onRowsPerPageChange={handleChangeRowsPerPage}
                />
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <VulnerabilityFindings applicationId={id} />
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              {remediations.map((remediation, index) => (
                <RemediationItem
                  key={index}
                  title={remediation.title}
                  description={remediation.description}
                  severity={remediation.severity}
                  effort={remediation.effort}
                />
              ))}
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>
    </Container>
  );
}

export default ApplicationDetails;
