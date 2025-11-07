import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import objectiveService from '../../services/objectiveService'
import { toast } from 'react-toastify'

function ObjectivesListPage() {
  const { user } = useAuth()
  const [searchParams, setSearchParams] = useSearchParams()
  const [objectives, setObjectives] = useState([])
  const [stats, setStats] = useState(null)
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
    level: searchParams.get('level') || '',
    status: searchParams.get('status') || '',
    department: searchParams.get('department') || '',
    search: searchParams.get('search') || '',
  })

  useEffect(() => {
    fetchObjectives()
    fetchStats()
  }, [filters, pagination.page])

  const fetchObjectives = async () => {
    try {
      setLoading(true)
      const skip = (pagination.page - 1) * pagination.page_size
      const data = await objectiveService.getObjectives({
        skip,
        limit: pagination.page_size,
        ...filters,
      })
      setObjectives(data.items || data)
      if (data.total !== undefined) {
        setPagination(prev => ({
          ...prev,
          total: data.total,
          total_pages: data.total_pages,
        }))
      }
    } catch (error) {
      console.error('Failed to fetch objectives:', error)
      toast.error('Failed to load objectives')
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const statsData = await objectiveService.getStats(filters)
      setStats(statsData)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
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

  const getLevelLabel = level => {
    const labels = {
      'company': 'Company',
      'unit': 'Unit',
      'division': 'Division',
      'team': 'Team',
      'individual': 'Individual',
      0: 'Company',
      1: 'Unit',
      2: 'Division',
      3: 'Team',
      4: 'Individual',
    }
    return labels[level] || `Level ${level}`
  }

  const getLevelColor = level => {
    const colors = {
      'company': 'bg-purple-100 text-purple-800',
      'unit': 'bg-indigo-100 text-indigo-800',
      'division': 'bg-blue-100 text-blue-800',
      'team': 'bg-green-100 text-green-800',
      'individual': 'bg-yellow-100 text-yellow-800',
      0: 'bg-purple-100 text-purple-800',
      1: 'bg-indigo-100 text-indigo-800',
      2: 'bg-blue-100 text-blue-800',
      3: 'bg-green-100 text-green-800',
      4: 'bg-yellow-100 text-yellow-800',
    }
    return colors[level] || 'bg-gray-100 text-gray-800'
  }

  const getLevelIcon = level => {
    const icons = {
      'company': '🏢',
      'unit': '🏛️',
      'division': '🏬',
      'team': '👥',
      'individual': '👤',
      0: '🏢',
      1: '🏛️',
      2: '🏬',
      3: '👥',
      4: '👤',
    }
    return icons[level] || '📊'
  }

  const getStatusColor = status => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
      on_hold: 'bg-yellow-100 text-yellow-800',
      cancelled: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getStatusIcon = status => {
    const icons = {
      active: '🎯',
      completed: '✅',
      on_hold: '⏸️',
      cancelled: '❌',
    }
    return icons[status] || '📄'
  }

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Objectives</h1>
          <p className="text-gray-600 mt-1">Manage organizational goals and key results</p>
        </div>
        {(user?.role === 'admin' || user?.role === 'manager') && (
          <Link to="/objectives/new" className="btn-primary">
            <span className="mr-2">➕</span>
            Create Objective
          </Link>
        )}
      </div>

      {/* Stats Summary */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
            <div className="text-sm font-medium text-blue-600 mb-1">Total Objectives</div>
            <div className="text-2xl font-bold text-blue-900">{stats.total || 0}</div>
          </div>
          <div className="card bg-gradient-to-br from-purple-50 to-purple-100">
            <div className="text-sm font-medium text-purple-600 mb-1">Company Level</div>
            <div className="text-2xl font-bold text-purple-900">{stats.by_level?.[0] || 0}</div>
          </div>
          <div className="card bg-gradient-to-br from-green-50 to-green-100">
            <div className="text-sm font-medium text-green-600 mb-1">Active</div>
            <div className="text-2xl font-bold text-green-900">{stats.by_status?.active || 0}</div>
          </div>
          <div className="card bg-gradient-to-br from-yellow-50 to-yellow-100">
            <div className="text-sm font-medium text-yellow-600 mb-1">Average Progress</div>
            <div className="text-2xl font-bold text-yellow-900">
              {stats.average_progress ? `${Math.round(stats.average_progress)}%` : '0%'}
            </div>
          </div>
          <div className="card bg-gradient-to-br from-indigo-50 to-indigo-100">
            <div className="text-sm font-medium text-indigo-600 mb-1">Linked KPIs</div>
            <div className="text-2xl font-bold text-indigo-900">{stats.total_kpis || 0}</div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
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

          {/* Level Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Level</label>
            <select
              value={filters.level}
              onChange={e => handleFilterChange('level', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Levels</option>
              <option value="company">Company</option>
              <option value="unit">Unit</option>
              <option value="division">Division</option>
              <option value="team">Team</option>
              <option value="individual">Individual</option>
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
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="on_hold">On Hold</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          {/* Department Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Department</label>
            <input
              type="text"
              placeholder="e.g. IT, Sales"
              value={filters.department}
              onChange={e => handleFilterChange('department', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
            <input
              type="text"
              placeholder="Search objectives..."
              value={filters.search}
              onChange={e => handleFilterChange('search', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* View Toggle */}
      <div className="mb-4 flex justify-end gap-2">
        <Link
          to="/objectives/tree"
          className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 text-sm font-medium"
        >
          🌳 Tree View
        </Link>
      </div>

      {/* Objectives List */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading objectives...</p>
          </div>
        </div>
      ) : objectives.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">🎯</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Objectives Found</h3>
          <p className="text-gray-600 mb-6">
            {filters.search || filters.status || filters.quarter || filters.level
              ? 'Try adjusting your filters'
              : 'Get started by creating your first objective'}
          </p>
          {(user?.role === 'admin' || user?.role === 'manager') && (
            <Link to="/objectives/new" className="btn-primary inline-block">
              Create Objective
            </Link>
          )}
        </div>
      ) : (
        <>
          {/* Objectives Cards */}
          <div className="grid grid-cols-1 gap-4 mb-6">
            {objectives.map(objective => (
              <Link
                key={objective.id}
                to={`/objectives/${objective.id}`}
                className="card hover:shadow-lg transition-all cursor-pointer"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{objective.title}</h3>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getLevelColor(objective.level)}`}>
                        {getLevelIcon(objective.level)} {getLevelLabel(objective.level)}
                      </span>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(objective.status)}`}>
                        {getStatusIcon(objective.status)} {objective.status}
                      </span>
                    </div>

                    {objective.description && (
                      <p className="text-gray-600 text-sm mb-3 line-clamp-2">{objective.description}</p>
                    )}

                    <div className="flex items-center gap-6 text-sm text-gray-500">
                      <span>📅 {objective.year} {objective.quarter}</span>
                      {objective.department && <span>🏢 {objective.department}</span>}
                      {objective.owner_name && <span>👤 {objective.owner_name}</span>}
                      {objective.linked_kpis_count > 0 && (
                        <span>🔗 {objective.linked_kpis_count} KPIs</span>
                      )}
                      {objective.children_count > 0 && (
                        <span>🌳 {objective.children_count} sub-objectives</span>
                      )}
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-32 ml-4">
                    <div className="text-right text-sm font-medium text-gray-700 mb-1">
                      {Math.round(objective.progress || 0)}%
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${
                          objective.progress >= 75
                            ? 'bg-green-600'
                            : objective.progress >= 50
                            ? 'bg-blue-600'
                            : objective.progress >= 25
                            ? 'bg-yellow-600'
                            : 'bg-red-600'
                        }`}
                        style={{ width: `${objective.progress || 0}%` }}
                      ></div>
                    </div>
                    <div className="text-right text-xs text-gray-500 mt-1">
                      {objective.start_date && objective.end_date && (
                        <>
                          {new Date(objective.start_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                          {' - '}
                          {new Date(objective.end_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                        </>
                      )}
                    </div>
                  </div>
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
                    {Array.from({ length: Math.min(pagination.total_pages, 5) }, (_, i) => {
                      let page
                      if (pagination.total_pages <= 5) {
                        page = i + 1
                      } else if (pagination.page <= 3) {
                        page = i + 1
                      } else if (pagination.page >= pagination.total_pages - 2) {
                        page = pagination.total_pages - 4 + i
                      } else {
                        page = pagination.page - 2 + i
                      }
                      return (
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
                      )
                    })}
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

export default ObjectivesListPage
