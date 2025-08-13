import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome back, {user?.first_name || user?.username}!
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Manage your tasks and stay organized
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <Link
                to="/tasks/new"
                className="block w-full bg-blue-600 text-white text-center py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
              >
                Create New Task
              </Link>
              <Link
                to="/tasks"
                className="block w-full bg-gray-600 text-white text-center py-2 px-4 rounded-md hover:bg-gray-700 transition-colors"
              >
                View All Tasks
              </Link>
              <Link
                to="/analytics"
                className="block w-full bg-green-600 text-white text-center py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
              >
                View Analytics
              </Link>
            </div>
          </div>

          {/* Recent Tasks */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Tasks</h2>
            <div className="text-gray-600">
              <p>No recent tasks</p>
              <Link
                to="/tasks"
                className="text-blue-600 hover:text-blue-800 text-sm mt-2 inline-block"
              >
                View all tasks →
              </Link>
            </div>
          </div>

          {/* Statistics */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Statistics</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Tasks:</span>
                <span className="font-semibold">0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Completed:</span>
                <span className="font-semibold text-green-600">0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">In Progress:</span>
                <span className="font-semibold text-yellow-600">0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Pending:</span>
                <span className="font-semibold text-red-600">0</span>
              </div>
            </div>
          </div>
        </div>

        {/* Getting Started */}
        <div className="mt-12 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Getting Started</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Create Tasks</h3>
              <p className="text-gray-600 text-sm">
                Start by creating your first task to get organized
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-green-600">2</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Track Progress</h3>
              <p className="text-gray-600 text-sm">
                Monitor your tasks and update their status as you work
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-600">3</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Analyze Performance</h3>
              <p className="text-gray-600 text-sm">
                View analytics to understand your productivity patterns
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 