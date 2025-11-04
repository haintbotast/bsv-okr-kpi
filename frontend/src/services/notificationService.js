/**
 * Notification Service - API client for notification operations
 */

import api from './api';

const notificationService = {
  /**
   * Get notifications for current user
   * @param {number} skip - Pagination skip
   * @param {number} limit - Pagination limit
   * @param {boolean} unreadOnly - Only fetch unread notifications
   * @returns {Promise} List of notifications
   */
  getNotifications: async (skip = 0, limit = 50, unreadOnly = false) => {
    const response = await api.get('/notifications', {
      params: { skip, limit, unread_only: unreadOnly },
    });
    return response.data;
  },

  /**
   * Get unread notification count
   * @returns {Promise} Unread count
   */
  getUnreadCount: async () => {
    const response = await api.get('/notifications/unread-count');
    return response.data;
  },

  /**
   * Mark notification as read
   * @param {number} notificationId - Notification ID
   * @returns {Promise} Updated notification
   */
  markAsRead: async (notificationId) => {
    const response = await api.put(`/notifications/${notificationId}`, {
      is_read: true,
    });
    return response.data;
  },

  /**
   * Mark all notifications as read
   * @returns {Promise} Response with count
   */
  markAllAsRead: async () => {
    const response = await api.post('/notifications/mark-all-read');
    return response.data;
  },

  /**
   * Delete a notification
   * @param {number} notificationId - Notification ID
   * @returns {Promise} Delete response
   */
  deleteNotification: async (notificationId) => {
    const response = await api.delete(`/notifications/${notificationId}`);
    return response.data;
  },
};

export default notificationService;
