from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TaskAPITest(TestCase):
    """Test cases for Task API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'high',
            'status': 'todo'
        }
    
    def test_create_task_authenticated(self):
        """Test creating a task when authenticated."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/tasks/', self.task_data)
        print(f"Task creation response: {response.status_code} - {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user, self.user)
    
    def test_create_task_unauthenticated(self):
        """Test creating a task when not authenticated."""
        response = self.client.post('/api/tasks/', self.task_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_list_tasks_authenticated(self):
        """Test listing tasks when authenticated."""
        # Create some tasks
        task1 = Task.objects.create(
            title='Task 1',
            user=self.user,
            priority='high'
        )
        task2 = Task.objects.create(
            title='Task 2',
            user=self.user,
            priority='medium'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_list_tasks_unauthenticated(self):
        """Test listing tasks when not authenticated."""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_task_owner(self):
        """Test retrieving a task by its owner."""
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            priority='high'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')
    
    def test_retrieve_task_not_owner(self):
        """Test retrieving a task by non-owner."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            priority='high'
        )
        
        self.client.force_authenticate(user=other_user)
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_task_owner(self):
        """Test updating a task by its owner."""
        task = Task.objects.create(
            title='Original Title',
            user=self.user,
            priority='low'
        )
        
        update_data = {
            'title': 'Updated Title',
            'priority': 'high'
        }
        
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/tasks/{task.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')
        self.assertEqual(task.priority, 'high')
    
    def test_delete_task_owner(self):
        """Test deleting a task by its owner."""
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            priority='high'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_search_tasks(self):
        """Test searching tasks."""
        # Clear any existing tasks
        Task.objects.filter(user=self.user).delete()
        
        Task.objects.create(
            title='Python Task',
            description='Learn Python programming',
            user=self.user
        )
        Task.objects.create(
            title='Django Task',
            description='Learn Django framework',
            user=self.user
        )
        Task.objects.create(
            title='React Task',
            description='Learn React',
            user=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/tasks/search/', {'q': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Task')
    
    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status."""
        # Clear any existing tasks
        Task.objects.filter(user=self.user).delete()
        
        Task.objects.create(
            title='Todo Task',
            status='todo',
            user=self.user
        )
        Task.objects.create(
            title='Done Task',
            status='done',
            user=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/tasks/by_status/', {'status': 'todo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Todo Task')
    
    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        # Clear any existing tasks
        Task.objects.filter(user=self.user).delete()
        
        Task.objects.create(
            title='High Priority Task',
            priority='high',
            user=self.user
        )
        Task.objects.create(
            title='Low Priority Task',
            priority='low',
            user=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/tasks/by_priority/', {'priority': 'high'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'High Priority Task')

class UserAPITest(TestCase):
    """Test cases for User API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_registration(self):
        """Test user registration."""
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    
    def test_user_registration_duplicate_username(self):
        """Test user registration with duplicate username."""
        # Create user without password_confirm
        user_data = {k: v for k, v in self.user_data.items() if k != 'password_confirm'}
        User.objects.create_user(**user_data)
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login(self):
        """Test user login."""
        # Create user without password_confirm
        user_data = {k: v for k, v in self.user_data.items() if k != 'password_confirm'}
        User.objects.create_user(**user_data)
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials."""
        # Create user without password_confirm
        user_data = {k: v for k, v in self.user_data.items() if k != 'password_confirm'}
        User.objects.create_user(**user_data)
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/users/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_profile_authenticated(self):
        """Test getting user profile when authenticated."""
        # Create user without password_confirm
        user_data = {k: v for k, v in self.user_data.items() if k != 'password_confirm'}
        user = User.objects.create_user(**user_data)
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_user_profile_unauthenticated(self):
        """Test getting user profile when not authenticated."""
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 