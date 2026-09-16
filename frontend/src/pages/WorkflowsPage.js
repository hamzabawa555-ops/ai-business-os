/**
 * Workflows Page
 */

import React, { useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import useWorkflowStore from '../store/workflowStore';
import Navbar from '../components/Navbar';

const statusColors = {
  draft: 'default',
  active: 'success',
  paused: 'warning',
  completed: 'info',
  failed: 'error',
};

const WorkflowsPage = () => {
  const navigate = useNavigate();
  const { workflows, isLoading, fetchWorkflows } = useWorkflowStore();

  useEffect(() => {
    fetchWorkflows();
  }, []);

  return (
    <>
      <Navbar />
      <Box sx={{ bgcolor: 'background.default', minHeight: '100vh', py: 4 }}>
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
            <Typography variant="h4" component="h1">
              Workflows
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate('/workflows/create')}
            >
              Create Workflow
            </Button>
          </Box>

          {isLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : workflows.length === 0 ? (
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="body1" color="text.secondary">
                No workflows yet. Create your first workflow to get started!
              </Typography>
              <Button
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
                onClick={() => navigate('/workflows/create')}
              >
                Create First Workflow
              </Button>
            </Paper>
          ) : (
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                    <TableCell>Name</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Trigger Type</TableCell>
                    <TableCell>Created</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {workflows.map((workflow) => (
                    <TableRow key={workflow.id} hover>
                      <TableCell>{workflow.name}</TableCell>
                      <TableCell>
                        <Chip
                          label={workflow.status}
                          color={statusColors[workflow.status] || 'default'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{workflow.trigger.type}</TableCell>
                      <TableCell>
                        {new Date(workflow.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <Button
                          size="small"
                          variant="text"
                          onClick={() => navigate(`/workflows/${workflow.id}`)}
                        >
                          View
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Container>
      </Box>
    </>
  );
};

export default WorkflowsPage;
