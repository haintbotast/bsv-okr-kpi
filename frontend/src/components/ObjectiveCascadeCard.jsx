import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronRight, ChevronDown, Star } from 'lucide-react'
import objectiveService from '../services/objectiveService'
import { toast } from 'react-toastify'

function ObjectiveCascadeCard({ objective, level = 0, onToggleFeatured }) {
  const [isExpanded, setIsExpanded] = useState(level === 0) // Expand company level by default
  const [isTogglingFeatured, setIsTogglingFeatured] = useState(false)

  const getLevelConfig = () => {
    const configs = {
      company: {
        icon: '🏢',
        label: 'Company',
        bgClass: 'bg-purple-50',
        borderClass: 'border-purple-300',
        textClass: 'text-purple-700',
        progressClass: 'bg-purple-600',
      },
      unit: {
        icon: '🏛️',
        label: 'Unit',
        bgClass: 'bg-indigo-50',
        borderClass: 'border-indigo-300',
        textClass: 'text-indigo-700',
        progressClass: 'bg-indigo-600',
      },
      division: {
        icon: '🏬',
        label: 'Division',
        bgClass: 'bg-blue-50',
        borderClass: 'border-blue-300',
        textClass: 'text-blue-700',
        progressClass: 'bg-blue-600',
      },
      team: {
        icon: '👥',
        label: 'Team',
        bgClass: 'bg-green-50',
        borderClass: 'border-green-300',
        textClass: 'text-green-700',
        progressClass: 'bg-green-600',
      },
      individual: {
        icon: '👤',
        label: 'Individual',
        bgClass: 'bg-yellow-50',
        borderClass: 'border-yellow-300',
        textClass: 'text-yellow-700',
        progressClass: 'bg-yellow-600',
      },
    }
    return configs[objective.level] || configs.individual
  }

  const handleToggleFeatured = async (e) => {
    e.stopPropagation()
    setIsTogglingFeatured(true)

    try {
      await objectiveService.toggleFeatured(objective.id)
      toast.success(objective.is_featured ? 'Removed from featured' : 'Added to featured')
      if (onToggleFeatured) {
        onToggleFeatured()
      }
    } catch (error) {
      console.error('Failed to toggle featured:', error)
      toast.error(error.response?.data?.detail || 'Failed to update featured status')
    } finally {
      setIsTogglingFeatured(false)
    }
  }

  const config = getLevelConfig()
  const hasChildren = objective.children && objective.children.length > 0
  const hasKPIs = objective.kpis && objective.kpis.length > 0
  const hasContent = hasChildren || hasKPIs

  // Indentation based on level
  const marginLeft = level * 24 // 24px per level

  return (
    <div className="mb-3" style={{ marginLeft: `${marginLeft}px` }}>
      <div
        className={`border-2 ${config.borderClass} ${config.bgClass} rounded-lg overflow-hidden transition-all hover:shadow-md`}
      >
        {/* Header */}
        <div
          className={`p-4 cursor-pointer ${hasContent ? '' : 'cursor-default'}`}
          onClick={() => hasContent && setIsExpanded(!isExpanded)}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1 flex items-start space-x-3">
              {/* Expand/Collapse Icon */}
              <div className="mt-0.5">
                {hasContent ? (
                  isExpanded ? (
                    <ChevronDown className={`w-5 h-5 ${config.textClass}`} />
                  ) : (
                    <ChevronRight className={`w-5 h-5 ${config.textClass}`} />
                  )
                ) : (
                  <div className="w-5 h-5"></div>
                )}
              </div>

              {/* Icon and Content */}
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-2xl">{config.icon}</span>
                  <div>
                    <Link
                      to={`/objectives/${objective.id}`}
                      className={`font-semibold ${config.textClass} hover:underline text-lg`}
                      onClick={(e) => e.stopPropagation()}
                    >
                      {objective.title}
                    </Link>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className={`text-xs px-2 py-0.5 rounded ${config.bgClass} ${config.textClass} border ${config.borderClass}`}>
                        {config.label} Level
                      </span>
                      <span className="text-xs text-gray-600">
                        {objective.owner_name || 'Unassigned'}
                      </span>
                      {objective.department && (
                        <span className="text-xs text-gray-600">• {objective.department}</span>
                      )}
                      {objective.quarter ? (
                        <span className="text-xs text-gray-600">
                          • {objective.year} {objective.quarter}
                        </span>
                      ) : (
                        <span className="text-xs text-gray-600">• {objective.year} Annual</span>
                      )}
                    </div>
                  </div>
                </div>

                {objective.description && (
                  <p className="text-sm text-gray-600 mt-2 ml-8">{objective.description}</p>
                )}

                {/* Counts */}
                <div className="flex items-center space-x-4 mt-2 ml-8 text-xs text-gray-600">
                  {hasKPIs && <span>📊 {objective.kpi_count} Key Results</span>}
                  {hasChildren && <span>🎯 {objective.children_count} Child Objectives</span>}
                </div>
              </div>
            </div>

            {/* Progress and Actions */}
            <div className="flex items-start space-x-3 ml-4">
              {/* Featured Star */}
              <button
                onClick={handleToggleFeatured}
                disabled={isTogglingFeatured}
                className={`p-1.5 rounded transition-colors ${
                  objective.is_featured
                    ? 'bg-yellow-100 text-yellow-600 hover:bg-yellow-200'
                    : 'text-gray-400 hover:text-yellow-600 hover:bg-yellow-50'
                }`}
                title={objective.is_featured ? 'Remove from featured' : 'Add to featured'}
              >
                <Star className={`w-5 h-5 ${objective.is_featured ? 'fill-current' : ''}`} />
              </button>

              {/* Progress */}
              <div className="text-right min-w-[80px]">
                <p className={`text-2xl font-bold ${config.textClass}`}>
                  {objective.progress_percentage.toFixed(0)}%
                </p>
                <p className="text-xs text-gray-600">progress</p>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-3">
            <div className="w-full bg-white rounded-full h-2.5 shadow-inner">
              <div
                className={`${config.progressClass} h-2.5 rounded-full transition-all duration-500`}
                style={{ width: `${objective.progress_percentage}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Expanded Content */}
        {isExpanded && hasContent && (
          <div className="border-t-2 border-gray-200 bg-white p-4">
            {/* KPIs Section */}
            {hasKPIs && (
              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                  <span className="mr-2">📊</span> Key Results ({objective.kpis.length})
                </h4>
                <div className="space-y-2">
                  {objective.kpis.map((kpi) => (
                    <div
                      key={kpi.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded border border-gray-200 hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex-1">
                        <Link
                          to={`/kpis/${kpi.id}`}
                          className="text-sm font-medium text-gray-900 hover:text-blue-600"
                          onClick={(e) => e.stopPropagation()}
                        >
                          {kpi.title}
                        </Link>
                        <div className="flex items-center space-x-3 mt-1 text-xs text-gray-600">
                          {kpi.current_value !== null && kpi.target_value !== null && (
                            <span>
                              {kpi.current_value} / {kpi.target_value} {kpi.unit}
                            </span>
                          )}
                          <span>Weight: {(kpi.weight * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="text-right">
                          <p className="text-lg font-bold text-blue-600">
                            {kpi.progress_percentage.toFixed(0)}%
                          </p>
                        </div>
                        <div className="w-24">
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full transition-all"
                              style={{ width: `${kpi.progress_percentage}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Children Objectives */}
            {hasChildren && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                  <span className="mr-2">🎯</span> Child Objectives ({objective.children.length})
                </h4>
                <div className="space-y-2">
                  {objective.children.map((child) => (
                    <ObjectiveCascadeCard
                      key={child.id}
                      objective={child}
                      level={0} // Reset level for visual nesting
                      onToggleFeatured={onToggleFeatured}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ObjectiveCascadeCard
