// Test harness for Results.jsx detectAndBuildTable logic
const sample = `-\t-\t-\t\tG\te\tn\te\tr\ta\tt\te\td\t\tS\tQ\tL\t\t-\t-\t-\n-\t-\t-\t\tG\te\tn\te\tr\ta\tt\te\td\t\tS\tQ\tL\t\t-\t-\t-\nW\tI\tT\tH\t\t\tr\ta\tt\t0\t(\ta\t0\t,\t\ta\t1\t,\t\ta\t2\t)\t\tA\tS\t\t(\tS\tE\tL\tE\tC\tT\t\t*\t\tF\tR\tO\tM\t\t"\tc\th\te\tc\tk\ti\tn\tg\t"\t)\t,\nr\ta\tt\t1\t(\ta\t0\t)\t\tA\tS\t\t(\tS\tE\tL\tE\tC\tT\t\tD\tI\tS\tT\tI\tN\tC\tT\t\t\tr\ta\tt\t0\t.\ta\t1\t\tF\tR\tO\tM\t\t\tr\ta\tt\t0\t)\nS\tE\tL\tE\tC\tT\t\t*\t\tF\tR\tO\tM\t\tr\ta\tt\t1\n-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\n(\tn\ta\tm\te\t:\ts\tt\tr\ti\tn\tg\t)\n-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t\nH\te\tn\tr\ty\nB\tr\ti\ta\tn\nL\ta\tu\tr\ta\nP\te\tt\te\tr\nA\tn\tg\te\tl\ta\nJ\ta\ts\to\tn\nC\ty\tn\th\ti\na\nG\tr\te\tg\to\nr\ty\nD\te\tb\to\nr\na\nh\nS\tc\to\tt\nt\nS\th\ta\tr\no\nn\nP\ta\tt\nr\ni\nc\nk\nC\ta\tr\to\nl\nB\tr\ta\tn\nd\to\nn\nM\ti\tc\th\te\nl\nl\ne\nE\tr\ti\nc\nR\te\tb\ne\nc\nc\na\nG\ta\tr\ty\nS\tt\te\t\np\th\ta\nn\ni\ne\nE\tm\ti\tl\ty\nD\ta\tv\ti\td\n-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\n2\t1\t\tt\tu\tp\tl\te\ts\t\tr\te\tt\tu\tr\tn\te\td\n`;

