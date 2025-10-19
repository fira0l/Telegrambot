// App.jsx - Updated
import { useEffect, useState, useCallback } from 'react'
import './App.css'
import Gallery from './components/Gallery.jsx'
import OrderForm from './components/OrderForm.jsx'
import CanvasViewer from './components/CanvasViewer.jsx'
import AdminUpload from './components/AdminUpload.jsx'
import Pagination from './components/Pagination.jsx'

function App() {
  const [images, setImages] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [viewerOpen, setViewerOpen] = useState(false)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [showAdmin, setShowAdmin] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [pagination, setPagination] = useState(null)

  const loadImages = useCallback((page = 1) => {
    setIsLoading(true)
    fetch(`https://tgbotbackend.up.railway.app/api/images?page=${page}&per_page=6`)
      .then(async (res) => {
        if (!res.ok) throw new Error('Failed to load images')
        const data = await res.json()
        console.log('API Response:', data)
        
        // Debug the API response
        console.log('Full API Response:', data)
        console.log('data.images:', data.images)
        console.log('data.pagination:', data.pagination)
        
        // Handle both formats for now
        if (Array.isArray(data)) {
          setImages(data)
          setPagination(null)
        } else {
          setImages(data.images || [])
          setPagination(data.pagination || null)
        }
        setError('')
      })
      .catch((e) => {
        console.error('Load images error:', e)
        setError(e.message || 'Error loading images')
      })
      .finally(() => {
        setIsLoading(false)
      })
  }, [])

  useEffect(() => {
    loadImages(currentPage)
  }, [currentPage, loadImages])

  // Keyboard shortcut for admin panel (Ctrl+Shift+A)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'A') {
        e.preventDefault()
        setShowAdmin(prev => !prev)
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const handlePageChange = useCallback((page) => {
    setCurrentPage(page)
    // Scroll to portfolio section instead of top
    const portfolioSection = document.getElementById('portfolio')
    if (portfolioSection) {
      portfolioSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [])

  const openViewer = useCallback((index) => {
    setCurrentIndex(index)
    setViewerOpen(true)
    document.body.style.overflow = 'hidden'
  }, [])

  const closeViewer = useCallback(() => {
    setViewerOpen(false)
    document.body.style.overflow = 'auto'
  }, [])

  const nextImage = useCallback(() => {
    setCurrentIndex((prev) => (images.length ? (prev + 1) % images.length : 0))
  }, [images.length])

  const prevImage = useCallback(() => {
    setCurrentIndex((prev) => (images.length ? (prev - 1 + images.length) % images.length : 0))
  }, [images.length])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
<nav className="sticky top-0 z-50 bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl border-b border-white/20 dark:border-slate-700/50">
  <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
    {/* Logo */}
    <div className="flex items-center space-x-3">
      <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
        <span className="text-white font-semibold text-sm">DS</span>
      </div>
      <span className="text-xl font-light text-slate-800 dark:text-white">DesignStudio</span>
    </div>
    
    {/* Centered Navigation */}
    <div className="flex items-center space-x-1 bg-white/50 dark:bg-slate-800/50 backdrop-blur-lg rounded-2xl px-2 py-2 border border-white/20 dark:border-slate-700/50">
      {[
        { name: 'Portfolio', href: '#portfolio', icon: '🖼️' },
        { name: 'Services', href: '#services', icon: '⚡' },
        { name: 'Projects', href: '#hire', icon: '🚀' },
        { name: 'Contact', href: '#contact', icon: '💬' }
      ].map((item) => (
        <a
          key={item.name}
          href={item.href}
          className="flex items-center space-x-2 px-4 py-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white rounded-xl transition-all duration-300 hover:bg-white/80 dark:hover:bg-slate-700/80 group"
        >
          <span className="text-sm opacity-60 group-hover:opacity-100 transition-opacity">{item.icon}</span>
          <span className="text-sm font-medium">{item.name}</span>
        </a>
      ))}
    </div>

    {/* CTA Button */}
    <div className="flex gap-2">
      <button className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2.5 rounded-xl font-medium hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5 text-sm shadow-md">
        Get Started
      </button>
    </div>
  </div>
</nav>
      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 py-16">
        <header className="text-center mb-16">
          <div className="max-w-3xl mx-auto">
            <h1 className="text-5xl font-light text-slate-800 dark:text-white mb-6 tracking-tight">
              Digital Design &<br />
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Creative Innovation
              </span>
            </h1>
            <p className="text-lg text-slate-600 dark:text-slate-300 mb-8 leading-relaxed">
              Transforming ideas into exceptional digital experiences through
              thoughtful design and cutting-edge technology.
            </p>
            <div className="flex gap-4 justify-center">
              <a href="#portfolio" className="bg-slate-800 dark:bg-white text-white dark:text-slate-900 px-8 py-3 rounded-full font-medium hover:bg-slate-700 dark:hover:bg-slate-100 transition-all duration-300 transform hover:-translate-y-1">
                View Work
              </a>
              <a href="#hire" className="border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 px-8 py-3 rounded-full font-medium hover:border-slate-400 dark:hover:border-slate-500 transition-all duration-300">
                Start Project
              </a>
            </div>
          </div>
        </header>

        {/* Admin Upload Section */}
        {showAdmin && (
          <section className="mb-12">
            <AdminUpload />
          </section>
        )}

        {/* Portfolio Section */}
        <section id="portfolio" className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-light text-slate-800 dark:text-white mb-4">Featured Work</h2>
            <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              A curated selection of projects showcasing our approach to design,
              technology, and user experience.
            </p>
          </div>

          {isLoading && (
            <div className="flex justify-center items-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          )}
          {error && (
            <div className="text-center text-red-600 dark:text-red-400 py-8">
              {error}
            </div>
          )}
          <Gallery images={images} onOpen={openViewer} />
          
          {pagination && (
            <Pagination 
              currentPage={pagination.page}
              totalPages={pagination.pages}
              onPageChange={handlePageChange}
            />
          )}
        </section>

        {/* Services Section */}
        <section id="services" className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-light text-slate-800 dark:text-white mb-4">What We Offer</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: 'UI/UX Design', description: 'User-centered interfaces that combine beauty with functionality and intuitive interactions.' },
              { title: 'Brand Identity', description: 'Comprehensive branding solutions that tell your unique story and connect with your audience.' },
              { title: 'Digital Strategy', description: 'Data-driven approaches to elevate your digital presence and achieve business objectives.' }
            ].map((service, index) => (
              <div key={index} className="bg-white dark:bg-slate-800 rounded-2xl p-8 shadow-sm hover:shadow-md transition-all duration-300 border border-slate-100 dark:border-slate-700">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl mb-6 flex items-center justify-center">
                  <span className="text-white font-bold">{index + 1}</span>
                </div>
                <h3 className="text-xl font-semibold text-slate-800 dark:text-white mb-4">{service.title}</h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">{service.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Project CTA Section */}
        <section id="hire" className="mb-20">
          <div className="bg-gradient-to-r from-blue-600 to-purple-700 rounded-3xl p-12 text-center text-white">
            <h2 className="text-3xl font-light mb-4">Ready to Bring Your Vision to Life?</h2>
            <p className="text-blue-100 mb-8 max-w-2xl mx-auto">
              Let's collaborate to create something extraordinary. Share your project details and we'll get back to you within 24 hours.
            </p>
            <OrderForm />
          </div>
        </section>
      </main>

      {/* Elegant Footer */}
      <footer id="contact" className="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-6 md:mb-0">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-3 h-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"></div>
                <span className="text-lg font-light text-slate-800 dark:text-white">DesignStudio</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 text-sm">
                Crafting digital excellence since 2025
              </p>
            </div>

            <div className="flex flex-col items-center md:items-end">
              <p className="text-slate-600 dark:text-slate-400 mb-4 text-sm">
                Connect with us
              </p>
              <div className="flex gap-6">
                {[
                  { name: 'Instagram', href: 'https://www.instagram.com/firaolanbessaofficial' },
                  { name: 'Behance', href: 'https://www.behance.net/firaoldebesa1' },
                  { name: 'Dribbble', href: 'https://dribbble.com/Firanova' }
                ].map((social, index) => (
                  <a
                    key={index}
                    href={social.href}
                    target="_blank"
                    rel="noreferrer"
                    className="text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300 text-sm"
                  >
                    {social.name}
                  </a>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t border-slate-200 dark:border-slate-800 mt-8 pt-8 text-center">
            <p className="text-slate-500 dark:text-slate-500 text-sm">
              © 2025 DesignStudio. All rights reserved.
            </p>
          </div>
        </div>
      </footer>

      {viewerOpen && (
        <CanvasViewer
          images={images}
          index={currentIndex}
          onClose={closeViewer}
          onPrev={prevImage}
          onNext={nextImage}
        />
      )}
    </div>
  )
}

export default App