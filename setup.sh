#!/bin/bash

# Task Management Application Setup Script
echo "🚀 Setting up Task Management Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories if they don't exist
echo "📁 Creating project structure..."
mkdir -p django-api/tasks
mkdir -p flask-api
mkdir -p fastapi-api
mkdir -p react-frontend

# Set up Django API
echo "🐍 Setting up Django API..."
cd django-api
if [ ! -f "requirements.txt" ]; then
    echo "❌ Django requirements.txt not found. Please ensure all files are present."
    exit 1
fi

# Set up Flask API
echo "🌶️ Setting up Flask API..."
cd ../flask-api
if [ ! -f "requirements.txt" ]; then
    echo "❌ Flask requirements.txt not found. Please ensure all files are present."
    exit 1
fi

# Set up FastAPI
echo "⚡ Setting up FastAPI..."
cd ../fastapi-api
if [ ! -f "requirements.txt" ]; then
    echo "❌ FastAPI requirements.txt not found. Please ensure all files are present."
    exit 1
fi

# Set up React Frontend
echo "⚛️ Setting up React Frontend..."
cd ../react-frontend
if [ ! -f "package.json" ]; then
    echo "❌ React package.json not found. Please ensure all files are present."
    exit 1
fi

# Return to project root
cd ..

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Django API: http://localhost:8000/api"
echo "   Flask API: http://localhost:5000/api"
echo "   FastAPI: http://localhost:8001/api"
echo "   FastAPI Docs: http://localhost:8001/docs"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Rebuild services: docker-compose up --build"
echo ""
echo "📚 For more information, see README.md" 