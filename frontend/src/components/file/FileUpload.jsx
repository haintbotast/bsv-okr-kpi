/**
 * FileUpload Component - Drag & drop file upload with progress
 * Requires: react-dropzone package (add to package.json)
 */

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-hot-toast';
import fileService from '../../services/fileService';

const FileUpload = ({ kpiId, onUploadComplete }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(
    async (acceptedFiles) => {
      if (acceptedFiles.length === 0) return;

      const file = acceptedFiles[0];

      // Validate file
      const validation = fileService.validateFile(file);
      if (!validation.valid) {
        toast.error(validation.error);
        return;
      }

      setUploading(true);
      setUploadProgress(0);

      try {
        await fileService.uploadFile(
          kpiId,
          file,
          null,
          (progress) => {
            setUploadProgress(progress);
          }
        );

        toast.success(`File "${file.name}" uploaded successfully`);
        setUploadProgress(0);

        if (onUploadComplete) {
          onUploadComplete();
        }
      } catch (error) {
        console.error('Upload error:', error);
        toast.error(
          error.response?.data?.detail || 'Failed to upload file'
        );
      } finally {
        setUploading(false);
      }
    },
    [kpiId, onUploadComplete]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
    disabled: uploading,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
    },
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors duration-200
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />

        {uploading ? (
          <div className="space-y-3">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="text-sm text-gray-600">Uploading... {uploadProgress}%</p>
            <div className="w-full bg-gray-200 rounded-full h-2 max-w-md mx-auto">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
              aria-hidden="true"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <div className="text-sm text-gray-600">
              {isDragActive ? (
                <p className="font-medium text-blue-600">Drop file here...</p>
              ) : (
                <>
                  <p>
                    <span className="font-medium text-blue-600 hover:text-blue-500">
                      Click to upload
                    </span>{' '}
                    or drag and drop
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    PDF, DOC, DOCX, XLS, XLSX, JPG, PNG (max 50MB)
                  </p>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
