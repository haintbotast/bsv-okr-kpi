import { useAuth } from '../../hooks/useAuth'
import NotificationDropdown from '../notification/NotificationDropdown'

function Header() {
  const { user, logout } = useAuth()

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-4 py-4 flex items-center justify-between">
        {/* Title */}
        <h1 className="text-xl font-semibold text-gray-900">KPI Management System</h1>

        {/* User Menu */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <NotificationDropdown />

          <div className="text-right">
            <p className="text-sm font-medium text-gray-900">{user?.full_name || user?.email}</p>
            <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
          </div>

          <button
            onClick={logout}
            className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
