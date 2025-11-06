/**
 * Settings Service - API calls for system settings management
 */

import api from './api'

const settingsService = {
  // ============================================================================
  // Category Operations
  // ============================================================================

  /**
   * Get list of available KPI categories
   */
  async getCategories() {
    const response = await api.get('/settings/categories')
    return response.data
  },

  /**
   * Add a new KPI category (admin only)
   */
  async addCategory(name) {
    const response = await api.post('/settings/categories', { name })
    return response.data
  },

  /**
   * Delete a KPI category (admin only)
   */
  async deleteCategory(categoryName) {
    const response = await api.delete(`/settings/categories/${encodeURIComponent(categoryName)}`)
    return response.data
  },

  // ============================================================================
  // SMTP Configuration (Admin Only)
  // ============================================================================

  /**
   * Get SMTP settings
   */
  async getSMTPSettings() {
    const response = await api.get('/admin/settings/smtp')
    return response.data
  },

  /**
   * Update SMTP settings
   */
  async updateSMTPSettings(smtpConfig) {
    const response = await api.put('/admin/settings/smtp', smtpConfig)
    return response.data
  },

  /**
   * Test SMTP connection
   */
  async testSMTPConnection(smtpConfig) {
    const response = await api.post('/admin/settings/smtp/test-connection', smtpConfig)
    return response.data
  },

  /**
   * Send test email
   */
  async sendTestEmail(toEmail, smtpConfig = null) {
    const response = await api.post('/admin/settings/smtp/send-test-email', {
      to_email: toEmail,
      smtp_config: smtpConfig
    })
    return response.data
  },
}

export default settingsService
