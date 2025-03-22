import React, { useState, useEffect } from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
} from '@mui/material';
import axios from 'axios';
import DraggableApplication from './DraggableApplication';
import GroupDropZone from './GroupDropZone';

function ApplicationGroups() {
  const [groups, setGroups] = useState([]);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [newGroup, setNewGroup] = useState({ name: '', description: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [groupsResponse, appsResponse] = await Promise.all([
        axios.get('http://localhost:5000/api/groups'),
        axios.get('http://localhost:5000/api/applications')
      ]);
      setGroups(groupsResponse.data);
      setApplications(appsResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateGroup = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/groups', newGroup);
      setGroups([...groups, response.data]);
      setOpenDialog(false);
      setNewGroup({ name: '', description: '' });
    } catch (error) {
      console.error('Error creating group:', error);
    }
  };

  const handleAddToGroup = async (groupId, applicationId) => {
    try {
      const response = await axios.post(
        `http://localhost:5000/api/groups/${groupId}/applications`,
        { application_id: applicationId }
      );
      setGroups(groups.map(g => g.id === groupId ? { ...g, ...response.data } : g));
    } catch (error) {
      console.error('Error adding to group:', error);
    }
  };

  const handleRemoveFromGroup = async (groupId, applicationId) => {
    try {
      const response = await axios.delete(
        `http://localhost:5000/api/groups/${groupId}/applications/${applicationId}`
      );
      setGroups(groups.map(g => g.id === groupId ? { ...g, ...response.data } : g));
    } catch (error) {
      console.error('Error removing from group:', error);
    }
  };

  if (loading) {
    return (
      <Container sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <DndProvider backend={HTML5Backend}>
      <Container sx={{ mt: 4 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
          <Typography variant="h4">Application Groups</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => setOpenDialog(true)}
          >
            Create New Group
          </Button>
        </div>

        <Grid container spacing={3}>
          {/* Available Applications */}
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Available Applications
                </Typography>
                {applications.map(app => (
                  <DraggableApplication
                    key={app.id}
                    application={app}
                    type="available"
                  />
                ))}
              </CardContent>
            </Card>
          </Grid>

          {/* Groups */}
          <Grid item xs={12} md={9}>
            <Grid container spacing={2}>
              {groups.map(group => (
                <Grid item xs={12} md={6} key={group.id}>
                  <GroupDropZone
                    group={group}
                    onAddApplication={handleAddToGroup}
                    onRemoveApplication={handleRemoveFromGroup}
                  />
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>

        {/* Create Group Dialog */}
        <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
          <DialogTitle>Create New Group</DialogTitle>
          <DialogContent>
            <TextField
              label="Group Name"
              value={newGroup.name}
              onChange={(e) => setNewGroup({ ...newGroup, name: e.target.value })}
              fullWidth
              margin="normal"
              required
            />
            <TextField
              label="Description"
              value={newGroup.description}
              onChange={(e) =>
                setNewGroup({ ...newGroup, description: e.target.value })
              }
              fullWidth
              margin="normal"
              multiline
              rows={4}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button onClick={handleCreateGroup} color="primary">
              Create
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </DndProvider>
  );
}

export default ApplicationGroups;
