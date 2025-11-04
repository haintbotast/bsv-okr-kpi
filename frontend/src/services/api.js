import axios from 'axios'
import { toast } from 'react-toastify'

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

// Response interceptor - handle errors and token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // Network error
    if (!error.response) {
      toast.error('Network error. Please check your connection.')
      return Promise.reject(error)
    }

    const { status } = error.response

    // Handle 401 Unauthorized - try to refresh token
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          throw new Error('No refresh token')
        }

        const response = await axios.post(`${api.defaults.baseURL}/auth/refresh`, {
          refresh_token: refreshToken,
        })

        const { access_token } = response.data
        localStorage.setItem('access_token', access_token)

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed - logout user
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    // Handle other errors
    const message = error.response?.data?.detail || 'An error occurred'

    if (status === 403) {
      toast.error('You do not have permission to perform this action')
    } else if (status === 404) {
      toast.error('Resource not found')
    } else if (status === 500) {
      toast.error('Server error. Please try again later.')
    } else {
      toast.error(message)
    }

    return Promise.reject(error)
  }
)

export default api
