// Temporary test for multi-column header detection
const sample = `acctid : numbername:stringbalance:number
1001, John, 2345.67
1002, Jane, 3456.78
1003, Bob, 1234.56
1004, Alice, 4567.89
1005, Mike, 2890.12
1006, Mary, 3789.45
1007, Tom, 1987.65
1008, Lisa, 4230.5
1009, Chris, 3120.78
1010, Karen, 2678.9
1011, Daniel, 1576.43
1012, Nancy, 3987.65
1013, Kevin, 2789.34
1014, Sandra, 3560.22
1015, George, 4123.45
1016, Betty, 2390.67
1017, Paul, 2987.56
1018, Linda, 3876.54
1111, Brad, 200.0
2321, America, 300.0
`;

function detectAndBuildTable(obj){
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

  function finalize(obj){
    if (!obj) return obj
    if (obj.cols && obj.cols.length === 1 && obj.rows){
      try{ obj.rows = mergeRowFragments(obj.rows) }catch(e){}
    }
    return obj
  }

  if (typeof obj !== 'string') return null
  const rawLines = obj.split(/\r?\n/)
  if (rawLines.length === 0) return null

  const delimiters = ['\t','\\|',',']
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

  // fallback: simple csv parse
  const nonEmpty = rawLines.map(l=> l.trim()).filter(l=> l.length > 0)
  if (nonEmpty.length > 0){
    const firstParts = nonEmpty[0].split(',').map(p=> p.trim())
    if (firstParts.length > 1){
      return { cols: firstParts.map((c,i)=> `col${i+1}`), rows: nonEmpty.map(l=> l.split(',').map(p=> p.trim())) }
    }
    return { cols: ['value'], rows: nonEmpty.map(l=> [l]) }
  }
  return null
}

console.log(JSON.stringify(detectAndBuildTable(sample), null, 2))
