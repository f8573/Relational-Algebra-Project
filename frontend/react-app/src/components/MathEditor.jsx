import React, { useState, useRef, useEffect } from 'react'
import SymbolPad from './SymbolPad'
import { admin } from '../lib/api'

// Prefer local vendor copies (see public/vendor/mathquill/)
const MATHQUILL_JS_MIN = '/vendor/mathquill/mathquill.min.js'
const MATHQUILL_JS = '/vendor/mathquill/mathquill.js'
const MATHQUILL_CSS = '/vendor/mathquill/mathquill.css'

function loadScript(src){
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) return resolve()
    const s = document.createElement('script')
    s.src = src
    s.async = true
    s.onload = () => resolve()
    s.onerror = () => reject(new Error('failed to load '+src))
    document.head.appendChild(s)
  })
}

function loadCss(href){
  return new Promise((resolve) => {
    if (document.querySelector(`link[href="${href}"]`)) return resolve()
    const l = document.createElement('link')
    l.rel = 'stylesheet'
    l.href = href
    l.onload = () => resolve()
    document.head.appendChild(l)
  })
}

export default function MathEditor({ onRun, registerInsert, registerSetContent, course, onSubmit }){
  const [mode, setMode] = useState('latex')
  const [mqAvailable, setMqAvailable] = useState(false)
  const mqContainer = useRef(null)
  const textareaRef = useRef(null)
  const mqField = useRef(null)
  const [dbs, setDbs] = useState([])
    const [selectedDb, setSelectedDb] = useState('DEFAULT')

  useEffect(()=>{
    // load available databases for the test interface
    let mounted = true
    ;(async ()=>{
      try{
        const res = await admin.listDatabases()
        if (!mounted) return
        if (res.ok && res.data) setDbs(res.data.databases || [])
      }catch(e){ console.debug('Failed to list DBs', e) }
    })()

    // if the uploaded DB list contains the configured bank DB, auto-select it
    ;(async ()=>{
      try{
        const res = await admin.listDatabases()
        if (!mounted) return
        if (res.ok && res.data){
          const list = res.data.databases || []
          const bank = list.find(x => x.is_bank)
          if (bank) setSelectedDb(String(bank.id))
        }
      }catch(e){ /* ignore */ }
    })()

    async function init(){
      try{
        await loadCss(MATHQUILL_CSS)
        await loadScript(MATHQUILL_JS)
        // diagnostic: if loaded but global missing, try the unminified build first
        if (!window.MathQuill) {
          console.warn('MathQuill script loaded but window.MathQuill is undefined — trying unminified build')
          try{
            await loadScript('/vendor/mathquill/mathquill.js')
          }catch(e){
            console.debug('unminified mathquill.js failed to load from public/vendor', e)
          }
        }
        // if still missing, try fetch+inject of whichever file responded (avoids empty mathquill.min.js cases)
        if (!window.MathQuill) {
          console.warn('MathQuill script loaded but window.MathQuill is undefined — attempting fetch+inject fallback')
          try{
            // prefer fetching the full (non-minified) build if available, otherwise fall back to the minified file
            let txt
            try{
              txt = await fetch(MATHQUILL_JS).then(r=>{ if(!r.ok) throw new Error('fetch failed '+r.status); return r.text() })
            }catch(_){
              txt = await fetch(MATHQUILL_JS_MIN).then(r=>{ if(!r.ok) throw new Error('fetch failed '+r.status); return r.text() })
            }
            const inline = document.createElement('script')
            inline.type = 'text/javascript'
            inline.text = txt
            document.head.appendChild(inline)
            console.debug('MathQuill script injected via fetch; window.MathQuill=', !!window.MathQuill)
            // heuristic: scan globals for an object exposing getInterface()
            if (!window.MathQuill) {
              try{
                for (const k in window) {
                  try{
                    const v = window[k]
                    if (v && typeof v.getInterface === 'function'){
                      window.MathQuill = v
                      console.debug('MathQuill discovered on window as', k)
                      break
                    }
                  }catch(inner){}
                }
              }catch(scanErr){ console.warn('global scan failed', scanErr) }
            }
            // final fallback: do not attempt bundler-resolved import here (Vite will try to resolve 'mathquill')
            if (!window.MathQuill) {
              console.warn('MathQuill not found; ensure MathQuill assets are available under `/public/vendor/mathquill/` (e.g. mathquill.js / mathquill.min.js), or adjust this loader if you prefer an npm-based setup')
            }
          }catch(fErr){
            console.warn('Fetch+inject fallback failed', fErr)
          }
        }
        if (!mounted) return
        if (window.MathQuill && mqContainer.current){
          // prefer interface v3 which doesn't require jQuery
          const MQ = window.MathQuill.getInterface(3)
          mqField.current = MQ.MathField(mqContainer.current, {
            spaceBehavesLikeTab: false,
            supSubsRequireOperand: true,
            autoCommands: 'pi sigma gamma delta rho',
          })
          setMqAvailable(true)
          // expose insertion function
          if (registerInsert) {
            registerInsert(insertLatex)
            console.debug('MathEditor: registerInsert called')
          }
        }
      }catch(e){
        // fail silently; fall back to textarea
        console.warn('MathQuill load failed', e)
        setMqAvailable(false)
      }
    }
    init()
    return ()=>{ mounted = false }
  }, [registerInsert])

  function getContent(){
    // Return content based on the active editor mode so switching between
    // MathPad and Raw LaTeX keeps the expected value for submission.
    if (mode === 'latex') {
      return textareaRef.current ? textareaRef.current.value : (mqField.current ? mqField.current.latex() : '')
    }
    // mode === 'pad'
    if (mqField.current) return mqField.current.latex()
    return textareaRef.current ? textareaRef.current.value : ''
  }

  function insertLatex(latex){
    if (mqField.current){
      mqField.current.write(latex)
      mqField.current.focus()
    } else if (textareaRef.current){
      const ta = textareaRef.current
      const start = ta.selectionStart || ta.value.length
      const v = ta.value
      ta.value = v.slice(0,start) + latex + v.slice(ta.selectionEnd || start)
      ta.selectionStart = ta.selectionEnd = start + latex.length
      ta.focus()
    }
  }

  // Insert a \mathcal{ } macro and place the cursor inside the braces when possible
  function insertMathcal(){
    const snippet = '\\mathcal{}'
    if (mqField.current){
      try{
        mqField.current.write(snippet)
        // attempt to move cursor left into the braces if keystroke API exists
        if (typeof mqField.current.keystroke === 'function'){
          // move left twice to land inside {}
          mqField.current.keystroke('Left')
          mqField.current.keystroke('Left')
        }
        mqField.current.focus()
      }catch(e){
        // fallback
        mqField.current.write(snippet)
        mqField.current.focus()
      }
    } else if (textareaRef.current){
      const ta = textareaRef.current
      const start = ta.selectionStart || ta.value.length
      const v = ta.value
      ta.value = v.slice(0,start) + snippet + v.slice(ta.selectionEnd || start)
      const pos = start + snippet.length - 1
      ta.selectionStart = ta.selectionEnd = pos
      ta.focus()
    }
  }

  function handleRun(){
    const q = getContent().trim()
    if (!q) return
    // Guard running until a course is selected
    if (!course) {
      window.alert('Please select a course before running queries.')
      return
    }
    const dbIdToSend = (selectedDb && selectedDb !== 'DEFAULT') ? parseInt(selectedDb, 10) : undefined
    onRun && onRun(q, dbIdToSend)
  }

  // Sync content when switching modes or when MathQuill becomes available.
  // When switching to 'latex', copy MathQuill's latex into the textarea.
  // When switching to 'pad', populate MathQuill from the textarea.
  React.useEffect(()=>{
    if (mode === 'latex'){
      try{
        const v = mqField.current && typeof mqField.current.latex === 'function' ? mqField.current.latex() : ''
        if (textareaRef.current) textareaRef.current.value = v
      }catch(e){ /* ignore */ }
    } else if (mode === 'pad'){
      try{
        const v = textareaRef.current ? textareaRef.current.value : ''
        if (mqField.current && typeof mqField.current.latex === 'function'){
          try{ mqField.current.latex(v) }catch(e){ mqField.current.write(v) }
        }
      }catch(e){ /* ignore */ }
    }
  }, [mode, mqAvailable])

  // Expose a setter so parent components (e.g. History) can replace the
  // editor contents programmatically.
  React.useEffect(()=>{
    if (registerSetContent){
      const setter = (latex)=>{
        try{
          if (textareaRef.current) textareaRef.current.value = latex || ''
        }catch(e){}
        try{
          if (mqField.current && typeof mqField.current.latex === 'function'){
            try{ mqField.current.latex(latex || '') }catch(e){ mqField.current.write(latex || '') }
          }
        }catch(e){}
      }
      registerSetContent(setter)
    }
  }, [registerSetContent])

  return (
    <div className="editor-container">
      <div className="editor-box">
        <div className="input-row" style={{display:'flex',alignItems:'stretch',gap:8}}>
          <div className="input-field" style={{flex:1}}>
              {/* keep mq container in DOM so MathQuill can initialize; hide visually when not used */}
              <div ref={mqContainer} className="mq-field" style={{display: mode==='pad' ? 'block' : 'none', minHeight:60, background:'#fff'}} />
              <textarea ref={textareaRef} placeholder="Raw LaTeX" style={{display: mode==='latex' ? 'block' : 'none', width:'100%', minHeight:120, padding:12}} />

              <div className="controls-wrapper" style={{marginTop:8}}>
                <div className="controls">
                    <button onClick={()=>setMode('pad')} className={mode==='pad'? 'active' : ''}>Symbol Pad</button>
                    <button onClick={()=>setMode('latex')} className={mode==='latex'? 'active' : ''} style={{marginLeft:8}}>Raw LaTeX</button>
                    <button onClick={insertMathcal} title="Insert \\mathcal{}" style={{marginLeft:12}}>Insert \u2113</button>
                </div>
              </div>
              {mode === 'pad' && (
                <div style={{marginTop:12}}>
                  <SymbolPad onInsert={insertLatex} />
                </div>
              )}
            </div>
          <div style={{display:'flex',alignItems:'center',gap:8}}>
            <div>
              <label style={{display:'block',fontSize:12,marginBottom:4}}>Execute on DB</label>
              <select value={selectedDb} onChange={e=>setSelectedDb(e.target.value)}>
                <option value="DEFAULT">(default bank)</option>
                {dbs.map(d=> (<option key={d.id} value={String(d.id)}>{d.name}</option>))}
              </select>
            </div>
            <div style={{display:'flex',flexDirection:'column',alignItems:'stretch',gap:8}}>
              <button onClick={()=>{ if (onSubmit) onSubmit() }} style={{padding:'6px 10px'}}>Submit Query</button>
              <button onClick={handleRun} className="run-btn">Run Query</button>
            </div>
          </div>
        </div>

        
      </div>
    </div>
  )
}
