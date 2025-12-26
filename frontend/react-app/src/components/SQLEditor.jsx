import React, { useEffect, useRef } from 'react'

export default function SQLEditor({ value, onChange }) {
  const textareaRef = useRef(null)
  const highlightRef = useRef(null)

  useEffect(() => {
    if (highlightRef.current && typeof window !== 'undefined' && window.hljs) {
      const highlighted = window.hljs.highlight(value || '', { language: 'sql', ignoreIllegals: true }).value
      highlightRef.current.innerHTML = highlighted
    }
  }, [value])

  const handleScroll = (e) => {
    if (highlightRef.current) {
      highlightRef.current.scrollTop = e.target.scrollTop
      highlightRef.current.scrollLeft = e.target.scrollLeft
    }
  }

  return (
    <div style={{ position: 'relative', width: '100%', fontFamily: 'monospace', fontSize: '14px' }}>
      <div
        ref={highlightRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          padding: '8px',
          margin: 0,
          border: '1px solid #22262b',
          borderRadius: '4px',
          background: '#011627',
          overflow: 'hidden',
          pointerEvents: 'none',
          whiteSpace: 'pre',
          wordWrap: 'normal',
          boxSizing: 'border-box',
          lineHeight: '1.5'
        }}
        className="hljs"
      />
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onScroll={handleScroll}
        style={{
          position: 'relative',
          width: '100%',
          padding: '8px',
          margin: 0,
          border: '1px solid transparent',
          borderRadius: '4px',
          background: 'transparent',
          color: 'transparent',
          caretColor: '#e6edf3',
          overflow: 'auto',
          whiteSpace: 'pre',
          wordWrap: 'normal',
          boxSizing: 'border-box',
          fontFamily: 'monospace',
          fontSize: '14px',
          lineHeight: '1.5',
          resize: 'vertical',
          minHeight: '200px'
        }}
      />
    </div>
  )
}
