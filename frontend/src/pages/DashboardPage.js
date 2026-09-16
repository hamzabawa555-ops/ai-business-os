/**
 * Dashboard Page
 */

import React, { useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import Navbar from '../components/Navbar';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { user, fetchCurrentUser } = useAuthStore();

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const stats = [
    { label: 'Active Workflows', value: '5' },
    { label: 'Completed Tasks', value: '42' },
    { label: 'API Calls', value: '1,234' },
    { label: 'Saved Time', value: '24 hrs' },
  ];

  return (
    <>
      <Navbar />
      <Box sx={{ bgcolor: 'background.default', minHeight: '100vh', py: 4 }}>
        <Container maxWidth="lg">
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Welcome, {user?.first_name || 'User'}! 👋
            </Typography>
            <Typography variant="body1" color="text.secondary">
              {user?.company_name || 'Your Company'}
            </Typography>
          </Box>

          <Grid container spacing={3} sx={{ mb: 4 }}>
            {stats.map((stat, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      {stat.label}
                    </Typography>
                    <Typography variant="h5">{stat.value}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Quick Actions
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => navigate('/workflows')}
                    >
                      View Workflows
                    </Button>
                    <Button
                      variant="outlined"
                      color="primary"
                      onClick={() => navigate('/workflows')}
                    >
                      Create New Workflow
                    </Button>
                    <Button variant="outlined" color="primary">
                      View Reports
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </>
  );
};

export default DashboardPage;
