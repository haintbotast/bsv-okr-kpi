import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/auth/ProtectedRoute'
import MainLayout from './components/layout/MainLayout'
import ErrorBoundary from './components/common/ErrorBoundary'

// Pages
import LoginPage from './pages/auth/LoginPage'
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage'
import ResetPasswordPage from './pages/auth/ResetPasswordPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import KPIListPage from './pages/kpi/KPIListPage'
import KPIFormPage from './pages/kpi/KPIFormPage'
import KPIDetailPage from './pages/kpi/KPIDetailPage'
import ObjectivesListPage from './pages/objectives/ObjectivesListPage'
import ObjectiveFormPage from './pages/objectives/ObjectiveFormPage'
import ObjectiveDetailPage from './pages/objectives/ObjectiveDetailPage'
import ApprovalsPage from './pages/approvals/ApprovalsPage'
import ReportsPage from './pages/reports/ReportsPage'
import AnalyticsDashboard from './pages/reports/AnalyticsDashboard'
import UserManagementPage from './pages/admin/UserManagementPage'
import TemplateManagementPage from './pages/admin/TemplateManagementPage'
import SystemSettingsPage from './pages/admin/SystemSettingsPage'
import UserProfilePage from './pages/profile/UserProfilePage'

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />

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
            <Route path="objectives" element={<ObjectivesListPage />} />
            <Route path="objectives/new" element={<ObjectiveFormPage />} />
            <Route path="objectives/:id" element={<ObjectiveDetailPage />} />
            <Route path="objectives/:id/edit" element={<ObjectiveFormPage />} />
            <Route path="approvals" element={<ApprovalsPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="analytics" element={<AnalyticsDashboard />} />
            <Route path="profile" element={<UserProfilePage />} />
            <Route path="admin/users" element={<UserManagementPage />} />
            <Route path="admin/templates" element={<TemplateManagementPage />} />
            <Route path="admin/settings" element={<SystemSettingsPage />} />
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
  </ErrorBoundary>
  )
}

export default App
