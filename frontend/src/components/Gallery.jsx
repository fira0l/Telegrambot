// Gallery.jsx - Updated
import { useEffect, useRef, useState } from 'react'

export default function Gallery({ images, onOpen }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {images.map((item, index) => (
        <LazyImageCard key={item.src} item={item} onClick={() => onOpen(index)} />
      ))}
    </div>
  )
}

function LazyImageCard({ item, onClick }) {
  const [isVisible, setIsVisible] = useState(false)
  const [loaded, setLoaded] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    const node = ref.current
    if (!node) return
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true)
            observer.disconnect()
          }
        })
      },
      { rootMargin: '100px' }
    )
    observer.observe(node)
    return () => observer.disconnect()
  }, [])

  return (
    <div
      className="group relative bg-white dark:bg-slate-800 rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-500 cursor-pointer border border-slate-100 dark:border-slate-700"
      ref={ref}
      onClick={onClick}
    >
      <div className="aspect-[4/3] overflow-hidden">
        {!loaded && (
          <div className="skeleton-thumb w-full h-full" aria-hidden="true" />
        )}
        {isVisible && (
          <img
            src={item.src}
            alt={item.title}
            loading="lazy"
            className={`w-full h-full object-cover transition-all duration-700 group-hover:scale-105 ${
              loaded ? 'opacity-100' : 'opacity-0'
            }`}
            onLoad={() => setLoaded(true)}
          />
        )}
      </div>
      
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all duration-500 flex items-end justify-start p-6">
        <div className="transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
          <h3 className="text-white font-medium text-lg mb-2">{item.title}</h3>
          <div className="w-8 h-0.5 bg-white/60 rounded-full"></div>
        </div>
      </div>
      
      {/* Hover overlay effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    </div>
  )
}