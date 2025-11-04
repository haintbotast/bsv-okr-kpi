/**
 * File Service - API client for file operations
 */

import api from './api';

const fileService = {
  /**
   * Upload file to KPI
   * @param {number} kpiId - KPI ID
   * @param {File} file - File to upload
   * @param {string} description - Optional file description
   * @param {function} onUploadProgress - Progress callback
   * @returns {Promise} Upload response
   */
  uploadFile: async (kpiId, file, description = null, onUploadProgress = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (description) {
      formData.append('description', description);
    }

    const response = await api.post(`/kpis/${kpiId}/files`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onUploadProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onUploadProgress(percentCompleted);
        }
      },
    });

    return response.data;
  },

  /**
   * Get all files for a KPI
   * @param {number} kpiId - KPI ID
   * @returns {Promise} List of files
   */
  getFilesByKPI: async (kpiId) => {
    const response = await api.get(`/kpis/${kpiId}/files`);
    return response.data;
  },

  /**
   * Download file
   * @param {number} evidenceId - Evidence ID
   * @param {string} fileName - Original filename for download
   * @returns {Promise} Download response
   */
  downloadFile: async (evidenceId, fileName) => {
    const response = await api.get(`/files/${evidenceId}/download`, {
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

    return response;
  },

  /**
   * Get file URL for preview
   * @param {number} evidenceId - Evidence ID
   * @returns {string} File URL
   */
  getFileUrl: (evidenceId) => {
    const baseURL = api.defaults.baseURL || '';
    return `${baseURL}/files/${evidenceId}/download`;
  },

  /**
   * Delete file
   * @param {number} evidenceId - Evidence ID
   * @returns {Promise} Delete response
   */
  deleteFile: async (evidenceId) => {
    const response = await api.delete(`/files/${evidenceId}`);
    return response.data;
  },

  /**
   * Validate file before upload
   * @param {File} file - File to validate
   * @returns {Object} Validation result {valid: boolean, error: string}
   */
  validateFile: (file) => {
    const maxSize = 50 * 1024 * 1024; // 50MB
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'image/jpeg',
      'image/png',
    ];

    const allowedExtensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png'];

    // Check file size
    if (file.size > maxSize) {
      return {
        valid: false,
        error: `File size (${(file.size / (1024 * 1024)).toFixed(2)}MB) exceeds maximum allowed size (50MB)`,
      };
    }

    // Check file extension
    const fileExt = file.name.split('.').pop().toLowerCase();
    if (!allowedExtensions.includes(fileExt)) {
      return {
        valid: false,
        error: `File type '.${fileExt}' is not allowed. Allowed types: ${allowedExtensions.join(', ')}`,
      };
    }

    // Check MIME type (if available)
    if (file.type && !allowedTypes.includes(file.type) && file.type !== '') {
      // Some files might have empty type, so we allow it to pass if extension is valid
      if (file.type !== 'application/octet-stream') {
        return {
          valid: false,
          error: `File MIME type '${file.type}' is not allowed`,
        };
      }
    }

    return { valid: true, error: null };
  },

  /**
   * Get file icon based on file type
   * @param {string} fileName - File name
   * @returns {string} Icon name
   */
  getFileIcon: (fileName) => {
    const ext = fileName.split('.').pop().toLowerCase();
    const iconMap = {
      pdf: 'file-text',
      doc: 'file-text',
      docx: 'file-text',
      xls: 'file-spreadsheet',
      xlsx: 'file-spreadsheet',
      jpg: 'image',
      jpeg: 'image',
      png: 'image',
    };
    return iconMap[ext] || 'file';
  },

  /**
   * Format file size
   * @param {number} bytes - File size in bytes
   * @returns {string} Formatted size
   */
  formatFileSize: (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  },
};

export default fileService;
