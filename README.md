# Task Management Application

**Author:** Eon (Himanshu Shekhar)  
**Email:** eonhimanshu@gmail.com

A comprehensive task management system built with multiple web frameworks demonstrating integration between Django, Flask, FastAPI, and React.

## 🏗️ Architecture

This project demonstrates the integration of multiple web frameworks:

- **Django** - User authentication and task CRUD operations
- **Flask** - Task categories and filtering
- **FastAPI** - Real-time task statistics and analytics
- **React** - Modern frontend consuming all three APIs

## 📁 Project Structure

```
task-management-app/
├── django-api/          # Django REST API
├── flask-api/           # Flask RESTful API
├── fastapi-api/         # FastAPI Analytics API
├── react-frontend/      # React TypeScript Frontend
├── docker-compose.yml   # Docker orchestration
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-management-app
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Django API: http://localhost:8000/api
   - Flask API: http://localhost:5000/api
   - FastAPI: http://localhost:8001/api
   - FastAPI Docs: http://localhost:8001/docs

### Local Development

#### Django API Setup
```bash
cd django-api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### Flask API Setup
```bash
cd flask-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### FastAPI Setup
```bash
cd fastapi-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### React Frontend Setup
```bash
cd react-frontend
npm install
npm start
```

## 🔧 API Documentation

### Django API (Port 8000)

#### Authentication Endpoints
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `GET /api/users/profile/` - Get user profile

#### Task Endpoints
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/complete/` - Mark task as complete
- `POST /api/tasks/{id}/cancel/` - Cancel task
- `GET /api/tasks/search/?q={query}` - Search tasks
- `GET /api/tasks/by_status/?status={status}` - Filter by status
- `GET /api/tasks/by_priority/?priority={priority}` - Filter by priority

### Flask API (Port 5000)

#### Category Endpoints
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create new category
- `GET /api/categories/{id}` - Get specific category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

#### Filtering Endpoints
- `GET /api/tasks/filter` - Advanced task filtering
- `GET /api/tasks/stats` - Task statistics

### FastAPI (Port 8001)

#### Analytics Endpoints
- `GET /api/analytics/overview` - Comprehensive analytics overview
- `GET /api/analytics/realtime` - Real-time statistics
- `GET /api/analytics/performance` - Performance metrics
- `