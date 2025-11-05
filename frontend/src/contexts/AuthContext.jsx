import { createContext, useState, useEffect } from 'react'
import { authService } from '../services/authService'
import { toast } from 'react-toastify'

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
      // Token invalid or expired
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await authService.login(email, password)

      // Store tokens
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)

      // Set user state
      setUser(response.user)
      setIsAuthenticated(true)

      toast.success('Login successful!')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const logout = async () => {
    await authService.logout()
    setUser(null)
    setIsAuthenticated(false)
  }

  const hasRole = role => {
    return user?.role === role
  }

  const isAdmin = () => {
    return user?.role === 'admin'
  }

  const isManager = () => {
    return ['admin', 'manager'].includes(user?.role)
  }

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    refreshUser: loadUser,
    hasRole,
    isAdmin,
    isManager,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
