// CommonJS parser module extracted from Results.jsx for unit testing
function mergeTokens(toks, { continueOnSingle = false } = {}){
  const out = []
  for (let i = 0; i < toks.length; i++){
    let t = toks[i]
    if (!t) continue
    const firstChar = t[0]
    if (out.length > 0 && firstChar && firstChar === firstChar.toLowerCase() && /[a-z]/.test(firstChar)){
      out[out.length-1] = out[out.length-1] + t
      continue
    }
    let cur = t
    while (i+1 < toks.length){
      const nxt = toks[i+1]
      if (!nxt) { i++; continue }
      const nc = nxt[0]
      const isLower = nc && nc === nc.toLowerCase() && /[a-z]/.test(nc)
      if (isLower || (continueOnSingle && nxt.length === 1)){
        cur = cur + nxt
        i++
      } else break
    }
    out.push(cur)
  }
  return out
}

function mergeContinuations(rows){
  const toks = rows.map(r => Array.isArray(r) ? String(r[0] ?? '') : String(r ?? ''))
  return mergeTokens(toks, { continueOnSingle: false }).map(s => [s])
}

function mergeRowFragments(rows){
  const toks = rows.map(r => Array.isArray(r) ? String(r[0] ?? '') : String(r ?? ''))
  return mergeTokens(toks, { continueOnSingle: true }).map(s => [s])
}

function finalize(obj){
  if (!obj) return obj
  if (obj.cols && obj.cols.length === 1 && obj.rows){
    try{ obj.rows = mergeRowFragments(obj.rows) }catch(e){}
  }
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
      const targetLen = newCols.length
      const newRows = (obj.rows || []).map(r => {
        const row = Array.isArray(r) ? r.slice() : [String(r||'')]
        if (row.length === 1 && typeof row[0] === 'string' && row[0].includes(',')){
          const parts = row[0].split(',').map(p=> p.trim())
          if (parts.length === targetLen) return parts
        }
        const flat = row.flatMap(cell => (typeof cell === 'string' && cell.includes(',')) ? cell.split(',').map(p=>p.trim()) : [cell])
        if (flat.length === targetLen) return flat
        if (row.length === targetLen) return row
        const out = row.slice(0, targetLen)
        while (out.length < targetLen) out.push('')
        return out
      })
      obj.cols = newCols
      obj.rows = newRows
    }
  }catch(e){/* ignore */}
  return obj
}

function detectAndBuildTable(obj){
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
  const isSep = l => /-{3,}/.test(String(l).replace(/\s/g,'')) || (/^[\-\s|]{5,}$/.test(l))
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
  if (schemaIdxs.length && sepIdx.length >= 1){
    for (const sIdx of schemaIdxs){
      const firstSep = sepIdx.find(x => x > sIdx)
      if (firstSep == null) continue
      let dataEnd = firstSep + 1
      const isCountLine = (str) => /^\d+\s+rows\b/i.test(String(str || '').trim())
      while (dataEnd < rawLines.length){
        const txt = String(rawLines[dataEnd] || '').trim()
        if (txt === '' || isSep(rawLines[dataEnd]) || isCountLine(txt)) break
        dataEnd++
      }
      const schemaLine = rawLines[sIdx]
      const header = String(schemaLine).replace(/\s/g,'').replace(/[^A-Za-z:]/g,'').replace(/:/,' : ')
      const dataLines = rawLines.slice(firstSep+1, dataEnd).map(l=> l.trim()).filter(l=> l.length > 0)
      if (dataLines.length === 0) continue
      const rows = dataLines.map(l=>{
        const partsTab = l.split('\t').map(p=> p.trim()).filter(Boolean)
        const parts = partsTab.length > 1 ? partsTab : l.split(/\s+/).map(p=> p.trim()).filter(Boolean)
        if (parts.length > 1 && parts.every(p=> p.length === 1)) return [ parts.join('') ]
        return [ parts.join(' ') ]
      })
      const rowsMerged = mergeContinuations(rows)
      const pre = rawLines.slice(0, sIdx).map(l=> l.trim()).filter(l=> l.length>0)
      const post = rawLines.slice(dataEnd).map(l=> l.trim()).filter(l=> l.length>0)
      return finalize({ pre, cols: [header], rows: rowsMerged, post })
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

module.exports = { detectAndBuildTable }
