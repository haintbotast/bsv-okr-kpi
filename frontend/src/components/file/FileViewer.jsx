/**
 * FileViewer Component - Preview PDF and images in modal
 * For PDF preview: requires react-pdf package (add to package.json)
 * For basic version without react-pdf, PDFs will open in new tab
 */

import { useState } from 'react';
import fileService from '../../services/fileService';

const FileViewer = ({ file, onClose }) => {
  const [imageError, setImageError] = useState(false);

  const fileUrl = fileService.getFileUrl(file.id);
  const fileExt = file.file_name.split('.').pop().toLowerCase();
  const isImage = ['jpg', 'jpeg', 'png'].includes(fileExt);
  const isPDF = fileExt === 'pdf';

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 p-4"
      onClick={handleOverlayClick}
    >
      <div className="relative bg-white rounded-lg shadow-xl max-w-6xl w-full max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-medium text-gray-900 truncate">
              {file.file_name}
            </h3>
            <p className="text-sm text-gray-500">
              {fileService.formatFileSize(file.file_size || 0)}
            </p>
          </div>

          <div className="flex items-center space-x-2 ml-4">
            {/* Download button */}
            <button
              onClick={() => fileService.downloadFile(file.id, file.file_name)}
              className="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
              title="Download"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>

            {/* Close button */}
            <button
              onClick={onClose}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              title="Close"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-4 bg-gray-50">
          {isImage && !imageError ? (
            <div className="flex items-center justify-center h-full">
              <img
                src={fileUrl}
                alt={file.file_name}
                className="max-w-full max-h-full object-contain rounded-lg shadow-lg"
                onError={() => setImageError(true)}
              />
            </div>
          ) : isPDF ? (
            <div className="h-full">
              {/*
                Option 1: Using iframe (simple but limited features)
                For better PDF viewing, install react-pdf and use Document/Page components
              */}
              <iframe
                src={fileUrl}
                className="w-full h-full rounded-lg shadow-lg"
                title={file.file_name}
              />

              {/*
                Option 2: Using react-pdf (better experience but requires package)
                Uncomment and install react-pdf to use:

                <Document
                  file={fileUrl}
                  onLoadError={(error) => console.error('Error loading PDF:', error)}
                >
                  <Page pageNumber={1} />
                </Document>
              */}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <svg className="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p className="text-lg font-medium mb-2">Preview not available</p>
              <p className="text-sm text-gray-400 mb-4">
                This file type cannot be previewed in the browser
              </p>
              <button
                onClick={() => fileService.downloadFile(file.id, file.file_name)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Download File
              </button>
            </div>
          )}

          {imageError && (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <svg className="w-16 h-16 mb-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-lg font-medium mb-2">Failed to load image</p>
              <p className="text-sm text-gray-400 mb-4">
                The image could not be displayed
              </p>
              <button
                onClick={() => fileService.downloadFile(file.id, file.file_name)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Download File
              </button>
            </div>
          )}
        </div>

        {/* Footer with description */}
        {file.description && (
          <div className="p-4 border-t border-gray-200 bg-gray-50">
            <p className="text-sm text-gray-600">
              <span className="font-medium">Description:</span> {file.description}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileViewer;
