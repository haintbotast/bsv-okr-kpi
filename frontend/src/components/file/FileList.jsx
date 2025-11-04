/**
 * FileList Component - Display list of uploaded files with actions
 */

import { useState } from 'react';
import { toast } from 'react-hot-toast';
import fileService from '../../services/fileService';
import FileViewer from './FileViewer';

const FileList = ({ files, onFileDeleted, canDelete = false }) => {
  const [viewerFile, setViewerFile] = useState(null);
  const [showViewer, setShowViewer] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const handleDownload = async (file) => {
    try {
      await fileService.downloadFile(file.id, file.file_name);
      toast.success('File downloaded');
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download file');
    }
  };

  const handlePreview = (file) => {
    // Only preview images and PDFs
    const ext = file.file_name.split('.').pop().toLowerCase();
    if (['jpg', 'jpeg', 'png', 'pdf'].includes(ext)) {
      setViewerFile(file);
      setShowViewer(true);
    } else {
      toast.info('Preview not available for this file type');
    }
  };

  const handleDelete = async (file) => {
    if (!window.confirm(`Are you sure you want to delete "${file.file_name}"?`)) {
      return;
    }

    setDeletingId(file.id);
    try {
      await fileService.deleteFile(file.id);
      toast.success('File deleted successfully');

      if (onFileDeleted) {
        onFileDeleted(file.id);
      }
    } catch (error) {
      console.error('Delete error:', error);
      toast.error(error.response?.data?.detail || 'Failed to delete file');
    } finally {
      setDeletingId(null);
    }
  };

  const getFileIcon = (fileName) => {
    const ext = fileName.split('.').pop().toLowerCase();

    const iconClasses = "w-10 h-10";

    if (['jpg', 'jpeg', 'png'].includes(ext)) {
      return (
        <svg className={`${iconClasses} text-green-500`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      );
    }

    if (ext === 'pdf') {
      return (
        <svg className={`${iconClasses} text-red-500`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      );
    }

    if (['xls', 'xlsx'].includes(ext)) {
      return (
        <svg className={`${iconClasses} text-emerald-600`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
        </svg>
      );
    }

    // Default document icon
    return (
      <svg className={`${iconClasses} text-blue-500`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    );
  };

  if (!files || files.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
          />
        </svg>
        <p className="mt-2">No files uploaded yet</p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-3">
        {files.map((file) => (
          <div
            key={file.id}
            className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
          >
            <div className="flex items-center space-x-4 flex-1 min-w-0">
              <div className="flex-shrink-0">
                {getFileIcon(file.file_name)}
              </div>

              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {file.file_name}
                </p>
                <p className="text-xs text-gray-500">
                  {fileService.formatFileSize(file.file_size || 0)}
                  {' · '}
                  {new Date(file.uploaded_at).toLocaleDateString()}
                </p>
                {file.description && (
                  <p className="text-xs text-gray-600 mt-1">{file.description}</p>
                )}
              </div>
            </div>

            <div className="flex items-center space-x-2 ml-4">
              {/* Preview button */}
              {['jpg', 'jpeg', 'png', 'pdf'].includes(
                file.file_name.split('.').pop().toLowerCase()
              ) && (
                <button
                  onClick={() => handlePreview(file)}
                  className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                  title="Preview"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              )}

              {/* Download button */}
              <button
                onClick={() => handleDownload(file)}
                className="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                title="Download"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
              </button>

              {/* Delete button */}
              {canDelete && (
                <button
                  onClick={() => handleDelete(file)}
                  disabled={deletingId === file.id}
                  className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  title="Delete"
                >
                  {deletingId === file.id ? (
                    <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  )}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* File Viewer Modal */}
      {showViewer && viewerFile && (
        <FileViewer
          file={viewerFile}
          onClose={() => {
            setShowViewer(false);
            setViewerFile(null);
          }}
        />
      )}
    </>
  );
};

export default FileList;
