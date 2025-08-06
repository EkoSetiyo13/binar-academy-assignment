import api from './axios-config';
import { PerformanceMonitor } from '../utils/performance';
import type { Task, CreateTaskRequest } from '../types';

export const taskApi = {
  // Get all tasks
  getTasks: async (): Promise<Task[]> => {
    return PerformanceMonitor.measureAsync('task-get-all', async () => {
      const response = await api.get('/tasks');
      return response.data;
    });
  },

  // Get tasks for a specific list
  getTasksByList: async (listId: string): Promise<Task[]> => {
    return PerformanceMonitor.measureAsync(`task-get-by-list-${listId}`, async () => {
      const response = await api.get(`/lists/${listId}/tasks`);
      return response.data;
    });
  },

  // Get a specific task
  getTask: async (id: string): Promise<Task> => {
    return PerformanceMonitor.measureAsync(`task-get-${id}`, async () => {
      const response = await api.get(`/tasks/${id}`);
      return response.data;
    });
  },

  // Create a new task
  createTask: async (data: CreateTaskRequest): Promise<Task> => {
    return PerformanceMonitor.measureAsync('task-create', async () => {
      const response = await api.post('/tasks', data);
      return response.data;
    });
  },

  // Update a task
  updateTask: async (id: string, data: Partial<CreateTaskRequest & { completed: boolean }>): Promise<Task> => {
    return PerformanceMonitor.measureAsync(`task-update-${id}`, async () => {
      const response = await api.put(`/tasks/${id}`, data);
      return response.data;
    });
  },

  // Delete a task
  deleteTask: async (id: string): Promise<void> => {
    return PerformanceMonitor.measureAsync(`task-delete-${id}`, async () => {
      await api.delete(`/tasks/${id}`);
    });
  },

  // Toggle task completion
  toggleTask: async (id: string): Promise<Task> => {
    return PerformanceMonitor.measureAsync(`task-toggle-${id}`, async () => {
      const response = await api.patch(`/tasks/${id}/toggle`);
      return response.data;
    });
  },
}; 