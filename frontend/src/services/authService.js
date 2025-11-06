import api from './api'

export const authService = {
  /**
   * Login with email and password
   */
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  /**
   * Refresh access token
   */
  refresh: async refreshToken => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },

  /**
   * Get current user info
   */
  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },

  /**
   * Logout
   */
  logout: async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      // Logout anyway even if API call fails
    }
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  /**
   * Request password reset
   */
  forgotPassword: async email => {
    const response = await api.post('/auth/forgot-password', { email })
    return response.data
  },

  /**
   * Reset password with token
   */
  resetPassword: async (token, newPassword) => {
    const response = await api.post('/auth/reset-password', {
      token,
      new_password: newPassword,
    })
    return response.data
  },
}
