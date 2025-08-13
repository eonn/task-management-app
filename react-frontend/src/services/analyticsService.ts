import axios from 'axios';

const FASTAPI_URL = 'http://localhost:8000/api';

const analyticsApi = axios.create({
  baseURL: FASTAPI_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
analyticsApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface AnalyticsOverview {
  total_tasks: number;
  completed_tasks: number;
  overdue_tasks: number;
  productivity_score: number;
  status_distribution: Record<string, number>;
  priority_distribution: Record<string, number>;
  daily_completion_rate: Array<{
    date: string;
    completed: number;
  }>;
  weekly_trends: {
    tasks_created: number;
    tasks_completed: number;
    completion_rate: number;
  };
  performance_metrics: {
    average_completion_time_hours: number;
    tasks_per_day: number;
    efficiency_score: number;
  };
}

export interface RealTimeStats {
  active_tasks: number;
  completed_today: number;
  overdue_tasks: number;
  average_completion_time: number;
  top_priorities: string[];
}

export interface PerformanceMetrics {
  total_tasks: number;
  completion_rate: number;
  on_time_completion: number;
  average_task_duration: number;
  productivity_trend: Array<{
    date: string;
    productivity: number;
  }>;
  category_performance: Record<string, any>;
  priority_efficiency: Record<string, any>;
}

export interface Insights {
  recommendations: Array<{
    type: 'warning' | 'suggestion' | 'alert';
    message: string;
  }>;
  trends: Record<string, any>;
  improvements: string[];
}

class AnalyticsService {
  async getAnalyticsOverview(): Promise<AnalyticsOverview> {
    const response = await analyticsApi.get('/analytics/overview');
    return response.data;
  }

  async getRealTimeStats(): Promise<RealTimeStats> {
    const response = await analyticsApi.get('/analytics/realtime');
    return response.data;
  }

  async getPerformanceMetrics(): Promise<PerformanceMetrics> {
    const response = await analyticsApi.get('/analytics/performance');
    return response.data;
  }

  async getInsights(): Promise<Insights> {
    const response = await analyticsApi.get('/analytics/insights');
    return response.data;
  }

  // Polling for real-time updates
  startRealTimePolling(callback: (data: RealTimeStats) => void, interval: number = 30000) {
    const poll = async () => {
      try {
        const data = await this.getRealTimeStats();
        callback(data);
      } catch (error) {
        console.error('Error polling real-time stats:', error);
      }
    };

    // Initial call
    poll();

    // Set up interval
    const intervalId = setInterval(poll, interval);

    // Return cleanup function
    return () => clearInterval(intervalId);
  }

  // Get analytics data with caching
  async getCachedAnalytics(): Promise<AnalyticsOverview> {
    const cached = localStorage.getItem('analytics_cache');
    const cacheTime = localStorage.getItem('analytics_cache_time');
    
    // Check if cache is valid (less than 5 minutes old)
    if (cached && cacheTime) {
      const age = Date.now() - parseInt(cacheTime);
      if (age < 5 * 60 * 1000) { // 5 minutes
        return JSON.parse(cached);
      }
    }

    // Fetch fresh data
    const data = await this.getAnalyticsOverview();
    
    // Cache the data
    localStorage.setItem('analytics_cache', JSON.stringify(data));
    localStorage.setItem('analytics_cache_time', Date.now().toString());
    
    return data;
  }

  // Clear analytics cache
  clearCache(): void {
    localStorage.removeItem('analytics_cache');
    localStorage.removeItem('analytics_cache_time');
  }
}

export const analyticsService = new AnalyticsService(); 