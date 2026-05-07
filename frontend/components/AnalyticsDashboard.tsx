'use client'

import { useQuery } from '@tanstack/react-query'
import { ChartBarIcon, CheckCircleIcon, XCircleIcon, ClockIcon } from '@heroicons/react/24/outline'

interface AnalyticsData {
  total_tests: number
  total_executions: number
  pass_rate: number
  avg_duration: number
  failure_rate: number
  most_failed_tests: Array<{
    test_id: number
    title: string
    failures: number
  }>
  recent_activity: Array<{
    action: string
    count: number
    timestamp: string
  }>
  generated_at: string
}

export default function AnalyticsDashboard() {
  const { data: analytics, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: async (): Promise<AnalyticsData> => {
      // Mock data - in production would fetch from API
      return {
        total_tests: 150,
        total_executions: 1200,
        pass_rate: 87.5,
        avg_duration: 45.2,
        failure_rate: 12.5,
        most_failed_tests: [
          { test_id: 1, title: 'Login Test', failures: 15 },
          { test_id: 2, title: 'Checkout Test', failures: 12 }
        ],
        recent_activity: [
          { action: 'test_generated', count: 25, timestamp: new Date().toISOString() },
          { action: 'test_executed', count: 45, timestamp: new Date().toISOString() }
        ],
        generated_at: new Date().toISOString()
      }
    }
  })

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white p-6 rounded-lg shadow">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (!analytics) return null

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date(analytics.generated_at).toLocaleString()}
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <ChartBarIcon className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Tests</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.total_tests}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <CheckCircleIcon className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pass Rate</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.pass_rate}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <XCircleIcon className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Failure Rate</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.failure_rate}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <ClockIcon className="h-8 w-8 text-yellow-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Duration</p>
              <p className="text-2xl font-bold text-gray-900">{analytics.avg_duration}s</p>
            </div>
          </div>
        </div>
      </div>

      {/* Most Failed Tests */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Most Failed Tests</h2>
        <div className="space-y-3">
          {analytics.most_failed_tests.map((test) => (
            <div key={test.test_id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <div>
                <p className="font-medium text-gray-900">{test.title}</p>
                <p className="text-sm text-gray-600">ID: {test.test_id}</p>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-red-600">{test.failures}</p>
                <p className="text-sm text-gray-600">failures</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          {analytics.recent_activity.map((activity, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <div>
                <p className="font-medium text-gray-900 capitalize">
                  {activity.action.replace('_', ' ')}
                </p>
                <p className="text-sm text-gray-600">
                  {new Date(activity.timestamp).toLocaleString()}
                </p>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-blue-600">{activity.count}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}