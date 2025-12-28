import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Modal from '../components/Modal'
import api, { admin } from '../lib/api'

export default function AssignmentView(){
  const { id } = useParams()
  const navigate = useNavigate()
  const [assignment, setAssignment] = useState(null)
  const [submissions, setSubmissions] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [title, setTitle] = useState('')
  const [saving, setSaving] = useState(false)
  const [showGrades, setShowGrades] = useState(false)
  const [gradesData, setGradesData] = useState(null)
  const [loadingGrades, setLoadingGrades] = useState(false)
  const [gradesError, setGradesError] = useState(null)
  const [curveEnabled, setCurveEnabled] = useState(false)
  const [curveModel, setCurveModel] = useState('beta')
  const [curveAlpha, setCurveAlpha] = useState(2.0)
  const [curveBeta, setCurveBeta] = useState(5.0)
  const [syntheticStudents, setSyntheticStudents] = useState(null)

  useEffect(()=>{
    let mounted = true
    const load = async ()=>{
      setLoading(true)
      try{
        // load submissions (current user)
        const sres = await api.getAssignmentSubmissions(id)
        if (mounted && sres.ok && sres.data) setSubmissions(sres.data.submissions || [])
        // attempt to find assignment metadata by scanning course assignments
        const cres = await admin.listCourses()
        if (mounted && cres.ok && cres.data){
          for (const c of (cres.data.courses||[])){
            const ares = await admin.getCourseAssignments(c.id)
            if (ares.ok && ares.data){
              const found = (ares.data.assignments||[]).find(a=>String(a.id)===String(id))
              if (found){
                setAssignment({...found, course: c})
                setTitle(found.title || '')
                break
              }
            }
          }
        }
      }catch(e){
        console.error('Failed loading assignment', e)
      }finally{
        if (mounted) setLoading(false)
      }
    }
    load()
    return ()=>{ mounted = false }
  },[id])

  const handleSave = async ()=>{
    setSaving(true)
    try{
      const res = await admin.updateAssignment(id, { title })
      if (res.ok){
        setAssignment(a=>({...a, title}))
        setEditing(false)
      } else {
        alert('Save failed')
      }
    }catch(e){
      console.error('Save error', e)
      alert('Network error')
    }finally{ setSaving(false) }
  }

  const loadGrades = async ()=>{
    setLoadingGrades(true)
    setGradesError(null)
    try{
      const res = await admin.getAssignmentGrades(id)
      if (res.ok && res.data){
        setGradesData(res.data)
      } else {
        setGradesError('Failed to load grades')
      }
    }catch(e){
      console.error('Grades load error', e)
      setGradesError('Network error')
    }finally{
      setLoadingGrades(false)
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div style={{padding:16}}>
      <button onClick={()=>navigate(-1)} style={{marginBottom:12}}>Back</button>
      <h2>{assignment ? assignment.title : `Assignment ${id}`}</h2>
      {assignment && <div style={{color:'#666',marginBottom:8}}>Course: {assignment.course?.title || '—'}</div>}
      <div style={{marginBottom:12,display:'flex',gap:8}}>
        <button onClick={()=>setEditing(true)}>Edit Assignment</button>
        <button onClick={async ()=>{ setShowGrades(true); await loadGrades() }}>View Grade Distribution</button>
      </div>

      <h3>Submissions</h3>
      <ul>
        {submissions.map(s=> (
          <li key={s.submission_id}>{s.student_id} — Score: {s.score}</li>
        ))}
      </ul>

      {editing && (
        <Modal title="Edit Assignment" onClose={()=>setEditing(false)} onSubmit={handleSave} submitting={saving} submitLabel="Save">
          <div style={{display:'flex',flexDirection:'column',gap:8}}>
            <label>Title</label>
            <input value={title} onChange={e=>setTitle(e.target.value)} />
          </div>
        </Modal>
      )}

      {showGrades && (
        <Modal title="Grade Distribution" onClose={()=>{ setShowGrades(false); setGradesData(null); setGradesError(null) }}>
          <div style={{minWidth:630}}>
            {loadingGrades && <div>Loading grades...</div>}
            {gradesError && <div style={{color:'red'}}>{gradesError}</div>}
            {gradesData && (
              <div>
                <div style={{marginBottom:8}}>Total points: {gradesData.total_points}</div>
                <div style={{display:'flex',gap:12}}>
                    <div>
                      <strong>Stats</strong>
                      <div>Count: {gradesData.stats.count}</div>
                      <div>Students: {gradesData.students ? gradesData.students.length : 0}</div>
                      {gradesData.students && gradesData.students.length>0 && <div style={{color:'#666',fontSize:12}}>Sample: {gradesData.students.slice(0,8).map(s=> (s.percent==null? '—' : (Math.round(s.percent*100)/100)+'%')).join(', ')}</div>}
                      <div>Mean: {gradesData.stats.mean ? gradesData.stats.mean.toFixed(2) : '—' }%</div>
                      <div>Median: {gradesData.stats.median ? gradesData.stats.median.toFixed(2) : '—' }%</div>
                      <div>Min: {gradesData.stats.min ? gradesData.stats.min.toFixed(2) : '—' }%</div>
                      <div>Max: {gradesData.stats.max ? gradesData.stats.max.toFixed(2) : '—' }%</div>
                    </div>
                    <div>
                      <strong>Scatter</strong>
                      <div style={{display:'flex',gap:8,alignItems:'center',marginBottom:6}}>
                        <label style={{display:'flex',alignItems:'center',gap:6}}><input type="checkbox" checked={curveEnabled} onChange={e=>setCurveEnabled(e.target.checked)} /> Show curve</label>
                        <label>Model: <select value={curveModel} onChange={e=>setCurveModel(e.target.value)}><option value="beta">Beta</option></select></label>
                        {curveModel === 'beta' && (
                          <div style={{display:'flex',gap:6,alignItems:'center'}}>
                            <label style={{fontSize:12}}>α <input type="number" step="0.1" min="0.1" value={curveAlpha} onChange={e=>setCurveAlpha(parseFloat(e.target.value)||1)} style={{width:64}}/></label>
                            <label style={{fontSize:12}}>β <input type="number" step="0.1" min="0.1" value={curveBeta} onChange={e=>setCurveBeta(parseFloat(e.target.value)||1)} style={{width:64}}/></label>
                          </div>
                        )}
                        <div style={{display:'flex',gap:6,alignItems:'center'}}>
                          <button onClick={()=>{
                            // apply: generate synthetic students from selected model
                            if (curveModel !== 'beta') return
                            const a = parseFloat(curveAlpha) || 2
                            const b = parseFloat(curveBeta) || 5
                            const n = Math.max(1, Math.floor(gradesData?.stats?.count || (gradesData?.students?.length || 100)))
                            const samples = []
                            const sampleBeta = (alpha, beta) => {
                              const gamma = (k) => {
                                if (k <= 0) return 0
                                if (k < 1) {
                                  // boost for <1
                                  const u = Math.random()
                                  return gamma(1 + k) * Math.pow(u, 1 / k)
                                }
                                const d = k - 1/3
                                const c = 1 / Math.sqrt(9 * d)
                                while (true){
                                  let x=0, v=0
                                  // normal via Box-Muller
                                  let u1 = Math.random(), u2 = Math.random()
                                  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2*Math.PI*u2)
                                  x = z
                                  v = Math.pow(1 + c * x, 3)
                                  if (v > 0){
                                    const u = Math.random()
                                    if (Math.log(u) < 0.5 * x * x + d - d * v + d * Math.log(v)) return d * v
                                  }
                                }
                              }
                              const g1 = gamma(alpha)
                              const g2 = gamma(beta)
                              return g1 / (g1 + g2)
                            }
                            for (let i=0;i<n;i++){
                              const t = sampleBeta(a,b)
                              const pct = (gradesData && gradesData.stats) ? (gradesData.stats.min + t * (gradesData.stats.max - gradesData.stats.min)) : (t*100)
                              samples.push({ student_id: `synth_${i+1}`, percent: pct })
                            }
                            setSyntheticStudents(samples)
                          }}>Apply</button>
                          <button onClick={()=>setSyntheticStudents(null)}>Reset</button>
                        </div>
                      </div>
                      <div style={{width:720,height:220,border:'1px solid #eee',padding:8}}>
                        <ScatterPlot histogramBins={12} buckets={gradesData.histogram.buckets} labels={gradesData.histogram.labels} stats={gradesData.stats} students={syntheticStudents || gradesData.students} curveEnabled={curveEnabled} curveModel={curveModel} curveParams={{alpha:curveAlpha,beta:curveBeta}} />
                      </div>
                    </div>
                  </div>
              </div>
            )}
          </div>
        </Modal>
      )}
    </div>
  )
}


