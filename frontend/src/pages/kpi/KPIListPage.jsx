import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import kpiService from '../../services/kpiService'
import { toast } from 'react-toastify'

function KPIListPage() {
  const { user } = useAuth()
  const [searchParams, setSearchParams] = useSearchParams()
  const [kpis, setKpis] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    page_size: 20,
    total_pages: 1,
  })

  // Filters
  const [filters, setFilters] = useState({
    year: searchParams.get('year') || new Date().getFullYear().toString(),
    quarter: searchParams.get('quarter') || '',
    status: searchParams.get('status') || '',
    search: searchParams.get('search') || '',
  })

  useEffect(() => {
    fetchKPIs()
  }, [filters, pagination.page])

  const fetchKPIs = async () => {
    try {
      setLoading(true)
      const skip = (pagination.page - 1) * pagination.page_size
      const data = await kpiService.getKPIs({
        skip,
        limit: pagination.page_size,
        ...filters,
      })
      setKpis(data.items)
      setPagination(prev => ({
        ...prev,
        total: data.total,
        total_pages: data.total_pages,
      }))
    } catch (error) {
      console.error('Failed to fetch KPIs:', error)
      toast.error('Failed to load KPIs')
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }))
    setPagination(prev => ({ ...prev, page: 1 }))

    // Update URL params
    const newParams = new URLSearchParams(searchParams)
    if (value) {
      newParams.set(key, value)
    } else {
      newParams.delete(key)
    }
    setSearchParams(newParams)
  }

  const handlePageChange = newPage => {
    setPagination(prev => ({ ...prev, page: newPage }))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const getStatusColor = status => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      submitted: 'bg-yellow-100 text-yellow-800',
      approved: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getStatusIcon = status => {
    const icons = {
      draft: '📝',
      submitted: '⏳',
      approved: '✅',
      rejected: '❌',
    }
    return icons[status] || '📄'
  }

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">My KPIs</h1>
        <Link
          to="/kpis/new"
          className="btn-primary"
        >
          <span className="mr-2">➕</span>
          Create New KPI
        </Link>
      </div>

      {/* Filters */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Year Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Year</label>
            <select
              value={filters.year}
              onChange={e => handleFilterChange('year', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Years</option>
              {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i).map(year => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>

          {/* Quarter Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Quarter</label>
            <select
              value={filters.quarter}
              onChange={e => handleFilterChange('quarter', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Quarters</option>
              <option value="Q1">Q1</option>
              <option value="Q2">Q2</option>
              <option value="Q3">Q3</option>
              <option value="Q4">Q4</option>
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              value={filters.status}
              onChange={e => handleFilterChange('status', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Status</option>
              <option value="draft">Draft</option>
              <option value="submitted">Submitted</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
            <input
              type="text"
              placeholder="Search KPIs..."
              value={filters.search}
              onChange={e => handleFilterChange('search', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* KPI List */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading KPIs...</p>
          </div>
        </div>
      ) : kpis.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No KPIs Found</h3>
          <p className="text-gray-600 mb-6">
            {filters.search || filters.status || filters.quarter
              ? 'Try adjusting your filters'
              : 'Get started by creating your first KPI'}
          </p>
          <Link to="/kpis/new" className="btn-primary inline-block">
            Create New KPI
          </Link>
        </div>
      ) : (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-1 gap-4 mb-6">
            {kpis.map(kpi => (
              <Link
                key={kpi.id}
                to={`/kpis/${kpi.id}`}
                className="card hover:shadow-lg transition-all cursor-pointer"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{kpi.title}</h3>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(kpi.status)}`}>
                        {getStatusIcon(kpi.status)} {kpi.status}
                      </span>
                    </div>

                    {kpi.description && (
                      <p className="text-gray-600 text-sm mb-3 line-clamp-2">{kpi.description}</p>
                    )}

                    <div className="flex items-center gap-6 text-sm text-gray-500">
                      <span>📅 {kpi.year} {kpi.quarter}</span>
                      {kpi.category && <span>🏷️ {kpi.category}</span>}
                      {kpi.progress_percentage !== null && (
                        <span>📊 {kpi.progress_percentage}% complete</span>
                      )}
                    </div>
                  </div>

                  {/* Progress Bar */}
                  {kpi.progress_percentage !== null && (
                    <div className="w-32 ml-4">
                      <div className="text-right text-sm font-medium text-gray-700 mb-1">
                        {kpi.progress_percentage}%
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all"
                          style={{ width: `${kpi.progress_percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>

          {/* Pagination */}
          {pagination.total_pages > 1 && (
            <div className="card">
              <div className="flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  Showing {(pagination.page - 1) * pagination.page_size + 1} to{' '}
                  {Math.min(pagination.page * pagination.page_size, pagination.total)} of{' '}
                  {pagination.total} results
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handlePageChange(pagination.page - 1)}
                    disabled={pagination.page === 1}
                    className="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    Previous
                  </button>
                  <div className="flex gap-1">
                    {Array.from({ length: pagination.total_pages }, (_, i) => i + 1).map(page => (
                      <button
                        key={page}
                        onClick={() => handlePageChange(page)}
                        className={`px-3 py-1 border rounded-md ${
                          page === pagination.page
                            ? 'bg-blue-600 text-white border-blue-600'
                            : 'border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        {page}
                      </button>
                    ))}
                  </div>
                  <button
                    onClick={() => handlePageChange(pagination.page + 1)}
                    disabled={pagination.page === pagination.total_pages}
                    className="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    Next
                  </button>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default KPIListPage
