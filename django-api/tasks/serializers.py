from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')

        return attrs

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'user', 'priority', 
            'status', 'due_date', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'completed_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        # The user will be set by the view
        task = Task.objects.create(**validated_data)
        return task

class TaskListSerializer(serializers.ModelSerializer):
    """Simplified serializer for task lists."""
    user = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'status', 'due_date', 'user', 'created_at'] 