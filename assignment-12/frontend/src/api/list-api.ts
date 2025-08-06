import api from './axios-config';
import { PerformanceMonitor } from '../utils/performance';
import type { List, CreateListRequest } from '../types';

export const listApi = {
  // Get all lists
  getLists: async (): Promise<List[]> => {
    return PerformanceMonitor.measureAsync('list-get-all', async () => {
      const response = await api.get('/lists');
      return response.data;
    });
  },

  // Get a specific list
  getList: async (id: string): Promise<List> => {
    return PerformanceMonitor.measureAsync(`list-get-${id}`, async () => {
      const response = await api.get(`/lists/${id}`);
      return response.data;
    });
  },

  // Create a new list
  createList: async (data: CreateListRequest): Promise<List> => {
    return PerformanceMonitor.measureAsync('list-create', async () => {
      const response = await api.post('/lists', data);
      return response.data;
    });
  },

  // Update a list
  updateList: async (id: string, data: Partial<CreateListRequest>): Promise<List> => {
    return PerformanceMonitor.measureAsync(`list-update-${id}`, async () => {
      const response = await api.put(`/lists/${id}`, data);
      return response.data;
    });
  },

  // Delete a list
  deleteList: async (id: string): Promise<void> => {
    return PerformanceMonitor.measureAsync(`list-delete-${id}`, async () => {
      await api.delete(`/lists/${id}`);
    });
  },
}; 