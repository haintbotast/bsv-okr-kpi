import { useEffect, useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import kpiService from '../../services/kpiService'
import objectiveService from '../../services/objectiveService'
import { toast } from 'react-toastify'
import { Link } from 'react-router-dom'

function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [objectiveStats, setObjectiveStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const [kpiData, objectiveData] = await Promise.all([
        kpiService.getDashboardStatistics(),
        objectiveService.getStats({ year: new Date().getFullYear() })
      ])
      setStats(kpiData)
      setObjectiveStats(objectiveData)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const getLevelConfig = (level) => {
    const configs = {
      company: {
        icon: '🏢',
        label: 'Company Level',
        color: 'purple',
        bgClass: 'bg-purple-50',
        textClass: 'text-purple-700',
        progressClass: 'bg-purple-600',
        borderClass: 'border-purple-200',
      },
      unit: {
        icon: '🏛️',
        label: 'Unit Level',
        color: 'indigo',
        bgClass: 'bg-indigo-50',
        textClass: 'text-indigo-700',
        progressClass: 'bg-indigo-600',
        borderClass: 'border-indigo-200',
      },
      division: {
        icon: '🏬',
        label: 'Division Level',
        color: 'blue',
        bgClass: 'bg-blue-50',
        textClass: 'text-blue-700',
        progressClass: 'bg-blue-600',
        borderClass: 'border-blue-200',
      },
      team: {
        icon: '👥',
        label: 'Team Level',
        color: 'green',
        bgClass: 'bg-green-50',
        textClass: 'text-green-700',
        progressClass: 'bg-green-600',
        borderClass: 'border-green-200',
      },
      individual: {
        icon: '👤',
        label: 'Individual Level',
        color: 'yellow',
        bgClass: 'bg-yellow-50',
        textClass: 'text-yellow-700',
        progressClass: 'bg-yellow-600',
        borderClass: 'border-yellow-200',
      },
    }
    return configs[level] || configs.individual
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

      {/* KPI Progress Card */}
      <div className="card mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">KPI Overall Progress</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Average KPI Progress</span>
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

      {/* OKR Objectives Overview */}
      <div className="card mb-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-xl font-bold text-gray-900">OKR Objectives Overview</h3>
            <p className="text-sm text-gray-600 mt-1">
              Progress across all organizational levels for {new Date().getFullYear()}
            </p>
          </div>
          <Link
            to="/objectives"
            className="text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            View All Objectives →
          </Link>
        </div>

        {/* Overall Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">
              {objectiveStats?.total || 0}
            </p>
            <p className="text-sm text-gray-600">Total Objectives</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">
              {objectiveStats?.by_status?.active || 0}
            </p>
            <p className="text-sm text-gray-600">Active</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">
              {objectiveStats?.average_progress?.toFixed(1) || 0}%
            </p>
            <p className="text-sm text-gray-600">Avg Progress</p>
          </div>
        </div>

        {/* Progress by Level */}
        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Progress by Organizational Level</h4>
          {['company', 'unit', 'division', 'team', 'individual'].map((level) => {
            const config = getLevelConfig(level)
            const levelData = objectiveStats?.progress_by_level?.[level] || { count: 0, average_progress: 0 }
            const count = levelData.count
            const progress = levelData.average_progress

            return (
              <div
                key={level}
                className={`border-2 ${config.borderClass} rounded-lg p-4 ${config.bgClass} hover:shadow-md transition-all`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <span className="text-3xl">{config.icon}</span>
                    <div>
                      <h5 className={`font-semibold ${config.textClass}`}>
                        {config.label}
                      </h5>
                      <p className="text-sm text-gray-600">
                        {count} {count === 1 ? 'objective' : 'objectives'}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`text-2xl font-bold ${config.textClass}`}>
                      {progress.toFixed(1)}%
                    </p>
                    <p className="text-xs text-gray-600">avg progress</p>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="relative">
                  <div className="w-full bg-white rounded-full h-3 shadow-inner">
                    <div
                      className={`${config.progressClass} h-3 rounded-full transition-all duration-500 relative overflow-hidden`}
                      style={{ width: `${progress}%` }}
                    >
                      {/* Animated shimmer effect for progress > 0 */}
                      {progress > 0 && (
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-20 animate-shimmer"></div>
                      )}
                    </div>
                  </div>
                </div>

                {/* View Link */}
                {count > 0 && (
                  <div className="mt-3 text-right">
                    <Link
                      to={`/objectives?level=${level}`}
                      className={`text-sm font-medium ${config.textClass} hover:underline`}
                    >
                      View {config.label} Objectives →
                    </Link>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            to="/objectives/new"
            className="flex items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
          >
            <span className="text-2xl mr-3">🎯</span>
            <div>
              <p className="font-medium text-gray-900">Create Objective</p>
              <p className="text-sm text-gray-600">Define new OKR objective</p>
            </div>
          </Link>

          <Link
            to="/kpis/new"
            className="flex items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <span className="text-2xl mr-3">➕</span>
            <div>
              <p className="font-medium text-gray-900">Create KPI</p>
              <p className="text-sm text-gray-600">Start a new key result</p>
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
              <p className="text-sm text-gray-600">Performance analytics</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
