import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import kpiService from '../../services/kpiService'
import { toast } from 'react-toastify'

function ApprovalsPage() {
  const { user } = useAuth()
  const [kpis, setKpis] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState({})
  const [showRejectModal, setShowRejectModal] = useState(false)
  const [selectedKPI, setSelectedKPI] = useState(null)
  const [rejectReason, setRejectReason] = useState('')

  useEffect(() => {
    fetchPendingApprovals()
  }, [])

  const fetchPendingApprovals = async () => {
    try {
      setLoading(true)
      const data = await kpiService.getPendingApprovals({
        skip: 0,
        limit: 100,
      })
      setKpis(data.items || [])
    } catch (error) {
      console.error('Failed to fetch pending approvals:', error)
      toast.error('Failed to load pending approvals')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (kpi) => {
    if (!window.confirm(`Are you sure you want to approve "${kpi.title}"?`)) {
      return
    }

    try {
      setActionLoading(prev => ({ ...prev, [kpi.id]: true }))
      await kpiService.approveKPI(kpi.id)
      toast.success(`KPI "${kpi.title}" has been approved`)
      // Remove from list
      setKpis(prev => prev.filter(k => k.id !== kpi.id))
    } catch (error) {
      console.error('Failed to approve KPI:', error)
      toast.error(error.response?.data?.detail || 'Failed to approve KPI')
    } finally {
      setActionLoading(prev => ({ ...prev, [kpi.id]: false }))
    }
  }

  const handleRejectClick = (kpi) => {
    setSelectedKPI(kpi)
    setRejectReason('')
    setShowRejectModal(true)
  }

  const handleRejectSubmit = async () => {
    if (!rejectReason.trim()) {
      toast.error('Please provide a reason for rejection')
      return
    }

    try {
      setActionLoading(prev => ({ ...prev, [selectedKPI.id]: true }))
      await kpiService.rejectKPI(selectedKPI.id, rejectReason)
      toast.success(`KPI "${selectedKPI.title}" has been rejected`)
      // Remove from list
      setKpis(prev => prev.filter(k => k.id !== selectedKPI.id))
      setShowRejectModal(false)
      setSelectedKPI(null)
      setRejectReason('')
    } catch (error) {
      console.error('Failed to reject KPI:', error)
      toast.error(error.response?.data?.detail || 'Failed to reject KPI')
    } finally {
      setActionLoading(prev => ({ ...prev, [selectedKPI.id]: false }))
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Pending Approvals</h1>
        <p className="text-gray-600 mt-1">Review and approve/reject KPIs submitted by your team</p>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading pending approvals...</p>
          </div>
        </div>
      ) : kpis.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">✅</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">All Caught Up!</h3>
          <p className="text-gray-600">
            There are no KPIs waiting for your approval at this time.
          </p>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    KPI Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Employee
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Period
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Progress
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Submitted
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {kpis.map(kpi => (
                  <tr key={kpi.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <Link
                          to={`/kpis/${kpi.id}`}
                          className="text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline"
                        >
                          {kpi.title}
                        </Link>
                        {kpi.description && (
                          <p className="text-sm text-gray-500 mt-1 line-clamp-1">
                            {kpi.description}
                          </p>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {kpi.user?.full_name || kpi.user?.username || 'Unknown'}
                      </div>
                      {kpi.user?.department && (
                        <div className="text-sm text-gray-500">{kpi.user.department}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {kpi.quarter} {kpi.year}
                      </div>
                      {kpi.category && (
                        <div className="text-xs text-gray-500 mt-1">{kpi.category}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-24">
                          <div className="text-xs font-medium text-gray-700 mb-1">
                            {kpi.progress_percentage || 0}%
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full transition-all"
                              style={{ width: `${kpi.progress_percentage || 0}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">
                        {formatDate(kpi.submitted_at)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleApprove(kpi)}
                          disabled={actionLoading[kpi.id]}
                          className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {actionLoading[kpi.id] ? (
                            <>
                              <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-1"></div>
                              Processing...
                            </>
                          ) : (
                            <>
                              ✓ Approve
                            </>
                          )}
                        </button>
                        <button
                          onClick={() => handleRejectClick(kpi)}
                          disabled={actionLoading[kpi.id]}
                          className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          ✗ Reject
                        </button>
                        <Link
                          to={`/kpis/${kpi.id}`}
                          className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          View Details
                        </Link>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Summary */}
          <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
            <p className="text-sm text-gray-600">
              Showing <span className="font-medium text-gray-900">{kpis.length}</span> pending approval{kpis.length !== 1 ? 's' : ''}
            </p>
          </div>
        </div>
      )}

      {/* Reject Modal */}
      {showRejectModal && selectedKPI && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-lg w-full p-6">
            <div className="mb-4">
              <h3 className="text-lg font-medium text-gray-900">Reject KPI</h3>
              <p className="text-sm text-gray-500 mt-1">
                Please provide a reason for rejecting "{selectedKPI.title}"
              </p>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Rejection Reason <span className="text-red-500">*</span>
              </label>
              <textarea
                value={rejectReason}
                onChange={(e) => setRejectReason(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Explain why this KPI is being rejected..."
                autoFocus
              />
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setShowRejectModal(false)
                  setSelectedKPI(null)
                  setRejectReason('')
                }}
                disabled={actionLoading[selectedKPI.id]}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Cancel
              </button>
              <button
                onClick={handleRejectSubmit}
                disabled={actionLoading[selectedKPI.id] || !rejectReason.trim()}
                className="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {actionLoading[selectedKPI.id] ? 'Rejecting...' : 'Reject KPI'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ApprovalsPage
