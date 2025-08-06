// Authentication types
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

// List types
export interface List {
  id: string;
  name: string;
  description: string;
}

export interface CreateListRequest {
  name: string;
  description: string;
}

// Task types
export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  list_id: string;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  list_id: string;
}

// Component prop types
export interface FormProps {
  onSubmit: (data: any) => void;
  onCancel: () => void;
  isLoading: boolean;
}

export interface TaskItemProps {
  task: Task;
}

export interface ListItemProps {
  list: List;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
} 