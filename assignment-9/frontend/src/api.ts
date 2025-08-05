import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface List {
  id: string;
  name: string;
  description: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  list_id: string;
}

export interface CreateListRequest {
  name: string;
  description: string;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  list_id: string;
}

export const listApi = {
  // Get all lists
  getLists: async (): Promise<List[]> => {
    const response = await api.get('/lists');
    return response.data;
  },

  // Get a specific list
  getList: async (id: string): Promise<List> => {
    const response = await api.get(`/lists/${id}`);
    return response.data;
  },

  // Create a new list
  createList: async (data: CreateListRequest): Promise<List> => {
    const response = await api.post('/lists', data);
    return response.data;
  },

  // Update a list
  updateList: async (id: string, data: Partial<CreateListRequest>): Promise<List> => {
    const response = await api.put(`/lists/${id}`, data);
    return response.data;
  },

  // Delete a list
  deleteList: async (id: string): Promise<void> => {
    await api.delete(`/lists/${id}`);
  },
};

export const taskApi = {
  // Get all tasks
  getTasks: async (): Promise<Task[]> => {
    const response = await api.get('/tasks');
    return response.data;
  },

  // Get tasks for a specific list
  getTasksByList: async (listId: string): Promise<Task[]> => {
    const response = await api.get(`/lists/${listId}/tasks`);
    return response.data;
  },

  // Get a specific task
  getTask: async (id: string): Promise<Task> => {
    const response = await api.get(`/tasks/${id}`);
    return response.data;
  },

  // Create a new task
  createTask: async (data: CreateTaskRequest): Promise<Task> => {
    const response = await api.post('/tasks', data);
    return response.data;
  },

  // Update a task
  updateTask: async (id: string, data: Partial<CreateTaskRequest & { completed: boolean }>): Promise<Task> => {
    const response = await api.put(`/tasks/${id}`, data);
    return response.data;
  },

  // Delete a task
  deleteTask: async (id: string): Promise<void> => {
    await api.delete(`/tasks/${id}`);
  },

  // Toggle task completion
  toggleTask: async (id: string): Promise<Task> => {
    const response = await api.patch(`/tasks/${id}/toggle`);
    return response.data;
  },
};

export default api;
