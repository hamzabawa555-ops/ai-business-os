/**
 * Landing Page
 */

import React from 'react';
import {
  Container,
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

const features = [
  {
    title: 'AI-Powered Automation',
    description: 'Automate repetitive business tasks using machine learning',
  },
  {
    title: 'Workflow Management',
    description: 'Create and manage complex business workflows easily',
  },
  {
    title: 'Real-time Analytics',
    description: 'Get actionable insights with real-time business metrics',
  },
  {
    title: 'Enterprise Security',
    description: 'Bank-level security for your business data',
  },
  {
    title: 'Easy Integrations',
    description: 'Connect with popular business tools and services',
  },
  {
    title: 'Mobile Optimized',
    description: 'Manage your business on the go with mobile apps',
  },
];

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <>
      <Navbar />
      <Box sx={{ bgcolor: 'background.default' }}>
        {/* Hero Section */}
        <Box
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            py: 8,
            textAlign: 'center',
          }}
        >
          <Container maxWidth="md">
            <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
              🤖 AI Business OS
            </Typography>
            <Typography variant="h5" paragraph>
              AI-powered business automation platform for African businesses
            </Typography>
            <Typography variant="body1" paragraph sx={{ mb: 4, fontSize: '1.1rem' }}>
              Automate your business processes, reduce costs, and scale effortlessly
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button
                variant="contained"
                color="secondary"
                size="large"
                onClick={() => navigate('/register')}
              >
                Get Started Free
              </Button>
              <Button
                variant="outlined"
                size="large"
                sx={{ borderColor: 'white', color: 'white' }}
              >
                Watch Demo
              </Button>
            </Box>
          </Container>
        </Box>

        {/* Features Section */}
        <Container maxWidth="lg" sx={{ py: 8 }}>
          <Typography variant="h3" component="h2" gutterBottom sx={{ textAlign: 'center', mb: 6 }}>
            Powerful Features
          </Typography>
          <Grid container spacing={3}>
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>

        {/* CTA Section */}
        <Box sx={{ bgcolor: '#f5f5f5', py: 8, textAlign: 'center' }}>
          <Container maxWidth="sm">
            <Typography variant="h4" gutterBottom>
              Ready to transform your business?
            </Typography>
            <Typography variant="body1" paragraph color="text.secondary" sx={{ mb: 4 }}>
              Start automating your business processes today
            </Typography>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={() => navigate('/register')}
            >
              Start Free Trial
            </Button>
          </Container>
        </Box>

        {/* Footer */}
        <Box sx={{ bgcolor: '#333', color: 'white', py: 4, textAlign: 'center' }}>
          <Typography variant="body2">
            © 2026 AI Business OS. All rights reserved.
          </Typography>
        </Box>
      </Box>
    </>
  );
};

export default LandingPage;
