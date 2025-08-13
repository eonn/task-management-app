import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          Task Manager
        </Link>
        
        {isAuthenticated ? (
          <div className="navbar-menu">
            <Link to="/" className="navbar-item">
              Dashboard
            </Link>
            <Link to="/tasks" className="navbar-item">
              Tasks
            </Link>
            <Link to="/analytics" className="navbar-item">
              Analytics
            </Link>
          </div>
        ) : null}
        
        <div className="navbar-end">
          {isAuthenticated ? (
            <div className="navbar-user">
              <span className="username">Welcome, {user?.username}</span>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          ) : (
            <div className="navbar-auth">
              <Link to="/login" className="auth-btn login-btn">
                Login
              </Link>
              <Link to="/register" className="auth-btn register-btn">
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 