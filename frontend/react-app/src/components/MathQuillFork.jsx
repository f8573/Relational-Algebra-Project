import React, { useEffect, useState } from 'react'

const KATEX_JS = 'https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'
const KATEX_CSS = 'https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'

function loadScript(src){
  return new Promise((resolve, reject)=>{
    if (typeof window !== 'undefined' && document.querySelector(`script[src="${src}"]`)) return resolve()
    const s = document.createElement('script')
    s.src = src
    s.async = true
    s.onload = () => resolve()
    s.onerror = () => reject(new Error('failed to load '+src))
    document.head.appendChild(s)
  })
}
function loadCss(href){
  return new Promise((resolve, reject)=>{
    if (typeof window !== 'undefined' && document.querySelector(`link[href="${href}"]`)) return resolve()
    const l = document.createElement('link')
    l.rel = 'stylesheet'
    l.href = href
    l.onload = () => resolve()
    l.onerror = () => reject(new Error('failed to load '+href))
    document.head.appendChild(l)
  })
}

// A lightweight wrapper to provide LaTeX input + KaTeX preview that supports \mathcal.
// This is not a full MathQuill fork; it provides immediate UX while preparing the upstream fork.
export default function MathQuillFork({ value = '', onChange }){
  const [latex, setLatex] = useState(value)
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState(null)

  useEffect(()=>{
    let mounted = true
    ;(async ()=>{
      try{
        await loadCss(KATEX_CSS)
        await loadScript(KATEX_JS)
        if (mounted) setLoaded(true)
      }catch(e){
        if (mounted) setError(e.message)
      }
    })()
    return ()=>{ mounted = false }
  }, [])

  useEffect(()=>{ if (onChange) onChange(latex) }, [latex])

  // Helper: when users press a toolbar button, insert \mathcal{<cursor>} into textarea
  function insertMathcal(){
    const ta = document.getElementById('mqf-input')
    if (!ta) return
    const start = ta.selectionStart || 0
    const end = ta.selectionEnd || 0
    const before = ta.value.slice(0, start)
    const after = ta.value.slice(end)
    const insert = '\\mathcal{}'
    const newVal = before + insert + after
    setLatex(newVal)
    // set cursor inside braces after render
    requestAnimationFrame(()=>{ ta.selectionStart = ta.selectionEnd = start + insert.length - 1; ta.focus() })
  }

  function renderPreview(){
    if (!loaded || !window.katex) return (<pre style={{whiteSpace:'pre-wrap'}}>{latex}</pre>)
    try{
      // KaTeX supports \mathcal; provide throwOnError:false for robustness
      const html = window.katex.renderToString(String(latex), { throwOnError:false })
      return (<div dangerouslySetInnerHTML={{ __html: html }} />)
    }catch(e){
      return (<pre style={{whiteSpace:'pre-wrap', color:'red'}}>{String(e.message)}</pre>)
    }
  }

  return (
    <div style={{border:'1px solid #ddd', padding:12, borderRadius:6}}>
      <div style={{marginBottom:8, display:'flex', gap:8}}>
        <button type="button" onClick={insertMathcal}>Insert \u201c\\mathcal{ }\\u201d</button>
        <div style={{flex:1}} />
        {error ? (<div style={{color:'red'}}>KaTeX load error: {error}</div>) : null}
      </div>
      <textarea id="mqf-input" value={latex} onChange={e=> setLatex(e.target.value)} rows={6} style={{width:'100%', fontFamily:'monospace'}} />
      <div style={{marginTop:8, padding:8, borderTop:'1px solid #f0f0f0'}}>
        <strong>Preview</strong>
        <div style={{minHeight:40, marginTop:6}}>
          {renderPreview()}
        </div>
      </div>
    </div>
  )
}
