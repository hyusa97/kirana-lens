'use client';

import { useState, useCallback } from 'react';
import { Upload, X, Image as ImageIcon, CheckCircle, Loader2 } from 'lucide-react';

interface ImageUploadZoneProps {
  onImagesChange: (files: File[]) => void;
  maxFiles?: number;
  minFiles?: number;
}

export default function ImageUploadZone({ onImagesChange, maxFiles = 5, minFiles = 3 }: ImageUploadZoneProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadingFiles, setUploadingFiles] = useState<Set<string>>(new Set());
  const [error, setError] = useState<string>('');

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      setError('');

      const droppedFiles = Array.from(e.dataTransfer.files).filter((file) =>
        file.type.startsWith('image/')
      );

      if (files.length + droppedFiles.length > maxFiles) {
        setError(`Maximum ${maxFiles} images allowed`);
        return;
      }

      const newFiles = [...files, ...droppedFiles].slice(0, maxFiles);
      setFiles(newFiles);
      onImagesChange(newFiles);

      // Simulate upload progress
      droppedFiles.forEach((file) => {
        setUploadingFiles((prev) => new Set(prev).add(file.name));
        setTimeout(() => {
          setUploadingFiles((prev) => {
            const next = new Set(prev);
            next.delete(file.name);
            return next;
          });
        }, 1500);
      });
    },
    [files, maxFiles, onImagesChange]
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      
      if (files.length + selectedFiles.length > maxFiles) {
        setError(`Maximum ${maxFiles} images allowed`);
        return;
      }

      const newFiles = [...files, ...selectedFiles].slice(0, maxFiles);
      setFiles(newFiles);
      onImagesChange(newFiles);

      // Simulate upload progress
      selectedFiles.forEach((file) => {
        setUploadingFiles((prev) => new Set(prev).add(file.name));
        setTimeout(() => {
          setUploadingFiles((prev) => {
            const next = new Set(prev);
            next.delete(file.name);
            return next;
          });
        }, 1500);
      });
    }
  };

  const removeFile = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index);
    setFiles(newFiles);
    onImagesChange(newFiles);
    setError('');
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-card p-8 text-center transition-colors ${
          isDragging
            ? 'border-accent bg-accent/5'
            : error
            ? 'border-danger bg-danger/5'
            : 'border-gray-300 hover:border-accent hover:bg-gray-50'
        }`}
      >
        <input
          type="file"
          id="image-upload"
          multiple
          accept="image/jpeg,image/png,image/webp"
          onChange={handleFileInput}
          className="hidden"
        />
        <label htmlFor="image-upload" className="cursor-pointer">
          <Upload className="mx-auto mb-4 text-gray-400" size={48} />
          <p className="text-gray-700 font-medium mb-2">
            Drag & drop store images here, or click to select
          </p>
          <p className="text-sm text-gray-500 mb-4">
            JPEG, PNG, WEBP • Min {minFiles}, Max {maxFiles} images
          </p>
          <div className="text-xs text-gray-600 space-y-1">
            <p className="flex items-center justify-center gap-2">
              <CheckCircle size={14} className="text-success" />
              Interior shelves (2 images)
            </p>
            <p className="flex items-center justify-center gap-2">
              <CheckCircle size={14} className="text-success" />
              Counter area
            </p>
            <p className="flex items-center justify-center gap-2">
              <CheckCircle size={14} className="text-success" />
              Storefront exterior
            </p>
          </div>
        </label>
      </div>

      {error && (
        <div className="text-sm text-danger bg-danger/10 border border-danger rounded-input p-3">
          {error}
        </div>
      )}

      {files.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {files.map((file, index) => {
            const isUploading = uploadingFiles.has(file.name);
            
            return (
              <div key={index} className="relative group bg-white border border-gray-200 rounded-input overflow-hidden">
                <div className="aspect-video bg-gray-100 relative">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={URL.createObjectURL(file)}
                    alt={`Upload ${index + 1}`}
                    className="w-full h-full object-cover"
                  />
                  {isUploading && (
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                      <Loader2 className="text-white animate-spin" size={32} />
                    </div>
                  )}
                  {!isUploading && (
                    <button
                      onClick={() => removeFile(index)}
                      className="absolute top-2 right-2 bg-danger text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <X size={16} />
                    </button>
                  )}
                </div>
                <div className="p-3">
                  <p className="text-xs font-medium text-gray-900 truncate">{file.name}</p>
                  <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {files.length > 0 && (
        <div className="flex items-center justify-between text-sm">
          <p className={files.length >= minFiles ? 'text-success' : 'text-warning'}>
            {files.length} of {maxFiles} images uploaded
            {files.length < minFiles && ` (minimum ${minFiles} required)`}
          </p>
        </div>
      )}
    </div>
  );
}
