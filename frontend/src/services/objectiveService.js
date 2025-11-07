/**
 * Objective Service
 * API client for OKR Objectives management
 */

import api from './api';

const objectiveService = {
  /**
   * Create new objective
   * @param {Object} data - Objective data
   * @returns {Promise<Object>} Created objective
   */
  createObjective: async (data) => {
    const response = await api.post('/objectives', data);
    return response.data;
  },

  /**
   * Get objectives list with filters
   * @param {Object} params - Query parameters
   * @returns {Promise<Array>} List of objectives
   */
  getObjectives: async (params = {}) => {
    const response = await api.get('/objectives', { params });
    return response.data;
  },

  /**
   * Get objective by ID
   * @param {number} id - Objective ID
   * @returns {Promise<Object>} Objective details
   */
  getObjective: async (id) => {
    const response = await api.get(`/objectives/${id}`);
    return response.data;
  },

  /**
   * Update objective
   * @param {number} id - Objective ID
   * @param {Object} data - Updated data
   * @returns {Promise<Object>} Updated objective
   */
  updateObjective: async (id, data) => {
    const response = await api.put(`/objectives/${id}`, data);
    return response.data;
  },

  /**
   * Delete objective
   * @param {number} id - Objective ID
   * @returns {Promise<void>}
   */
  deleteObjective: async (id) => {
    await api.delete(`/objectives/${id}`);
  },

  /**
   * Get objective children
   * @param {number} id - Parent objective ID
   * @returns {Promise<Array>} Child objectives
   */
  getChildren: async (id) => {
    const response = await api.get(`/objectives/${id}/children`);
    return response.data;
  },

  /**
   * Get objective ancestors (parent chain)
   * @param {number} id - Objective ID
   * @returns {Promise<Array>} Ancestor chain
   */
  getAncestors: async (id) => {
    const response = await api.get(`/objectives/${id}/ancestors`);
    return response.data;
  },

  /**
   * Get tree view
   * @param {Object} params - Query parameters (root_id, year)
   * @returns {Promise<Array>} Tree structure
   */
  getTree: async (params = {}) => {
    const response = await api.get('/objectives/tree/view', { params });
    return response.data;
  },

  /**
   * Move objective to new parent
   * @param {number} id - Objective ID
   * @param {number|null} newParentId - New parent ID
   * @returns {Promise<Object>} Updated objective
   */
  moveObjective: async (id, newParentId) => {
    const response = await api.post(`/objectives/${id}/move`, null, {
      params: { new_parent_id: newParentId }
    });
    return response.data;
  },

  /**
   * Link KPI to objective
   * @param {number} objectiveId - Objective ID
   * @param {Object} data - {kpi_id, weight}
   * @returns {Promise<Object>} Link details
   */
  linkKPI: async (objectiveId, data) => {
    const response = await api.post(`/objectives/${objectiveId}/kpis`, data);
    return response.data;
  },

  /**
   * Unlink KPI from objective
   * @param {number} objectiveId - Objective ID
   * @param {number} kpiId - KPI ID
   * @returns {Promise<void>}
   */
  unlinkKPI: async (objectiveId, kpiId) => {
    await api.delete(`/objectives/${objectiveId}/kpis/${kpiId}`);
  },

  /**
   * Get linked KPIs
   * @param {number} objectiveId - Objective ID
   * @returns {Promise<Array>} Linked KPIs
   */
  getLinkedKPIs: async (objectiveId) => {
    const response = await api.get(`/objectives/${objectiveId}/kpis`);
    return response.data;
  },

  /**
   * Calculate objective progress
   * @param {number} id - Objective ID
   * @returns {Promise<Object>} Progress calculation details
   */
  getProgress: async (id) => {
    const response = await api.get(`/objectives/${id}/progress`);
    return response.data;
  },

  /**
   * Recalculate objective progress (cascades to parents)
   * @param {number} id - Objective ID
   * @returns {Promise<Object>} Updated objective
   */
  recalculateProgress: async (id) => {
    const response = await api.post(`/objectives/${id}/recalculate`);
    return response.data;
  },

  /**
   * Get objectives statistics
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} Statistics
   */
  getStats: async (params = {}) => {
    const response = await api.get('/objectives/stats/summary', { params });
    return response.data;
  },

  /**
   * Get objectives linked to a KPI
   * @param {number} kpiId - KPI ID
   * @returns {Promise<Array>} Linked objectives
   */
  getObjectivesByKPI: async (kpiId) => {
    const response = await api.get(`/kpis/${kpiId}/objectives`);
    return response.data;
  },
};

export default objectiveService;
