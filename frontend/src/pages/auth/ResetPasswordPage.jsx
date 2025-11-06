/**
 * ResetPasswordPage - Reset password with token
 */

import { useState, useEffect } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { toast } from 'react-toastify'
import { authService } from '../../services/authService'

function ResetPasswordPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [token, setToken] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  useEffect(() => {
    const tokenParam = searchParams.get('token')
    if (tokenParam) {
      setToken(tokenParam)
    } else {
      toast.error('Invalid reset link')
      navigate('/login')
    }
  }, [searchParams, navigate])

  const validatePassword = password => {
    if (password.length < 8) {
      return 'Password must be at least 8 characters long'
    }
    return null
  }

  const handleSubmit = async e => {
    e.preventDefault()

    // Validate password
    const passwordError = validatePassword(newPassword)
    if (passwordError) {
      toast.error(passwordError)
      return
    }

    // Check if passwords match
    if (newPassword !== confirmPassword) {
      toast.error('Passwords do not match')
      return
    }

    try {
      setLoading(true)
      const result = await authService.resetPassword(token, newPassword)
      toast.success(result.message || 'Password reset successfully')

      // Redirect to login after 2 seconds
      setTimeout(() => {
        navigate('/login')
      }, 2000)
    } catch (error) {
      console.error('Reset password error:', error)
      const errorMessage = error.response?.data?.detail || 'Failed to reset password'
      toast.error(errorMessage)

      // If token is invalid/expired, redirect to forgot password page
      if (errorMessage.includes('Invalid') || errorMessage.includes('expired')) {
        setTimeout(() => {
          navigate('/forgot-password')
        }, 3000)
      }
    } finally {
      setLoading(false)
    }
  }

  const passwordStrength = password => {
    if (!password) return null
    if (password.length < 8) return { color: 'red', text: 'Too short' }
    if (password.length < 12) return { color: 'yellow', text: 'Fair' }
    return { color: 'green', text: 'Strong' }
  }

  const strength = passwordStrength(newPassword)

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Set new password
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Choose a strong password to protect your account
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/* New Password */}
            <div>
              <label htmlFor="new-password" className="block text-sm font-medium text-gray-700 mb-1">
                New Password
              </label>
              <div className="relative">
                <input
                  id="new-password"
                  name="new-password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                  className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter new password"
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm text-gray-600 hover:text-gray-900"
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>

              {/* Password strength indicator */}
              {strength && (
                <div className="mt-2">
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className={`h-full transition-all duration-300 ${
                          strength.color === 'red'
                            ? 'bg-red-500 w-1/3'
                            : strength.color === 'yellow'
                            ? 'bg-yellow-500 w-2/3'
                            : 'bg-green-500 w-full'
                        }`}
                      />
                    </div>
                    <span className={`text-xs font-medium text-${strength.color}-600`}>
                      {strength.text}
                    </span>
                  </div>
                </div>
              )}

              <p className="mt-1 text-xs text-gray-500">
                Must be at least 8 characters. Cannot reuse your last 3 passwords.
              </p>
            </div>

            {/* Confirm Password */}
            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password
              </label>
              <input
                id="confirm-password"
                name="confirm-password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="new-password"
                required
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Confirm new password"
                disabled={loading}
              />
              {confirmPassword && newPassword !== confirmPassword && (
                <p className="mt-1 text-xs text-red-600">Passwords do not match</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading || !newPassword || !confirmPassword || newPassword !== confirmPassword}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Resetting...' : 'Reset password'}
            </button>
          </div>

          <div className="text-center">
            <Link
              to="/login"
              className="font-medium text-sm text-blue-600 hover:text-blue-500"
            >
              Back to login
            </Link>
          </div>
        </form>

        <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-yellow-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-800">
                <strong>Security tips:</strong>
              </p>
              <ul className="mt-1 text-sm text-yellow-800 list-disc list-inside space-y-1">
                <li>Use a unique password you haven't used before</li>
                <li>Include uppercase, lowercase, numbers, and symbols</li>
                <li>Avoid common words or personal information</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResetPasswordPage
