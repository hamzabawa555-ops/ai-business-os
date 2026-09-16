/**
 * Workflow API Service
 */

import apiClient from '../config/apiClient';

const workflowService = {
  // Get all workflows
  getWorkflows: async (skip = 0, limit = 100, status = null) => {
    const params = { skip, limit };
    if (status) {
      params.status = status;
    }
    const response = await apiClient.get('/api/v1/workflows', { params });
    return response.data;
  },

  // Get single workflow
  getWorkflow: async (workflowId) => {
    const response = await apiClient.get(`/api/v1/workflows/${workflowId}`);
    return response.data;
  },

  // Create workflow
  createWorkflow: async (workflowData) => {
    const response = await apiClient.post('/api/v1/workflows', workflowData);
    return response.data;
  },

  // Update workflow
  updateWorkflow: async (workflowId, workflowData) => {
    const response = await apiClient.put(
      `/api/v1/workflows/${workflowId}`,
      workflowData
    );
    return response.data;
  },

  // Delete workflow
  deleteWorkflow: async (workflowId) => {
    const response = await apiClient.delete(`/api/v1/workflows/${workflowId}`);
    return response.data;
  },

  // Activate workflow
  activateWorkflow: async (workflowId) => {
    const response = await apiClient.post(
      `/api/v1/workflows/${workflowId}/activate`
    );
    return response.data;
  },

  // Pause workflow
  pauseWorkflow: async (workflowId) => {
    const response = await apiClient.post(
      `/api/v1/workflows/${workflowId}/pause`
    );
    return response.data;
  },

  // Execute workflow
  executeWorkflow: async (workflowId) => {
    const response = await apiClient.post(
      `/api/v1/workflows/${workflowId}/execute`
    );
    return response.data;
  },

  // Get workflow executions
  getWorkflowExecutions: async (workflowId, skip = 0, limit = 100) => {
    const response = await apiClient.get(
      `/api/v1/workflows/${workflowId}/executions`,
      { params: { skip, limit } }
    );
    return response.data;
  },
};

export default workflowService;
