import { useEffect, useMemo } from 'react'

export default function Lightbox({ images, index, onClose, onPrev, onNext }) {
  const item = images[index]
  const next = images.length ? images[(index + 1) % images.length] : null
  const prev = images.length ? images[(index - 1 + images.length) % images.length] : null

  // Prefetch adjacent images
  useEffect(() => {
    if (next) {
      const img = new Image()
      img.src = next.src
    }
    if (prev) {
      const img = new Image()
      img.src = prev.src
    }
  }, [next, prev])

  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'ArrowLeft') onPrev()
      if (e.key === 'ArrowRight') onNext()
    }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [onClose, onPrev, onNext])

  if (!item) return null

  return (
    <div className="lightbox active" onClick={(e) => { if (e.target.classList.contains('lightbox')) onClose() }}>
      <div className="lightbox-content">
        <button className="lightbox-close" onClick={onClose}>✕</button>
        <div className="lightbox-loading" />
        <img className="lightbox-image" src={item.src} alt={item.title} />
        <div className="lightbox-caption">{item.title}</div>
        <div className="lightbox-nav">
          <button className="lightbox-prev" onClick={(e) => { e.stopPropagation(); onPrev() }}>‹</button>
          <button className="lightbox-next" onClick={(e) => { e.stopPropagation(); onNext() }}>›</button>
        </div>
      </div>
    </div>
  )
}
