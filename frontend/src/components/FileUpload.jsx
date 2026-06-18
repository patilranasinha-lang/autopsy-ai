import { useState } from 'react'
import { Upload, File, X } from 'lucide-react'

const FileUpload = ({ onFileSelect, accept = '*', multiple = false }) => {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState([])

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = Array.from(e.dataTransfer.files)
    setSelectedFiles(files)
    onFileSelect?.(files)
  }

  const handleFileInput = (e) => {
    const files = Array.from(e.target.files)
    setSelectedFiles(files)
    onFileSelect?.(files)
  }

  const removeFile = (index) => {
    const newFiles = [...selectedFiles]
    newFiles.splice(index, 1)
    setSelectedFiles(newFiles)
    onFileSelect?.(newFiles)
  }

  return (
    <div className="w-full">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input').click()}
        className={`
          border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
          transition-all duration-200
          ${isDragging 
            ? 'border-emerald-500 bg-emerald-50' 
            : 'border-slate-300 hover:border-emerald-400 hover:bg-slate-50'}
        `}
      >
        <input
          id="file-input"
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={handleFileInput}
          className="hidden"
        />
        <div className="flex flex-col items-center gap-3">
          <div className={`
            w-16 h-16 rounded-full flex items-center justify-center
            ${isDragging ? 'bg-emerald-100 text-emerald-600' : 'bg-slate-100 text-slate-500'}
          `}>
            <Upload size={32} />
          </div>
          <div>
            <p className="text-lg font-medium text-slate-900">
              Drag & drop files here
            </p>
            <p className="text-sm text-slate-500 mt-1">
              or click to browse
            </p>
          </div>
          <p className="text-xs text-slate-400">
            Supports CSV, JSON, Excel files
          </p>
        </div>
      </div>

      {selectedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          {selectedFiles.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-emerald-100 text-emerald-600 rounded-lg flex items-center justify-center">
                  <File size={20} />
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-slate-900 truncate">
                    {file.name}
                  </p>
                  <p className="text-xs text-slate-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  removeFile(index)
                }}
                className="p-1 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded transition-colors"
              >
                <X size={16} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default FileUpload
