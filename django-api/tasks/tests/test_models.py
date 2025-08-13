from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from tasks.models import Task
from datetime import datetime, timedelta

User = get_user_model()

class UserModelTest(TestCase):
    """Test cases for the User model."""
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_create_user(self):
        """Test creating a new user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.created_at)
        self.assertTrue(user.updated_at)
    
    def test_user_str_representation(self):
        """Test the string representation of a user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_user_email_unique(self):
        """Test that email must be unique."""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='test@example.com',
                password='testpass123'
            )

class TaskModelTest(TestCase):
    """Test cases for the Task model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'user': self.user,
            'priority': 'high',
            'status': 'todo',
            'due_date': timezone.now() + timedelta(days=1)
        }
    
    def test_create_task(self):
        """Test creating a new task."""
        task = Task.objects.create(**self.task_data)
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'This is a test task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.priority, 'high')
        self.assertEqual(task.status, 'todo')
        self.assertTrue(task.created_at)
        self.assertTrue(task.updated_at)
    
    def test_task_str_representation(self):
        """Test the string representation of a task."""
        task = Task.objects.create(**self.task_data)
        self.assertEqual(str(task), 'Test Task')
    
    def test_task_default_values(self):
        """Test default values for task fields."""
        task = Task.objects.create(
            title='Default Task',
            user=self.user
        )
        self.assertEqual(task.priority, 'medium')
        self.assertEqual(task.status, 'todo')
        self.assertIsNone(task.completed_at)
    
    def test_task_completed_at_auto_set(self):
        """Test that completed_at is automatically set when status changes to 'done'."""
        task = Task.objects.create(**self.task_data)
        self.assertIsNone(task.completed_at)
        
        # Change status to done
        task.status = 'done'
        task.save()
        self.assertIsNotNone(task.completed_at)
    
    def test_task_completed_at_cleared(self):
        """Test that completed_at is cleared when status changes from 'done'."""
        task = Task.objects.create(**self.task_data)
        task.status = 'done'
        task.save()
        self.assertIsNotNone(task.completed_at)
        
        # Change status back to todo
        task.status = 'todo'
        task.save()
        self.assertIsNone(task.completed_at)
    
    def test_task_ordering(self):
        """Test that tasks are ordered by created_at descending."""
        task1 = Task.objects.create(
            title='First Task',
            user=self.user
        )
        task2 = Task.objects.create(
            title='Second Task',
            user=self.user
        )
        
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], task2)  # Most recent first
        self.assertEqual(tasks[1], task1)
    
    def test_task_priority_choices(self):
        """Test that priority field accepts valid choices."""
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        for priority in valid_priorities:
            task = Task.objects.create(
                title=f'Task with {priority} priority',
                user=self.user,
                priority=priority
            )
            self.assertEqual(task.priority, priority)
    
    def test_task_status_choices(self):
        """Test that status field accepts valid choices."""
        valid_statuses = ['todo', 'in_progress', 'review', 'done', 'cancelled']
        for status in valid_statuses:
            task = Task.objects.create(
                title=f'Task with {status} status',
                user=self.user,
                status=status
            )
            self.assertEqual(task.status, status) 