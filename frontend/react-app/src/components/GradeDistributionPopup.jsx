import React, { useRef, useEffect, useState } from 'react'
import { invNorm, betaInv, betaInvFactory, betaPdf, kdeGaussian, linearShift, fitBetaFromConstraints, fitBetaToCounts, mapPercentilesToBeta } from '../utils/gradeCurve'

export default function GradeDistributionPopup({ scores = [], bins = 30, width = 700, height = 320, curveType = 'raw', onChangeCurve = ()=>{}, clusterBy = null, previewOnly = false, viewOnly = false }){
  const canvasRef = useRef(null)
  const [selectedCurve, setSelectedCurve] = useState('raw')
  const [curveParams, setCurveParams] = useState(() => ({}))
  const [fittedParams, setFittedParams] = useState(() => ({}))
  const [showHalfBins, setShowHalfBins] = useState(false)
  const [rawStats, setRawStats] = useState({ mean: 0, variance: 0 })
  const [adjStats, setAdjStats] = useState({ mean: 0, variance: 0 })
  const [gradePercents, setGradePercents] = useState({ A:0, B:0, C:0, D:0, F:0 })

  // initialize from prop which may be a string or an object { type, params }
  useEffect(()=>{
    if (!curveType) return
    if (typeof curveType === 'string'){
      setSelectedCurve(curveType)
    } else if (typeof curveType === 'object'){
      setSelectedCurve(curveType.type || 'raw')
      setCurveParams(curveType.params || {})
    }
    if (viewOnly) setSelectedCurve('raw')
  }, [curveType])

  // Do not auto-call onChangeCurve here to avoid update loops with parent.
  // We'll invoke onChangeCurve only in response to user actions below.

  const callChange = (type, params) => {
    try{ onChangeCurve({ type, params }) }catch(e){}
  }

  const curveParamsStr = JSON.stringify(curveParams)

  useEffect(() => {
    // helper functions for statistical transforms are provided by ../utils/gradeCurve
    const transformScores = () => {
      if (!scores || scores.length === 0) return []
      const n = scores.length
      // compute percentile ranks in (0,1) to avoid endpoint infinities
      const idxs = scores.map((s,i)=>({s,i})).sort((a,b)=>a.s - b.s)
      const ranks = new Array(n)
      for (let i=0;i<n;i++) ranks[idxs[i].i] = (i + 1) / (n + 1)

      // normalize raw scores to 0-100 percent scale so transforms operate on percents
      const rawMin = Math.min(...scores)
      const rawMax = Math.max(...scores)
      const normalized = scores.map(s => {
        if (rawMax === rawMin) return 100 * 0.5
        return (s - rawMin) / (rawMax - rawMin) * 100
      })

      const mean = normalized.reduce((a,b)=>a+b,0)/n
      const variance = normalized.reduce((a,b)=>a+Math.pow(b-mean,2),0)/n
      const std = Math.sqrt(variance || 1)

      // log stats on normalized (avoid log of non-positive)
      const eps = 1e-6
      const logVals = normalized.map(s => Math.log(Math.max(eps, s)))
      const meanLog = logVals.reduce((a,b)=>a+b,0)/n
      const varLog = logVals.reduce((a,b)=>a+Math.pow(b-meanLog,2),0)/n
      const stdLog = Math.sqrt(varLog || 1)

      // We'll compute a single mapping curve on a percentile grid and then
      // interpolate for each data point. This uses the curve as the baseline
      // and avoids per-point expensive operations.
      const mapped = new Array(n)
      const pArr = ranks
      const mg = 201
      const pGrid = new Array(mg)
      for (let i=0;i<mg;i++) pGrid[i] = (i + 1) / (mg + 1)

      // compute base empirical mapping (bucketed by clusterBy or 5%)
      const stepPct = Number(clusterBy && !isNaN(Number(clusterBy)) ? Number(clusterBy) : 5)
      const binsN = Math.max(1, Math.round(100 / stepPct))
      const binWidth = 100 / binsN
      const sorted = normalized.slice().sort((a,b)=>a-b)
      const binCounts = new Array(binsN).fill(0)
      for (let v of sorted){
        const idx = Math.min(binsN - 1, Math.max(0, Math.floor(v / binWidth)))
        binCounts[idx] += 1
      }
      const centers = new Array(binsN).fill(0).map((_,i) => Math.min(100, (i + 0.5) * binWidth))
      // empirical inverse-CDF via bucket centers
      const cdf = new Array(binsN)
      let acc = 0
      const total = sorted.length || 1
      for (let i = 0; i < binsN; i++){ acc += binCounts[i]; cdf[i] = acc / total }

      // helper: compute mapXs on pGrid for selectedCurve
      let mapXs = new Array(mg)
      const interpModel = (p) => {
        // linear search in pGrid (mg small)
        if (p <= 0) return pGrid[0]
        if (p >= 1) return pGrid[mg-1]
        const pos = p * (mg - 1)
        const i = Math.floor(pos), frac = pos - i
        if (i + 1 < mg) return pGrid[i] * (1 - frac) + pGrid[i+1] * frac
        return pGrid[mg-1]
      }

      // compute raw-mapping once (empirical inverse-CDF via bucket centers)
      const mapXsRaw = new Array(mg)
      for (let i=0;i<mg;i++){
        const p = pGrid[i]
        let found = centers[centers.length - 1]
        for (let j=0;j<cdf.length;j++){ if (cdf[j] >= p){ found = centers[j]; break } }
        mapXsRaw[i] = found
      }

      if (selectedCurve === 'raw'){
        for (let i=0;i<mg;i++) mapXs[i] = mapXsRaw[i]
      } else if (selectedCurve === 'linear'){
        const shift = Number(curveParams.shift || 0)
        for (let i=0;i<mg;i++) mapXs[i] = Math.min(100, Math.max(0, mapXsRaw[i] + shift))
      } else if (selectedCurve === 'quantile'){
        for (let i=0;i<mg;i++) mapXs[i] = pGrid[i]*100
      } else if (selectedCurve === 'beta'){
        const a = Math.max(0.01, Number(curveParams.alpha) || 2)
        const b = Math.max(0.01, Number(curveParams.beta) || 5)
        const vals = mapPercentilesToBeta(a, b, pGrid, 2001)
        for (let i=0;i<mg;i++) mapXs[i] = vals[i] * 100
      } else if (selectedCurve === 'normal_clip'){
        for (let i=0;i<mg;i++){
          const p = pGrid[i]
          const z = invNorm(p)
          const raw = mean + z * std
          mapXs[i] = raw
        }
        const mn = Math.min(...mapXs), mx = Math.max(...mapXs)
        if (mx !== mn) for (let i=0;i<mg;i++) mapXs[i] = (mapXs[i] - mn) / (mx - mn) * 100
      } else if (selectedCurve === 'log_normal'){
        const meanLogVal = meanLog
        const stdLogVal = stdLog
        for (let i=0;i<mg;i++){
          const p = pGrid[i]
          const z = invNorm(p)
          const raw = Math.exp(meanLogVal + z * stdLogVal)
          mapXs[i] = raw
        }
        const mn = Math.min(...mapXs), mx = Math.max(...mapXs)
        if (mx !== mn) for (let i=0;i<mg;i++) mapXs[i] = (mapXs[i] - mn) / (mx - mn) * 100
      } else if (selectedCurve === 'gpa_targeted'){
        const topPct = Math.max(0.0, Math.min(100.0, Number(curveParams.top_pct) || 90))
        const bottomPct = Math.max(0.0, Math.min(100.0, Number(curveParams.bottom_pct) || 10))
        const meanArg = (curveParams.average_pct !== undefined) ? Number(curveParams.average_pct) : null
        const seed = (fittedParams && fittedParams.fitted_alpha && fittedParams.fitted_beta) ? { a: fittedParams.fitted_alpha, b: fittedParams.fitted_beta } : null
        const [aFit, bFit] = fitBetaToCounts(topPct, bottomPct, n, meanArg, seed, 10001)
        const vals = mapPercentilesToBeta(aFit, bFit, pGrid, 10001)
        for (let i=0;i<mg;i++) mapXs[i] = vals[i] * 100
        setFittedParams(prev => {
          const prevA = Number(prev?.fitted_alpha || 0)
          const prevB = Number(prev?.fitted_beta || 0)
          if (Math.abs(prevA - aFit) < 1e-12 && Math.abs(prevB - bFit) < 1e-12) return prev
          return { ...prev, fitted_mode: 'beta', fitted_alpha: aFit, fitted_beta: bFit }
        })
      } else if (selectedCurve === 'mix'){
        // fallback to computing per-component on pGrid
        const comps = curveParams.components || []
        const totalW = comps.reduce((s,c)=>s + (Number(c.weight)||0), 0) || 1
        const compVals = comps.map(c => {
          if (c.type === 'beta'){
            const a_ = Math.max(0.01, Number(c.params?.alpha) || 2)
            const b_ = Math.max(0.01, Number(c.params?.beta) || 5)
            return mapPercentilesToBeta(a_, b_, pGrid, 2001).map(v=>v*100)
          } else if (c.type === 'quantile'){
            return pGrid.map(p=>p*100)
          } else if (c.type === 'raw'){
            // use empirical quantile via centers
            return pGrid.map(p => {
              for (let j=0;j<cdf.length;j++) if (cdf[j] >= p) return centers[j]
              return centers[centers.length-1]
            })
          } else if (c.type === 'normal_clip'){
            const arr = []
            for (let i=0;i<mg;i++){ const z = invNorm(pGrid[i]); arr.push(mean + z * std) }
            const mn = Math.min(...arr), mx = Math.max(...arr)
            if (mx !== mn) for (let k=0;k<arr.length;k++) arr[k] = (arr[k] - mn) / (mx - mn) * 100
            return arr
          } else if (c.type === 'log_normal'){
            const arr = []
            for (let i=0;i<mg;i++){ const z = invNorm(pGrid[i]); arr.push(Math.exp(meanLog + z * stdLog)) }
            const mn = Math.min(...arr), mx = Math.max(...arr)
            if (mx !== mn) for (let k=0;k<arr.length;k++) arr[k] = (arr[k] - mn) / (mx - mn) * 100
            return arr
          }
          return pGrid.map(p=>p*100)
        })
        for (let i=0;i<mg;i++){
          let acc = 0
          for (let j=0;j<comps.length;j++) acc += (Number(comps[j].weight)||0) * (compVals[j][i] || 0)
          mapXs[i] = acc / totalW
        }
      } else {
        for (let i=0;i<mg;i++) mapXs[i] = pGrid[i]*100
      }

      // interpolate mapXs defined on pGrid for each point percentile
      const interp = (p) => {
        if (p <= 0) return mapXs[0]
        if (p >= 1) return mapXs[mapXs.length-1]
        const pos = p * (mg - 1)
        const i0 = Math.floor(pos)
        const frac = pos - i0
        const v0 = mapXs[i0]
        const v1 = mapXs[Math.min(mapXs.length-1, i0+1)]
        return v0 * (1 - frac) + v1 * frac
      }

      for (let i=0;i<n;i++) mapped[i] = interp(pArr[i])
      return mapped
    }

    const transformed = transformScores()
    // compute normalized and basic stats here so previewOnly drawing can access them
    let normalized = []
    if (scores && scores.length > 0){
      const rawMin = Math.min(...scores)
      const rawMax = Math.max(...scores)
      normalized = scores.map(s => {
        if (rawMax === rawMin) return 100 * 0.5
        return (s - rawMin) / (rawMax - rawMin) * 100
      })
    }
    // publish raw stats for display
    if (normalized.length){
      const nRaw = normalized.length
      const meanRaw = normalized.reduce((a,b)=>a+b,0)/nRaw
      const varRaw = normalized.reduce((a,b)=>a+Math.pow(b-meanRaw,2),0)/nRaw
      setRawStats(prev => {
        if (Math.abs((prev.mean || 0) - meanRaw) < 1e-12 && Math.abs((prev.variance||0) - varRaw) < 1e-12) return prev
        return { mean: meanRaw, variance: varRaw }
      })
    }
    const nStats = normalized.length || 0
    const mean = nStats ? normalized.reduce((a,b)=>a+b,0)/nStats : 0
    const variance = nStats ? normalized.reduce((a,b)=>a+Math.pow(b-mean,2),0)/nStats : 0
    const std = Math.sqrt(variance || 1)
    const eps = 1e-6
    const logVals = normalized.map(s => Math.log(Math.max(eps, s)))
    const meanLog = nStats ? logVals.reduce((a,b)=>a+b,0)/nStats : 0
    const varLog = nStats ? logVals.reduce((a,b)=>a+Math.pow(b-meanLog,2),0)/nStats : 0
    const stdLog = Math.sqrt(varLog || 1)
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    // device pixel ratio for crisp canvas
    const dpr = window.devicePixelRatio || 1
    canvas.width = width * dpr
    canvas.height = height * dpr
    canvas.style.width = width + 'px'
    canvas.style.height = height + 'px'
    ctx.scale(dpr, dpr)

    // clear
    ctx.clearRect(0, 0, width, height)

    if (!transformed || transformed.length === 0){
      ctx.fillStyle = '#333'
      ctx.font = '14px sans-serif'
      ctx.fillText('No graded submissions available.', 12, 24)
      return
    }

    // force x axis range to 0..100 and clamp transformed values
    const min = 0
    const max = 100

    const padding = { left: 48, right: 16, top: 16, bottom: 48 }
    const plotW = width - padding.left - padding.right
    const plotH = height - padding.top - padding.bottom

    // background
    ctx.fillStyle = '#fff'
    ctx.fillRect(0, 0, width, height)

    // clamp transformed values to 0..100 and sanitize non-finite values
    let n = transformed.length
    const adj = transformed.map(v => {
      const num = Number(v)
      if (!Number.isFinite(num)) return 0
      return Math.min(100, Math.max(0, num))
    })
    // If clusterBy is provided (e.g., 5%), quantize x values to nearest bucket
    if (clusterBy && !isNaN(Number(clusterBy))){
      const step = Number(clusterBy)
      for (let i = 0; i < adj.length; i++) adj[i] = Math.min(100, Math.max(0, Math.round(adj[i] / step) * step))
    }
    const range = max - min || 1

    // If the mapped values are extremely narrowly clustered (e.g. beta with
    // large concentration), expand them slightly for visualization so points
    // don't all stack exactly on top of each other. This preserves order but
    // ensures perceptible spread. If all values are identical, evenly spread
    // them across a small window centered at the cluster.
    const rawMin = Math.min(...adj)
    const rawMax = Math.max(...adj)
    const rawSpread = rawMax - rawMin
    const MIN_SPREAD = 1.0 // percent; adjust as needed
    if (rawSpread < MIN_SPREAD){
      const center = (rawMax + rawMin) / 2
      const half = MIN_SPREAD / 2
      const newMin = Math.max(0, center - half)
      const newMax = Math.min(100, center + half)
      if (rawSpread === 0){
        // evenly distribute across new window to avoid exact stacking
        for (let i = 0; i < n; i++) adj[i] = newMin + (i / Math.max(1, n - 1)) * (newMax - newMin)
      } else {
        for (let i = 0; i < n; i++) adj[i] = newMin + ((adj[i] - rawMin) / rawSpread) * (newMax - newMin)
      }
    }

    // If still too few unique x-values (rare numeric collapse), spread by index
    const uniqCount = new Set(adj.map(v => v.toFixed(12))).size
    const minUnique = Math.min(20, Math.max(3, Math.floor(n * 0.02)))
    if (uniqCount <= minUnique){
      const span = Math.max(0.5, Math.min(5, MIN_SPREAD))
      const center = (Math.min(...adj) + Math.max(...adj)) / 2
      const start = Math.max(0, center - span / 2)
      const end = Math.min(100, center + span / 2)
      for (let i = 0; i < n; i++) adj[i] = start + (i / Math.max(1, n - 1)) * (end - start)
    }

    // publish adjusted stats for display
    if (adj.length){
      const nAdj = adj.length
      const meanAdj = adj.reduce((a,b)=>a+b,0)/nAdj
      const varAdj = adj.reduce((a,b)=>a+Math.pow(b-meanAdj,2),0)/nAdj
      setAdjStats(prev => {
        if (Math.abs((prev.mean || 0) - meanAdj) < 1e-12 && Math.abs((prev.variance||0) - varAdj) < 1e-12) return prev
        return { mean: meanAdj, variance: varAdj }
      })
      // compute A/B/C/D/F percentages from adjusted mapped values (0..100)
      const counts = { A:0, B:0, C:0, D:0, F:0 }
      for (let v of adj){
        const num = Number(v)
        if (num >= 90) counts.A += 1
        else if (num >= 80) counts.B += 1
        else if (num >= 70) counts.C += 1
        else if (num >= 60) counts.D += 1
        else counts.F += 1
      }
      const totalPts = Math.max(1, adj.length)
      const perc = {
        A: (counts.A / totalPts) * 100,
        B: (counts.B / totalPts) * 100,
        C: (counts.C / totalPts) * 100,
        D: (counts.D / totalPts) * 100,
        F: (counts.F / totalPts) * 100,
      }
      setGradePercents(prev => {
        if (Math.abs((prev.A||0) - perc.A) < 1e-6 && Math.abs((prev.B||0) - perc.B) < 1e-6) return prev
        return perc
      })
    }

    // support either per-exact-value counts or a histogram with contiguous bins
    const precision = 6
    // when "Histogram" is enabled, use bin size = clusterBy or default 5%
    let histStep = showHalfBins ? (clusterBy && !isNaN(Number(clusterBy)) ? Number(clusterBy) : 5) : null
    if (histStep) histStep = Math.max(1, Math.min(100, Math.round(Number(histStep))))
    const binsCount = showHalfBins ? (Math.max(1, Math.round(100 / histStep))) : (bins || 30)
    let countsArr = []
    let maxCount = 1
    let histogramBinCounts = null
    let histogramBinIdxs = null
    if (showHalfBins){
      // histogram bins spanning 0..100 with binsCount bins (e.g., 20 bins for 5%)
      const stepPct = (max - min) / binsCount
      histogramBinCounts = new Array(binsCount).fill(0)
      histogramBinIdxs = adj.map(v => {
        const idx = Math.floor((v - min) / stepPct)
        return Math.min(binsCount - 1, Math.max(0, idx))
      })
      for (let i = 0; i < histogramBinIdxs.length; i++) histogramBinCounts[histogramBinIdxs[i]] += 1
      countsArr = histogramBinIdxs.map(i => histogramBinCounts[i])
      maxCount = Math.max(...histogramBinCounts, 1)
    } else {
      // Deduplicate identical adj values by applying tiny alternating offsets.
      // This ensures every grade is unique while preserving original ordering
      // and keeping differences substantially smaller than the smallest
      // observed change (tinyStep = minDiff/1000 fallback 0.0005).
      const groups = new Map()
      for (let i = 0; i < n; i++){
        const key = adj[i].toFixed(precision)
        if (!groups.has(key)) groups.set(key, [])
        groups.get(key).push(i)
      }
      const uniqueVals = Array.from(new Set(adj.map(v=>Number(v)))).sort((a,b)=>a-b)
      let minNonZeroDiff = null
      for (let i = 1; i < uniqueVals.length; i++){
        const diff = uniqueVals[i] - uniqueVals[i-1]
        if (diff > 1e-12 && (minNonZeroDiff === null || diff < minNonZeroDiff)) minNonZeroDiff = diff
      }
      const tinyStep = (minNonZeroDiff && minNonZeroDiff > 0) ? (minNonZeroDiff / 1000) : 0.0005
      for (let [k, idxs] of groups.entries()){
        if (!idxs || idxs.length <= 1) continue
        idxs.sort((a,b)=>a-b)
        const m = idxs.length
        const baseVal = Number(k)
        if (baseVal === 0){
          // shift upward from zero
          for (let j = 0; j < m; j++) adj[idxs[j]] = Math.min(100, 0 + tinyStep * (j + 1))
        } else if (baseVal === 100){
          // shift downward from 100
          for (let j = 0; j < m; j++) adj[idxs[j]] = Math.max(0, 100 - tinyStep * (j + 1))
        } else if (m % 2 === 1){
          const center = Math.floor(m / 2)
          for (let j = 0; j < m; j++) adj[idxs[j]] = baseVal + (j - center) * tinyStep
        } else {
          // even count: create half-step symmetric offsets and randomly flip
          const half = m / 2
          let offsets = new Array(m)
          for (let j = 0; j < m; j++) offsets[j] = (j - (half - 0.5)) * tinyStep
          if (Math.random() < 0.5) offsets = offsets.map(x => -x)
          for (let j = 0; j < m; j++) adj[idxs[j]] = baseVal + offsets[j]
        }
      }

      const countsMap = new Map()
      for (let i = 0; i < n; i++){
        const key = adj[i].toFixed(precision)
        countsMap.set(key, (countsMap.get(key) || 0) + 1)
      }
      countsArr = adj.map(v => countsMap.get(v.toFixed(precision)) || 0)
      maxCount = Math.max(...Array.from(countsMap.values()), 1)
    }

    // draw horizontal gridlines with numeric tick labels (counts)
    // Draw gridlines before histogram so bars render on top.
    ctx.strokeStyle = '#eee'
    ctx.fillStyle = '#333'
    ctx.font = '12px sans-serif'
    ctx.textAlign = 'right'
    const yTicks = 4
    for (let i = 0; i <= yTicks; i++){
      const frac = 1 - (i / yTicks)
      const y = padding.top + (plotH * (i / yTicks))
      const tickVal = Math.round(maxCount * frac)
      ctx.beginPath(); ctx.moveTo(padding.left, y); ctx.lineTo(padding.left + plotW, y); ctx.stroke();
      ctx.fillText(String(tickVal), padding.left - 8, y + 4)
    }

    // if histogramBinCounts computed, draw contiguous histogram bars (include empty bins)
    if (histogramBinCounts){
      // draw contiguous histogram bars (no gaps). each bin spans stepPx
      const stepPx = plotW / binsCount
      ctx.fillStyle = 'rgba(66,133,244,0.9)'
      const plotLeft = padding.left
      const plotRight = padding.left + plotW
      for (let i = 0; i < binsCount; i++){
        const cnt = histogramBinCounts[i]
        if (!cnt) continue // skip zero-height bars (no visible bar)
        const h = (cnt / maxCount) * plotH
        let left = plotLeft + i * stepPx
        let widthPx = stepPx
        // clamp last bar to right edge to avoid sub-pixel overflow
        if (i === binsCount - 1) widthPx = Math.max(0, plotRight - left)
        const y = padding.top + (plotH - h)
        ctx.fillRect(left, y, widthPx, Math.max(1, h))
      }
    }

    

    // x axis labels: min, selected ticks (60/70/80/90) and max
    ctx.textAlign = 'center'
    const labelY = padding.top + plotH + 24
    ctx.fillText(String(min.toFixed(0)), padding.left, labelY)
    ctx.fillText(String(max.toFixed(0)), padding.left + plotW, labelY)
    // draw intermediate tick labels and small tick marks
    const ticks = [60, 70, 80, 90]
    ctx.strokeStyle = '#333'
    for (let t of ticks){
      if (t < min || t > max) continue
      const x = padding.left + ((t - min) / range) * plotW
      ctx.beginPath(); ctx.moveTo(x, padding.top + plotH); ctx.lineTo(x, padding.top + plotH + 6); ctx.stroke()
      ctx.fillText(String(t), x, labelY)
    }

    // draw scatter points where Y encodes numeric frequency for that value
    // when histogram mode is active (histogramBinCounts != null) we skip scatter
    if (!previewOnly){
      if (!histogramBinCounts){
        for (let i=0;i<n;i++){
          const s = adj[i]
          const count = countsArr[i]
          const x = padding.left + ((s - min) / range) * plotW
          const y = padding.top + (1 - (count / maxCount)) * plotH
          ctx.beginPath()
          ctx.fillStyle = 'rgba(66,133,244,0.9)'
          ctx.arc(x, y, 3, 0, Math.PI * 2)
          ctx.fill()
        }
      }
    } else {
      // previewOnly: draw KDE of the raw normalized scores and overlay mapping curve
      try{
        const samples01 = normalized.map(v => Math.min(100, Math.max(0, v)) / 100)
        const xs01 = []
        const mPts = 201
        for (let i=0;i<mPts;i++) xs01.push(i/(mPts-1))
        const dens = kdeGaussian(samples01, xs01, 0.08)
        const densMax = Math.max(...dens, 1e-9)
        // scale KDE to match count axis: scale so dens peak == maxCount
        const densScaled = dens.map(d => d * (maxCount / densMax))
        // draw density as filled area scaled to counts (so y-axis matches)
        ctx.fillStyle = 'rgba(66,133,244,0.18)'
        ctx.beginPath()
        for (let i=0;i<xs01.length;i++){
          const xv = padding.left + (xs01[i] * plotW)
          const yv = padding.top + plotH - (densScaled[i] / maxCount) * plotH
          if (i===0) ctx.moveTo(xv, yv)
          else ctx.lineTo(xv, yv)
        }
        // close path down to baseline
        ctx.lineTo(padding.left + plotW, padding.top + plotH)
        ctx.lineTo(padding.left, padding.top + plotH)
        ctx.closePath()
        ctx.fill()

        // draw scatter points over KDE using vertical stacking per x-column
        try{
          ctx.fillStyle = 'rgba(66,133,244,0.85)'
          const rawSamples = normalized.map(v => Math.min(100, Math.max(0, v)))
          const dotR = 2
          // column width in pixels: choose fine resolution but >=1px
          const colW = Math.max(2, Math.floor(plotW / 250))
          const plotLeftPx = padding.left
          // assign samples to column indices
          const cols = new Map()
          for (let i = 0; i < rawSamples.length; i++){
            const s = rawSamples[i]
            const x = plotLeftPx + ((s - min) / range) * plotW
            const col = Math.min(Math.floor((x - plotLeftPx) / colW), Math.max(0, Math.floor(plotW/colW)))
            const arr = cols.get(col) || []
            arr.push(x)
            cols.set(col, arr)
          }
          // draw stacked points in each column, stacking upward from baseline
          for (const [col, xs] of cols.entries()){
            for (let j = 0; j < xs.length; j++){
              const x = xs[j]
              const y = padding.top + plotH - (j * (dotR * 2.2)) - dotR - 1
              ctx.beginPath()
              ctx.arc(x, y, dotR, 0, Math.PI*2)
              ctx.fill()
            }
          }
        }catch(e){ /* non-fatal */ }

        // mapping curve: compute percentiles -> mapped x (0..100)
        const pGrid = []
        const mg = 201
        for (let i=0;i<mg;i++) pGrid.push((i + 1) / (mg + 1))
        let mapXs = []
        // empirical quantile helper (normalized contains 0..100 values)
        const normalizedSorted = (normalized && normalized.length) ? normalized.slice().sort((a,b)=>a-b) : []
        const empiricalQuantile = (arr, p) => {
          if (!arr || arr.length === 0) return p * 100
          const pos = p * (arr.length - 1)
          const i = Math.floor(pos)
          const frac = pos - i
          if (i + 1 < arr.length) return arr[i] * (1 - frac) + arr[i + 1] * frac
          return arr[i]
        }

        if (selectedCurve === 'raw' || selectedCurve === 'linear'){
          // map percentiles to an empirical inverse-CDF computed on 5% buckets
          const stepPct = Number(clusterBy && !isNaN(Number(clusterBy)) ? Number(clusterBy) : 5)
          const binsN = Math.max(1, Math.round(100 / stepPct))
          const binWidth = 100 / binsN
          const binCounts = new Array(binsN).fill(0)
          for (let v of normalizedSorted){
            const idx = Math.min(binsN - 1, Math.max(0, Math.floor(v / binWidth)))
            binCounts[idx] += 1
          }
          const total = normalizedSorted.length || 1
          const cdf = new Array(binsN)
          let acc = 0
          for (let i = 0; i < binsN; i++){ acc += binCounts[i]; cdf[i] = acc / total }
          const centers = new Array(binsN).fill(0).map((_,i) => Math.min(100, (i + 0.5) * binWidth))
          // build raw mapping
          const mapXsRawPreview = pGrid.map(p => {
            for (let i=0;i<cdf.length;i++) if (cdf[i] >= p) return centers[i]
            return centers[centers.length - 1]
          })
          if (selectedCurve === 'raw') mapXs = mapXsRawPreview.slice()
          else {
            const shift = Number(curveParams.shift || 0)
            mapXs = mapXsRawPreview.map(v => Math.min(100, Math.max(0, v + shift)))
          }
        } else if (selectedCurve === 'quantile'){
          mapXs = pGrid.map(p => p * 100)
        } else if (selectedCurve === 'beta'){
          const a = Math.max(0.01, Number(curveParams.alpha) || 2)
          const b = Math.max(0.01, Number(curveParams.beta) || 5)
          mapXs = mapPercentilesToBeta(a, b, pGrid, 2001).map(v=>v*100)
        } else if (selectedCurve === 'normal_clip'){
          const meanVal = mean
          const stdVal = std
          mapXs = pGrid.map(p => {
            const z = invNorm(p)
            return (function(){
              const raw = meanVal + z * stdVal
              return raw
            })()
          })
          // normalize raw to 0..100
          const mn = Math.min(...mapXs)
          const mx = Math.max(...mapXs)
          if (mx !== mn) mapXs = mapXs.map(v => (v - mn) / (mx - mn) * 100)
        } else if (selectedCurve === 'log_normal'){
          const meanLog = normalized.map(v=>Math.log(Math.max(1e-6,v))).reduce((a,b)=>a+b,0)/normalized.length
          const varLog = normalized.map(v=>Math.log(Math.max(1e-6,v))).reduce((a,b)=>a+Math.pow(b-meanLog,2),0)/normalized.length
          const stdLog = Math.sqrt(varLog||1)
          mapXs = pGrid.map(p => {
            const z = invNorm(p)
            const raw = Math.exp(meanLog + z * stdLog)
            return raw
          })
          const mn = Math.min(...mapXs)
          const mx = Math.max(...mapXs)
          if (mx !== mn) mapXs = mapXs.map(v => (v - mn) / (mx - mn) * 100)
        } else if (selectedCurve === 'gpa_targeted'){
          const topPct = Math.max(0.0, Math.min(100.0, Number(curveParams.top_pct) || 90))
          const bottomPct = Math.max(0.0, Math.min(100.0, Number(curveParams.bottom_pct) || 10))
          const meanArg = (curveParams.average_pct !== undefined) ? Number(curveParams.average_pct) : null
          const seed = (fittedParams && fittedParams.fitted_alpha && fittedParams.fitted_beta) ? { a: fittedParams.fitted_alpha, b: fittedParams.fitted_beta } : null
          try{
            const [aFit, bFit] = fitBetaToCounts(topPct, bottomPct, normalized.length || 0, meanArg, seed, 10001)
            const vals = mapPercentilesToBeta(aFit, bFit, pGrid, 10001)
            mapXs = vals.map(v=>v*100)
            setFittedParams(prev => {
              const prevA = Number(prev?.fitted_alpha || 0)
              const prevB = Number(prev?.fitted_beta || 0)
              if (Math.abs(prevA - aFit) < 1e-12 && Math.abs(prevB - bFit) < 1e-12) return prev
              return { ...prev, fitted_mode: 'beta', fitted_alpha: aFit, fitted_beta: bFit }
            })
          }catch(e){
            console.error('gpa_targeted fit error', e)
            mapXs = pGrid.map(p => p * 100)
          }
        } else {
          // fallback linear mapping
          mapXs = pGrid.map(p => p * 100)
        }
        // draw mapping preview: for raw, overlay KDE ridge; for beta, draw
        // the Beta PDF scaled to counts; otherwise draw the small mapping
        // preview polyline across the top.
        if (selectedCurve === 'raw'){
          try{
            ctx.strokeStyle = 'rgba(220,20,60,0.9)'
            ctx.lineWidth = 2
            ctx.beginPath()
            for (let i=0;i<xs01.length;i++){
              const x = padding.left + xs01[i] * plotW
              const y = padding.top + plotH - (densScaled[i] / maxCount) * plotH
              if (i===0) ctx.moveTo(x,y)
              else ctx.lineTo(x,y)
            }
            ctx.stroke()
          }catch(e){ console.error('Mapping draw error', e) }
        } else if (selectedCurve === 'linear'){
          try{
            const shift = Number(curveParams.shift || 0)
            const shiftFrac = shift / 100
            ctx.strokeStyle = 'rgba(220,20,60,0.9)'
            ctx.lineWidth = 2
            ctx.beginPath()
            for (let i=0;i<xs01.length;i++){
              const xVal = Math.min(1, Math.max(0, xs01[i] + shiftFrac))
              const x = padding.left + xVal * plotW
              const y = padding.top + plotH - (densScaled[i] / maxCount) * plotH
              if (i===0) ctx.moveTo(x,y)
              else ctx.lineTo(x,y)
            }
            ctx.stroke()
          }catch(e){ console.error('Mapping draw error', e) }
        } else if (selectedCurve === 'beta' || selectedCurve === 'gpa_targeted'){
          try{
            let a = Math.max(0.01, Number(curveParams.alpha) || 2)
            let b = Math.max(0.01, Number(curveParams.beta) || 5)
            if (selectedCurve === 'gpa_targeted' && fittedParams && fittedParams.fitted_alpha && fittedParams.fitted_beta){
              a = Number(fittedParams.fitted_alpha)
              b = Number(fittedParams.fitted_beta)
            }
            const pdf = xs01.map(x => betaPdf(x, a, b))
            const pdfMax = Math.max(...pdf, 1e-9)
            const pdfScaled = pdf.map(d => d * (maxCount / pdfMax))
            // draw filled area
            ctx.fillStyle = 'rgba(220,20,60,0.12)'
            ctx.beginPath()
            for (let i=0;i<xs01.length;i++){
              const xv = padding.left + xs01[i] * plotW
              const yv = padding.top + plotH - (pdfScaled[i] / maxCount) * plotH
              if (i===0) ctx.moveTo(xv, yv)
              else ctx.lineTo(xv, yv)
            }
            ctx.lineTo(padding.left + plotW, padding.top + plotH)
            ctx.lineTo(padding.left, padding.top + plotH)
            ctx.closePath()
            ctx.fill()
            // draw ridge
            ctx.strokeStyle = 'rgba(220,20,60,0.9)'
            ctx.lineWidth = 2
            ctx.beginPath()
            for (let i=0;i<xs01.length;i++){
              const x = padding.left + xs01[i] * plotW
              const y = padding.top + plotH - (pdfScaled[i] / maxCount) * plotH
              if (i===0) ctx.moveTo(x,y)
              else ctx.lineTo(x,y)
            }
            ctx.stroke()
          }catch(e){ console.error('Beta draw error', e) }
        } else {
          // quantile remains a nearly-flat visual line
          if (selectedCurve === 'quantile'){
            ctx.strokeStyle = 'rgba(220,20,60,0.9)'
            ctx.lineWidth = 2
            ctx.beginPath()
            const flatY = padding.top + 10
            for (let i=0;i<mapXs.length;i++){
              const x = padding.left + ((mapXs[i] - min) / range) * plotW
              const y = flatY
              if (i===0) ctx.moveTo(x,y)
              else ctx.lineTo(x,y)
            }
            ctx.stroke()
          } else if (mapXs && mapXs.length > 2){
            // numerically approximate density via derivative: dx/dp
            const mgLocal = mapXs.length
            const deriv = new Array(mgLocal)
            const epsDeriv = 1e-6
            for (let i=0;i<mgLocal-1;i++){
              const dp = pGrid[i+1] - pGrid[i]
              const dx = (mapXs[i+1] - mapXs[i])
              const d = Math.abs(dx / Math.max(dp, 1e-12))
              deriv[i] = Math.max(d, epsDeriv)
            }
            deriv[mgLocal-1] = deriv[mgLocal-2]
            // density proportional to 1 / deriv
            const densApprox = deriv.map(d => 1 / d)
            const densMaxApprox = Math.max(...densApprox, 1e-9)
            const densScaledApprox = densApprox.map(d => d * (maxCount / densMaxApprox))
            // draw filled area across mapped x positions
            ctx.fillStyle = 'rgba(220,20,60,0.12)'
            ctx.beginPath()
            for (let i=0;i<mgLocal;i++){
              const xv = padding.left + ((mapXs[i] - min) / range) * plotW
              const yv = padding.top + plotH - (densScaledApprox[i] / maxCount) * plotH
              if (i===0) ctx.moveTo(xv, yv)
              else ctx.lineTo(xv, yv)
            }
            ctx.lineTo(padding.left + plotW, padding.top + plotH)
            ctx.lineTo(padding.left, padding.top + plotH)
            ctx.closePath()
            ctx.fill()
            // draw ridge
            ctx.strokeStyle = 'rgba(220,20,60,0.9)'
            ctx.lineWidth = 2
            ctx.beginPath()
            for (let i=0;i<mgLocal;i++){
              const xv = padding.left + ((mapXs[i] - min) / range) * plotW
              const yv = padding.top + plotH - (densScaledApprox[i] / maxCount) * plotH
              if (i===0) ctx.moveTo(xv, yv)
              else ctx.lineTo(xv, yv)
            }
            ctx.stroke()
          }
        }
      }catch(e){ console.error('Preview draw error', e) }
    }

    // axes
    ctx.strokeStyle = '#333'
    ctx.beginPath(); ctx.moveTo(padding.left, padding.top); ctx.lineTo(padding.left, padding.top + plotH); ctx.lineTo(padding.left + plotW, padding.top + plotH); ctx.stroke()

    // title
    ctx.fillStyle = '#111'
    ctx.font = '14px sans-serif'
    ctx.textAlign = 'left'
    ctx.fillText(`Scatterplot — ${scores.length} data points`, padding.left, 14)

  }, [scores, bins, width, height, selectedCurve, curveParamsStr, showHalfBins, clusterBy, previewOnly])

  return (
    <div style={{display:'flex',flexDirection:'column',gap:8,alignItems:'stretch'}}>
      <div style={{display:'flex',gap:8,alignItems:'center'}}>
        {!viewOnly ? (
          <>
            <label style={{margin:0,fontWeight:600}}>Curve</label>
            <select value={selectedCurve} onChange={e=>{ const t = e.target.value; setSelectedCurve(t); callChange(t, curveParams); }}>
              <option value="raw">raw</option>
              <option value="linear">linear</option>
              <option value="normal_clip">normal (clipped)</option>
              <option value="quantile">quantile</option>
              <option value="beta">beta</option>
              <option value="log_normal">log-normal</option>
            </select>
          </>
        ) : (
          <div style={{fontWeight:600}}>Raw scores</div>
        )}
        <div style={{marginLeft:'auto',display:'flex',gap:8,alignItems:'center'}}>
          <label style={{fontSize:12,display:'flex',alignItems:'center',gap:6}}><input type="checkbox" checked={showHalfBins} onChange={e=>setShowHalfBins(e.target.checked)} /> Histogram</label>
          <div style={{fontSize:12,color:'#666'}}>Selected: {String(selectedCurve).replace('_',' ')}</div>
        </div>
      </div>

      {/* Parameter controls for selected curve */}
      <div style={{padding:'6px 0 0 0'}}>
        {selectedCurve === 'linear' && (
          <div style={{display:'flex',gap:8,alignItems:'center'}}>
            <label style={{minWidth:120}}>Shift (-100..100)</label>
            <input type="number" step="1" min={-100} max={100} value={curveParams.shift ?? 0} onChange={e=>{ const v = Number(e.target.value); const np = {...curveParams, shift: v}; setCurveParams(np); callChange(selectedCurve, np); }} />
            <div style={{color:'#666',fontSize:12}}>Shift moves mass toward 0 (negative) or 100 (positive). Values are capped at 0/100.</div>
          </div>
        )}

        {selectedCurve === 'beta' && (
          <div style={{display:'flex',gap:8,alignItems:'center'}}>
            <label style={{minWidth:120}}>Alpha</label>
            <input type="number" step="0.1" min={0.01} value={curveParams.alpha ?? 2.0} onChange={e=>{ const v = Number(e.target.value); const np = {...curveParams, alpha: v}; setCurveParams(np); callChange(selectedCurve, np); }} />
            <label style={{minWidth:80}}>Beta</label>
            <input type="number" step="0.1" min={0.01} value={curveParams.beta ?? 5.0} onChange={e=>{ const v = Number(e.target.value); const np = {...curveParams, beta: v}; setCurveParams(np); callChange(selectedCurve, np); }} />
          </div>
        )}

        {selectedCurve === 'mix' && (
          <div style={{display:'flex',flexDirection:'column',gap:8}}>
            {(curveParams.components || []).map((c, idx) => (
              <div key={idx} style={{display:'flex',gap:8,alignItems:'center'}}>
                <select value={c.type} onChange={e=>{ const comps = (curveParams.components||[]).slice(); comps[idx] = {...comps[idx], type: e.target.value}; const np = {...curveParams, components: comps}; setCurveParams(np); callChange(selectedCurve, np); }}>
                  <option value="raw">raw</option>
                  <option value="linear">linear</option>
                  <option value="normal_clip">normal (clipped)</option>
                  <option value="quantile">quantile</option>
                  <option value="beta">beta</option>
                  <option value="log_normal">log-normal</option>
                </select>
                <input type="number" step="0.01" min={0} value={c.weight ?? 1} onChange={e=>{ const comps = (curveParams.components||[]).slice(); comps[idx] = {...comps[idx], weight: Number(e.target.value)}; const np = {...curveParams, components: comps}; setCurveParams(np); callChange(selectedCurve, np); }} style={{width:100}} />
                <button onClick={()=>{ const comps = (curveParams.components||[]).slice(); comps.splice(idx,1); const np = {...curveParams, components: comps}; setCurveParams(np); callChange(selectedCurve, np); }}>Remove</button>
              </div>
            ))}
            <div>
              <button onClick={()=>{ const comps = [...(curveParams.components||[]), { type: 'raw', weight: 1 }]; const np = {...curveParams, components: comps}; setCurveParams(np); callChange(selectedCurve, np); }}>Add Component</button>
            </div>
            <div style={{color:'#666',fontSize:12}}>Mix combines multiple models; weights are relative.</div>
          </div>
        )}

        {selectedCurve === 'gpa_targeted' && (
          <div style={{display:'flex',gap:8,alignItems:'center'}}>
            <label style={{minWidth:140}}>Average %</label>
            <input type="number" step="0.1" min={0} max={100} value={curveParams.average_pct ?? 50} onChange={e=>{ const v = Number(e.target.value); const np = {...curveParams, average_pct: v}; setCurveParams(np); callChange(selectedCurve, np); }} />
            <label style={{minWidth:120}}>Top grade % (A)</label>
            <input type="number" step="0.1" min={0} max={100} value={curveParams.top_pct ?? 90} onChange={e=>{ const v = Number(e.target.value); const np = {...curveParams, top_pct: v}; setCurveParams(np); callChange(selectedCurve, np); }} />
            <label style={{minWidth:120}}>Bottom grade % (F)</label>
            <input type="number" step="0.1" min={0} max={100} value={curveParams.bottom_pct ?? 10} onChange={e=>{ const v = Number(e.target.value); const np = {...curveParams, bottom_pct: v}; setCurveParams(np); callChange(selectedCurve, np); }} />
            <div style={{marginLeft:8,fontSize:12,color:'#333'}}>
              {fittedParams.fitted_alpha ? (
                <div>Fitted: α={Number(fittedParams.fitted_alpha).toFixed(3)}, β={Number(fittedParams.fitted_beta).toFixed(3)}</div>
              ) : (
                <div style={{color:'#666'}}>Fitted params will appear after mapping.</div>
              )}
            </div>
          </div>
        )}

        {(selectedCurve === 'normal_clip' || selectedCurve === 'log_normal') && (
          <div style={{color:'#666',fontSize:12}}>Parameters are auto-calculated from the distribution variance.</div>
        )}

        {selectedCurve === 'quantile' && (
          <div style={{color:'#666',fontSize:12}}>Quantile mapping will spread scores uniformly across 0–100.</div>
        )}

      </div>

      <canvas ref={canvasRef} />
      <div style={{display:'flex',gap:12,alignItems:'center',fontSize:12,color:'#666',marginTop:6}}>
        <div>
          <div style={{fontWeight:600}}>Raw (normalized)</div>
          <div>Mean: {rawStats.mean.toFixed(3)}  ·  Var: {rawStats.variance.toFixed(3)}</div>
        </div>
        <div>
          <div style={{fontWeight:600}}>Adjusted (mapped)</div>
          <div>Mean: {adjStats.mean.toFixed(3)}  ·  Var: {adjStats.variance.toFixed(3)}</div>
        </div>
        <div style={{display:'flex',gap:12,alignItems:'center',marginLeft:'auto'}}>
          <div style={{fontSize:12}}>
            <div style={{fontWeight:600}}>Grade bands (adjusted)</div>
            <div>A (90-100): {gradePercents.A.toFixed(1)}% · B (80-89): {gradePercents.B.toFixed(1)}%</div>
            <div>C (70-79): {gradePercents.C.toFixed(1)}% · D (60-69): {gradePercents.D.toFixed(1)}% · F (0-59): {gradePercents.F.toFixed(1)}%</div>
          </div>
          <div style={{marginLeft:16,fontSize:12}}>X-axis: score range (min to max). Y-axis: frequency (count in bin).</div>
        </div>
      </div>
    </div>
  )
}