function ScatterPlot({ buckets = [], labels = [], stats = {}, students = [], histogramBins = null, curveEnabled=false, curveModel='beta', curveParams={} }){
  const w = 520, h = 220, pad = 40
  const innerW = w - pad*2
  const innerH = h - pad*2

  // Build groups keyed by rounded percent, and get min/max from stats
  let groups = {}
  let maxFreq = 1
  const minGrade = (stats && typeof stats.min === 'number') ? stats.min : 0
  let maxGrade = (stats && typeof stats.max === 'number') ? stats.max : 100
  if (minGrade === maxGrade) maxGrade = minGrade + 1
  if (students && students.length > 0){
    students.forEach(s => {
      if (!s || s.percent == null) return
      const pct = Math.round((s.percent||0) * 100) / 100
      const key = String(pct)
      if (!groups[key]) groups[key] = []
      groups[key].push(s)
      if (pct > maxGrade) maxGrade = pct
    })
    maxFreq = Math.max(1, ...Object.values(groups).map(g=>g.length))
  } else {
    // fallback to buckets
    const n = buckets.length || 1
    const bucketWidth = 100 / n
    for (let i=0;i<n;i++){
      const center = i*bucketWidth + bucketWidth/2
      const count = buckets[i] || 0
      if (count > 0) groups[String(Math.round(center*100)/100)] = Array.from({length: count}).map((_,idx)=>({__idx: idx}))
      maxFreq = Math.max(maxFreq, count)
      maxGrade = Math.max(maxGrade, center)
    }
  }

  // tile sizing: compute bin width and tileSize to ensure square, even tiles
  const keys = Object.keys(groups).map(k=>parseFloat(k)).sort((a,b)=>a-b)
  const binsCount = Math.max(1, keys.length)
  const binWidth = innerW / binsCount
  const sqSize = Math.max(2, Math.min(binWidth * 0.9, innerH / Math.max(1, maxFreq) * 0.9))
  const tileSize = Math.max(1, Math.floor(sqSize))

  const xFor = v => pad + ((v - minGrade) / (maxGrade - minGrade)) * innerW

  const xTicks = Array.from({length:5}).map((_,i)=>Math.round(minGrade + (i/4)*(maxGrade - minGrade)))
  const total = students && students.length > 0 ? students.length : ((buckets||[]).reduce((s,n)=>s+(n||0),0) || 0)
  const maxCount = Math.max(1, maxFreq)
  const yTickCounts = [0, Math.ceil(maxCount/4), Math.ceil(maxCount/2), Math.ceil((3*maxCount)/4), maxCount]

  // compute curve path if requested (beta model)
  const curvePath = (() => {
    if (!curveEnabled || curveModel !== 'beta') return null
    const a = parseFloat(curveParams.alpha) || 2
    const b = parseFloat(curveParams.beta) || 5
    const samples = 200
    const ys = []
    const xs = []
    for (let i=0;i<samples;i++){
      const t = i / (samples - 1)
      xs.push(minGrade + t * (maxGrade - minGrade))
      const tt = Math.max(1e-8, Math.min(1-1e-8, t))
      ys.push(Math.pow(tt, a-1) * Math.pow(1-tt, b-1))
    }
    const dt = 1 / (samples - 1)
    const sumY = ys.reduce((s,v)=>s+v,0)
    const area = Math.max(1e-12, sumY * dt)
    const pdf = ys.map(v => v / area)
    const scaleFactor = 0.9
    const scaled = pdf.map(p => p * maxCount * scaleFactor)
    const points = scaled.map((val, i) => {
      const cx = xFor(xs[i])
      const cy = pad + innerH - (val / Math.max(1, maxCount)) * innerH
      return `${cx.toFixed(2)},${cy.toFixed(2)}`
    })
    if (points.length === 0) return null
    return `M ${points.join(' L ')}`
  })()

  return (
    <svg width={w} height={h} style={{display:'block'}}>
      <line x1={pad} y1={pad+innerH} x2={pad+innerW} y2={pad+innerH} stroke="#444" strokeWidth={1} />
      <line x1={pad} y1={pad} x2={pad} y2={pad+innerH} stroke="#444" strokeWidth={1} />
      {xTicks.map((label,i)=>{
        const gx = pad + (i/4)*innerW
        return (<g key={i}><line x1={gx} y1={pad+innerH} x2={gx} y2={pad+innerH+6} stroke="#444"/><text x={gx} y={pad+innerH+20} fontSize={10} textAnchor="middle">{label}</text></g>)
      })}
      {yTickCounts.map((count,i)=>{
        const gy = pad + innerH - (count / Math.max(1,maxCount)) * innerH
        const label = total > 0 ? Math.round((count / total) * 100) : 0
        return (<g key={i}><line x1={pad-6} y1={gy} x2={pad} y2={gy} stroke="#444"/><text x={pad-10} y={gy+4} fontSize={10} textAnchor="end">{label}%</text></g>)
      })}

      {/* histogram + scatter rendering (single IIFE with clear branches) */}
      {(() => {
        const Histogram = (bins=12) => {
          const b = Array.from({length: bins}).map(()=>0)
          const min = minGrade
          const max = maxGrade
          const wRange = max - min
          if (students && students.length>0){
            students.forEach(s=>{
              const v = s.percent == null ? min : s.percent
              const t = Math.min(bins-1, Math.max(0, Math.floor(((v - min) / (wRange || 1)) * bins)))
              b[t] = (b[t]||0) + 1
            })
          } else {
            const n = (buckets||[]).length || 1
            for (let i=0;i<n;i++){
              const center = i*(100/n) + (100/n)/2
              const v = center
              const t = Math.min(bins-1, Math.max(0, Math.floor(((v - min) / (wRange || 1)) * bins)))
              b[t] = (b[t]||0) + (buckets[i] || 0)
            }
          }
          const maxB = Math.max(1, ...b)
          return b.map((count, i)=>{
            const centerVal = min + (i + 0.5) * ( (max - min) / bins )
            const cx = xFor(centerVal)
            const barW = (innerW / bins) * 0.9
            const barH = (count / maxB) * innerH
            const x = cx - barW/2
            const y = pad + innerH - barH
            const fill = '#66bb6a'
            return (<g key={i}><rect x={x} y={y} width={barW} height={Math.max(1,barH)} fill={fill} stroke="#2e7d32" strokeWidth={0.5}><title>{`${Math.round(centerVal)} — ${count}`}</title></rect></g>)
          })
        }

        if (histogramBins) {
          return Histogram(histogramBins)
        }

        if (students && students.length>0) {
          const pts = students.map((s, i) => ({...s, i}))
          pts.sort((a,b)=> (a.percent||0) - (b.percent||0))
          const totalPts = Math.max(1, pts.length)
          const counts = {}
          pts.forEach(p=>{ const k = p.percent == null ? 0 : Math.round(p.percent*100)/100; counts[k] = (counts[k]||0)+1 })
          const maxCount = Math.max(1, ...Object.values(counts))
          return pts.map((p, idx) => {
            const x = xFor(p.percent == null ? minGrade : p.percent)
            const groupKey = Math.round((p.percent||0)*100)/100
            const groupCount = counts[groupKey] || 1
            const y = pad + innerH - (groupCount / Math.max(1, maxCount)) * innerH
            const intensity = Math.max(0, Math.min(1, groupCount / maxCount))
            const fill = `hsl(120,60%,${80 - intensity * 50}%)`
            return (<circle key={p.student_id || p.i} cx={x} cy={y} r={3} fill={fill} stroke="#2e7d32" strokeWidth={0.5}><title>{`${p.percent}% — ${p.student_id||''} — ${groupCount} students`}</title></circle>)
          })
        }

        // fallback: use buckets
        const pts2 = []
        const n = buckets.length || 1
        const centers = Array.from({length:n}, (_,i)=> i*(100/n) + (100/n)/2)
        for (let i=0;i<n;i++){ const count = buckets[i]||0; for (let k=0;k<count;k++) pts2.push({center: centers[i]}) }
        const total2 = Math.max(1, pts2.length)
        const counts2 = {}
        pts2.forEach(p=>{ counts2[p.center] = (counts2[p.center]||0)+1 })
        const maxCount2 = Math.max(1, ...Object.values(counts2))
        return pts2.map((p, idx)=>{
          const x = xFor(p.center)
          const y = pad + innerH - (idx / Math.max(1, total2-1)) * innerH
          const groupCount = counts2[p.center] || 1
          const intensity = Math.max(0, Math.min(1, groupCount / maxCount2))
          const fill = `hsl(120,60%,${80 - intensity * 50}%)`
          return (<circle key={idx} cx={x} cy={y} r={3} fill={fill} stroke="#2e7d32" strokeWidth={0.5}><title>{`${p.center}% — ${idx+1}`}</title></circle>)
        })
      })()}
      {curvePath && <path d={curvePath} stroke="#c62828" strokeWidth={2} fill="none" />}
    </svg>
  )
}
