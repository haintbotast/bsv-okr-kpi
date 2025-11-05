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
}

export default settingsService
