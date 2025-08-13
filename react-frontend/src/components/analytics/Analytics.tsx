import React from 'react';
import { useQuery } from '@tanstack/react-query';

const Analytics: React.FC = () => {
  // Mock data for now - this would be replaced with actual API calls
  const mockAnalytics = {
    totalTasks: 25,
    completedTasks: 18,
    inProgressTasks: 5,
    pendingTasks: 2,
    overdueTasks: 1,
    completionRate: 72,
    averageCompletionTime: 3.2,
    priorityDistribution: {
      urgent: 3,
      high: 8,
      medium: 10,
      low: 4,
    },
    statusDistribution: {
      done: 18,
      in_progress: 5,
      review: 1,
      todo: 1,
      cancelled: 0,
    },
    weeklyProgress: [
      { week: 'Week 1', completed: 5, total: 8 },
      { week: 'Week 2', completed: 7, total: 10 },
      { week: 'Week 3', completed: 6, total: 7 },
    ],
  };

  const { data: analytics = mockAnalytics, isLoading, error } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => Promise.resolve(mockAnalytics), // Replace with actual API call
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-xl text-gray-600">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 text-xl mb-4">Error loading analytics</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Track your productivity and task management performance
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                <span className="text-white font-semibold">T</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Tasks</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.totalTasks}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                <span className="text-white font-semibold">C</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Completed</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.completedTasks}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                <span className="text-white font-semibold">P</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">In Progress</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.inProgressTasks}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center">
                <span className="text-white font-semibold">O</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Overdue</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.overdueTasks}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Completion Rate and Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Completion Rate</h2>
          <div className="flex items-center">
            <div className="flex-1">
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-green-500 h-4 rounded-full transition-all duration-300"
                  style={{ width: `${analytics.completionRate}%` }}
                ></div>
              </div>
            </div>
            <div className="ml-4">
              <span className="text-2xl font-bold text-gray-900">{analytics.completionRate}%</span>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {analytics.completedTasks} out of {analytics.totalTasks} tasks completed
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Average Completion Time</h2>
          <div className="text-center">
            <span className="text-4xl font-bold text-blue-600">{analytics.averageCompletionTime}</span>
            <p className="text-lg text-gray-600">days</p>
          </div>
          <p className="text-sm text-gray-600 mt-2 text-center">
            Average time to complete a task
          </p>
        </div>
      </div>

      {/* Priority and Status Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Priority Distribution</h2>
          <div className="space-y-3">
            {Object.entries(analytics.priorityDistribution).map(([priority, count]) => (
              <div key={priority} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 capitalize">{priority}</span>
                <div className="flex items-center">
                  <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="h-2 rounded-full"
                      style={{
                        width: `${(count / analytics.totalTasks) * 100}%`,
                        backgroundColor: 
                          priority === 'urgent' ? '#ef4444' :
                          priority === 'high' ? '#f97316' :
                          priority === 'medium' ? '#eab308' : '#22c55e'
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-900">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Status Distribution</h2>
          <div className="space-y-3">
            {Object.entries(analytics.statusDistribution).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {status.replace('_', ' ')}
                </span>
                <div className="flex items-center">
                  <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="h-2 rounded-full"
                      style={{
                        width: `${(count / analytics.totalTasks) * 100}%`,
                        backgroundColor: 
                          status === 'done' ? '#22c55e' :
                          status === 'in_progress' ? '#3b82f6' :
                          status === 'review' ? '#a855f7' :
                          status === 'cancelled' ? '#ef4444' : '#6b7280'
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-900">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Weekly Progress */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Weekly Progress</h2>
        <div className="space-y-4">
          {analytics.weeklyProgress.map((week, index) => (
            <div key={index} className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">{week.week}</span>
              <div className="flex items-center">
                <div className="w-32 bg-gray-200 rounded-full h-3 mr-3">
                  <div
                    className="bg-blue-500 h-3 rounded-full transition-all duration-300"
                    style={{ width: `${(week.completed / week.total) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-semibold text-gray-900">
                  {week.completed}/{week.total}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Analytics; 