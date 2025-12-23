import React from 'react'

const SYMBOLS = [
  { latex: '\\pi_{}()', display: ['π','☐'], title: 'project' },
  { latex: '\\sigma_{}()', display: ['σ','☐'], title: 'select' },
  { latex: '\\rho_{}()', display: ['ρ','☐'], title: 'rename' },
  { latex: '\\text{}', display: ['Text'], title: 'text' },
  { latex: '\\gamma_{}()', display: ['γ','☐'], title: 'aggregate' },
  { latex: '{}_{} \\gamma_{}()', display: ['☐','γ','☐'], title: 'group' },
  { latex: '\\leftarrow', display: ['←'], title: 'assign' },
  { latex: '-', display: ['−'], title: 'minus' },
  { latex: '\\cup', display: ['∪'], title: 'union' },
  { latex: '\\cap', display: ['∩'], title: 'intersection' },
  { latex: '\\times', display: ['×'], title: 'product' },
  { latex: '⋈', display: ['⋈'], title: 'join' },
  { latex: '⋈_{}', display: ['⋈','☐'], title: 'theta-join' },
  { latex: '⟕', display: ['⟕'], title: 'left-join' }
]

export default function SymbolPad({ onInsert }){
  return (
    <div className="symbol-pad">
      <div style={{display:'flex',gap:8,alignItems:'center',flexWrap:'wrap',justifyContent:'flex-start',padding:'6px 0'}}>
        {SYMBOLS.map((s, i) => (
          <button
            key={i}
            className="symbol-btn"
            title={s.title || ''}
            aria-label={s.title || (s.display ? s.display.join('') : s.label)}
            onClick={()=> onInsert && onInsert(s.latex)}
            style={{padding:6, minWidth:40, minHeight:34, textAlign:'center'}}
          >
            {/* Render display parts; render '☐' as a subscript-like element */}
            { (s.display || []).map((part, idx) => (
              part === '☐' ? (
                <span key={idx} style={{fontSize:'0.8em', verticalAlign:'sub', marginLeft:0}}>{part}</span>
              ) : (
                <span key={idx} style={{fontSize:'1.05em'}}>{part}</span>
              )
            )) }
          </button>
        ))}
      </div>
    </div>
  )
}
