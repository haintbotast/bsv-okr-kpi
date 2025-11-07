import { useEffect, useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import objectiveService from '../../services/objectiveService'
import kpiService from '../../services/kpiService'
import { toast } from 'react-toastify'

function ObjectiveDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [objective, setObjective] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [children, setChildren] = useState([])
  const [ancestors, setAncestors] = useState([])
  const [linkedKPIs, setLinkedKPIs] = useState([])
  const [progressDetails, setProgressDetails] = useState(null)

  // Modals
  const [showLinkKPIModal, setShowLinkKPIModal] = useState(false)
  const [availableKPIs, setAvailableKPIs] = useState([])
  const [selectedKPI, setSelectedKPI] = useState(null)
  const [kpiWeight, setKpiWeight] = useState(100)

  useEffect(() => {
    fetchObjective()
    fetchChildren()
    fetchAncestors()
    fetchLinkedKPIs()
    fetchProgress()
  }, [id])

  const fetchObjective = async () => {
    try {
      setLoading(true)
      const data = await objectiveService.getObjective(id)
      setObjective(data)
    } catch (error) {
      console.error('Failed to fetch objective:', error)
      toast.error('Failed to load objective')
      navigate('/objectives')
    } finally {
      setLoading(false)
    }
  }

  const fetchChildren = async () => {
    try {
      const data = await objectiveService.getChildren(id)
      setChildren(data)
    } catch (error) {
      console.error('Failed to fetch children:', error)
      setChildren([])
    }
  }

  const fetchAncestors = async () => {
    try {
      const data = await objectiveService.getAncestors(id)
      setAncestors(data)
    } catch (error) {
      console.error('Failed to fetch ancestors:', error)
      setAncestors([])
    }
  }

  const fetchLinkedKPIs = async () => {
    try {
      const data = await objectiveService.getLinkedKPIs(id)
      setLinkedKPIs(data)
    } catch (error) {
      console.error('Failed to fetch linked KPIs:', error)
      setLinkedKPIs([])
    }
  }

  const fetchProgress = async () => {
    try {
      const data = await objectiveService.getProgress(id)
      setProgressDetails(data)
    } catch (error) {
      console.error('Failed to fetch progress:', error)
    }
  }

  const handleRecalculateProgress = async () => {
    try {
      setActionLoading(true)
      await objectiveService.recalculateProgress(id)
      toast.success('Progress recalculated successfully')
      fetchObjective()
      fetchProgress()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to recalculate progress')
    } finally {
      setActionLoading(false)
    }
  }

  const handleLinkKPI = async () => {
    try {
      // Fetch available KPIs for linking
      const kpisData = await kpiService.getKPIs({
        year: objective.year,
        status: 'approved',
      })
      setAvailableKPIs(kpisData.items || kpisData)
      setShowLinkKPIModal(true)
    } catch (error) {
      toast.error('Failed to load available KPIs')
    }
  }

  const handleConfirmLinkKPI = async () => {
    if (!selectedKPI) {
      toast.error('Please select a KPI')
      return
    }

    try {
      setActionLoading(true)
      await objectiveService.linkKPI(id, {
        kpi_id: selectedKPI,
        weight: parseFloat(kpiWeight) || 100,
      })
      toast.success('KPI linked successfully')
      setShowLinkKPIModal(false)
      setSelectedKPI(null)
      setKpiWeight(100)
      fetchLinkedKPIs()
      fetchProgress()
      fetchObjective()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to link KPI')
    } finally {
      setActionLoading(false)
    }
  }

  const handleUnlinkKPI = async (kpiId) => {
    if (!window.confirm('Remove this KPI from the objective?')) return

    try {
      setActionLoading(true)
      await objectiveService.unlinkKPI(id, kpiId)
      toast.success('KPI unlinked successfully')
      fetchLinkedKPIs()
      fetchProgress()
      fetchObjective()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to unlink KPI')
    } finally {
      setActionLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this objective? This action cannot be undone.')) return

    try {
      setActionLoading(true)
      await objectiveService.deleteObjective(id)
      toast.success('Objective deleted successfully')
      navigate('/objectives')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to delete objective')
      setActionLoading(false)
    }
  }

  const getLevelLabel = (level) => {
    const labels = {
      0: 'Company',
      1: 'Division',
      2: 'Team',
      3: 'Individual',
    }
    return labels[level] || `Level ${level}`
  }

  const getLevelIcon = (level) => {
    const icons = {
      0: '🏢',
      1: '🏛️',
      2: '👥',
      3: '👤',
    }
    return icons[level] || '📊'
  }

  const getStatusColor = (status) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
      on_hold: 'bg-yellow-100 text-yellow-800',
      cancelled: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const canEdit = objective && ['admin', 'manager'].includes(user?.role)
  const canDelete = objective && user?.role === 'admin'

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading objective...</p>
        </div>
      </div>
    )
  }

  if (!objective) return null

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <Link to="/objectives" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
          ← Back to Objectives
        </Link>
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{objective.title}</h1>
            <div className="flex items-center gap-4">
              <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(objective.status)}`}>
                {objective.status}
              </span>
              <span className="px-3 py-1 text-sm font-medium rounded-full bg-purple-100 text-purple-800">
                {getLevelIcon(objective.level)} {getLevelLabel(objective.level)}
              </span>
              <span className="text-gray-600">
                {objective.year} {objective.quarter}
              </span>
              {objective.department && (
                <span className="text-gray-600">
                  🏢 {objective.department}
                </span>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            <button
              onClick={handleRecalculateProgress}
              disabled={actionLoading}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
            >
              🔄 Recalculate
            </button>
            {canEdit && (
              <Link
                to={`/objectives/${id}/edit`}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Edit
              </Link>
            )}
            {canDelete && (
              <button
                onClick={handleDelete}
                disabled={actionLoading}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
              >
                Delete
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Breadcrumb - Ancestor Chain */}
      {ancestors.length > 0 && (
        <div className="card mb-6 bg-blue-50 border-blue-200">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">Hierarchy Path</h3>
          <div className="flex items-center gap-2 text-sm">
            {ancestors.map((ancestor, index) => (
              <div key={ancestor.id} className="flex items-center">
                {index > 0 && <span className="text-blue-400 mx-2">→</span>}
                <Link
                  to={`/objectives/${ancestor.id}`}
                  className="text-blue-700 hover:text-blue-900 font-medium"
                >
                  {getLevelIcon(ancestor.level)} {ancestor.title}
                </Link>
              </div>
            ))}
            <span className="text-blue-400 mx-2">→</span>
            <span className="text-blue-900 font-semibold">
              {getLevelIcon(objective.level)} {objective.title}
            </span>
          </div>
        </div>
      )}

      {/* Description */}
      {objective.description && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Description</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{objective.description}</p>
        </div>
      )}

      {/* Progress */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Progress</h2>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Overall Progress</span>
              <span className="font-semibold text-gray-900">
                {Math.round(objective.progress || 0)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className={`h-4 rounded-full transition-all ${
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
          </div>

          {progressDetails && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg text-sm">
              <p className="text-gray-700">
                <strong>Calculation Method:</strong> {progressDetails.method}
              </p>
              {progressDetails.details && (
                <p className="text-gray-600 mt-1">{progressDetails.details}</p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Timeline */}
      {(objective.start_date || objective.end_date) && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Timeline</h2>
          <div className="grid grid-cols-2 gap-4">
            {objective.start_date && (
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Start Date</p>
                <p className="text-xl font-semibold text-gray-900">
                  {new Date(objective.start_date).toLocaleDateString()}
                </p>
              </div>
            )}
            {objective.end_date && (
              <div className="p-4 bg-green-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">End Date</p>
                <p className="text-xl font-semibold text-gray-900">
                  {new Date(objective.end_date).toLocaleDateString()}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Linked KPIs */}
      <div className="card mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Linked KPIs ({linkedKPIs.length})</h2>
          {canEdit && (
            <button
              onClick={handleLinkKPI}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
            >
              + Link KPI
            </button>
          )}
        </div>

        {linkedKPIs.length === 0 ? (
          <p className="text-gray-600 text-sm">No KPIs linked yet</p>
        ) : (
          <div className="space-y-3">
            {linkedKPIs.map((link) => (
              <div key={link.kpi_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <Link
                    to={`/kpis/${link.kpi_id}`}
                    className="text-blue-600 hover:text-blue-700 font-medium"
                  >
                    {link.kpi_title}
                  </Link>
                  <div className="text-sm text-gray-600 mt-1">
                    Weight: {link.weight}% • Progress: {Math.round(link.kpi_progress || 0)}%
                  </div>
                </div>
                {canEdit && (
                  <button
                    onClick={() => handleUnlinkKPI(link.kpi_id)}
                    className="ml-4 px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                  >
                    Unlink
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Sub-objectives */}
      {children.length > 0 && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Sub-objectives ({children.length})
          </h2>
          <div className="space-y-3">
            {children.map((child) => (
              <Link
                key={child.id}
                to={`/objectives/${child.id}`}
                className="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-lg font-semibold text-gray-900">{child.title}</span>
                      <span className="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800">
                        {getLevelIcon(child.level)} {getLevelLabel(child.level)}
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      {child.year} {child.quarter} • {Math.round(child.progress || 0)}% complete
                    </div>
                  </div>
                  <div className="w-24">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          child.progress >= 75
                            ? 'bg-green-600'
                            : child.progress >= 50
                            ? 'bg-blue-600'
                            : 'bg-yellow-600'
                        }`}
                        style={{ width: `${child.progress || 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Details */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Details</h2>
        <dl className="grid grid-cols-2 gap-4">
          {objective.owner_name && (
            <div>
              <dt className="text-sm text-gray-600">Owner</dt>
              <dd className="text-gray-900 font-medium">{objective.owner_name}</dd>
            </div>
          )}
          <div>
            <dt className="text-sm text-gray-600">Created At</dt>
            <dd className="text-gray-900 font-medium">
              {new Date(objective.created_at).toLocaleDateString()}
            </dd>
          </div>
          <div>
            <dt className="text-sm text-gray-600">Last Updated</dt>
            <dd className="text-gray-900 font-medium">
              {new Date(objective.updated_at).toLocaleDateString()}
            </dd>
          </div>
        </dl>
      </div>

      {/* Link KPI Modal */}
      {showLinkKPIModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Link KPI to Objective</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select KPI <span className="text-red-500">*</span>
                </label>
                <select
                  value={selectedKPI || ''}
                  onChange={(e) => setSelectedKPI(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Choose a KPI...</option>
                  {availableKPIs.map((kpi) => (
                    <option key={kpi.id} value={kpi.id}>
                      {kpi.title} ({kpi.year} {kpi.quarter}) - {kpi.progress_percentage || 0}%
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Weight (%) <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={kpiWeight}
                  onChange={(e) => setKpiWeight(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Weight determines how much this KPI contributes to the objective's progress
                </p>
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => {
                  setShowLinkKPIModal(false)
                  setSelectedKPI(null)
                  setKpiWeight(100)
                }}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmLinkKPI}
                disabled={!selectedKPI || actionLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {actionLoading ? 'Linking...' : 'Link KPI'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ObjectiveDetailPage
