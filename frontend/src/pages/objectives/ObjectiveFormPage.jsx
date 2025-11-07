import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import objectiveService from '../../services/objectiveService'
import { toast } from 'react-toastify'

function ObjectiveFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const isEditMode = Boolean(id)

  const [loading, setLoading] = useState(isEditMode)
  const [submitting, setSubmitting] = useState(false)
  const [parentObjectives, setParentObjectives] = useState([])
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    year: new Date().getFullYear(),
    quarter: '', // Default to Annual
    level: 4, // Default to individual level
    status: 'active',
    department: user?.department || '',
    parent_id: null,
    start_date: '',
    end_date: '',
    manual_progress: 0,
  })

  useEffect(() => {
    if (isEditMode) {
      fetchObjective()
    }
    fetchParentObjectives()
  }, [id])

  const fetchObjective = async () => {
    try {
      setLoading(true)
      const data = await objectiveService.getObjective(id)

      // Convert string level to integer for form
      const levelMap = {
        'company': 0,
        'unit': 1,
        'division': 2,
        'team': 3,
        'individual': 4
      }

      setFormData({
        title: data.title,
        description: data.description || '',
        year: data.year,
        quarter: data.quarter,
        level: levelMap[data.level] || 3,
        status: data.status,
        department: data.department || '',
        parent_id: data.parent_id,
        start_date: data.start_date ? data.start_date.split('T')[0] : '',
        end_date: data.end_date ? data.end_date.split('T')[0] : '',
        manual_progress: data.manual_progress || 0,
      })
    } catch (error) {
      console.error('Failed to fetch objective:', error)
      toast.error('Failed to load objective')
      navigate('/objectives')
    } finally {
      setLoading(false)
    }
  }

  const fetchParentObjectives = async () => {
    try {
      // Fetch objectives that can be parents (based on level)
      const currentLevel = parseInt(formData.level)
      if (currentLevel > 0) {
        // Convert to string level for API
        const levelMap = ['company', 'unit', 'division', 'team', 'individual']
        const parentLevel = levelMap[currentLevel - 1]

        const data = await objectiveService.getObjectives({
          level: parentLevel,
          status: 'active',
          year: formData.year,
        })
        setParentObjectives(data.items || data)
      } else {
        setParentObjectives([])
      }
    } catch (error) {
      console.error('Failed to fetch parent objectives:', error)
    }
  }

  useEffect(() => {
    if (!isEditMode) {
      fetchParentObjectives()
    }
  }, [formData.level, formData.year])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleLevelChange = (e) => {
    const newLevel = parseInt(e.target.value)
    setFormData(prev => ({
      ...prev,
      level: newLevel,
      parent_id: null, // Reset parent when level changes
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validation
    if (!formData.title.trim()) {
      toast.error('Title is required')
      return
    }

    if (formData.start_date && formData.end_date) {
      if (new Date(formData.start_date) > new Date(formData.end_date)) {
        toast.error('Start date must be before end date')
        return
      }
    }

    try {
      setSubmitting(true)

      // Convert level integer to string for backend
      const levelMap = {
        0: 'company',
        1: 'unit',
        2: 'division',
        3: 'team',
        4: 'individual'
      }

      const submitData = {
        ...formData,
        level: levelMap[parseInt(formData.level)],
        quarter: formData.quarter || null, // Convert empty string to null for annual objectives
        manual_progress: parseFloat(formData.manual_progress) || 0,
        owner_id: user.id, // Add owner_id for creation
      }

      if (isEditMode) {
        await objectiveService.updateObjective(id, submitData)
        toast.success('Objective updated successfully')
      } else {
        await objectiveService.createObjective(submitData)
        toast.success('Objective created successfully')
      }
      navigate('/objectives')
    } catch (error) {
      console.error('Failed to save objective:', error)
      toast.error(error.response?.data?.detail || 'Failed to save objective')
    } finally {
      setSubmitting(false)
    }
  }

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

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {isEditMode ? 'Edit Objective' : 'Create New Objective'}
        </h1>
        <p className="text-gray-600 mt-1">
          {isEditMode ? 'Update objective details' : 'Create a new organizational objective'}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>

          <div className="space-y-4">
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Increase market share in Southeast Asia"
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows="4"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Describe the objective and its strategic importance..."
              />
            </div>
          </div>
        </div>

        {/* Organization & Hierarchy */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Organization & Hierarchy</h2>

          <div className="space-y-4">
            {/* Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Level <span className="text-red-500">*</span>
              </label>
              <select
                name="level"
                value={formData.level}
                onChange={handleLevelChange}
                required
                disabled={isEditMode} // Can't change level after creation
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              >
                <option value="0">🏢 Company Level (0)</option>
                <option value="1">🏛️ Unit Level (1)</option>
                <option value="2">🏢 Division Level (2)</option>
                <option value="3">👥 Team Level (3)</option>
                <option value="4">👤 Individual Level (4)</option>
              </select>
              {isEditMode && (
                <p className="text-xs text-gray-500 mt-1">
                  Level cannot be changed after creation
                </p>
              )}
            </div>

            {/* Parent Objective */}
            {formData.level > 0 && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Parent Objective {formData.level === 1 && <span className="text-red-500">*</span>}
                </label>
                <select
                  name="parent_id"
                  value={formData.parent_id || ''}
                  onChange={handleChange}
                  required={formData.level === 1}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">
                    {parentObjectives.length === 0
                      ? `No Level ${formData.level - 1} objectives available`
                      : 'Select parent objective...'}
                  </option>
                  {parentObjectives.map(obj => (
                    <option key={obj.id} value={obj.id}>
                      {obj.title} ({obj.year} {obj.quarter})
                    </option>
                  ))}
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  Select a Level {formData.level - 1} objective as the parent
                </p>
              </div>
            )}

            {/* Department */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Department
              </label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Sales, Engineering, Marketing"
              />
            </div>
          </div>
        </div>

        {/* Timeline & Status */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Timeline & Status</h2>

          <div className="space-y-4">
            {/* Year and Quarter */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Year <span className="text-red-500">*</span>
                </label>
                <select
                  name="year"
                  value={formData.year}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() + i).map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Period
                </label>
                <select
                  name="quarter"
                  value={formData.quarter}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Annual (Full Year)</option>
                  <option value="H1">H1 - First Half (Jan-Jun)</option>
                  <option value="H2">H2 - Second Half (Jul-Dec)</option>
                  <option value="Q1">Q1 (Jan-Mar)</option>
                  <option value="Q2">Q2 (Apr-Jun)</option>
                  <option value="Q3">Q3 (Jul-Sep)</option>
                  <option value="Q4">Q4 (Oct-Dec)</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  Leave as "Annual" for year-long objectives, or select specific period
                </p>
              </div>
            </div>

            {/* Start and End Dates */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Start Date
                </label>
                <input
                  type="date"
                  name="start_date"
                  value={formData.start_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  End Date
                </label>
                <input
                  type="date"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Status */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status <span className="text-red-500">*</span>
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="active">🎯 Active</option>
                <option value="completed">✅ Completed</option>
                <option value="on_hold">⏸️ On Hold</option>
                <option value="cancelled">❌ Cancelled</option>
              </select>
            </div>
          </div>
        </div>

        {/* Progress */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Progress</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Manual Progress: {formData.manual_progress}%
              </label>
              <input
                type="range"
                name="manual_progress"
                min="0"
                max="100"
                value={formData.manual_progress}
                onChange={handleChange}
                className="w-full"
              />
              <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
                <div
                  className={`h-3 rounded-full transition-all ${
                    formData.manual_progress >= 75
                      ? 'bg-green-600'
                      : formData.manual_progress >= 50
                      ? 'bg-blue-600'
                      : formData.manual_progress >= 25
                      ? 'bg-yellow-600'
                      : 'bg-red-600'
                  }`}
                  style={{ width: `${formData.manual_progress}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Note: Progress will be automatically calculated from linked KPIs and sub-objectives.
                Manual progress is used only when there are no linked items.
              </p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-4">
          <button
            type="button"
            onClick={() => navigate('/objectives')}
            className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="btn-primary disabled:opacity-50"
          >
            {submitting ? 'Saving...' : isEditMode ? 'Update Objective' : 'Create Objective'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default ObjectiveFormPage
