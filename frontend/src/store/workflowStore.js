/**
 * Workflow Store (Zustand)
 */

import { create } from 'zustand';
import workflowService from '../services/workflowService';

const useWorkflowStore = create((set, get) => ({
  workflows: [],
  currentWorkflow: null,
  isLoading: false,
  error: null,

  // Fetch workflows
  fetchWorkflows: async (skip = 0, limit = 100, status = null) => {
    set({ isLoading: true, error: null });
    try {
      const workflows = await workflowService.getWorkflows(skip, limit, status);
      set({ workflows, isLoading: false });
    } catch (error) {
      set({ isLoading: false, error: 'Failed to fetch workflows' });
    }
  },

  // Fetch single workflow
  fetchWorkflow: async (workflowId) => {
    set({ isLoading: true, error: null });
    try {
      const workflow = await workflowService.getWorkflow(workflowId);
      set({ currentWorkflow: workflow, isLoading: false });
    } catch (error) {
      set({ isLoading: false, error: 'Failed to fetch workflow' });
    }
  },

  // Create workflow
  createWorkflow: async (workflowData) => {
    set({ isLoading: true, error: null });
    try {
      const workflow = await workflowService.createWorkflow(workflowData);
      set((state) => ({
        workflows: [...state.workflows, workflow],
        isLoading: false,
      }));
      return workflow;
    } catch (error) {
      set({ isLoading: false, error: 'Failed to create workflow' });
      throw error;
    }
  },

  // Update workflow
  updateWorkflow: async (workflowId, workflowData) => {
    set({ isLoading: true, error: null });
    try {
      const workflow = await workflowService.updateWorkflow(
        workflowId,
        workflowData
      );
      set((state) => ({
        workflows: state.workflows.map((w) =>
          w.id === workflowId ? workflow : w
        ),
        currentWorkflow: workflow,
        isLoading: false,
      }));
      return workflow;
    } catch (error) {
      set({ isLoading: false, error: 'Failed to update workflow' });
      throw error;
    }
  },

  // Delete workflow
  deleteWorkflow: async (workflowId) => {
    set({ isLoading: true, error: null });
    try {
      await workflowService.deleteWorkflow(workflowId);
      set((state) => ({
        workflows: state.workflows.filter((w) => w.id !== workflowId),
        isLoading: false,
      }));
    } catch (error) {
      set({ isLoading: false, error: 'Failed to delete workflow' });
      throw error;
    }
  },

  // Clear error
  clearError: () => set({ error: null }),
}));

export default useWorkflowStore;
