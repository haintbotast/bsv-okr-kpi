/**
 * SystemSettingsPage - Admin system settings management
 */

import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import settingsService from '../../services/settingsService'
import SMTPSettingsTab from './components/SMTPSettingsTab'

function SystemSettingsPage() {
  const [activeTab, setActiveTab] = useState('categories') // 'categories' or 'email'
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [newCategory, setNewCategory] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    try {
      setLoading(true)
      const data = await settingsService.getCategories()
      setCategories(data)
    } catch (error) {
      console.error('Failed to fetch categories:', error)
      toast.error('Failed to load categories')
    } finally {
      setLoading(false)
    }
  }

  const handleAddCategory = async (e) => {
    e.preventDefault()

    if (!newCategory.trim()) {
      toast.error('Category name is required')
      return
    }

    // Check if category already exists
    if (categories.some(cat => cat.name.toLowerCase() === newCategory.trim().toLowerCase())) {
      toast.error('Category already exists')
      return
    }

    try {
      setSubmitting(true)
      await settingsService.addCategory(newCategory.trim())
      toast.success(`Category "${newCategory}" added successfully`)
      setNewCategory('')
      setShowAddModal(false)
      fetchCategories()
    } catch (error) {
      console.error('Failed to add category:', error)
      toast.error(error.response?.data?.detail || 'Failed to add category')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteCategory = async (categoryName) => {
    if (!window.confirm(`Are you sure you want to delete category "${categoryName}"?\n\nNote: Existing KPIs with this category will keep their value.`)) {
      return
    }

    try {
      await settingsService.deleteCategory(categoryName)
      toast.success(`Category "${categoryName}" deleted successfully`)
      fetchCategories()
    } catch (error) {
      console.error('Failed to delete category:', error)
      toast.error(error.response?.data?.detail || 'Failed to delete category')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading settings...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">System Settings</h1>
        <p className="text-gray-600 mt-1">Manage system-wide configuration and settings</p>
      </div>

      {/* Tabs */}
      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('categories')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'categories'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📂 KPI Categories
          </button>
          <button
            onClick={() => setActiveTab('email')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'email'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📧 Email / SMTP
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'categories' && (
        <>
          {/* KPI Categories Section */}
          <div className="card">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">KPI Categories</h2>
            <p className="text-sm text-gray-600 mt-1">
              Define categories that users can select when creating KPIs
            </p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Add Category
          </button>
        </div>

        {/* Categories List */}
        {categories.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-md">
            <div className="text-4xl mb-3">📂</div>
            <p className="text-gray-600 mb-4">No categories defined yet</p>
            <button
              onClick={() => setShowAddModal(true)}
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Add your first category
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            {categories.map((category, index) => (
              <div
                key={category.name}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center">
                  <span className="text-gray-500 font-mono text-sm w-8">{index + 1}.</span>
                  <span className="font-medium text-gray-900">{category.name}</span>
                </div>
                <button
                  onClick={() => handleDeleteCategory(category.name)}
                  className="px-3 py-1 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition-colors"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600">
            Total: <span className="font-medium text-gray-900">{categories.length}</span> {categories.length === 1 ? 'category' : 'categories'}
          </p>
        </div>
          </div>
        </>
      )}

      {activeTab === 'email' && (
        <SMTPSettingsTab />
      )}

      {/* Add Category Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Category</h3>
            <form onSubmit={handleAddCategory}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Finance, HR, Quality Assurance"
                  autoFocus
                  required
                />
                <p className="text-xs text-gray-500 mt-1">
                  This category will appear in the dropdown when users create KPIs
                </p>
              </div>

              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowAddModal(false)
                    setNewCategory('')
                  }}
                  disabled={submitting}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting || !newCategory.trim()}
                  className="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {submitting ? 'Adding...' : 'Add Category'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default SystemSettingsPage
