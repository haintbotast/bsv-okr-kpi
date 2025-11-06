/**
 * ReportsPage - Generate and export reports
 */

import { useState } from 'react';
import { toast } from 'react-hot-toast';
import reportService from '../../services/reportService';

const ReportsPage = () => {
  const [filters, setFilters] = useState({
    year: new Date().getFullYear(),
    quarter: '',
    status: '',
  });
  const [exportingExcel, setExportingExcel] = useState(false);
  const [exportingPDF, setExportingPDF] = useState(false);

  const handleExportExcel = async () => {
    try {
      setExportingExcel(true);
      await reportService.exportExcel(filters);
      toast.success('Excel report exported successfully');
    } catch (error) {
      console.error('Export failed:', error);
      toast.error('Failed to export Excel report');
    } finally {
      setExportingExcel(false);
    }
  };

  const handleExportPDF = async () => {
    try {
      setExportingPDF(true);
      await reportService.exportPDF(filters);
      toast.success('PDF report exported successfully');
    } catch (error) {
      console.error('Export failed:', error);
      toast.error('Failed to export PDF report');
    } finally {
      setExportingPDF(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Reports</h1>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Export KPI Report</h2>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Year
            </label>
            <input
              type="number"
              value={filters.year}
              onChange={(e) => setFilters({ ...filters, year: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quarter
            </label>
            <select
              value={filters.quarter}
              onChange={(e) => setFilters({ ...filters, quarter: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">All Quarters</option>
              <option value="Q1">Q1</option>
              <option value="Q2">Q2</option>
              <option value="Q3">Q3</option>
              <option value="Q4">Q4</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">All Status</option>
              <option value="draft">Draft</option>
              <option value="submitted">Submitted</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>

        <div className="flex gap-4">
          <button
            onClick={handleExportExcel}
            disabled={exportingExcel || exportingPDF}
            className="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            {exportingExcel ? 'Exporting...' : 'Export to Excel'}
          </button>

          <button
            onClick={handleExportPDF}
            disabled={exportingExcel || exportingPDF}
            className="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            {exportingPDF ? 'Exporting...' : 'Export to PDF'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReportsPage;
