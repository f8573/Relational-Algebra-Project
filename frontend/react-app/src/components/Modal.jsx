import React from 'react'

export default function Modal({ title, children, onClose, onSubmit, submitLabel = 'Save', submitting = false, submitDisabled = false, submitDisabledReason = '' }){
  const disable = submitting || submitDisabled
  return (
    <div className="modal-overlay">
      <div className="modal">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:8}}>
          <h3 style={{margin:0}}>{title}</h3>
          <button onClick={onClose} style={{background:'transparent',border:'none',fontSize:18}}>✕</button>
        </div>
        <div className="modal-body">{children}</div>
        {submitDisabledReason && <div style={{color:'red',marginTop:8}}>{submitDisabledReason}</div>}
        <div style={{display:'flex',justifyContent:'flex-end',gap:8,marginTop:12}}>
          <button onClick={onClose} disabled={submitting} style={{background:'#ddd',color:'#111',padding:'8px 10px',borderRadius:6}}>Cancel</button>
          {onSubmit && <button onClick={onSubmit} disabled={disable} style={{background: disable ? '#999' : (submitting ? '#9ad69a' : '#4CAF50'),color:'#fff',padding:'8px 10px',borderRadius:6}}>{submitting ? 'Saving...' : submitLabel}</button>}
        </div>
      </div>
    </div>
  )
}
