/**
 * User Service - API client for user management (admin only)
 */

import api from './api';

const userService = {
  /**
   * Get all users
   */
  getUsers: async (skip = 0, limit = 100) => {
    const response = await api.get('/admin/users', { params: { skip, limit } });
    return response.data;
  },

  /**
   * Get user by ID
   */
  getUser: async (userId) => {
    const response = await api.get(`/admin/users/${userId}`);
    return response.data;
  },

  /**
   * Create new user
   */
  createUser: async (userData) => {
    const response = await api.post('/admin/users', userData);
    return response.data;
  },

  /**
   * Update user
   */
  updateUser: async (userId, userData) => {
    const response = await api.put(`/admin/users/${userId}`, userData);
    return response.data;
  },

  /**
   * Delete user
   */
  deleteUser: async (userId) => {
    const response = await api.delete(`/admin/users/${userId}`);
    return response.data;
  },

  /**
   * Upload own avatar
   */
  uploadAvatar: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Upload avatar for user (admin only)
   */
  uploadUserAvatar: async (userId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`/upload/avatar/${userId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Delete own avatar
   */
  deleteAvatar: async () => {
    const response = await api.delete('/upload/avatar');
    return response.data;
  },

  /**
   * Delete user avatar (admin only)
   */
  deleteUserAvatar: async (userId) => {
    const response = await api.delete(`/upload/avatar/${userId}`);
    return response.data;
  },
};

export default userService;
