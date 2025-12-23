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
  return new Promise((resolve, reject)=>{
    if (document.querySelector(`link[href="${href}"]`)) return resolve()
    const l = document.createElement('link')
    l.rel = 'stylesheet'
    l.href = href
    l.onload = () => resolve()
    l.onerror = () => reject(new Error('failed to load '+href))
    document.head.appendChild(l)
  })
}

function toCSV(cols, rows){
  const esc = v => String(v ?? '').replace(/"/g,'""')
  const head = (cols && cols.length) ? cols.map(c=> `"${esc(c)}"`).join(',') : '"value"'
  const body = (rows||[]).map(r => r.map(c=> `"${esc(c)}"`).join(',')).join('\n')
  return head + '\n' + body
}

function detectAndBuildTable(obj){
  function mergeContinuations(rows){
    const toks = rows.map(r => Array.isArray(r) ? String(r[0] ?? '') : String(r ?? ''))
    const out = []
    for (const t of toks){
      if (!t) continue
      const firstChar = t[0]
      if (out.length > 0 && firstChar && firstChar === firstChar.toLowerCase() && /[a-z]/.test(firstChar)){
        out[out.length-1] = out[out.length-1] + t
      } else {
        out.push(t)
      }
    }
    return out.map(s=> [s])
  }

  function mergeRowFragments(rows){
    // rows: array of arrays -> [[str], [str], ...]
    const toks = rows.map(r => Array.isArray(r) ? String(r[0] ?? '') : String(r ?? ''))
    const out = []
    for (let i = 0; i < toks.length; i++){
      let cur = toks[i]
      if (!cur) continue
      // merge subsequent fragments that look like continuations: start with lowercase or are single-letter
      while (i+1 < toks.length){
        const nxt = toks[i+1]
        if (!nxt) { i++; continue }
        const nc = nxt[0]
        if ((nc && nc === nc.toLowerCase() && /[a-z]/.test(nc)) || nxt.length === 1){
          cur = cur + nxt
          i++
        } else break
      }
      out.push([cur])
    }
    return out
  }

  function finalize(obj){
    if (!obj) return obj
    if (obj.cols && obj.cols.length === 1 && obj.rows){
      try{ obj.rows = mergeRowFragments(obj.rows) }catch(e){}
    }
    // split any concatenated field:type headers into separate columns
    try{
      const headerFieldRegex = /[A-Za-z_][A-Za-z0-9_]*\s*:\s*(?:number|string|int|float|text|bool)/gi
      let expanded = false
      const newCols = []
      for (const c of obj.cols || []){
        const m = Array.from(String(c).matchAll(headerFieldRegex)).map(x=> x[0])
        if (m.length > 1){
          expanded = true
          for (const mm of m) newCols.push(mm.replace(/\s*/g,'').replace(/:/,' : '))
        } else {
          newCols.push(c)
        }
      }
      if (expanded){
        const oldColsLen = (obj.cols || []).length
        const targetLen = newCols.length
        const newRows = (obj.rows || []).map(r => {
          const row = Array.isArray(r) ? r.slice() : [String(r||'')]
          // common case: single cell contains comma-separated values
          if (row.length === 1 && typeof row[0] === 'string' && row[0].includes(',')){
            const parts = row[0].split(',').map(p=> p.trim())
            if (parts.length === targetLen) return parts
          }
          // try to expand cells that contain commas
          const flat = row.flatMap(cell => (typeof cell === 'string' && cell.includes(',')) ? cell.split(',').map(p=>p.trim()) : [cell])
          if (flat.length === targetLen) return flat
          // if already matches target length, return as-is
          if (row.length === targetLen) return row
          // otherwise pad/truncate
          const out = row.slice(0, targetLen)
          while (out.length < targetLen) out.push('')
          return out
        })
        obj.cols = newCols
        obj.rows = newRows
      }
    }catch(e){ /* ignore */ }

    return obj
  }

  if (Array.isArray(obj)){
    if (obj.length === 0) return null
    const first = obj[0]
    if (typeof first === 'object' && !Array.isArray(first)){
      const cols = Array.from(new Set(obj.flatMap(o=> Object.keys(o))))
      const rows = obj.map(o=> cols.map(c=> o[c] == null ? '' : o[c]))
      return finalize({ cols, rows })
    }
    if (Array.isArray(first)){
      const maybeHeader = first.every(v => typeof v === 'string')
      if (maybeHeader) return finalize({ cols: first.slice(), rows: obj.slice(1) })
      const maxLen = Math.max(...obj.map(r=> Array.isArray(r)? r.length : 1))
      const cols = Array.from({length: maxLen}, (_,i)=>`col${i+1}`)
      const rows = obj.map(r=> Array.isArray(r)? r.concat(Array(maxLen - r.length).fill('')) : [r])
      return finalize({ cols, rows })
    }
    return finalize({ cols: ['value'], rows: obj.map(v=> [v]) })
  }

  if (typeof obj !== 'string') return null
  const rawLines = obj.split(/\r?\n/)
  if (rawLines.length === 0) return null

  const delimiters = ['\t','\\|',',']
  // Detect contiguous header patterns like "acctid : numbername:stringbalance:number"
  const isSep = l => /-{3,}/.test(String(l).replace(/\s/g,'')) || (/^[\-\s|]{5,}$/.test(l))

  // Detect contiguous header patterns like "acctid : numbername:stringbalance:number"
  // prefer matching common types to avoid merging type+nextField when no delimiter present
  const fieldTypeRegex = /[A-Za-z_][A-Za-z0-9_]*\s*:\s*(?:number|string|int|float|text|bool)/gi
  for (let i = 0; i < rawLines.length; i++){
    const line = String(rawLines[i] || '')
    const matches = Array.from(line.matchAll(fieldTypeRegex)).map(m => m[0])
    if (matches.length >= 2){
      const dataStart = i + 1
      let dataEnd = dataStart
      while (dataEnd < rawLines.length && String(rawLines[dataEnd] || '').trim() !== '' && !isSep(rawLines[dataEnd])) dataEnd++
      const dataLines = rawLines.slice(dataStart, dataEnd).map(l=> l.trim()).filter(l=> l.length > 0)
      if (dataLines.length === 0) continue
      const headerCols = matches.map(m => m.replace(/\s*/g,'').replace(/:/,' : '))
      const rows = dataLines.map(l => l.split(',').map(p => p.trim()))
      const pre = rawLines.slice(0, i).map(l=> l.trim()).filter(l=> l.length>0)
      const post = rawLines.slice(dataEnd).map(l=> l.trim()).filter(l=> l.length>0)
      return finalize({ pre, cols: headerCols, rows, post })
    }
  }

  const sepIdx = rawLines.map((l,i)=> isSep(l) ? i : -1).filter(i=> i >= 0)

  const schemaIdxs = rawLines.map((l,i)=> /\(.*:\s*\w+\)/i.test(l.replace(/\s/g,'')) ? i : -1).filter(i=> i >= 0)
  if (schemaIdxs.length && sepIdx.length >= 2){
    for (const sIdx of schemaIdxs){
      const firstSep = sepIdx.find(x => x > sIdx)
      if (firstSep == null) continue
      const secondSep = sepIdx.find(x => x > firstSep)
      if (secondSep == null) continue
      const schemaLine = rawLines[sIdx]
      const header = String(schemaLine).replace(/\s/g,'').replace(/[^A-Za-z:]/g,'').replace(/:/,' : ')
      const dataLines = rawLines.slice(firstSep+1, secondSep).map(l=> l.trim()).filter(l=> l.length > 0)
      if (dataLines.length === 0) continue
      const rows = dataLines.map(l=>{
        const partsTab = l.split('\t').map(p=> p.trim()).filter(Boolean)
        const parts = partsTab.length > 1 ? partsTab : l.split(/\s+/).map(p=> p.trim()).filter(Boolean)
        if (parts.length > 1 && parts.every(p=> p.length === 1)) return [ parts.join('') ]
        return [ parts.join(' ') ]
      })
      const rowsMerged = mergeContinuations(rows)
      const pre = rawLines.slice(0, sIdx).map(l=> l.trim()).filter(l=> l.length>0)
      const post = rawLines.slice(secondSep+1).map(l=> l.trim()).filter(l=> l.length>0)
      return finalize({ pre, cols: [header], rows: rowsMerged, post })
    }
  }

  if (rawLines.some(l=> /\(.*:\s*\w+\)/i.test(l)) && sepIdx.length >= 2){
    for (let a=0; a<sepIdx.length-1; a++){
      for (let b=a+1; b<sepIdx.length; b++){
        const start = sepIdx[a]
        const end = sepIdx[b]
        if (end - start < 2) continue
        const inner = rawLines.slice(start+1, end)
        const schemaRel = inner.findIndex(l=> /\(.*:\s*\w+\)/i.test(l))
        if (schemaRel >= 0){
          const schemaLine = inner[schemaRel]
          const header = String(schemaLine).replace(/[^A-Za-z:]/g,'').replace(/:/,' : ')
          const dataLines = inner.slice(schemaRel+1).map(l=> l.trim()).filter(l=> l.length > 0)
          const rows = dataLines.map(l=> {
            const parts = l.split(/\s+/).map(p=> p.trim()).filter(Boolean)
            const toks = []
            let buf = ''
            for (const p of parts){ if (p.length === 1) buf += p; else { if (buf) { toks.push(buf); buf = '' }; toks.push(p) } }
            if (buf) toks.push(buf)
            return [ toks.join(' ') ]
          })
          const pre = rawLines.slice(0, start).map(l=> l.trim()).filter(l=> l.length>0)
          const post = rawLines.slice(end+1).map(l=> l.trim()).filter(l=> l.length>0)
          return finalize({ pre, cols: [header], rows, post })
        }
      }
    }
  }

  const nonEmpty = rawLines.map(l=> l.trim()).filter(l=> l.length > 0)
  if (nonEmpty.length > 0){
    const charLineFlags = rawLines.map(l => {
      const parts = String(l).split('\t').map(p=> p.trim()).filter(Boolean)
      return parts.length >= 2 && parts.every(p => p.length === 1)
    })
    let s = 0
    while (s < charLineFlags.length){
      if (charLineFlags[s]){
        let e = s+1
        while (e < charLineFlags.length && charLineFlags[e]) e++
        const block = rawLines.slice(s, e).map(l=> l.split('\t').map(p=> p.trim()).filter(Boolean))
        if (block.length){
          let header = null
          for (let k = s-1; k >= 0; k--){
            const txt = String(rawLines[k] || '').trim()
            if (!txt) continue
            if (/\(.*:\s*\w+\)/i.test(txt.replace(/\s/g,''))){ header = txt.replace(/\s/g,'').replace(/[^A-Za-z:]/g,'').replace(/:/,' : '); break }
            break
          }
          const rows = block.map(parts => [ parts.join('') ])
          const rowsMerged = mergeContinuations(rows)
          const pre = rawLines.slice(0, s).map(l=> l.trim()).filter(l=> l.length>0)
          const post = rawLines.slice(e).map(l=> l.trim()).filter(l=> l.length>0)
          return header ? finalize({ pre, cols: [header], rows: rowsMerged, post }) : finalize({ pre, cols: ['value'], rows: rowsMerged, post })
        }
        s = e
      } else s++
    }
    for (const d of delimiters){
      const splitRows = nonEmpty.map(l=> l.split(new RegExp(d)).map(c=> c.trim()))
      const parts = splitRows[0]
      if (parts && parts.length > 1){
        const ratios = splitRows.map(r => (r.length ? (r.filter(c=> c.length === 1).length / r.length) : 0))
        const avg = ratios.reduce((a,b)=> a+b, 0) / ratios.length
        if (avg > 0.6 && parts.length >= 3){
          const merged = splitRows.map(r => {
            const out = []
            let buf = ''
            for (const c of r){ if (c.length === 1) buf += c; else { if (buf) { out.push(buf); buf = '' }; out.push(c) } }
            if (buf) out.push(buf)
            return out
          })
          const maxLen = Math.max(...merged.map(r=> r.length))
          const cols = Array.from({length: maxLen}, (_,i)=> `col${i+1}`)
          const rows = merged.map(r=> r.concat(Array(maxLen - r.length).fill('')))
          return finalize({ cols, rows })
        }
        const cols = parts.map(p=> p.trim())
        const rows = splitRows
        return finalize({ cols, rows })
      }
    }

    const splitBySpace = nonEmpty.map(l=> l.split(/\s+/).map(p=> p.trim()).filter(Boolean))
    const allSingle = splitBySpace.every(r => r.length > 0 && r.every(p => p.length === 1))
    if (allSingle){
      const merged = splitBySpace.map(r => {
        const out = []
        let buf = ''
        for (const c of r){ if (c.length === 1) buf += c; else { if (buf) { out.push(buf); buf = '' }; out.push(c) } }
        if (buf) out.push(buf)
        return out
      })
      const maxLen = Math.max(...merged.map(r=> r.length))
      const cols = Array.from({length: maxLen}, (_,i)=> `col${i+1}`)
      const rows = merged.map(r=> r.concat(Array(maxLen - r.length).fill('')))
      return finalize({ cols, rows })
    }

    return finalize({ cols: ['value'], rows: nonEmpty.map(l=> [l]) })
  }

  return null
}

function TableRenderer({table}){
  if (!table) return null
  const cols = table.cols || []
  const rows = table.rows || []
  const pre = table.pre || []
  const post = table.post || []
  const csv = toCSV(cols, rows)
  return (
    <div>
      {pre.length ? (
        <div style={{marginBottom:8}}>
          {pre.map((l,i)=> <div key={i} style={{whiteSpace:'pre-wrap'}}>{l}</div>)}
        </div>
      ) : null}

      <div style={{overflowX:'auto'}}>
        <table style={{borderCollapse:'collapse', width:'100%'}}>
          <thead>
            <tr>
              {cols.map((c,i)=> (
                <th key={i} style={{textAlign:'left', borderBottom:'1px solid #ccc', padding:'6px'}}>{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r,ri)=> (
              <tr key={ri}>
                {(r||[]).map((cell,ci)=> (
                  <td key={ci} style={{padding:'6px', borderBottom:'1px solid #eee'}}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {post.length ? (
        <div style={{marginTop:8}}>
          {post.map((l,i)=> <div key={i} style={{whiteSpace:'pre-wrap'}}>{l}</div>)}
        </div>
      ) : null}
    </div>
  )
}

export default function Results({ output }){
  const containerRef = useRef(null)
  useEffect(()=>{
    let mounted = true
    ;(async ()=>{
      try{
        await loadCss(KATEX_CSS)
        await loadScript(KATEX_JS)
      }catch(e){ /* ignore */ }
    })()
    return ()=>{ mounted = false }
  }, [])

  let parsed = null
  if (typeof output === 'string'){
    try{ parsed = JSON.parse(output) }catch(e){ parsed = output }
  } else {
    parsed = output
  }

  return (
    <div>
      <h3>Output</h3>
      {parsed ? (
        (()=>{
          const table = detectAndBuildTable(parsed)
          if (table) return <TableRenderer table={table} />
          if (typeof parsed === 'object') return <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(parsed, null, 2)}</pre>
          return <pre style={{whiteSpace:'pre-wrap'}}>{String(parsed)}</pre>
        })()
      ) : (
        <div ref={containerRef}>
          {typeof output === 'string' && output.length < 2000 && !/^Error:/.test(output) && !/^Server error/.test(output) && /\\[a-zA-Z]|\\frac|_|\^|\{|\}/.test(output) ? (
            <div dangerouslySetInnerHTML={{__html: (window.katex ? (()=>{ try{ return window.katex.renderToString(String(output), {throwOnError:false}) }catch(e){ return '<pre>'+String(output)+'</pre>' } })() : '<pre>'+String(output)+'</pre>') }} />
          ) : (
            <pre style={{whiteSpace:'pre-wrap'}}>{output}</pre>
          )}
        </div>
      )}
    </div>
  )
}
