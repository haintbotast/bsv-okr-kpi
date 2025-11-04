/**
 * TemplateManagementPage - Admin template management
 */

import { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import kpiService from '../../services/kpiService';

const TemplateManagementPage = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    role: 'employee',
    measurement_method: '',
    target_type: '',
  });

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const data = await kpiService.getTemplates();
      setTemplates(data);
    } catch (error) {
      console.error('Failed to fetch templates:', error);
      toast.error('Failed to load templates');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTemplate) {
        await kpiService.updateTemplate(editingTemplate.id, formData);
        toast.success('Template updated');
      } else {
        await kpiService.createTemplate(formData);
        toast.success('Template created');
      }
      setShowModal(false);
      resetForm();
      fetchTemplates();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Operation failed');
    }
  };

  const handleEdit = (template) => {
    setEditingTemplate(template);
    setFormData({
      name: template.name,
      description: template.description || '',
      category: template.category || '',
      role: template.role || 'employee',
      measurement_method: template.measurement_method || '',
      target_type: template.target_type || '',
    });
    setShowModal(true);
  };

  const handleDelete = async (templateId) => {
    if (!window.confirm('Are you sure you want to delete this template?')) return;
    try {
      await kpiService.deleteTemplate(templateId);
      toast.success('Template deleted');
      fetchTemplates();
    } catch (error) {
      toast.error('Failed to delete template');
    }
  };

  const resetForm = () => {
    setEditingTemplate(null);
    setFormData({
      name: '',
      description: '',
      category: '',
      role: 'employee',
      measurement_method: '',
      target_type: '',
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Template Management</h1>
        <button
          onClick={() => { resetForm(); setShowModal(true); }}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Add Template
        </button>
      </div>

      {/* Templates Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map((template) => (
          <div key={template.id} className="card">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold text-gray-900">{template.name}</h3>
              <span className="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 capitalize">
                {template.role}
              </span>
            </div>
            {template.description && (
              <p className="text-sm text-gray-600 mb-3">{template.description}</p>
            )}
            {template.category && (
              <p className="text-sm text-gray-500 mb-2">Category: {template.category}</p>
            )}
            <div className="flex space-x-2 mt-4">
              <button
                onClick={() => handleEdit(template)}
                className="flex-1 px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(template.id)}
                className="flex-1 px-3 py-1 text-sm bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {editingTemplate ? 'Edit Template' : 'Add Template'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  rows="3"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <input
                  type="text"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                <select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="employee">Employee</option>
                  <option value="manager">Manager</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div className="flex space-x-2 pt-4">
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  {editingTemplate ? 'Update' : 'Create'}
                </button>
                <button
                  type="button"
                  onClick={() => { setShowModal(false); resetForm(); }}
                  className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TemplateManagementPage;
