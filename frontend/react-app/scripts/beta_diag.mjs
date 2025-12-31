import { fileURLToPath } from 'url'
import path from 'path'
// Self-contained beta utilities (ported from gradeCurve.js) to avoid module import issues
function logGamma(z){
  const g = 7
  const p = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
  if (z < 0.5) return Math.log(Math.PI) - Math.log(Math.sin(Math.PI * z)) - logGamma(1 - z)
  z -= 1
  let x = p[0]
  for (let i = 1; i < p.length; i++) x += p[i] / (z + i)
  const t = z + g + 0.5
  return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x) - Math.log(z + 1)
}

function betacf(a, b, x) {
  const MAXIT = 200
  const EPS = 3e-7
  const FPMIN = 1e-30
  let qab = a + b
  let qap = a + 1
  let qam = a - 1
  let c = 1
  let d = 1 - qab * x / qap
  if (Math.abs(d) < FPMIN) d = FPMIN
  d = 1 / d
  let h = d
  for (let m = 1; m <= MAXIT; m++){
    const m2 = 2 * m
    let aa = m * (b - m) * x / ((qam + m2) * (a + m2))
    d = 1 + aa * d
    if (Math.abs(d) < FPMIN) d = FPMIN
    c = 1 + aa / c
    if (Math.abs(c) < FPMIN) c = FPMIN
    d = 1 / d
    h *= d * c
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
    d = 1 + aa * d
    if (Math.abs(d) < FPMIN) d = FPMIN
    c = 1 + aa / c
    if (Math.abs(c) < FPMIN) c = FPMIN
    d = 1 / d
    const del = d * c
    h *= del
    if (Math.abs(del - 1.0) < EPS) break
  }
  return h
}

function ibeta(a, b, x){
  if (x <= 0) return 0
  if (x >= 1) return 1
  const lnBeta = logGamma(a) + logGamma(b) - logGamma(a + b)
  const bt = Math.exp(Math.log(x) * a + Math.log(1 - x) * b + lnBeta)
  if (x < (a + 1) / (a + b + 2)){
    return bt * betacf(a, b, x) / a
  } else {
    return 1 - bt * betacf(b, a, 1 - x) / b
  }
}

const _betaInvCache = new Map()
function betaInvFactory(a, b, samples = 10001){
  const key = `${a.toFixed(8)}:${b.toFixed(8)}:${samples}`
  if (_betaInvCache.has(key)) return _betaInvCache.get(key)
  const xs = new Array(samples)
  const cdf = new Array(samples)
  for (let i = 0; i < samples; i++){
    const x = i / (samples - 1)
    xs[i] = x
    cdf[i] = ibeta(a, b, x)
  }
  const EPS_CDF = 1e-15
  for (let i = 1; i < samples; i++){
    if (cdf[i] <= cdf[i-1]) cdf[i] = cdf[i-1] + EPS_CDF
  }
  cdf[samples - 1] = 1
  const inv = function(p){
    if (p <= 0) return 0
    if (p >= 1) return 1
    let lo = 0, hi = samples - 1
    while (lo < hi){
      const mid = (lo + hi) >> 1
      if (cdf[mid] >= p) hi = mid
      else lo = mid + 1
    }
    const idx = lo
    if (idx === 0) return xs[0]
    const x0 = xs[idx - 1], x1 = xs[idx]
    const y0 = cdf[idx - 1], y1 = cdf[idx]
    if (y1 <= y0) return x0
    const t = (p - y0) / (y1 - y0)
    return x0 + t * (x1 - x0)
  }
  _betaInvCache.set(key, inv)
  return inv
}

function analyzePair(a,b){
  const inv = betaInvFactory(a,b)
  const ps = []
  const xs = []
  const step = 0.001
  for (let p = step; p < 1.0; p += step){
    ps.push(p)
    xs.push(inv(p))
  }
  // compute diffs
  let monotonic = true
  let maxJump = 0
  let largeJumps = 0
  let total = xs.length
  for (let i=1;i<xs.length;i++){
    const d = xs[i] - xs[i-1]
    if (d < -1e-12) monotonic = false
    if (d > maxJump) maxJump = d
    if (d > 0.02) largeJumps++
  }
  // collect detailed spike info if any large jumps
  const spikes = []
  for (let i=1;i<xs.length;i++){
    const d = xs[i] - xs[i-1]
    if (d > 0.02) spikes.push({i, pPrev: ps[i-1], pCurr: ps[i], xPrev: xs[i-1], xCurr: xs[i], diff: d})
  }
  // right-half disappearance check: proportion of values > 0.5
  const rightCount = xs.filter(x=>x>0.5).length
  return { a,b, monotonic, maxJump, largeJumps, total, rightProportion: rightCount/total, spikes }
}

const pairs = [ [1,1], [2,2], [0.5,0.5], [1.5,1.5], [3,3], [5,5], [2,5], [5,2] ]
for (const [a,b] of pairs){
  const res = analyzePair(a,b)
  console.log(JSON.stringify(res))
}

