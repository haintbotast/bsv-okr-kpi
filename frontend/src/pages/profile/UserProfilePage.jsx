/**
 * UserProfilePage - User profile with avatar upload
 */

import { useState, useRef } from 'react'
import { toast } from 'react-toastify'
import { useAuth } from '../../hooks/useAuth'
import userService from '../../services/userService'

function UserProfilePage() {
  const { user, refreshUser } = useAuth()
  const [uploading, setUploading] = useState(false)
  const [avatarPreview, setAvatarPreview] = useState(null)
  const fileInputRef = useRef(null)

  const getAvatarUrl = (avatarUrl) => {
    if (!avatarUrl) return null
    // If it's already a full URL, return it
    if (avatarUrl.startsWith('http')) return avatarUrl
    // Otherwise, prepend the API base URL
    return `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${avatarUrl}`
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (!file) return

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if (!validTypes.includes(file.type)) {
      toast.error('Invalid file type. Please upload a JPG, PNG, GIF, or WebP image.')
      return
    }

    // Validate file size (5MB)
    const maxSize = 5 * 1024 * 1024 // 5MB
    if (file.size > maxSize) {
      toast.error('File too large. Maximum size is 5MB.')
      return
    }

    // Show preview
    const reader = new FileReader()
    reader.onloadend = () => {
      setAvatarPreview(reader.result)
    }
    reader.readAsDataURL(file)

    // Upload
    handleUpload(file)
  }

  const handleUpload = async (file) => {
    try {
      setUploading(true)
      const result = await userService.uploadAvatar(file)
      toast.success('Avatar uploaded successfully')

      // Refresh user data to get new avatar
      await refreshUser()
      setAvatarPreview(null)
    } catch (error) {
      console.error('Failed to upload avatar:', error)
      toast.error(error.response?.data?.detail || 'Failed to upload avatar')
      setAvatarPreview(null)
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete your avatar?')) {
      return
    }

    try {
      await userService.deleteAvatar()
      toast.success('Avatar deleted successfully')
      await refreshUser()
    } catch (error) {
      console.error('Failed to delete avatar:', error)
      toast.error(error.response?.data?.detail || 'Failed to delete avatar')
    }
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
        <p className="text-gray-600 mt-1">Manage your account settings and preferences</p>
      </div>

      {/* Avatar Section */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Profile Picture</h2>

        <div className="flex items-center space-x-6">
          {/* Avatar Display */}
          <div className="relative">
            {avatarPreview || user?.avatar_url ? (
              <img
                src={avatarPreview || getAvatarUrl(user.avatar_url)}
                alt="Avatar"
                className="w-32 h-32 rounded-full object-cover border-4 border-gray-200"
              />
            ) : (
              <div className="w-32 h-32 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center border-4 border-gray-200">
                <span className="text-4xl font-bold text-white">
                  {user?.full_name?.charAt(0)?.toUpperCase() || user?.username?.charAt(0)?.toUpperCase() || '?'}
                </span>
              </div>
            )}
            {uploading && (
              <div className="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
              </div>
            )}
          </div>

          {/* Upload/Delete Controls */}
          <div className="flex-1">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
              onChange={handleFileSelect}
              className="hidden"
            />

            <div className="space-y-2">
              <button
                onClick={triggerFileInput}
                disabled={uploading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploading ? 'Uploading...' : user?.avatar_url ? 'Change Avatar' : 'Upload Avatar'}
              </button>

              {user?.avatar_url && (
                <button
                  onClick={handleDelete}
                  disabled={uploading}
                  className="ml-2 px-4 py-2 border border-red-600 text-red-600 rounded-md hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Delete Avatar
                </button>
              )}
            </div>

            <p className="text-sm text-gray-500 mt-2">
              Accepted formats: JPG, PNG, GIF, WebP
              <br />
              Maximum size: 5MB
            </p>
          </div>
        </div>
      </div>

      {/* Profile Information */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Profile Information</h2>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name
              </label>
              <div className="px-3 py-2 border border-gray-300 rounded-md bg-gray-50">
                {user?.full_name || 'N/A'}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <div className="px-3 py-2 border border-gray-300 rounded-md bg-gray-50">
                {user?.username}
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <div className="px-3 py-2 border border-gray-300 rounded-md bg-gray-50">
              {user?.email}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Department
              </label>
              <div className="px-3 py-2 border border-gray-300 rounded-md bg-gray-50">
                {user?.department || 'N/A'}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Position
              </label>
              <div className="px-3 py-2 border border-gray-300 rounded-md bg-gray-50">
                {user?.position || 'N/A'}
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role
            </label>
            <div className="px-3 py-2 border border-gray-300 rounded-md bg-gray-50">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 capitalize">
                {user?.role}
              </span>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600">
            To update your profile information, please contact an administrator.
          </p>
        </div>
      </div>
    </div>
  )
}

export default UserProfilePage
