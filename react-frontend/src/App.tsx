/**
 * Task Management Application - Main App Component
 * 
 * Author: Eon (Himanshu Shekhar)
 * Email: eonhimanshu@gmail.com
 * 
 * This is the main React application component that handles routing and authentication.
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/Dashboard';
import TaskList from './components/tasks/TaskList';
import TaskForm from './components/tasks/TaskForm';
import Analytics from './components/analytics/Analytics';
import './App.css';

// Create a client
const queryClient = new QueryClient();

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="App">
            <Navbar />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route 
                  path="/" 
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/tasks" 
                  element={
                    <ProtectedRoute>
                      <TaskList />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/tasks/new" 
                  element={
                    <ProtectedRoute>
                      <TaskForm />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/tasks/:id/edit" 
                  element={
                    <ProtectedRoute>
                      <TaskForm />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/analytics" 
                  element={
                    <ProtectedRoute>
                      <Analytics />
                    </ProtectedRoute>
                  } 
                />
              </Routes>
            </main>
          </div>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
