import { useAuth } from '../../hooks/useAuth'

function DashboardPage() {
  const { user } = useAuth()

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
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total KPIs</p>
              <p className="text-3xl font-bold text-gray-900">0</p>
            </div>
            <div className="text-4xl">🎯</div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Pending Approval</p>
              <p className="text-3xl font-bold text-gray-900">0</p>
            </div>
            <div className="text-4xl">⏳</div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Approved</p>
              <p className="text-3xl font-bold text-gray-900">0</p>
            </div>
            <div className="text-4xl">✅</div>
          </div>
        </div>
      </div>

      {/* Phase 1 Complete Notice */}
      <div className="card bg-green-50 border border-green-200">
        <div className="flex items-start space-x-3">
          <span className="text-2xl">🎉</span>
          <div>
            <h3 className="font-semibold text-green-900 mb-1">Phase 1 Complete!</h3>
            <p className="text-green-800 text-sm">
              Authentication system is working. You can now proceed to Phase 2: KPI Management.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
