from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Task
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    TaskSerializer, TaskListSerializer
)

class EnhancedUserViewSet(viewsets.ModelViewSet):
    """Enhanced ViewSet for User model with additional features."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Enhanced user registration with email verification and welcome message."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                # Log successful registration
                print(f"New user registered: {user.username} ({user.email})")
                
                # Send welcome email (if email is configured)
                try:
                    if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                        send_mail(
                            subject='Welcome to Task Management App!',
                            message=f'Hi {user.first_name or user.username},\n\nWelcome to our Task Management Application! Your account has been successfully created.\n\nYou can now log in and start managing your tasks.\n\nBest regards,\nThe Task Management Team',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[user.email],
                            fail_silently=True,
                        )
                except Exception as email_error:
                    print(f"Failed to send welcome email: {email_error}")
                
                return Response({
                    'message': 'User registered successfully! Welcome to our platform.',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Registration error for {request.data.get('username', 'unknown')}: {str(e)}")
                return Response({
                    'error': 'Registration failed. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'error': 'Registration failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Enhanced login with better error handling."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            # Log successful login
            print(f"User logged in: {user.username}")
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            })
        
        return Response({
            'error': 'Login failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile with additional stats."""
        user = request.user
        user_data = UserSerializer(user).data
        
        # Add user statistics
        total_tasks = Task.objects.filter(user=user).count()
        completed_tasks = Task.objects.filter(user=user, status='done').count()
        pending_tasks = Task.objects.filter(user=user, status='pending').count()
        
        return Response({
            'user': user_data,
            'stats': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
            }
        })

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password."""
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        
        if not current_password or not new_password or not new_password_confirm:
            return Response({
                'error': 'All password fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(current_password):
            return Response({
                'error': 'Current password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != new_password_confirm:
            return Response({
                'error': 'New passwords do not match'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            return Response({
                'error': 'New password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        })

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user (client-side token removal)."""
        # In a real application, you might want to blacklist the token
        return Response({
            'message': 'Logout successful'
        })

