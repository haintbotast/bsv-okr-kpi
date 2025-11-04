# Frontend Architecture - KPI Management System

**Stack**: React 18 + Vite + Tailwind CSS
**State Management**: React Context API + Hooks
**Routing**: React Router v6

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Component Hierarchy](#component-hierarchy)
3. [State Management](#state-management)
4. [Routing Structure](#routing-structure)
5. [API Client Architecture](#api-client-architecture)
6. [Form Handling](#form-handling)
7. [Authentication Flow](#authentication-flow)
8. [Best Practices](#best-practices)

---

## Project Structure

```
frontend/src/
├── main.jsx                 # Entry point
├── App.jsx                  # Root component
├── index.css               # Global styles (Tailwind)
│
├── components/             # Reusable components
│   ├── common/            # Generic UI components
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Card.jsx
│   │   ├── Modal.jsx
│   │   ├── Spinner.jsx
│   │   ├── Toast.jsx
│   │   └── Pagination.jsx
│   │
│   ├── layout/            # Layout components
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Footer.jsx
│   │   └── MainLayout.jsx
│   │
│   ├── kpi/              # KPI-specific components
│   │   ├── KPICard.jsx
│   │   ├── KPIForm.jsx
│   │   ├── KPIList.jsx
│   │   ├── KPIDetail.jsx
│   │   ├── KPIFilters.jsx
│   │   └── KPIStatusBadge.jsx
│   │
│   ├── file/             # File handling components
│   │   ├── FileUpload.jsx
│   │   ├── FileList.jsx
│   │   ├── FilePreview.jsx
│   │   └── DragDropZone.jsx
│   │
│   ├── chart/            # Chart components
│   │   ├── ProgressChart.jsx
│   │   ├── QuarterlyChart.jsx
│   │   └── ComparisonChart.jsx
│   │
│   └── auth/             # Authentication components
│       ├── LoginForm.jsx
│       ├── ProtectedRoute.jsx
│       └── RoleGuard.jsx
│
├── pages/                # Page components (routes)
│   ├── auth/
│   │   ├── LoginPage.jsx
│   │   └── ForgotPasswordPage.jsx
│   │
│   ├── dashboard/
│   │   └── DashboardPage.jsx
│   │
│   ├── kpi/
│   │   ├── KPIListPage.jsx
│   │   ├── KPICreatePage.jsx
│   │   ├── KPIEditPage.jsx
│   │   └── KPIDetailPage.jsx
│   │
│   ├── reports/
│   │   └── ReportsPage.jsx
│   │
│   ├── profile/
│   │   └── ProfilePage.jsx
│   │
│   └── admin/
│       ├── UsersPage.jsx
│       ├── TemplatesPage.jsx
│       └── SettingsPage.jsx
│
├── services/            # API services
│   ├── api.js          # Axios instance
│   ├── authService.js  # Authentication API
│   ├── kpiService.js   # KPI API
│   ├── userService.js  # User API
│   ├── fileService.js  # File upload/download
│   └── reportService.js # Reports API
│
├── contexts/           # React Context providers
│   ├── AuthContext.jsx
│   ├── ThemeContext.jsx
│   └── NotificationContext.jsx
│
├── hooks/              # Custom hooks
│   ├── useAuth.js
│   ├── useKPI.js
│   ├── useDebounce.js
│   ├── usePagination.js
│   └── useFileUpload.js
│
├── utils/              # Utility functions
│   ├── validation.js
│   ├── formatters.js
│   ├── constants.js
│   └── helpers.js
│
├── assets/            # Static assets
│   ├── images/
│   └── icons/
│
└── test/              # Test utilities
    ├── setup.js
    └── helpers.js
```

---

## Component Hierarchy

```
App
├── AuthContext.Provider
│   ├── NotificationContext.Provider
│   │   ├── Router
│   │   │   ├── LoginPage (public)
│   │   │   │
│   │   │   └── ProtectedRoute (authenticated)
│   │   │       └── MainLayout
│   │   │           ├── Header
│   │   │           │   ├── UserMenu
│   │   │           │   └── NotificationBell
│   │   │           │
│   │   │           ├── Sidebar
│   │   │           │   └── Navigation
│   │   │           │
│   │   │           ├── Main (route content)
│   │   │           │   ├── DashboardPage
│   │   │           │   │   ├── StatCard × 4
│   │   │           │   │   ├── ProgressChart
│   │   │           │   │   └── RecentKPIList
│   │   │           │   │
│   │   │           │   ├── KPIListPage
│   │   │           │   │   ├── KPIFilters
│   │   │           │   │   ├── KPIList
│   │   │           │   │   │   └── KPICard × N
│   │   │           │   │   └── Pagination
│   │   │           │   │
│   │   │           │   ├── KPIDetailPage
│   │   │           │   │   ├── KPIDetail
│   │   │           │   │   ├── FileList
│   │   │           │   │   ├── CommentSection
│   │   │           │   │   └── ActivityTimeline
│   │   │           │   │
│   │   │           │   └── (other pages...)
│   │   │           │
│   │   │           └── Footer
│   │   │
│   │   └── Toast (global notifications)
```

---

## State Management

### 1. AuthContext

**Purpose**: Manage user authentication state globally.

```jsx
// contexts/AuthContext.jsx
import { createContext, useState, useEffect } from 'react'
import { authService } from '@services/authService'

export const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem('access_token')
    if (token) {
      loadUser()
    } else {
      setLoading(false)
    }
  }, [])

  const loadUser = async () => {
    try {
      const userData = await authService.getCurrentUser()
      setUser(userData)
      setIsAuthenticated(true)
    } catch (error) {
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const response = await authService.login(email, password)
    localStorage.setItem('access_token', response.access_token)
    localStorage.setItem('refresh_token', response.refresh_token)
    setUser(response.user)
    setIsAuthenticated(true)
    return response
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    setIsAuthenticated(false)
  }

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    hasRole: role => user?.role === role,
    isAdmin: () => user?.role === 'admin',
    isManager: () => ['admin', 'manager'].includes(user?.role),
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
```

**Usage**:
```jsx
import { useAuth } from '@hooks/useAuth'

function MyComponent() {
  const { user, isAuthenticated, logout } = useAuth()

  if (!isAuthenticated) return <LoginPage />

  return <div>Welcome, {user.full_name}!</div>
}
```

### 2. NotificationContext

**Purpose**: Manage toast notifications and in-app notifications.

```jsx
// contexts/NotificationContext.jsx
import { createContext, useState, useCallback } from 'react'
import { toast } from 'react-toastify'

export const NotificationContext = createContext(null)

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([])

  const showToast = useCallback((message, type = 'info') => {
    toast[type](message, {
      position: 'top-right',
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
    })
  }, [])

  const addNotification = useCallback(notification => {
    setNotifications(prev => [notification, ...prev])
  }, [])

  const markAsRead = useCallback(id => {
    setNotifications(prev =>
      prev.map(n => (n.id === id ? { ...n, is_read: true } : n))
    )
  }, [])

  const value = {
    notifications,
    showToast,
    addNotification,
    markAsRead,
    unreadCount: notifications.filter(n => !n.is_read).length,
  }

  return <NotificationContext.Provider value={value}>{children}</NotificationContext.Provider>
}
```

---

## Routing Structure

```jsx
// App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@contexts/AuthContext'
import ProtectedRoute from '@components/auth/ProtectedRoute'
import MainLayout from '@components/layout/MainLayout'

// Pages
import LoginPage from '@pages/auth/LoginPage'
import DashboardPage from '@pages/dashboard/DashboardPage'
import KPIListPage from '@pages/kpi/KPIListPage'
import KPIDetailPage from '@pages/kpi/KPIDetailPage'
import KPICreatePage from '@pages/kpi/KPICreatePage'
import ReportsPage from '@pages/reports/ReportsPage'
import ProfilePage from '@pages/profile/ProfilePage'
import UsersPage from '@pages/admin/UsersPage'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />

            {/* KPI routes */}
            <Route path="/kpis" element={<KPIListPage />} />
            <Route path="/kpis/create" element={<KPICreatePage />} />
            <Route path="/kpis/:id" element={<KPIDetailPage />} />
            <Route path="/kpis/:id/edit" element={<KPICreatePage />} />

            {/* Reports */}
            <Route path="/reports" element={<ReportsPage />} />

            {/* Profile */}
            <Route path="/profile" element={<ProfilePage />} />

            {/* Admin routes (role-based) */}
            <Route
              path="/admin/users"
              element={
                <ProtectedRoute requiredRole="admin">
                  <UsersPage />
                </ProtectedRoute>
              }
            />
          </Route>

          {/* 404 */}
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
```

### Route Guard Component

```jsx
// components/auth/ProtectedRoute.jsx
import { Navigate } from 'react-router-dom'
import { useAuth } from '@hooks/useAuth'

function ProtectedRoute({ children, requiredRole }) {
  const { isAuthenticated, user, loading } = useAuth()

  if (loading) {
    return <div>Loading...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && user.role !== requiredRole && user.role !== 'admin') {
    return <div>Access Denied</div>
  }

  return children
}
```

---

## API Client Architecture

### Base Axios Instance

```js
// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor - handle token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${api.defaults.baseURL}/auth/refresh`, {
          refresh_token: refreshToken,
        })

        const { access_token } = response.data
        localStorage.setItem('access_token', access_token)

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api
```

### Service Layer Example

```js
// services/kpiService.js
import api from './api'

export const kpiService = {
  // Get all KPIs with filters
  getAll: async (filters = {}) => {
    const response = await api.get('/kpis', { params: filters })
    return response.data
  },

  // Get single KPI
  getById: async id => {
    const response = await api.get(`/kpis/${id}`)
    return response.data
  },

  // Create KPI
  create: async data => {
    const response = await api.post('/kpis', data)
    return response.data
  },

  // Update KPI
  update: async (id, data) => {
    const response = await api.put(`/kpis/${id}`, data)
    return response.data
  },

  // Delete KPI
  delete: async id => {
    const response = await api.delete(`/kpis/${id}`)
    return response.data
  },

  // Submit for approval
  submit: async id => {
    const response = await api.post(`/kpis/${id}/submit`)
    return response.data
  },

  // Approve KPI (manager only)
  approve: async (id, comment) => {
    const response = await api.post(`/kpis/${id}/approve`, { comment })
    return response.data
  },

  // Reject KPI (manager only)
  reject: async (id, reason) => {
    const response = await api.post(`/kpis/${id}/reject`, { reason })
    return response.data
  },
}
```

---

## Form Handling

Using **React Hook Form** for form validation and submission.

```jsx
// components/kpi/KPIForm.jsx
import { useForm } from 'react-hook-form'
import { kpiService } from '@services/kpiService'
import { useNotification } from '@hooks/useNotification'

function KPIForm({ initialData, onSuccess }) {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: initialData,
  })
  const { showToast } = useNotification()

  const onSubmit = async data => {
    try {
      if (initialData?.id) {
        await kpiService.update(initialData.id, data)
        showToast('KPI updated successfully', 'success')
      } else {
        await kpiService.create(data)
        showToast('KPI created successfully', 'success')
      }
      onSuccess?.()
    } catch (error) {
      showToast(error.response?.data?.detail || 'An error occurred', 'error')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium">Title</label>
        <input
          {...register('title', { required: 'Title is required', minLength: 3 })}
          className="mt-1 block w-full rounded-md border p-2"
        />
        {errors.title && <p className="text-red-500 text-sm">{errors.title.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium">Category</label>
        <select {...register('category', { required: true })} className="mt-1 block w-full">
          <option value="">Select category</option>
          <option value="mission">Mission</option>
          <option value="goal">Goal</option>
          <option value="task">Task</option>
        </select>
      </div>

      {/* More fields... */}

      <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">
        {initialData?.id ? 'Update' : 'Create'} KPI
      </button>
    </form>
  )
}
```

---

## Authentication Flow

1. **User visits protected route** → Check if authenticated
2. **Not authenticated** → Redirect to `/login`
3. **User submits login form** → Call `authService.login()`
4. **Success** → Store tokens, update AuthContext, redirect to dashboard
5. **API requests** → Attach Bearer token via interceptor
6. **Token expires (401)** → Auto-refresh token, retry request
7. **Refresh fails** → Logout, redirect to login

---

## Best Practices

### 1. Component Organization
- **One component per file**
- **Group related components** in folders
- **Separate presentational from container components**

### 2. State Management
- **Use Context for global state** (auth, notifications)
- **Use local state for component-specific** data
- **Custom hooks for reusable logic**

### 3. Performance
- **React.memo** for expensive components
- **useMemo/useCallback** for expensive calculations
- **Code splitting** with React.lazy
- **Virtual scrolling** for long lists

### 4. Error Handling
- **Try-catch in async functions**
- **Error boundaries** for component errors
- **User-friendly error messages**

### 5. Accessibility
- **Semantic HTML**
- **ARIA labels**
- **Keyboard navigation**
- **Focus management**

---

**Next**: See [ERROR_HANDLING.md](./ERROR_HANDLING.md) for error handling patterns.
