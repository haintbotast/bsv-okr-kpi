/**
 * KPI Service - API calls for KPI management
 */

import api from './api'

const kpiService = {
  // ============================================================================
  // KPI Operations
  // ============================================================================

  /**
   * Get list of KPIs with filters
   */
  async getKPIs(params = {}) {
    const { skip = 0, limit = 100, user_id, year, quarter, status, search } = params

    // Filter out empty/null values to avoid validation errors
    const filteredParams = {
      skip,
      limit,
      ...(user_id && { user_id }),
      ...(year && { year }),
      ...(quarter && { quarter }),
      ...(status && { status }),
      ...(search && { search }),
    }

    const response = await api.get('/kpis', {
      params: filteredParams,
    })
    return response.data
  },

  /**
   * Get a single KPI by ID
   */
  async getKPI(kpiId) {
    const response = await api.get(`/kpis/${kpiId}`)
    return response.data
  },

  /**
   * Create a new KPI
   */
  async createKPI(kpiData) {
    const response = await api.post('/kpis', kpiData)
    return response.data
  },

  /**
   * Update a KPI
   */
  async updateKPI(kpiId, kpiData) {
    const response = await api.put(`/kpis/${kpiId}`, kpiData)
    return response.data
  },

  /**
   * Delete a KPI
   */
  async deleteKPI(kpiId) {
    const response = await api.delete(`/kpis/${kpiId}`)
    return response.data
  },

  /**
   * Submit KPI for approval
   */
  async submitKPI(kpiId) {
    const response = await api.post(`/kpis/${kpiId}/submit`, {})
    return response.data
  },

  /**
   * Approve a KPI (managers only)
   */
  async approveKPI(kpiId, comment = null) {
    const response = await api.post(`/kpis/${kpiId}/approve`, { comment })
    return response.data
  },

  /**
   * Reject a KPI (managers only)
   */
  async rejectKPI(kpiId, reason) {
    const response = await api.post(`/kpis/${kpiId}/reject`, { reason })
    return response.data
  },

  // ============================================================================
  // Statistics & Dashboard
  // ============================================================================

  /**
   * Get KPI statistics
   */
  async getStatistics() {
    const response = await api.get('/kpis/statistics')
    return response.data
  },

  /**
   * Get dashboard statistics
   */
  async getDashboardStatistics() {
    const response = await api.get('/kpis/dashboard')
    return response.data
  },

  /**
   * Get pending approvals (managers only)
   */
  async getPendingApprovals(params = {}) {
    const { skip = 0, limit = 100 } = params
    const response = await api.get('/kpis/pending', {
      params: { skip, limit },
    })
    return response.data
  },

  // ============================================================================
  // Templates
  // ============================================================================

  /**
   * Get list of KPI templates
   */
  async getTemplates(params = {}) {
    const { skip = 0, limit = 100, is_active = true, role, category } = params
    const response = await api.get('/templates', {
      params: { skip, limit, is_active, role, category },
    })
    return response.data
  },

  /**
   * Get a single template by ID
   */
  async getTemplate(templateId) {
    const response = await api.get(`/templates/${templateId}`)
    return response.data
  },

  /**
   * Create a new template (admin only)
   */
  async createTemplate(templateData) {
    const response = await api.post('/templates', templateData)
    return response.data
  },

  /**
   * Update a template (admin only)
   */
  async updateTemplate(templateId, templateData) {
    const response = await api.put(`/templates/${templateId}`, templateData)
    return response.data
  },

  /**
   * Delete a template (admin only)
   */
  async deleteTemplate(templateId) {
    const response = await api.delete(`/templates/${templateId}`)
    return response.data
  },
}

export default kpiService
