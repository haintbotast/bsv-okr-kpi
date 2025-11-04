/**
 * Report Service - API client for reports and analytics
 */

import api from './api';

const reportService = {
  /**
   * Export KPIs to Excel
   */
  exportExcel: async (filters = {}) => {
    const response = await api.get('/reports/excel', {
      params: filters,
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `kpi_report_${Date.now()}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },

  /**
   * Get analytics data
   */
  getAnalytics: async (filters = {}) => {
    const response = await api.get('/analytics', { params: filters });
    return response.data;
  },
};

export default reportService;
