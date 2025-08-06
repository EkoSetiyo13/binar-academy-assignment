import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add authentication interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

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

// Authentication interfaces
export interface User {
  id: string;
  username: string;
  email: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export const authApi = {
  // Register a new user
  register: async (data: RegisterRequest): Promise<User> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  // Login user
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  // Get current user info
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};

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
