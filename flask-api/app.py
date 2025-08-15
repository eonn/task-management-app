"""
Flask RESTful API for Task Management Application

Author: Eon (Himanshu Shekhar)
Email: eonhimanshu@gmail.com

This module provides task categories and filtering functionality.
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
api = Api(app)
CORS(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    """User model for Flask API."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class TaskCategory(db.Model):
    """Task Category model for Flask API."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#007bff')  # Hex color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Task(db.Model):
    """Task model for Flask API."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('task_category.id'))
    priority = db.Column(db.String(10), default='medium')
    status = db.Column(db.String(15), default='todo')
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    category = db.relationship('TaskCategory', backref=db.backref('tasks', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# API Resources
class CategoryResource(Resource):
    """Resource for task categories."""
    
    @jwt_required()
    def get(self, category_id=None):
        """Get all categories or a specific category."""
        if category_id:
            category = TaskCategory.query.get_or_404(category_id)
            return category.to_dict()
        
        categories = TaskCategory.query.all()
        return [category.to_dict() for category in categories]

    @jwt_required()
    def post(self):
        """Create a new category."""
        data = request.get_json()
        
        if not data or 'name' not in data:
            return {'error': 'Name is required'}, 400
        
        category = TaskCategory(
            name=data['name'],
            description=data.get('description', ''),
            color=data.get('color', '#007bff')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return category.to_dict(), 201

    @jwt_required()
    def put(self, category_id):
        """Update a category."""
        category = TaskCategory.query.get_or_404(category_id)
        data = request.get_json()
        
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'color' in data:
            category.color = data['color']
        
        db.session.commit()
        return category.to_dict()

    @jwt_required()
    def delete(self, category_id):
        """Delete a category."""
        category = TaskCategory.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return '', 204

class TaskFilterResource(Resource):
    """Resource for task filtering."""
    
    @jwt_required()
    def get(self):
        """Filter tasks by various criteria."""
        user_id = get_jwt_identity()
        
        # Base query
        query = Task.query.filter_by(user_id=user_id)
        
        # Filter by category
        category_id = request.args.get('category_id')
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        # Filter by status
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        # Filter by priority
        priority = request.args.get('priority')
        if priority:
            query = query.filter_by(priority=priority)
        
        # Filter by date range
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date)
                query = query.filter(Task.created_at >= start_date)
            except ValueError:
                return {'error': 'Invalid start_date format'}, 400
        
        if end_date:
            try:
                end_date = datetime.fromisoformat(end_date)
                query = query.filter(Task.created_at <= end_date)
            except ValueError:
                return {'error': 'Invalid end_date format'}, 400
        
        # Search by title or description
        search = request.args.get('search')
        if search:
            query = query.filter(
                db.or_(
                    Task.title.ilike(f'%{search}%'),
                    Task.description.ilike(f'%{search}%')
                )
            )
        
        # Sort by
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        if hasattr(Task, sort_by):
            if sort_order == 'desc':
                query = query.order_by(getattr(Task, sort_by).desc())
            else:
                query = query.order_by(getattr(Task, sort_by).asc())
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        tasks = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'tasks': [task.to_dict() for task in tasks.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': tasks.total,
                'pages': tasks.pages,
                'has_next': tasks.has_next,
                'has_prev': tasks.has_prev
            }
        }

class TaskStatsResource(Resource):
    """Resource for task statistics."""
    
    @jwt_required()
    def get(self):
        """Get task statistics for the current user."""
        user_id = get_jwt_identity()
        
        # Total tasks
        total_tasks = Task.query.filter_by(user_id=user_id).count()
        
        # Tasks by status
        status_stats = db.session.query(
            Task.status, db.func.count(Task.id)
        ).filter_by(user_id=user_id).group_by(Task.status).all()
        
        # Tasks by priority
        priority_stats = db.session.query(
            Task.priority, db.func.count(Task.id)
        ).filter_by(user_id=user_id).group_by(Task.priority).all()
        
        # Tasks by category
        category_stats = db.session.query(
            TaskCategory.name, db.func.count(Task.id)
        ).join(Task).filter_by(user_id=user_id).group_by(TaskCategory.name).all()
        
        # Completed tasks this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        completed_this_week = Task.query.filter(
            Task.user_id == user_id,
            Task.completed_at >= week_ago
        ).count()
        
        # Overdue tasks
        overdue_tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.due_date < datetime.utcnow(),
            Task.status != 'done'
        ).count()
        
        return {
            'total_tasks': total_tasks,
            'status_distribution': dict(status_stats),
            'priority_distribution': dict(priority_stats),
            'category_distribution': dict(category_stats),
            'completed_this_week': completed_this_week,
            'overdue_tasks': overdue_tasks
        }

# Register API resources
api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')
api.add_resource(TaskFilterResource, '/api/tasks/filter')
api.add_resource(TaskStatsResource, '/api/tasks/stats')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Create database tables
with app.app_context():
    db.create_all()
    
    # Create default categories if they don't exist
    default_categories = [
        {'name': 'Work', 'description': 'Work-related tasks', 'color': '#dc3545'},
        {'name': 'Personal', 'description': 'Personal tasks', 'color': '#28a745'},
        {'name': 'Shopping', 'description': 'Shopping tasks', 'color': '#ffc107'},
        {'name': 'Health', 'description': 'Health and fitness tasks', 'color': '#17a2b8'},
        {'name': 'Learning', 'description': 'Learning and education tasks', 'color': '#6f42c1'},
    ]
    
    for cat_data in default_categories:
        if not TaskCategory.query.filter_by(name=cat_data['name']).first():
            category = TaskCategory(**cat_data)
            db.session.add(category)
    
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 