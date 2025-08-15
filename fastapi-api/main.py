"""
FastAPI Analytics API for Task Management Application

Author: Eon (Himanshu Shekhar)
Email: eonhimanshu@gmail.com

This module provides real-time task statistics and analytics endpoints.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from jose import JWTError, jwt as jose_jwt
from passlib.context import CryptContext
import asyncio
from collections import defaultdict

# FastAPI app initialization
app = FastAPI(
    title="Task Management Analytics API",
    description="Real-time task statistics and analytics API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./analytics.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    priority = Column(String)
    status = Column(String)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TaskAnalytics(Base):
    __tablename__ = "task_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    overdue_tasks = Column(Integer, default=0)
    productivity_score = Column(Integer, default=0)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "todo"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    overdue_tasks: int
    productivity_score: float
    status_distribution: Dict[str, int]
    priority_distribution: Dict[str, int]
    daily_completion_rate: List[Dict[str, Any]]
    weekly_trends: Dict[str, Any]
    performance_metrics: Dict[str, Any]

class RealTimeStats(BaseModel):
    active_tasks: int
    completed_today: int
    overdue_tasks: int
    average_completion_time: float
    top_priorities: List[str]

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Security functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jose_jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# API Endpoints
@app.post("/api/auth/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/analytics/overview", response_model=AnalyticsResponse)
async def get_analytics_overview(
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics overview."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all tasks for the user
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    
    # Calculate basic metrics
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == "done"])
    overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != "done"])
    
    # Calculate productivity score
    if total_tasks > 0:
        productivity_score = (completed_tasks / total_tasks) * 100
    else:
        productivity_score = 0
    
    # Status distribution
    status_distribution = defaultdict(int)
    for task in tasks:
        status_distribution[task.status] += 1
    
    # Priority distribution
    priority_distribution = defaultdict(int)
    for task in tasks:
        priority_distribution[task.priority] += 1
    
    # Daily completion rate (last 7 days)
    daily_completion_rate = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        completed_that_day = len([
            t for t in tasks 
            if t.completed_at and start_of_day <= t.completed_at < end_of_day
        ])
        
        daily_completion_rate.append({
            "date": start_of_day.date().isoformat(),
            "completed": completed_that_day
        })
    
    # Weekly trends
    week_ago = datetime.utcnow() - timedelta(days=7)
    tasks_last_week = [t for t in tasks if t.created_at >= week_ago]
    completed_last_week = [t for t in tasks_last_week if t.status == "done"]
    
    weekly_trends = {
        "tasks_created": len(tasks_last_week),
        "tasks_completed": len(completed_last_week),
        "completion_rate": len(completed_last_week) / len(tasks_last_week) * 100 if tasks_last_week else 0
    }
    
    # Performance metrics
    if completed_tasks > 0:
        avg_completion_time = sum([
            (t.completed_at - t.created_at).total_seconds() / 3600  # hours
            for t in tasks if t.completed_at
        ]) / completed_tasks
    else:
        avg_completion_time = 0
    
    performance_metrics = {
        "average_completion_time_hours": round(avg_completion_time, 2),
        "tasks_per_day": round(total_tasks / 30, 2) if total_tasks > 0 else 0,
        "efficiency_score": round(productivity_score * (1 - overdue_tasks / total_tasks) if total_tasks > 0 else 0, 2)
    }
    
    return AnalyticsResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        productivity_score=round(productivity_score, 2),
        status_distribution=dict(status_distribution),
        priority_distribution=dict(priority_distribution),
        daily_completion_rate=daily_completion_rate,
        weekly_trends=weekly_trends,
        performance_metrics=performance_metrics
    )

@app.get("/api/analytics/realtime", response_model=RealTimeStats)
async def get_realtime_stats(
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get real-time task statistics."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get current tasks
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    
    # Active tasks (not completed or cancelled)
    active_tasks = len([t for t in tasks if t.status not in ["done", "cancelled"]])
    
    # Completed today
    today = datetime.utcnow().date()
    completed_today = len([
        t for t in tasks 
        if t.completed_at and t.completed_at.date() == today
    ])
    
    # Overdue tasks
    overdue_tasks = len([
        t for t in tasks 
        if t.due_date and t.due_date < datetime.utcnow() and t.status != "done"
    ])
    
    # Average completion time
    completed_tasks = [t for t in tasks if t.completed_at]
    if completed_tasks:
        avg_completion_time = sum([
            (t.completed_at - t.created_at).total_seconds() / 3600
            for t in completed_tasks
        ]) / len(completed_tasks)
    else:
        avg_completion_time = 0
    
    # Top priorities (most common high priority tasks)
    high_priority_tasks = [t.title for t in tasks if t.priority == "high" and t.status != "done"]
    top_priorities = high_priority_tasks[:5]  # Top 5 high priority tasks
    
    return RealTimeStats(
        active_tasks=active_tasks,
        completed_today=completed_today,
        overdue_tasks=overdue_tasks,
        average_completion_time=round(avg_completion_time, 2),
        top_priorities=top_priorities
    )

@app.get("/api/analytics/performance")
async def get_performance_metrics(
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get detailed performance metrics."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    
    # Calculate various performance metrics
    metrics = {
        "total_tasks": len(tasks),
        "completion_rate": len([t for t in tasks if t.status == "done"]) / len(tasks) * 100 if tasks else 0,
        "on_time_completion": len([t for t in tasks if t.status == "done" and (not t.due_date or t.completed_at <= t.due_date)]) / len(tasks) * 100 if tasks else 0,
        "average_task_duration": 0,
        "productivity_trend": [],
        "category_performance": {},
        "priority_efficiency": {}
    }
    
    # Calculate average task duration
    completed_tasks = [t for t in tasks if t.completed_at]
    if completed_tasks:
        total_duration = sum([
            (t.completed_at - t.created_at).total_seconds() / 3600
            for t in completed_tasks
        ])
        metrics["average_task_duration"] = round(total_duration / len(completed_tasks), 2)
    
    # Productivity trend (last 30 days)
    for i in range(30):
        date = datetime.utcnow() - timedelta(days=i)
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        tasks_that_day = [t for t in tasks if start_of_day <= t.created_at < end_of_day]
        completed_that_day = [t for t in tasks_that_day if t.status == "done"]
        
        productivity = len(completed_that_day) / len(tasks_that_day) * 100 if tasks_that_day else 0
        
        metrics["productivity_trend"].append({
            "date": start_of_day.date().isoformat(),
            "productivity": round(productivity, 2)
        })
    
    return metrics

@app.get("/api/analytics/insights")
async def get_insights(
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get actionable insights and recommendations."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    
    insights = {
        "recommendations": [],
        "trends": {},
        "improvements": []
    }
    
    # Analyze patterns and generate insights
    if tasks:
        # Overdue tasks analysis
        overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != "done"]
        if overdue_tasks:
            insights["recommendations"].append({
                "type": "warning",
                "message": f"You have {len(overdue_tasks)} overdue tasks. Consider reviewing your priorities."
            })
        
        # Completion rate analysis
        completion_rate = len([t for t in tasks if t.status == "done"]) / len(tasks) * 100
        if completion_rate < 70:
            insights["recommendations"].append({
                "type": "suggestion",
                "message": "Your completion rate is below 70%. Try breaking down larger tasks into smaller ones."
            })
        
        # Priority distribution analysis
        high_priority_tasks = [t for t in tasks if t.priority == "high" and t.status != "done"]
        if len(high_priority_tasks) > 5:
            insights["recommendations"].append({
                "type": "alert",
                "message": "You have many high-priority tasks. Consider delegating or rescheduling some."
            })
    
    return insights

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 