// also sweep along a==b values from 0.5..10
for (const v of [0.5,0.75,1,1.25,1.5,1.75,2,3,4,5,7,10]){
  const r = analyzePair(v,v)
  console.log('diag-eq', JSON.stringify(r))
}

// Debug CDF values for problematic pairs
function debugCdf(a,b){
  console.log('DEBUG CDF for', a, b)
  const xs = [0.49,0.5,0.55,0.6,0.65,0.7,0.75]
  for (const x of xs){
    console.log('x=',x,'ibeta=', ibeta(a,b,x))
  }
  // approximate PDF by finite diff
  const eps = 1e-6
  for (const x of [0.49,0.55,0.6,0.65,0.7]){
    const pdf = (ibeta(a,b,x+eps) - ibeta(a,b,x-eps)) / (2*eps)
    console.log('x=',x,'pdf~',pdf)
  }
}

debugCdf(3,3)
debugCdf(2,5)

// Test mapping behavior for N ranks (simulate clustering)
function testMapping(a,b,n=1398){
  const inv = betaInvFactory(a,b)
  const vals = []
  for (let i=0;i<n;i++){
    const p = (i+1)/(n+1)
    vals.push(inv(p))
  }
  const uniq = new Set(vals.map(v=>v.toFixed(12)))
  const min = Math.min(...vals), max = Math.max(...vals)
  console.log('map-test',a,b,'n',n,'unique',uniq.size,'min',min,'max',max)
  return {a,b,n,unique:uniq.size,min,max}
}

for (const [a,b] of [[1,1],[2,2],[3,3],[5,5],[0.5,0.5],[2,5]]){
  testMapping(a,b,1398)
}

// Simulate the UI spreading logic on mapped values
function simulateUiSpread(a,b,n=1398){
  const inv = betaInvFactory(a,b)
  let adj = []
  for (let i=0;i<n;i++){
    const p = (i+1)/(n+1)
    adj.push(inv(p) * 100)
  }
  const uniqBefore = new Set(adj.map(v=>v.toFixed(12))).size
  const rawMin = Math.min(...adj)
  const rawMax = Math.max(...adj)
  const rawSpread = rawMax - rawMin
  const MIN_SPREAD = 1.0
  if (rawSpread < MIN_SPREAD){
    const center = (rawMax + rawMin) / 2
    const half = MIN_SPREAD / 2
    const newMin = Math.max(0, center - half)
    const newMax = Math.min(100, center + half)
    if (rawSpread === 0){
      for (let i=0;i<n;i++) adj[i] = newMin + (i / Math.max(1, n - 1)) * (newMax - newMin)
    } else {
      for (let i=0;i<n;i++) adj[i] = newMin + ((adj[i] - rawMin) / rawSpread) * (newMax - newMin)
    }
  }
  const uniqMid = new Set(adj.map(v=>v.toFixed(12))).size
  const uniqCount = uniqMid
  const minUnique = Math.min(20, Math.max(3, Math.floor(n * 0.02)))
  if (uniqCount <= minUnique){
    const span = Math.max(0.5, Math.min(5, MIN_SPREAD))
    const center = (Math.min(...adj) + Math.max(...adj)) / 2
    const start = Math.max(0, center - span / 2)
    const end = Math.min(100, center + span / 2)
    for (let i=0;i<n;i++) adj[i] = start + (i / Math.max(1, n - 1)) * (end - start)
  }
  const uniqAfter = new Set(adj.map(v=>v.toFixed(12))).size
  const min = Math.min(...adj), max = Math.max(...adj)
  console.log('simulate-ui',a,b,'unique_before',uniqBefore,'unique_mid',uniqMid,'unique_after',uniqAfter,'min',min,'max',max)
  return {a,b,uniqBefore,uniqMid,uniqAfter,min,max}
}

for (const [a,b] of [[1,1],[2,2],[3,3],[5,5],[0.5,0.5],[2,5]]){
  simulateUiSpread(a,b,1398)
}

// Dense sweep for a==b to locate parameters with spikes
function denseSweep(){
  const bad = []
  for (let a = 0.5; a <= 10; a += 0.25){
    const r = analyzePair(a,a)
    if ((r.spikes || []).length > 0) bad.push({a:r.a, spikes: r.spikes.length, maxJump: r.maxJump})
  }
  console.log('dense-sweep-results', JSON.stringify(bad, null, 2))
  return bad
}

denseSweep()

// User-specified focus: alpha=5, test beta around 1..3 and some extras
const focusPairs = [[5,1],[5,1.3],[5,1.5],[5,2],[5,2.5],[5,3],[5,4],[5,5]]
for (const [a,b] of focusPairs){
  console.log('--- FOCUS', a, b)
  console.log('analyze:', JSON.stringify(analyzePair(a,b)))
  console.log('map-test:', JSON.stringify(testMapping(a,b,1398)))
  console.log('simulate-ui:', JSON.stringify(simulateUiSpread(a,b,1398)))
}
