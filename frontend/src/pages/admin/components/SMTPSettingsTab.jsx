/**
 * SMTPSettingsTab - SMTP/Email configuration component
 */

import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import settingsService from '../../../services/settingsService'

function SMTPSettingsTab() {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [testing, setTesting] = useState(false)
  const [sendingTest, setSendingTest] = useState(false)

  const [formData, setFormData] = useState({
    enabled: false,
    host: 'smtp.gmail.com',
    port: 587,
    user: '',
    password: '',
    from_email: '',
    use_tls: true
  })

  const [testEmail, setTestEmail] = useState('')

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      setLoading(true)
      const data = await settingsService.getSMTPSettings()
      setFormData({
        ...data,
        password: '' // Don't load password from server
      })
    } catch (error) {
      console.error('Failed to fetch SMTP settings:', error)
      toast.error('Failed to load SMTP settings')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSave = async () => {
    // Validation
    if (formData.enabled) {
      if (!formData.host || !formData.user || !formData.from_email) {
        toast.error('Please fill in all required fields')
        return
      }

      if (!formData.password) {
        toast.error('Password is required when enabling SMTP')
        return
      }
    }

    try {
      setSaving(true)
      await settingsService.updateSMTPSettings(formData)
      toast.success('SMTP settings saved successfully')
    } catch (error) {
      console.error('Failed to save SMTP settings:', error)
      toast.error(error.response?.data?.detail || 'Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const handleTestConnection = async () => {
    if (!formData.host || !formData.user || !formData.password) {
      toast.error('Please fill in host, user, and password to test connection')
      return
    }

    try {
      setTesting(true)
      const result = await settingsService.testSMTPConnection(formData)
      toast.success(result.message || 'Connection successful!')
    } catch (error) {
      console.error('Connection test failed:', error)
      toast.error(error.response?.data?.detail || 'Connection failed')
    } finally {
      setTesting(false)
    }
  }

  const handleSendTestEmail = async () => {
    if (!testEmail) {
      toast.error('Please enter an email address')
      return
    }

    if (!formData.host || !formData.user || !formData.password) {
      toast.error('Please configure and test SMTP connection first')
      return
    }

    try {
      setSendingTest(true)
      const result = await settingsService.sendTestEmail(testEmail, formData)
      toast.success(result.message || 'Test email sent!')
      setTestEmail('')
    } catch (error) {
      console.error('Failed to send test email:', error)
      toast.error(error.response?.data?.detail || 'Failed to send test email')
    } finally {
      setSendingTest(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading SMTP settings...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Enable/Disable Toggle */}
      <div className="card">
        <label className="flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={formData.enabled}
            onChange={(e) => handleChange('enabled', e.target.checked)}
            className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <span className="ml-3">
            <span className="text-lg font-medium text-gray-900">Enable Email Notifications</span>
            <p className="text-sm text-gray-500">Send email notifications to users for KPI events</p>
          </span>
        </label>
      </div>

      {/* SMTP Configuration Form */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">SMTP Configuration</h3>

        <div className="space-y-4">
          {/* Host */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              SMTP Host <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.host}
              onChange={(e) => handleChange('host', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="smtp.gmail.com"
              disabled={!formData.enabled}
            />
            <p className="text-xs text-gray-500 mt-1">
              Gmail: smtp.gmail.com | Outlook: smtp.office365.com
            </p>
          </div>

          {/* Port */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              SMTP Port <span className="text-red-500">*</span>
            </label>
            <input
              type="number"
              value={formData.port}
              onChange={(e) => handleChange('port', parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="587"
              min="1"
              max="65535"
              disabled={!formData.enabled}
            />
            <p className="text-xs text-gray-500 mt-1">
              Common ports: 587 (TLS), 465 (SSL), 25 (Plain)
            </p>
          </div>

          {/* Username */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              SMTP Username <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.user}
              onChange={(e) => handleChange('user', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="your-email@gmail.com"
              autoComplete="username"
              disabled={!formData.enabled}
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              SMTP Password <span className="text-red-500">*</span>
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => handleChange('password', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder={formData.password ? '********' : 'Enter password'}
              autoComplete="current-password"
              disabled={!formData.enabled}
            />
            <p className="text-xs text-gray-500 mt-1">
              For Gmail: Use App Password from https://myaccount.google.com/apppasswords
            </p>
          </div>

          {/* From Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              From Email Address <span className="text-red-500">*</span>
            </label>
            <input
              type="email"
              value={formData.from_email}
              onChange={(e) => handleChange('from_email', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="noreply@your-company.com"
              disabled={!formData.enabled}
            />
          </div>

          {/* Use TLS */}
          <div>
            <label className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={formData.use_tls}
                onChange={(e) => handleChange('use_tls', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                disabled={!formData.enabled}
              />
              <span className="ml-2 text-sm text-gray-700">Use TLS encryption (recommended)</span>
            </label>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex gap-3">
          <button
            onClick={handleTestConnection}
            disabled={!formData.enabled || testing}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {testing ? 'Testing...' : 'Test Connection'}
          </button>

          <button
            onClick={handleSave}
            disabled={saving}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </div>

      {/* Test Email Section */}
      {formData.enabled && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Send Test Email</h3>
          <p className="text-sm text-gray-600 mb-4">
            Send a test email to verify your configuration is working correctly.
          </p>

          <div className="flex gap-3">
            <input
              type="email"
              value={testEmail}
              onChange={(e) => setTestEmail(e.target.value)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="your-email@example.com"
            />
            <button
              onClick={handleSendTestEmail}
              disabled={!testEmail || sendingTest}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {sendingTest ? 'Sending...' : 'Send Test Email'}
            </button>
          </div>

          <p className="text-xs text-gray-500 mt-2">
            Check your inbox (and spam folder) for the test email.
          </p>
        </div>
      )}

      {/* Help Section */}
      <div className="card bg-blue-50 border-blue-200">
        <h4 className="font-medium text-blue-900 mb-2">💡 Quick Setup Guide</h4>
        <div className="text-sm text-blue-800 space-y-1">
          <p><strong>For Gmail:</strong></p>
          <ol className="list-decimal list-inside ml-2 space-y-1">
            <li>Enable 2-Factor Authentication on your Google account</li>
            <li>Go to https://myaccount.google.com/apppasswords</li>
            <li>Create an App Password for "Mail"</li>
            <li>Use that 16-character password above (not your regular password)</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

export default SMTPSettingsTab
