import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
} from '@mui/material';
import axios from 'axios';

function AddApplication() {
  const navigate = useNavigate();
  const [application, setApplication] = useState({
    name: '',
    description: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/applications', application);
      navigate('/');
    } catch (error) {
      console.error('Error creating application:', error);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Add New Application
      </Typography>
      <Card>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Application Name"
              value={application.name}
              onChange={(e) =>
                setApplication({ ...application, name: e.target.value })
              }
              fullWidth
              required
              margin="normal"
            />
            <TextField
              label="Description"
              value={application.description}
              onChange={(e) =>
                setApplication({ ...application, description: e.target.value })
              }
              fullWidth
              multiline
              rows={4}
              margin="normal"
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              sx={{ mt: 2 }}
            >
              Add Application
            </Button>
          </form>
        </CardContent>
      </Card>
    </Container>
  );
}

export default AddApplication;
