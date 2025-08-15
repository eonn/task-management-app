"""
Django Views for Task Management Application

Author: Eon (Himanshu Shekhar)
Email: eonhimanshu@gmail.com

This module contains the API viewsets for users and tasks.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import User, Task
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    TaskSerializer, TaskListSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login user and return JWT tokens."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for Task model."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter tasks by current user."""
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        """Set the user to the current user when creating a task."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search tasks by title or description."""
        query = request.query_params.get('q', '')
        if query:
            tasks = self.get_queryset().filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            tasks = self.get_queryset()
        
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Filter tasks by status."""
        status_filter = request.query_params.get('status', '')
        if status_filter:
            tasks = self.get_queryset().filter(status=status_filter)
        else:
            tasks = self.get_queryset()
        
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        """Filter tasks by priority."""
        priority_filter = request.query_params.get('priority', '')
        if priority_filter:
            tasks = self.get_queryset().filter(priority=priority_filter)
        else:
            tasks = self.get_queryset()
        
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a task as completed."""
        task = self.get_object()
        task.status = 'done'
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a task."""
        task = self.get_object()
        task.status = 'cancelled'
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data) 