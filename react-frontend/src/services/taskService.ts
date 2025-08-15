/**
 * Task Service for Task Management Application
 * 
 * Author: Eon (Himanshu Shekhar)
 * Email: eonhimanshu@gmail.com
 * 
 * This service handles task CRUD operations and filtering.
 */

import axios from 'axios';

const DJANGO_API_URL = 'http://localhost:8000/api';
const FLASK_API_URL = 'http://localhost:5000/api';

// Django API for CRUD operations
const djangoApi = axios.create({
  baseURL: DJANGO_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Flask API for filtering and categories
const flaskApi = axios.create({
  baseURL: FLASK_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
const addAuthToken = (config: any) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

djangoApi.interceptors.request.use(addAuthToken);
flaskApi.interceptors.request.use(addAuthToken);

export interface Task {
  id: number;
  title: string;
  description?: string;
  user: number;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'todo' | 'in_progress' | 'review' | 'done' | 'cancelled';
  due_date?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCategory {
  id: number;
  name: string;
  description?: string;
  color: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  status?: 'todo' | 'in_progress' | 'review' | 'done' | 'cancelled';
  due_date?: string;
}

export interface UpdateTaskData extends Partial<CreateTaskData> {}

export interface TaskFilterParams {
  category_id?: number;
  status?: string;
  priority?: string;
  search?: string;
  start_date?: string;
  end_date?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  page?: number;
  per_page?: number;
}

export interface TaskStats {
  total_tasks: number;
  completed_tasks: number;
  overdue_tasks: number;
  productivity_score: number;
  status_distribution: Record<string, number>;
  priority_distribution: Record<string, number>;
}

class TaskService {
  // Django API - CRUD operations
  async getTasks(): Promise<Task[]> {
    const response = await djangoApi.get('/tasks/');
    return response.data.results || response.data;
  }

  async getTask(id: number): Promise<Task> {
    const response = await djangoApi.get(`/tasks/${id}/`);
    return response.data;
  }

  async createTask(taskData: CreateTaskData): Promise<Task> {
    const response = await djangoApi.post('/tasks/', taskData);
    return response.data;
  }

  async updateTask(id: number, taskData: UpdateTaskData): Promise<Task> {
    const response = await djangoApi.put(`/tasks/${id}/`, taskData);
    return response.data;
  }

  async deleteTask(id: number): Promise<void> {
    await djangoApi.delete(`/tasks/${id}/`);
  }

  async completeTask(id: number): Promise<Task> {
    const response = await djangoApi.post(`/tasks/${id}/complete/`);
    return response.data;
  }

  async cancelTask(id: number): Promise<Task> {
    const response = await djangoApi.post(`/tasks/${id}/cancel/`);
    return response.data;
  }

  async searchTasks(query: string): Promise<Task[]> {
    const response = await djangoApi.get(`/tasks/search/?q=${encodeURIComponent(query)}`);
    return response.data;
  }

  async getTasksByStatus(status: string): Promise<Task[]> {
    const response = await djangoApi.get(`/tasks/by_status/?status=${status}`);
    return response.data;
  }

  async getTasksByPriority(priority: string): Promise<Task[]> {
    const response = await djangoApi.get(`/tasks/by_priority/?priority=${priority}`);
    return response.data;
  }

  // Flask API - Filtering and categories
  async getCategories(): Promise<TaskCategory[]> {
    const response = await flaskApi.get('/categories');
    return response.data;
  }

  async getCategory(id: number): Promise<TaskCategory> {
    const response = await flaskApi.get(`/categories/${id}`);
    return response.data;
  }

  async createCategory(categoryData: Partial<TaskCategory>): Promise<TaskCategory> {
    const response = await flaskApi.post('/categories', categoryData);
    return response.data;
  }

  async updateCategory(id: number, categoryData: Partial<TaskCategory>): Promise<TaskCategory> {
    const response = await flaskApi.put(`/categories/${id}`, categoryData);
    return response.data;
  }

  async deleteCategory(id: number): Promise<void> {
    await flaskApi.delete(`/categories/${id}`);
  }

  async filterTasks(params: TaskFilterParams): Promise<{
    tasks: Task[];
    pagination: {
      page: number;
      per_page: number;
      total: number;
      pages: number;
      has_next: boolean;
      has_prev: boolean;
    };
  }> {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        queryParams.append(key, value.toString());
      }
    });

    const response = await flaskApi.get(`/tasks/filter?${queryParams.toString()}`);
    return response.data;
  }

  async getTaskStats(): Promise<TaskStats> {
    const response = await flaskApi.get('/tasks/stats');
    return response.data;
  }
}

export const taskService = new TaskService(); 