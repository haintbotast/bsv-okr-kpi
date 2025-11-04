import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

function Sidebar() {
  const location = useLocation()
  const { user } = useAuth()

  const isActive = path => location.pathname === path

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊', roles: ['admin', 'manager', 'employee'] },
    { path: '/kpis', label: 'My KPIs', icon: '🎯', roles: ['admin', 'manager', 'employee'] },
    { path: '/approvals', label: 'Approvals', icon: '✅', roles: ['admin', 'manager'] },
    { path: '/reports', label: 'Reports', icon: '📈', roles: ['admin', 'manager', 'employee'] },
    { path: '/admin/users', label: 'Users', icon: '👥', roles: ['admin'] },
    { path: '/admin/templates', label: 'Templates', icon: '📋', roles: ['admin'] },
  ]

  const filteredNavItems = navItems.filter(item => item.roles.includes(user?.role))

  return (
    <aside className="w-64 bg-white border-r border-gray-200 h-full">
      <nav className="p-4 space-y-2">
        {filteredNavItems.map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
              isActive(item.path)
                ? 'bg-blue-50 text-blue-600 font-medium'
                : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
