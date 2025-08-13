# API Examples and Usage

This document provides comprehensive examples of API requests and responses for all three backend services.

## 🔐 Authentication

All APIs use JWT authentication. First, register and login to get your access token.

### Register User (Django API)

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### Login User (Django API)

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

## 📝 Task Management (Django API)

### Create Task

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the task management system",
    "priority": "high",
    "status": "todo",
    "due_date": "2024-01-15T00:00:00Z"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the task management system",
  "user": 1,
  "priority": "high",
  "status": "todo",
  "due_date": "2024-01-15T00:00:00Z",
  "completed_at": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Get All Tasks

```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "priority": "high",
      "status": "todo",
      "due_date": "2024-01-15T00:00:00Z",
      "user": "john_doe",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "title": "Review code changes",
      "priority": "medium",
      "status": "in_progress",
      "due_date": "2024-01-10T00:00:00Z",
      "user": "john_doe",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Update Task

```bash
curl -X PUT http://localhost:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "status": "in_progress",
    "priority": "urgent"
  }'
```

### Complete Task

```bash
curl -X POST http://localhost:8000/api/tasks/1/complete/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Search Tasks

```bash
curl -X GET "http://localhost:8000/api/tasks/search/?q=documentation" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🏷️ Category Management (Flask API)

### Create Category

```bash
curl -X POST http://localhost:5000/api/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Development",
    "description": "Software development tasks",
    "color": "#007bff"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Development",
  "description": "Software development tasks",
  "color": "#007bff",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Get All Categories

```bash
curl -X GET http://localhost:5000/api/categories \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Work",
    "description": "Work-related tasks",
    "color": "#dc3545",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "name": "Personal",
    "description": "Personal tasks",
    "color": "#28a745",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 3,
    "name": "Development",
    "description": "Software development tasks",
    "color": "#007bff",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Filter Tasks

```bash
curl -X GET "http://localhost:5000/api/tasks/filter?status=todo&priority=high&category_id=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive documentation",
      "user_id": 1,
      "category_id": 1,
      "category": {
        "id": 1,
        "name": "Work",
        "description": "Work-related tasks",
        "color": "#dc3545"
      },
      "priority": "high",
      "status": "todo",
      "due_date": "2024-01-15T00:00:00Z",
      "completed_at": null,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### Get Task Statistics

```bash
curl -X GET http://localhost:5000/api/tasks/stats \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "total_tasks": 5,
  "status_distribution": {
    "todo": 2,
    "in_progress": 2,
    "done": 1
  },
  "priority_distribution": {
    "low": 1,
    "medium": 2,
    "high": 2
  },
  "category_distribution": {
    "Work": 3,
    "Personal": 2
  },
  "completed_this_week": 1,
  "overdue_tasks": 1
}
```

## 📊 Analytics (FastAPI)

### Get Analytics Overview

```bash
curl -X GET http://localhost:8001/api/analytics/overview \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "total_tasks": 10,
  "completed_tasks": 6,
  "overdue_tasks": 2,
  "productivity_score": 60.0,
  "status_distribution": {
    "todo": 2,
    "in_progress": 2,
    "done": 6
  },
  "priority_distribution": {
    "low": 2,
    "medium": 4,
    "high": 3,
    "urgent": 1
  },
  "daily_completion_rate": [
    {
      "date": "2024-01-01",
      "completed": 2
    },
    {
      "date": "2024-01-02",
      "completed": 1
    },
    {
      "date": "2024-01-03",
      "completed": 3
    }
  ],
  "weekly_trends": {
    "tasks_created": 5,
    "tasks_completed": 6,
    "completion_rate": 120.0
  },
  "performance_metrics": {
    "average_completion_time_hours": 24.5,
    "tasks_per_day": 3.3,
    "efficiency_score": 54.0
  }
}
```

### Get Real-time Statistics

```bash
curl -X GET http://localhost:8001/api/analytics/realtime \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "active_tasks": 4,
  "completed_today": 2,
  "overdue_tasks": 1,
  "average_completion_time": 24.5,
  "top_priorities": [
    "Complete project documentation",
    "Review code changes",
    "Update dependencies"
  ]
}
```

### Get Performance Metrics

```bash
curl -X GET http://localhost:8001/api/analytics/performance \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "total_tasks": 10,
  "completion_rate": 60.0,
  "on_time_completion": 50.0,
  "average_task_duration": 24.5,
  "productivity_trend": [
    {
      "date": "2024-01-01",
      "productivity": 66.7
    },
    {
      "date": "2024-01-02",
      "productivity": 50.0
    },
    {
      "date": "2024-01-03",
      "productivity": 100.0
    }
  ],
  "category_performance": {},
  "priority_efficiency": {}
}
```

### Get Insights

```bash
curl -X GET http://localhost:8001/api/analytics/insights \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "recommendations": [
    {
      "type": "warning",
      "message": "You have 1 overdue tasks. Consider reviewing your priorities."
    },
    {
      "type": "suggestion",
      "message": "Your completion rate is below 70%. Try breaking down larger tasks into smaller ones."
    }
  ],
  "trends": {},
  "improvements": []
}
```

## 🔧 Error Handling

### Authentication Error

```json
{
  "detail": "Invalid token"
}
```

### Validation Error

```json
{
  "title": [
    "This field is required."
  ],
  "priority": [
    "\"invalid\" is not a valid choice."
  ]
}
```

### Not Found Error

```json
{
  "detail": "Not found."
}
```

## 📱 Frontend Integration

### React Query Example

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { taskService } from '../services/taskService';

// Fetch tasks
const { data: tasks, isLoading, error } = useQuery({
  queryKey: ['tasks'],
  queryFn: taskService.getTasks,
});

// Create task
const createTaskMutation = useMutation({
  mutationFn: taskService.createTask,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['tasks'] });
  },
});

// Update task
const updateTaskMutation = useMutation({
  mutationFn: ({ id, data }: { id: number; data: UpdateTaskData }) =>
    taskService.updateTask(id, data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['tasks'] });
  },
});
```

### Axios Interceptor Example

```typescript
// Add auth token to requests
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## 🧪 Testing Examples

### Python Testing (Django)

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'medium'
        }
        response = self.client.post(reverse('task-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
```

### JavaScript Testing (React)

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import TaskList from '../components/TaskList';

const queryClient = new QueryClient();

test('renders task list', async () => {
  render(
    <QueryClientProvider client={queryClient}>
      <TaskList />
    </QueryClientProvider>
  );
  
  await waitFor(() => {
    expect(screen.getByText('Complete project documentation')).toBeInTheDocument();
  });
});
```

## 📈 Performance Tips

1. **Use pagination** for large datasets
2. **Implement caching** for frequently accessed data
3. **Optimize database queries** with select_related/prefetch_related
4. **Use React Query** for efficient data fetching and caching
5. **Implement real-time updates** with WebSockets (planned)

## 🔒 Security Best Practices

1. **Always validate input** on both client and server
2. **Use HTTPS** in production
3. **Implement rate limiting** to prevent abuse
4. **Sanitize user input** to prevent XSS attacks
5. **Use environment variables** for sensitive configuration
6. **Regularly update dependencies** to patch security vulnerabilities 