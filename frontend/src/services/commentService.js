/**
 * Comment Service - API client for comment operations
 */

import api from './api';

const commentService = {
  /**
   * Create a comment on a KPI
   * @param {number} kpiId - KPI ID
   * @param {string} comment - Comment text
   * @returns {Promise} Created comment
   */
  createComment: async (kpiId, comment) => {
    const response = await api.post(`/kpis/${kpiId}/comments`, { comment });
    return response.data;
  },

  /**
   * Get all comments for a KPI
   * @param {number} kpiId - KPI ID
   * @param {number} skip - Pagination skip
   * @param {number} limit - Pagination limit
   * @returns {Promise} List of comments
   */
  getComments: async (kpiId, skip = 0, limit = 100) => {
    const response = await api.get(`/kpis/${kpiId}/comments`, {
      params: { skip, limit },
    });
    return response.data;
  },

  /**
   * Update a comment
   * @param {number} commentId - Comment ID
   * @param {string} commentText - New comment text
   * @returns {Promise} Updated comment
   */
  updateComment: async (commentId, commentText) => {
    const response = await api.put(`/comments/${commentId}`, null, {
      params: { comment_text: commentText },
    });
    return response.data;
  },

  /**
   * Delete a comment
   * @param {number} commentId - Comment ID
   * @returns {Promise} Delete response
   */
  deleteComment: async (commentId) => {
    const response = await api.delete(`/comments/${commentId}`);
    return response.data;
  },
};

export default commentService;
