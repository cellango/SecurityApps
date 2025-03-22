import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Link,
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineContent,
  TimelineSeparator,
  TimelineDot,
} from '@mui/lab';
import {
  ErrorOutline as CriticalIcon,
  Warning as HighIcon,
  Info as MediumIcon,
  CheckCircleOutline as LowIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Sync as SyncIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
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
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend
);

function SecurityDashboard({ applicationId }) {
  const [score, setScore] = useState(null);
  const [priorities, setPriorities] = useState([]);
  const [scoreHistory, setScoreHistory] = useState([]);
  const [findings, setFindings] = useState([]);
  const [application, setApplication] = useState(null);
  const [isSyncing, setIsSyncing] = useState(false);

  useEffect(() => {
    fetchData();
  }, [applicationId]);

  const fetchData = async () => {
    try {
      const [scoreRes, findingsRes, historyRes, appRes] = await Promise.all([
        axios.get(`http://localhost:5000/api/applications/${applicationId}/generate-score`),
        axios.get(`http://localhost:5000/api/applications/${applicationId}/findings`),
        axios.get(`http://localhost:5000/api/applications/${applicationId}/score-history`),
        axios.get(`http://localhost:5000/api/applications/${applicationId}`),
      ]);

      setScore(scoreRes.data.score);
      processFindings(findingsRes.data);
      setScoreHistory(historyRes.data);
      setApplication(appRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleSyncCatalog = async () => {
    if (!application?.catalog_id) return;

    setIsSyncing(true);
    try {
      await axios.post(`http://localhost:5000/api/applications/${applicationId}/sync`);
      await fetchData(); // Refresh data after sync
    } catch (error) {
      console.error('Error syncing with catalog:', error);
    } finally {
      setIsSyncing(false);
    }
  };

  const processFindings = (data) => {
    // Group findings by priority
    const priorityGroups = data.reduce((acc, finding) => {
      const priority = finding.severity.toLowerCase();
      if (!acc[priority]) {
        acc[priority] = [];
      }
      acc[priority].push(finding);
      return acc;
    }, {});

    setPriorities(priorityGroups);
    setFindings(data);
  };

  const getSeverityIcon = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return <CriticalIcon color="error" />;
      case 'high':
        return <HighIcon sx={{ color: '#ff9800' }} />;
      case 'medium':
        return <MediumIcon color="primary" />;
      case 'low':
        return <LowIcon color="success" />;
      default:
        return <InfoIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'open':
        return 'error';
      case 'in progress':
        return 'warning';
      case 'planned':
        return 'info';
      case 'closed':
        return 'success';
      default:
        return 'default';
    }
  };

  const calculateAction = (finding) => {
    const daysSinceOpen = Math.floor(
      (new Date() - new Date(finding.dateOpen)) / (1000 * 60 * 60 * 24)
    );

    if (finding.severity === 'CRITICAL' && daysSinceOpen > 7) {
      return 'IMMEDIATE ACTION REQUIRED';
    } else if (finding.severity === 'HIGH' && daysSinceOpen > 30) {
      return 'ESCALATE';
    } else if (finding.status === 'PLANNED' && new Date(finding.plannedCloseDate) < new Date()) {
      return 'OVERDUE';
    }
    return 'MONITOR';
  };

  const chartData = {
    labels: scoreHistory.map((item) =>
      new Date(item.timestamp).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    ),
    datasets: [
      {
        label: 'Security Score',
        data: scoreHistory.map((item) => item.score),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Security Score Trend',
      },
    },
    scales: {
      y: {
        min: 0,
        max: 100,
      },
    },
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      {/* Application Info */}
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h4">{application?.name}</Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {application?.app_type === 'vendor' ? 'Vendor Application' : 'Built Application'}
            </Typography>
          </Box>
          {application?.catalog_id && (
            <Button
              variant="outlined"
              onClick={handleSyncCatalog}
              disabled={isSyncing}
              startIcon={<SyncIcon />}
            >
              {isSyncing ? 'Syncing...' : 'Sync with Catalog'}
            </Button>
          )}
        </Box>
        {application?.app_type === 'vendor' && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body1">
              <strong>Vendor:</strong> {application.vendor_name}
            </Typography>
            <Typography variant="body1">
              <strong>Contact:</strong> {application.vendor_contact}
            </Typography>
            {application.support_url && (
              <Link href={application.support_url} target="_blank" rel="noopener">
                Support Portal
              </Link>
            )}
          </Box>
        )}
      </Paper>

      {/* Score Display */}
      <Paper
        elevation={3}
        sx={{
          p: 3,
          mb: 4,
          textAlign: 'center',
          background: `linear-gradient(45deg, 
            ${score >= 90 ? '#4caf50' : score >= 70 ? '#ff9800' : '#f44336'} 0%, 
            ${score >= 90 ? '#81c784' : score >= 70 ? '#ffb74d' : '#e57373'} 100%)`,
          color: 'white',
        }}
      >
        <Typography variant="h2">{score}</Typography>
        <Typography variant="h6">Security Score</Typography>
      </Paper>

      {/* Priority Findings */}
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h5">Priority Findings</Typography>
          {application?.app_type === 'vendor' && (
            <Chip
              label="Vendor Application"
              color="primary"
              variant="outlined"
            />
          )}
        </Box>
        <Timeline>
          {Object.entries(priorities).map(([severity, items]) => (
            <TimelineItem key={severity}>
              <TimelineSeparator>
                <TimelineDot color={getStatusColor(severity)}>
                  {getSeverityIcon(severity)}
                </TimelineDot>
              </TimelineSeparator>
              <TimelineContent>
                <Typography variant="h6" component="span">
                  {severity.toUpperCase()} ({items.length})
                </Typography>
                <Box sx={{ ml: 2 }}>
                  {items.map((finding) => (
                    <Typography key={finding.id} color="text.secondary">
                      {finding.title}
                    </Typography>
                  ))}
                </Box>
              </TimelineContent>
            </TimelineItem>
          ))}
        </Timeline>
      </Paper>

      {/* Score Trend */}
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          Score Trend
        </Typography>
        <Box sx={{ height: 300 }}>
          <Line data={chartData} options={chartOptions} />
        </Box>
      </Paper>

      {/* Security Findings Table */}
      <Paper elevation={3} sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h5">Security Findings</Typography>
          {application?.app_type === 'vendor' && (
            <Button
              variant="contained"
              color="primary"
              onClick={() => window.open(application.support_url, '_blank')}
              disabled={!application.support_url}
            >
              Open Vendor Support
            </Button>
          )}
        </Box>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Finding</TableCell>
                <TableCell>Application Name</TableCell>
                <TableCell>Severity</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Date Open</TableCell>
                <TableCell>Planned Close Date</TableCell>
                <TableCell>Comments</TableCell>
                <TableCell>Action</TableCell>
                <TableCell>Operations</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {findings.map((finding) => (
                <TableRow key={finding.id}>
                  <TableCell>{finding.title}</TableCell>
                  <TableCell>{finding.applicationName}</TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getSeverityIcon(finding.severity)}
                      {finding.severity}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={finding.status}
                      color={getStatusColor(finding.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(finding.dateOpen).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    {finding.plannedCloseDate
                      ? new Date(finding.plannedCloseDate).toLocaleDateString()
                      : 'N/A'}
                  </TableCell>
                  <TableCell>{finding.comments}</TableCell>
                  <TableCell>
                    <Chip
                      label={calculateAction(finding)}
                      color={
                        calculateAction(finding) === 'IMMEDIATE ACTION REQUIRED'
                          ? 'error'
                          : calculateAction(finding) === 'ESCALATE'
                          ? 'warning'
                          : 'default'
                      }
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Tooltip title="Edit">
                      <IconButton size="small">
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete">
                      <IconButton size="small" color="error">
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Container>
  );
}

export default SecurityDashboard;
