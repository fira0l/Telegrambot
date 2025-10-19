// OrderForm.jsx - Updated
import { useRef, useState } from 'react'

export default function OrderForm() {
  const formRef = useRef(null)
  const [submitting, setSubmitting] = useState(false)
  const [ok, setOk] = useState(false)
  const [error, setError] = useState('')

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!formRef.current) return
    setSubmitting(true)
    setError('')
    setOk(false)

    try {
      const form = new FormData(formRef.current)
      const res = await fetch('https://tgbotbackend.up.railway.app/submit-order', { method: 'POST', body: form })
      if (!res.ok) throw new Error('Failed to submit. Please try again.')
      setOk(true)
      formRef.current.reset()
    } catch (err) {
      setError(err.message || 'An error occurred')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <form 
        ref={formRef} 
        method="POST" 
        action="/submit-order" 
        onSubmit={onSubmit}
        className="space-y-6"
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
          <div>
            <input 
              type="text" 
              name="name" 
              placeholder="Your Name" 
              required 
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-white/30 transition-all duration-300"
            />
          </div>
          <div>
            <input 
              type="email" 
              name="email" 
              placeholder="Email Address" 
              required 
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-white/30 transition-all duration-300"
            />
          </div>
        </div>
        
        <div>
          <input 
            type="text" 
            name="project_type" 
            placeholder="Project Type (e.g., Website, Branding, App)" 
            required 
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-white/30 transition-all duration-300"
          />
        </div>
        
        <div>
          <textarea 
            name="description" 
            placeholder="Tell us about your project..." 
            rows={5} 
            required 
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-white/30 transition-all duration-300 resize-none"
          />
        </div>
        
        <button 
          type="submit" 
          disabled={submitting}
          className="w-full bg-white text-slate-900 py-4 px-8 rounded-xl font-semibold hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg"
        >
          {submitting ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-slate-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Sending...
            </span>
          ) : (
            'Start Your Project'
          )}
        </button>
        
        {ok && (
          <div className="bg-green-500/20 border border-green-500/30 rounded-xl p-4 text-green-100 text-center">
            ✅ Thank you! Your project request has been sent. We'll get back to you within 24 hours.
          </div>
        )}
        
        {error && (
          <div className="bg-red-500/20 border border-red-500/30 rounded-xl p-4 text-red-100 text-center">
            ❌ {error}
          </div>
        )}
      </form>
    </div>
  )
}