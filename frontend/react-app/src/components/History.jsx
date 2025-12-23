import React, { useEffect, useRef } from 'react'

const KATEX_JS = 'https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'
const KATEX_CSS = 'https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'

function loadScript(src){
  return new Promise((resolve, reject)=>{
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
  return new Promise((resolve)=>{
    if (document.querySelector(`link[href="${href}"]`)) return resolve()
    const l = document.createElement('link')
    l.rel = 'stylesheet'
    l.href = href
    l.onload = () => resolve()
    document.head.appendChild(l)
  })
}

export default function History({ items, onLoad }){
  const refs = useRef([])

  useEffect(()=>{
    let mounted = true
    ;(async ()=>{
      try{
        await loadCss(KATEX_CSS)
        await loadScript(KATEX_JS)
        if (!mounted) return
        const katex = window.katex
        if (!katex) return
        // render each item into its container
        items.forEach((it, i)=>{
          const el = refs.current[i]
          if (!el) return
          try{
            katex.render(String(it), el, { throwOnError: false })
          }catch(e){
            // fallback to text
            el.textContent = String(it)
          }
        })
      }catch(e){
        // ignore; leave plaintext
      }
    })()
    return ()=>{ mounted = false }
  }, [items])

  return (
    <div>
      <h3>History</h3>
      <ul style={{listStyle:'none', padding:0}}>
        {items.map((it, i)=> (
          <li key={i} style={{marginBottom:6}}>
            <button onClick={()=>onLoad && onLoad(it)} style={{width:'100%', textAlign:'left', padding:6}}>
              <span ref={el=> refs.current[i] = el} style={{display:'inline-block',width:'100%',textAlign:'left'}}>{typeof it === 'string' ? it.slice(0,120) : String(it)}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