// Minimal copy of detectAndBuildTable logic (simplified for test)
function detectAndBuildTable(obj){
  if (typeof obj !== 'string') return null
  const rawLines = obj.split(/\r?\n/)
  const delimiters = ['\t','\\|',',']

  // hyphen separator scan
  const sepIndices = []
  rawLines.forEach((l,i)=>{
    const compact = l.replace(/\s/g,'')
    if (/-{3,}/.test(compact) || (/^[\-\s|]{5,}$/.test(l))) sepIndices.push(i)
  })

  // schema before separator pattern
  const schemaIdxs = rawLines.map((l,i)=> /\(.*:\s*\w+\)/i.test(l.replace(/\s/g,'')) ? i : -1).filter(i=> i>=0)
  if (schemaIdxs.length && sepIndices.length >= 2){
    for (const sIdx of schemaIdxs){
      const firstSep = sepIndices.find(x => x > sIdx)
      if (firstSep == null) continue
      const secondSep = sepIndices.find(x => x > firstSep)
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
      const pre = rawLines.slice(0, sIdx).map(l=> l.trim()).filter(l=> l.length>0)
      const post = rawLines.slice(secondSep+1).map(l=> l.trim()).filter(l=> l.length>0)
      return { pre, cols: [header], rows, post }
    }
  }

  // contiguous tab-separated single-char blocks
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
        // merge continuation fragments: append tokens that start with lowercase
        const toks = rows.map(r=> r[0])
        const merged = []
        for (const t of toks){
          if (!t) continue
          const firstChar = t[0]
          if (merged.length > 0 && firstChar && firstChar === firstChar.toLowerCase() && /[a-z]/.test(firstChar)){
            merged[merged.length-1] = merged[merged.length-1] + t
          } else merged.push(t)
        }
        const rowsMerged = merged.map(s=> [s])
        const pre = rawLines.slice(0, s).map(l=> l.trim()).filter(l=> l.length>0)
        const post = rawLines.slice(e).map(l=> l.trim()).filter(l=> l.length>0)
        return header ? { pre, cols: [header], rows: rowsMerged, post } : { pre, cols: ['value'], rows: rowsMerged, post }
      }
      s = e
    } else s++
  }

  // fallback: try hyphen-bounded inner blocks (old behavior)
  if (sepIndices.length >= 2){
    for (let a = 0; a < sepIndices.length - 1; a++){
      for (let b = a+1; b < sepIndices.length; b++){
        const firstSep = sepIndices[a]
        const lastSep = sepIndices[b]
        if (lastSep - firstSep < 1) continue
        const inner = rawLines.slice(firstSep+1, lastSep)
        const schemaIdx = inner.findIndex(l => /\(.*:\s*\w+\)/i.test(l))
        const charGridIdx = inner.findIndex(l => {
          const parts = l.split(/\s+/).map(x=>x.trim()).filter(Boolean)
          return parts.length >= 3 && parts.every(p => p.length === 1)
        })
        if (schemaIdx >= 0 || charGridIdx >= 0){
          const pre = rawLines.slice(0, firstSep).map(l=> l.trim()).filter(l=> l.length > 0)
          const post = rawLines.slice(lastSep+1).map(l=> l.trim()).filter(l=> l.length > 0)
          // delimiter parse
          for (const d of delimiters){
            const firstParts = (inner[0] || '').split(new RegExp(d)).map(c=> String(c).trim())
            if (firstParts.length > 1){
              const cols = firstParts.slice()
              const rows = inner.map(l=> l.split(new RegExp(d)).map(c=> String(c).trim()))
              return { pre, cols, rows, post }
            }
          }
          // merge whitespace tokens
          const innerRows = inner.map(l=> l.split(/\s+/).map(c=> String(c).trim()).filter(x=>x.length>0))
          const merged = innerRows.map(row => {
            const out = []
            let buf = ''
            for (const cell of row){
              if (cell.length === 1) buf += cell
              else { if (buf) { out.push(buf); buf = '' } out.push(cell) }
            }
            if (buf) out.push(buf)
            return out.length ? out : row.slice()
          })
          const maxLen = Math.max(...merged.map(r=> Array.isArray(r)? r.length : 1))
          const cols = Array.from({length: maxLen}, (_,i)=> `col${i+1}`)
          const rows = merged.map(r=> (Array.isArray(r) ? r.concat(Array(maxLen - r.length).fill('')) : [r]).map(c=>c))
          return { pre, cols, rows, post }
        }
      }
    }
  }

  // fallback
  const lines = rawLines.map(l=> l.trim()).filter(l=> l.length > 0)
  for (const d of ['\t','\\|',',']){
    const parts = (lines[0]||'').split(new RegExp(d))
    if (parts.length > 1){
      return { cols: parts.map(p=>p.trim()), rows: lines.map(l=> l.split(new RegExp(d)).map(c=>c.trim())) }
    }
  }
  return { cols: ['value'], rows: lines.map(l=> [l]) }
}

// Also test with escaped tab sequences converted into real tabs
const sampleRealTabs = sample.replace(/\\t/g, '\t')
console.log('\n--- Parsed with escaped \\\t sequences (literal) ---')
function mergeRowFragments(rows){
  const toks = rows.map(r => Array.isArray(r) ? String(r[0] ?? '') : String(r ?? ''))
  const out = []
  for (let i = 0; i < toks.length; i++){
    let cur = toks[i]
    if (!cur) continue
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

const parsedA = detectAndBuildTable(sample)
if (parsedA && parsedA.cols && parsedA.cols.length === 1 && parsedA.rows) parsedA.rows = mergeRowFragments(parsedA.rows)
console.log(JSON.stringify(parsedA, null, 2))
console.log('\n--- Parsed with actual TAB characters ---')
const parsedB = detectAndBuildTable(sampleRealTabs)
if (parsedB && parsedB.cols && parsedB.cols.length === 1 && parsedB.rows) parsedB.rows = mergeRowFragments(parsedB.rows)
console.log(JSON.stringify(parsedB, null, 2))
