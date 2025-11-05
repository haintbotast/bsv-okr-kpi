import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import kpiService from '../../services/kpiService'
import settingsService from '../../services/settingsService'
import { toast } from 'react-toastify'

function KPIFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const isEditMode = Boolean(id)

  const [loading, setLoading] = useState(isEditMode)
  const [submitting, setSubmitting] = useState(false)
  const [templates, setTemplates] = useState([])
  const [categories, setCategories] = useState([])
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    year: new Date().getFullYear(),
    quarter: 'Q1',
    category: '',
    target_value: '',
    current_value: '',
    progress_percentage: 0,
    measurement_method: '',
    template_id: null,
  })

  useEffect(() => {
    fetchTemplates()
    fetchCategories()
    if (isEditMode) {
      fetchKPI()
    }
  }, [id])

  const fetchTemplates = async () => {
    try {
      const data = await kpiService.getTemplates({ role: user?.role })
      setTemplates(data)
    } catch (error) {
      console.error('Failed to fetch templates:', error)
    }
  }

  const fetchCategories = async () => {
    try {
      const data = await settingsService.getCategories()
      setCategories(data)
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  }

  const fetchKPI = async () => {
    try {
      setLoading(true)
      const data = await kpiService.getKPI(id)
      setFormData({
        title: data.title,
        description: data.description || '',
        year: data.year,
        quarter: data.quarter,
        category: data.category || '',
        target_value: data.target_value || '',
        current_value: data.current_value || '',
        progress_percentage: data.progress_percentage || 0,
        measurement_method: data.measurement_method || '',
        template_id: data.template_id,
      })
    } catch (error) {
      console.error('Failed to fetch KPI:', error)
      toast.error('Failed to load KPI')
      navigate('/kpis')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleTemplateSelect = (templateId) => {
    const template = templates.find(t => t.id === parseInt(templateId))
    if (template) {
      setFormData(prev => ({
        ...prev,
        template_id: template.id,
        title: template.name,
        description: template.description || prev.description,
        category: template.category || prev.category,
        measurement_method: template.measurement_method || prev.measurement_method,
      }))
    } else {
      setFormData(prev => ({ ...prev, template_id: null }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validation
    if (!formData.title.trim()) {
      toast.error('Title is required')
      return
    }

    try {
      setSubmitting(true)
      if (isEditMode) {
        await kpiService.updateKPI(id, formData)
        toast.success('KPI updated successfully')
      } else {
        await kpiService.createKPI(formData)
        toast.success('KPI created successfully')
      }
      navigate('/kpis')
    } catch (error) {
      console.error('Failed to save KPI:', error)
      toast.error(error.response?.data?.detail || 'Failed to save KPI')
    } finally {
      setSubmitting(false)
    }
  }

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

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {isEditMode ? 'Edit KPI' : 'Create New KPI'}
        </h1>
        <p className="text-gray-600 mt-1">
          {isEditMode ? 'Update your KPI details' : 'Fill in the details to create a new KPI'}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Template Selection */}
        {!isEditMode && templates.length > 0 && (
          <div className="card">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Use Template (Optional)
            </label>
            <select
              value={formData.template_id || ''}
              onChange={(e) => handleTemplateSelect(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select a template...</option>
              {templates.map(template => (
                <option key={template.id} value={template.id}>
                  {template.name} {template.category && `(${template.category})`}
                </option>
              ))}
            </select>
          </div>
        )}

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
                placeholder="e.g., Increase customer satisfaction score"
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
                placeholder="Describe your KPI objectives and how it will be measured..."
              />
            </div>

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
                  Quarter <span className="text-red-500">*</span>
                </label>
                <select
                  name="quarter"
                  value={formData.quarter}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Q1">Q1 (Jan-Mar)</option>
                  <option value="Q2">Q2 (Apr-Jun)</option>
                  <option value="Q3">Q3 (Jul-Sep)</option>
                  <option value="Q4">Q4 (Oct-Dec)</option>
                </select>
              </div>
            </div>

            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Category
              </label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a category...</option>
                {categories.map(cat => (
                  <option key={cat.name} value={cat.name}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Targets & Progress */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Targets & Progress</h2>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Target Value
                </label>
                <input
                  type="text"
                  name="target_value"
                  value={formData.target_value}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 100 units, 95%, $50,000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Current Value
                </label>
                <input
                  type="text"
                  name="current_value"
                  value={formData.current_value}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 75 units, 80%, $40,000"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Progress Percentage: {formData.progress_percentage}%
              </label>
              <input
                type="range"
                name="progress_percentage"
                min="0"
                max="100"
                value={formData.progress_percentage}
                onChange={handleChange}
                className="w-full"
              />
              <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
                <div
                  className="bg-blue-600 h-3 rounded-full transition-all"
                  style={{ width: `${formData.progress_percentage}%` }}
                ></div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Measurement Method
              </label>
              <input
                type="text"
                name="measurement_method"
                value={formData.measurement_method}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Monthly reports, Customer surveys"
              />
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-4">
          <button
            type="button"
            onClick={() => navigate('/kpis')}
            className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="btn-primary disabled:opacity-50"
          >
            {submitting ? 'Saving...' : isEditMode ? 'Update KPI' : 'Create KPI'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default KPIFormPage
