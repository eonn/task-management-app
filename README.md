# Task Management Application

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
- `GET /api/analytics/insights` - Actionable insights

## 📊 Data Models

### User Model
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Task Model
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the project",
  "user": 1,
  "priority": "high",
  "status": "in_progress",
  "due_date": "2024-01-15T00:00:00Z",
  "completed_at": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Category Model
```json
{
  "id": 1,
  "name": "Work",
  "description": "Work-related tasks",
  "color": "#dc3545",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## 🔐 Authentication

The application uses JWT (JSON Web Tokens) for authentication:

1. **Register** a new user
2. **Login** to receive access and refresh tokens
3. **Include** the access token in the Authorization header:
   ```
   Authorization: Bearer <your-access-token>
   ```

## 🎨 Frontend Features

- **Modern UI** with responsive design
- **Real-time updates** using React Query
- **Authentication** with protected routes
- **Task management** with drag-and-drop (planned)
- **Analytics dashboard** with charts and insights
- **Category management** with color coding
- **Advanced filtering** and search capabilities

## 🧪 Testing

### API Testing
```bash
# Django API tests
cd django-api
python manage.py test

# Flask API tests
cd flask-api
python -m pytest

# FastAPI tests
cd fastapi-api
python -m pytest
```

### Frontend Testing
```bash
cd react-frontend
npm test
```

## 📈 Performance Features

- **Caching** with Redis
- **Database optimization** with proper indexing
- **API pagination** for large datasets
- **Real-time polling** for analytics
- **Lazy loading** for better UX

## 🔒 Security Features

- **JWT authentication** with refresh tokens
- **Password hashing** with bcrypt
- **CORS configuration** for cross-origin requests
- **Input validation** and sanitization
- **Rate limiting** (planned)

## 🚀 Deployment

### Production Setup
1. Update environment variables for production
2. Use production databases (PostgreSQL recommended)
3. Configure SSL certificates
4. Set up monitoring and logging
5. Use a reverse proxy (Nginx)

### Environment Variables
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# Flask
FLASK_ENV=production
SECRET_KEY=your-secret-key

# FastAPI
SECRET_KEY=your-secret-key

# React
REACT_APP_API_URL=https://your-api-domain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the code examples

## 🔄 Updates and Maintenance

- Regular dependency updates
- Security patches
- Performance improvements
- Feature additions

---

**Note**: This is a demonstration project showing integration between multiple web frameworks. For production use, consider using a single framework or microservices architecture based on your specific requirements. 