import { useEffect, useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import kpiService from '../../services/kpiService'
import { toast } from 'react-toastify'
import { Link } from 'react-router-dom'

function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const data = await kpiService.getDashboardStatistics()
      setStats(data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      {/* Welcome Card */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          Welcome back, {user?.full_name || user?.email}!
        </h2>
        <p className="text-gray-600">
          You are logged in as <span className="font-medium capitalize">{user?.role}</span>
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        {/* Total KPIs */}
        <div className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total KPIs</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.total_kpis || 0}</p>
            </div>
            <div className="text-4xl">🎯</div>
          </div>
          <div className="mt-4">
            <Link
              to="/kpis"
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              View all KPIs →
            </Link>
          </div>
        </div>

        {/* Pending Approval */}
        <div className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Pending Approval</p>
              <p className="text-3xl font-bold text-yellow-600">{stats?.pending_approval || 0}</p>
            </div>
            <div className="text-4xl">⏳</div>
          </div>
          <div className="mt-4">
            {user?.role !== 'employee' ? (
              <Link
                to="/approvals"
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                Review approvals →
              </Link>
            ) : (
              <span className="text-sm text-gray-500">Awaiting review</span>
            )}
          </div>
        </div>

        {/* Approved */}
        <div className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Approved</p>
              <p className="text-3xl font-bold text-green-600">{stats?.approved || 0}</p>
            </div>
            <div className="text-4xl">✅</div>
          </div>
          <div className="mt-4">
            <Link
              to="/kpis?status=approved"
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              View approved →
            </Link>
          </div>
        </div>

        {/* My KPIs */}
        <div className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">My KPIs</p>
              <p className="text-3xl font-bold text-blue-600">{stats?.my_kpis || 0}</p>
            </div>
            <div className="text-4xl">📊</div>
          </div>
          <div className="mt-4">
            <Link
              to="/kpis"
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Manage my KPIs →
            </Link>
          </div>
        </div>
      </div>

      {/* Progress Card */}
      <div className="card mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Overall Progress</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Average Progress</span>
              <span className="font-semibold text-gray-900">
                {stats?.average_progress?.toFixed(1) || 0}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                style={{ width: `${stats?.average_progress || 0}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/kpis/new"
            className="flex items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <span className="text-2xl mr-3">➕</span>
            <div>
              <p className="font-medium text-gray-900">Create New KPI</p>
              <p className="text-sm text-gray-600">Start a new KPI</p>
            </div>
          </Link>

          <Link
            to="/kpis?status=draft"
            className="flex items-center p-4 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors"
          >
            <span className="text-2xl mr-3">📝</span>
            <div>
              <p className="font-medium text-gray-900">Draft KPIs</p>
              <p className="text-sm text-gray-600">Continue working on drafts</p>
            </div>
          </Link>

          <Link
            to="/reports"
            className="flex items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
          >
            <span className="text-2xl mr-3">📈</span>
            <div>
              <p className="font-medium text-gray-900">View Reports</p>
              <p className="text-sm text-gray-600">Generate performance reports</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
