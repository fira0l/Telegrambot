// CanvasViewer.jsx - Updated
import { useEffect, useRef, useState } from 'react'

export default function CanvasViewer({ images, index, onClose, onPrev, onNext }) {
  const canvasRef = useRef(null)
  const [img, setImg] = useState(null)
  const [view, setView] = useState({ scale: 1, offsetX: 0, offsetY: 0 })
  const [fitScale, setFitScale] = useState(1)
  const [drag, setDrag] = useState({ active: false, startX: 0, startY: 0, baseX: 0, baseY: 0 })

  const current = images[index]

  // Load image
  useEffect(() => {
    if (!current) return
    const image = new Image()
    image.src = current.src
    image.onload = () => setImg(image)
    return () => setImg(null)
  }, [current])

  // Fit to screen on load or resize
  useEffect(() => {
    const fit = () => {
      const canvas = canvasRef.current
      if (!canvas || !img) return
      const dpr = Math.max(1, window.devicePixelRatio || 1)
      const cssW = window.innerWidth
      const cssH = window.innerHeight
      
      canvas.width = Math.floor(cssW * dpr)
      canvas.height = Math.floor(cssH * dpr)
      canvas.style.width = cssW + 'px'
      canvas.style.height = cssH + 'px'

      const fittedScale = Math.min(cssW / img.width, cssH / img.height)
      setFitScale(fittedScale)
      setView({
        scale: fittedScale,
        offsetX: (cssW - img.width * fittedScale) / 2,
        offsetY: (cssH - img.height * fittedScale) / 2,
      })
      draw()
    }
    
    const onResize = () => fit()
    fit()
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [img])

  const draw = () => {
    const canvas = canvasRef.current
    if (!canvas || !img) return
    const ctx = canvas.getContext('2d')
    const dpr = Math.max(1, window.devicePixelRatio || 1)
    const cssW = canvas.clientWidth || window.innerWidth
    const cssH = canvas.clientHeight || window.innerHeight

    ctx.setTransform(1, 0, 0, 1, 0, 0)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.scale(dpr, dpr)

    ctx.save()
    ctx.translate(view.offsetX, view.offsetY)
    ctx.scale(view.scale, view.scale)
    ctx.drawImage(img, 0, 0)
    ctx.restore()
  }

  useEffect(() => { draw() })
  useEffect(() => { draw() }, [view])

  // Event handlers remain the same...
  const onMouseDown = (e) => {
    setDrag({ active: true, startX: e.clientX, startY: e.clientY, baseX: view.offsetX, baseY: view.offsetY })
  }
  
  const onMouseMove = (e) => {
    if (!drag.active) return
    const dx = e.clientX - drag.startX
    const dy = e.clientY - drag.startY
    setView((v) => ({ ...v, offsetX: drag.baseX + dx, offsetY: drag.baseY + dy }))
  }
  
  const onMouseUp = () => setDrag((d) => ({ ...d, active: false }))

  const onWheel = (e) => {
    if (!img) return
    e.preventDefault()
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const mouseX = e.clientX - rect.left
    const mouseY = e.clientY - rect.top

    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9
    const desiredScale = view.scale * zoomFactor
    const minScale = fitScale
    const maxScale = 5
    const newScale = Math.max(minScale, Math.min(maxScale, desiredScale))

    const worldX = (mouseX - view.offsetX) / view.scale
    const worldY = (mouseY - view.offsetY) / view.scale
    const newOffsetX = mouseX - worldX * newScale
    const newOffsetY = mouseY - worldY * newScale

    setView({ scale: newScale, offsetX: newOffsetX, offsetY: newOffsetY })
  }

  const onDoubleClick = () => {
    if (!img) return
    const cssW = window.innerWidth
    const cssH = window.innerHeight
    if (Math.abs(view.scale - fitScale) < 0.01) {
      const offsetX = (cssW - img.width) / 2
      const offsetY = (cssH - img.height) / 2
      setView({ scale: 1, offsetX, offsetY })
    } else {
      setView({ scale: fitScale, offsetX: (cssW - img.width * fitScale) / 2, offsetY: (cssH - img.height * fitScale) / 2 })
    }
  }

  const onBackdrop = (e) => {
    if (e.target.classList.contains('canvas-viewer')) onClose()
  }

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'ArrowLeft') onPrev()
      if (e.key === 'ArrowRight') onNext()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose, onPrev, onNext])

  if (!current) return null

  return (
    <div className="fixed inset-0 bg-black/95 backdrop-blur-xl z-50 flex items-center justify-center" onClick={onBackdrop}>
      <canvas
        ref={canvasRef}
        className="cursor-grab active:cursor-grabbing"
        onMouseDown={onMouseDown}
        onMouseMove={onMouseMove}
        onMouseUp={onMouseUp}
        onMouseLeave={onMouseUp}
        onWheel={onWheel}
        onDoubleClick={onDoubleClick}
      />
      
      {/* Elegant controls */}
      <button 
        className="absolute top-6 right-6 w-10 h-10 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full flex items-center justify-center text-white backdrop-blur-sm transition-all duration-300 hover:scale-110"
        onClick={onClose}
      >
        ✕
      </button>
      
      <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 bg-black/40 backdrop-blur-sm rounded-full px-6 py-3 border border-white/10">
        <span className="text-white text-sm font-medium">{current.title}</span>
      </div>
      
      <div className="absolute left-6 right-6 top-1/2 transform -translate-y-1/2 flex justify-between">
        <button 
          className="w-12 h-12 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full flex items-center justify-center text-white backdrop-blur-sm transition-all duration-300 hover:scale-110"
          onClick={(e) => { e.stopPropagation(); onPrev() }}
        >
          ‹
        </button>
        <button 
          className="w-12 h-12 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full flex items-center justify-center text-white backdrop-blur-sm transition-all duration-300 hover:scale-110"
          onClick={(e) => { e.stopPropagation(); onNext() }}
        >
          ›
        </button>
      </div>
      
      <div className="absolute bottom-6 right-6 text-white/60 text-sm">
        {index + 1} / {images.length}
      </div>
    </div>
  )
}