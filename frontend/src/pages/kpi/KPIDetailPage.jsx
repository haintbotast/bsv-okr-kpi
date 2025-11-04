import { useEffect, useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import kpiService from '../../services/kpiService'
import fileService from '../../services/fileService'
import { toast } from 'react-toastify'
import FileUpload from '../../components/file/FileUpload'
import FileList from '../../components/file/FileList'

function KPIDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [kpi, setKpi] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [files, setFiles] = useState([])
  const [filesLoading, setFilesLoading] = useState(false)

  useEffect(() => {
    fetchKPI()
    fetchFiles()
  }, [id])

  const fetchKPI = async () => {
    try {
      setLoading(true)
      const data = await kpiService.getKPI(id)
      setKpi(data)
    } catch (error) {
      console.error('Failed to fetch KPI:', error)
      toast.error('Failed to load KPI')
      navigate('/kpis')
    } finally {
      setLoading(false)
    }
  }

  const fetchFiles = async () => {
    try {
      setFilesLoading(true)
      const data = await fileService.getFilesByKPI(id)
      setFiles(data)
    } catch (error) {
      console.error('Failed to fetch files:', error)
      // Don't show error toast - files might not be accessible
      setFiles([])
    } finally {
      setFilesLoading(false)
    }
  }

  const handleFileUploadComplete = () => {
    fetchFiles()
  }

  const handleFileDeleted = (fileId) => {
    setFiles(files.filter(f => f.id !== fileId))
  }

  const handleSubmit = async () => {
    if (!window.confirm('Submit this KPI for approval?')) return

    try {
      setActionLoading(true)
      await kpiService.submitKPI(id)
      toast.success('KPI submitted for approval')
      fetchKPI()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit KPI')
    } finally {
      setActionLoading(false)
    }
  }

  const handleApprove = async () => {
    const comment = window.prompt('Add a comment (optional):')
    if (comment === null) return

    try {
      setActionLoading(true)
      await kpiService.approveKPI(id, comment || null)
      toast.success('KPI approved successfully')
      fetchKPI()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to approve KPI')
    } finally {
      setActionLoading(false)
    }
  }

  const handleReject = async () => {
    const reason = window.prompt('Reason for rejection:')
    if (!reason) return

    try {
      setActionLoading(true)
      await kpiService.rejectKPI(id, reason)
      toast.success('KPI rejected')
      fetchKPI()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to reject KPI')
    } finally {
      setActionLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this KPI? This action cannot be undone.')) return

    try {
      setActionLoading(true)
      await kpiService.deleteKPI(id)
      toast.success('KPI deleted successfully')
      navigate('/kpis')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to delete KPI')
      setActionLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      submitted: 'bg-yellow-100 text-yellow-800',
      approved: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const canEdit = kpi && kpi.user_id === user?.id && ['draft', 'rejected'].includes(kpi.status)
  const canSubmit = kpi && kpi.user_id === user?.id && kpi.status === 'draft'
  const canDelete = kpi && kpi.user_id === user?.id && kpi.status === 'draft'
  const canApprove = kpi && ['admin', 'manager'].includes(user?.role) && kpi.status === 'submitted'

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading KPI...</p>
        </div>
      </div>
    )
  }

  if (!kpi) return null

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <Link to="/kpis" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
          ← Back to KPIs
        </Link>
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{kpi.title}</h1>
            <div className="flex items-center gap-4">
              <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(kpi.status)}`}>
                {kpi.status}
              </span>
              <span className="text-gray-600">
                {kpi.year} {kpi.quarter}
              </span>
              {kpi.category && (
                <span className="text-gray-600">
                  🏷️ {kpi.category}
                </span>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            {canEdit && (
              <Link
                to={`/kpis/${id}/edit`}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Edit
              </Link>
            )}
            {canSubmit && (
              <button
                onClick={handleSubmit}
                disabled={actionLoading}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                Submit for Approval
              </button>
            )}
            {canApprove && (
              <>
                <button
                  onClick={handleApprove}
                  disabled={actionLoading}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
                >
                  Approve
                </button>
                <button
                  onClick={handleReject}
                  disabled={actionLoading}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
                >
                  Reject
                </button>
              </>
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

      {/* Description */}
      {kpi.description && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Description</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{kpi.description}</p>
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
                {kpi.progress_percentage || 0}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className="bg-blue-600 h-4 rounded-full transition-all"
                style={{ width: `${kpi.progress_percentage || 0}%` }}
              ></div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Target Value</p>
              <p className="text-xl font-semibold text-gray-900">
                {kpi.target_value || 'Not set'}
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Current Value</p>
              <p className="text-xl font-semibold text-gray-900">
                {kpi.current_value || 'Not set'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Details */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Details</h2>
        <dl className="grid grid-cols-2 gap-4">
          <div>
            <dt className="text-sm text-gray-600">Measurement Method</dt>
            <dd className="text-gray-900 font-medium">
              {kpi.measurement_method || 'Not specified'}
            </dd>
          </div>
          <div>
            <dt className="text-sm text-gray-600">Created At</dt>
            <dd className="text-gray-900 font-medium">
              {new Date(kpi.created_at).toLocaleDateString()}
            </dd>
          </div>
          <div>
            <dt className="text-sm text-gray-600">Last Updated</dt>
            <dd className="text-gray-900 font-medium">
              {new Date(kpi.updated_at).toLocaleDateString()}
            </dd>
          </div>
          {kpi.submitted_at && (
            <div>
              <dt className="text-sm text-gray-600">Submitted At</dt>
              <dd className="text-gray-900 font-medium">
                {new Date(kpi.submitted_at).toLocaleDateString()}
              </dd>
            </div>
          )}
          {kpi.approved_at && (
            <div>
              <dt className="text-sm text-gray-600">Approved At</dt>
              <dd className="text-gray-900 font-medium">
                {new Date(kpi.approved_at).toLocaleDateString()}
              </dd>
            </div>
          )}
        </dl>
      </div>

      {/* Evidence Files */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Evidence Files</h2>

        {/* Upload section - only show if user owns the KPI */}
        {kpi.user_id === user?.id && (
          <div className="mb-6">
            <FileUpload kpiId={id} onUploadComplete={handleFileUploadComplete} />
          </div>
        )}

        {/* Files list */}
        {filesLoading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-sm text-gray-600">Loading files...</p>
          </div>
        ) : (
          <FileList
            files={files}
            onFileDeleted={handleFileDeleted}
            canDelete={kpi.user_id === user?.id || user?.role === 'admin'}
          />
        )}
      </div>

      {/* Placeholder for future sections */}
      <div className="card bg-gray-50">
        <p className="text-gray-600 text-sm">
          💬 Comments and 📋 history will be available in Phase 4
        </p>
      </div>
    </div>
  )
}

export default KPIDetailPage
