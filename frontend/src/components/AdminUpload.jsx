import { useState, useEffect } from 'react'

export default function AdminUpload() {
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('')
  const [preview, setPreview] = useState('')
  const [uploading, setUploading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  // File preview cleanup
  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview)
      }
    }
  }, [preview])

  // Auto-hide success message
  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => {
        setSuccess(false)
      }, 5000)
      return () => clearTimeout(timer)
    }
  }, [success])

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    
    if (!selectedFile) {
      setFile(null)
      setPreview('')
      return
    }

    // File type validation
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please select an image file (JPEG, PNG, GIF, etc.)')
      setFile(null)
      setPreview('')
      e.target.value = ''
      return
    }

    // File size validation (5MB limit)
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB')
      setFile(null)
      setPreview('')
      e.target.value = ''
      return
    }

    setFile(selectedFile)
    setError('')
    
    // Create preview
    const objectUrl = URL.createObjectURL(selectedFile)
    setPreview(objectUrl)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file || !title) return

    setUploading(true)
    setError('')
    setSuccess(false)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', title)

    try {
      const res = await fetch('https://graphicdesign.onrender.com/api/upload', {
        method: 'POST',
        body: formData
      })
      
      const data = await res.json()
      
      if (!res.ok) {
        throw new Error(data.message || `Upload failed with status: ${res.status}`)
      }
      
      setSuccess(true)
      setFile(null)
      setTitle('')
      setDescription('')
      setCategory('')
      setPreview('')
      e.target.reset()
      
      // Refresh gallery to show new image
      setTimeout(() => window.location.reload(), 1000)
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during upload')
    } finally {
      setUploading(false)
    }
  }

  const resetForm = () => {
    setFile(null)
    setTitle('')
    setDescription('')
    setCategory('')
    setPreview('')
    setError('')
    setSuccess(false)
  }

  return (
    <div className="w-full max-w-lg mx-auto bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-6 shadow-lg overflow-hidden">
      <h3 className="text-xl font-bold mb-6 text-slate-800 dark:text-white">Upload New Project</h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Title */}
        <div>
          <label htmlFor="title" className="block text-sm font-medium mb-1 text-slate-700 dark:text-slate-300">
            Project Title *
          </label>
          <input
            id="title"
            type="text"
            placeholder="Enter project title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors box-border min-w-0"
            required
          />
        </div>

        {/* Description */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium mb-1 text-slate-700 dark:text-slate-300">
            Project Description
          </label>
          <textarea
            id="description"
            placeholder="Describe your project..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
            className="w-full px-3 py-2 text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors resize-none box-border min-w-0"
          />
        </div>

        {/* Category */}
        <div>
          <label htmlFor="category" className="block text-sm font-medium mb-1 text-slate-700 dark:text-slate-300">
            Category
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-3 py-2 text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors box-border min-w-0"
          >
            <option value="">Select a category</option>
            <option value="web-design">Web Design</option>
            <option value="development">Development</option>
            <option value="branding">Branding</option>
            <option value="marketing">Marketing</option>
            <option value="other">Other</option>
          </select>
        </div>

        {/* File Upload */}
        <div>
          <label htmlFor="file-upload" className="block text-sm font-medium mb-1 text-slate-700 dark:text-slate-300">
            Project Image *
          </label>
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="w-full text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white file:mr-3 file:py-1.5 file:px-3 file:rounded file:border-0 file:text-xs file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-blue-900 dark:file:text-blue-300 transition-colors box-border min-w-0"
            required
          />
          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
            JPEG, PNG, GIF, WEBP. Max 5MB
          </p>
        </div>

        {/* File Preview */}
        {preview && (
          <div className="border border-dashed border-slate-300 dark:border-slate-600 rounded-lg p-3 text-center">
            <p className="text-xs font-medium mb-2 text-slate-700 dark:text-slate-300">Image Preview</p>
            <img 
              src={preview} 
              alt="Preview" 
              className="max-w-full max-h-48 mx-auto rounded shadow-sm"
            />
          </div>
        )}

        {/* Buttons */}
        <div className="flex gap-3 pt-2">
          <button
            type="button"
            onClick={resetForm}
            disabled={uploading}
            className="flex-1 px-4 py-2 text-sm border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Reset
          </button>
          <button
            type="submit"
            disabled={uploading || !file || !title}
            className="flex-1 bg-blue-600 text-white py-2 px-4 text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {uploading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Uploading...
              </span>
            ) : (
              'Upload Project'
            )}
          </button>
        </div>

        {/* Success Message */}
        {success && (
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-800 dark:text-green-300 px-3 py-2 rounded-lg flex items-center text-sm">
            <svg className="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            Project uploaded successfully!
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-300 px-3 py-2 rounded-lg flex items-center text-sm">
            <svg className="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}
      </form>
    </div>
  )
}