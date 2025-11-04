import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/auth/ProtectedRoute'
import MainLayout from './components/layout/MainLayout'

// Pages
import LoginPage from './pages/auth/LoginPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import KPIListPage from './pages/kpi/KPIListPage'
import KPIFormPage from './pages/kpi/KPIFormPage'
import KPIDetailPage from './pages/kpi/KPIDetailPage'
import ReportsPage from './pages/reports/ReportsPage'
import AnalyticsDashboard from './pages/reports/AnalyticsDashboard'
import UserManagementPage from './pages/admin/UserManagementPage'
import TemplateManagementPage from './pages/admin/TemplateManagementPage'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <MainLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="kpis" element={<KPIListPage />} />
            <Route path="kpis/new" element={<KPIFormPage />} />
            <Route path="kpis/:id" element={<KPIDetailPage />} />
            <Route path="kpis/:id/edit" element={<KPIFormPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="analytics" element={<AnalyticsDashboard />} />
            <Route path="admin/users" element={<UserManagementPage />} />
            <Route path="admin/templates" element={<TemplateManagementPage />} />
          </Route>
        </Routes>

        {/* Toast notifications */}
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
