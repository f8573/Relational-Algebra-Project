// Shared grade-curve utilities moved from GradeDistributionPopup

export function logGamma(z){
  const g = 7
  const p = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
  if (z < 0.5) return Math.log(Math.PI) - Math.log(Math.sin(Math.PI * z)) - logGamma(1 - z)
  z -= 1
  let x = p[0]
  for (let i = 1; i < p.length; i++) x += p[i] / (z + i)
  const t = z + g + 0.5
  return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x) - Math.log(z + 1)
}

// Beta PDF (ported from the Python visualizer):
export function betaPdf(x, a, b){
  if (x <= 0.0 || x >= 1.0) return 0.0
  const lnB = logGamma(a) + logGamma(b) - logGamma(a + b)
  return Math.exp((a - 1) * Math.log(x) + (b - 1) * Math.log(1 - x) - lnB)
}

// Numeric CDF for Beta via composite trapezoid integration. Steps controls accuracy.
export function betaCdfNumeric(x, a, b, steps = 2000){
  if (x <= 0.0) return 0.0
  if (x >= 1.0) return 1.0
  const n = Math.max(2, Math.floor(steps))
  const dx = x / n
  let s = 0.0
  let prev = betaPdf(0 + 0, a, b)
  for (let i = 1; i <= n; i++){
    const xi = i * dx
    const cur = betaPdf(xi, a, b)
    s += 0.5 * (prev + cur) * dx
    prev = cur
  }
  return Math.min(1.0, Math.max(0.0, s))
}

// Regularized incomplete beta (ibeta) backed by numeric integration.
export function ibeta(a, b, x, steps = 2000){
  return betaCdfNumeric(x, a, b, steps)
}

// Inverse CDF using bisection over numeric CDF evaluations.
export function betaInv(p, a, b){
  if (p <= 0) return 0
  if (p >= 1) return 1
  let lo = 0.0, hi = 1.0
  const tol = 1e-9
  const maxIt = 60
  for (let i = 0; i < maxIt; i++){
    const mid = 0.5 * (lo + hi)
    const v = betaCdfNumeric(mid, a, b, 1000)
    if (v > p) hi = mid
    else lo = mid
    if (hi - lo < tol) break
  }
  return 0.5 * (lo + hi)
}

// Create an inverse-beta sampler backed by a cached sampled PDF/CDF grid.
// We compute PDF once at each sample node, build the CDF by trapezoid
// integration, and reuse the grid for mapping many percentiles quickly.
const _betaInvCache = new Map()
function _buildGrid(a, b, samples){
  const n = Math.max(3, Math.floor(samples))
  const xs = new Array(n)
  const pdf = new Array(n)
  for (let i = 0; i < n; i++){
    const x = i / (n - 1)
    xs[i] = x
    pdf[i] = betaPdf(x, a, b)
  }
  // trapezoid cumulative integration to produce CDF
  const cdf = new Array(n)
  cdf[0] = 0.0
  for (let i = 1; i < n; i++){
    const dx = xs[i] - xs[i-1]
    cdf[i] = cdf[i-1] + 0.5 * (pdf[i-1] + pdf[i]) * dx
  }
  // normalize to 1.0 (total integral should be 1 but numeric error can exist)
  const total = cdf[n - 1]
  if (total > 0){
    for (let i = 0; i < n; i++) cdf[i] = cdf[i] / total
  } else {
    // fallback: produce a linear cdf if pdf collapsed
    for (let i = 0; i < n; i++) cdf[i] = i / (n - 1)
  }
  // enforce strictly non-decreasing
  const EPS_CDF = 1e-15
  for (let i = 1; i < n; i++){
    if (cdf[i] <= cdf[i-1]) cdf[i] = cdf[i-1] + EPS_CDF
  }
  cdf[n - 1] = 1.0
  return {xs, pdf, cdf, n}
}

function _gridKey(a, b, samples){
  return `${a.toFixed(8)}:${b.toFixed(8)}:${Math.floor(samples)}`
}

function _ensureGrid(a, b, samples){
  const key = _gridKey(a, b, samples)
  let g = _betaInvCache.get(key)
  if (!g){
    g = _buildGrid(a, b, samples)
    _betaInvCache.set(key, g)
  }
  return g
}

export function betaInvFactory(a, b, samples = 10001){
  const g = _ensureGrid(a, b, samples)
  const {xs, cdf, n} = g
  const inv = function(p){
    if (p <= 0) return 0
    if (p >= 1) return 1
    // binary search in cdf
    let lo = 0, hi = n - 1
    while (lo < hi){
      const mid = (lo + hi) >> 1
      if (cdf[mid] >= p) hi = mid
      else lo = mid + 1
    }
    const idx = lo
    if (idx === 0) return xs[0]
    const i0 = idx - 1, i1 = idx
    const t = (p - cdf[i0]) / (cdf[i1] - cdf[i0])
    // linear interpolation
    const x = xs[i0] + t * (xs[i1] - xs[i0])
    // local refinement using a few bisection steps inside the bracket
    const bracketLo = Math.max(0, xs[i0])
    const bracketHi = Math.min(1, xs[i1])
    let rlo = bracketLo, rhi = bracketHi
    for (let k = 0; k < 8; k++){
      const rm = 0.5 * (rlo + rhi)
      // evaluate CDF by interpolating on the sampled grid for speed
      // (avoid expensive numeric integration during refinement)
      // find cdf at rm by linear interpolation in sampled grid
      // first locate index
      let alo = 0, ahi = n - 1
      while (alo < ahi){
        const amid = (alo + ahi) >> 1
        if (xs[amid] >= rm) ahi = amid
        else alo = amid + 1
      }
      const aidx = alo
      let cval
      if (aidx === 0) cval = cdf[0]
      else {
        const j0 = aidx - 1, j1 = aidx
        const tt = (rm - xs[j0]) / (xs[j1] - xs[j0])
        cval = cdf[j0] + tt * (cdf[j1] - cdf[j0])
      }
      if (cval > p) rhi = rm
      else rlo = rm
    }
    return 0.5 * (rlo + rhi)
  }
  return inv
}

// Map many percentiles to beta samples using the cached grid (vectorized, fast)
export function mapPercentilesToBeta(a, b, percentiles, samples = 10001){
  if (!Array.isArray(percentiles)) return []
  const g = _ensureGrid(a, b, samples)
  const {xs, cdf, n} = g
  const out = new Array(percentiles.length)
  for (let i = 0; i < percentiles.length; i++){
    const p = percentiles[i]
    if (p <= 0) { out[i] = 0; continue }
    if (p >= 1) { out[i] = 1; continue }
    // binary search
    let lo = 0, hi = n - 1
    while (lo < hi){
      const mid = (lo + hi) >> 1
      if (cdf[mid] >= p) hi = mid
      else lo = mid + 1
    }
    const idx = lo
    if (idx === 0) { out[i] = xs[0]; continue }
    const i0 = idx - 1, i1 = idx
    const t = (p - cdf[i0]) / (cdf[i1] - cdf[i0])
    out[i] = xs[i0] + t * (xs[i1] - xs[i0])
  }
  return out
}

// Fit beta parameters so that A_pct percent of class >= 90% and F_pct percent < 60%.
// Optional mean_target (0..100) constrains the mean; when provided we search over 'a'
// and compute 'b' from mean via b = a*(1-m)/m. Returns [a,b].
export function fitBetaFromConstraints(A_pct, F_pct, mean_target = null, seed = null){
  const target_cdf_90 = 1.0 - (A_pct / 100.0)
  const target_cdf_60 = (F_pct / 100.0)
  let best = null

  // If a seed is provided, do a local refinement around it first to
  // ensure continuity when parameters change slightly.
  if (seed && typeof seed === 'object' && seed.a && seed.b){
    const a0 = Math.max(0.01, Number(seed.a))
    const b0 = Math.max(0.01, Number(seed.b))
    const a_min = Math.max(0.01, a0 * 0.5)
    const a_max = a0 * 1.5
    const b_min = Math.max(0.01, b0 * 0.5)
    const b_max = b0 * 1.5
    let bestLocal = null
    for (let i = 0; i <= 20; i++){
      const a = a_min + i * (a_max - a_min) / 20.0
      for (let j = 0; j <= 20; j++){
        const b = b_min + j * (b_max - b_min) / 20.0
        const c90 = betaCdfNumeric(0.9, a, b, 200)
        const c60 = betaCdfNumeric(0.6, a, b, 200)
        const err = (c90 - target_cdf_90) ** 2 + (c60 - target_cdf_60) ** 2
        if (bestLocal === null || err < bestLocal[0]) bestLocal = [err, a, b]
      }
    }
    if (bestLocal) best = bestLocal
  }

  if (mean_target !== null && mean_target !== undefined){
    const m = mean_target / 100.0
    if (!(m > 0 && m < 1)) throw new Error('mean_target must be between 0 and 100')
    // coarse search over a
    for (let ai = 1; ai <= 200; ai++){
      const a = 0.2 + ai * 0.2
      const b = a * (1.0 - m) / m
      if (!(b > 0)) continue
      const c90 = betaCdfNumeric(0.9, a, b, 200)
      const c60 = betaCdfNumeric(0.6, a, b, 200)
      const err = (c90 - target_cdf_90) ** 2 + (c60 - target_cdf_60) ** 2
      if (best === null || err < best[0]) best = [err, a, b]
    }
    if (best === null) throw new Error('Unable to find beta parameters matching mean constraint')
    // refine around best a
    let [err0, a0, b0] = best
    const a_min = Math.max(0.1, a0 - 1.0)
    const a_max = a0 + 1.0
    let best2 = best
    for (let i = 0; i <= 200; i++){
      const a = a_min + i * (a_max - a_min) / 200.0
      const b = a * (1.0 - m) / m
      if (!(b > 0)) continue
      const c90 = betaCdfNumeric(0.9, a, b, 400)
      const c60 = betaCdfNumeric(0.6, a, b, 400)
      const err = (c90 - target_cdf_90) ** 2 + (c60 - target_cdf_60) ** 2
      if (err < best2[0]) best2 = [err, a, b]
    }
    return [best2[1], best2[2]]
  }

  // Search over a and b
  for (let ai = 1; ai <= 100; ai++){
    const a = 0.2 + ai * 0.2
    for (let bi = 1; bi <= 100; bi++){
      const b = 0.2 + bi * 0.2
      const c90 = betaCdfNumeric(0.9, a, b, 200)
      const c60 = betaCdfNumeric(0.6, a, b, 200)
      const err = (c90 - target_cdf_90) ** 2 + (c60 - target_cdf_60) ** 2
      if (best === null || err < best[0]) best = [err, a, b]
    }
  }
  // local refinement
  let [err0, a0, b0] = best
  const a_min = Math.max(0.1, a0 - 1.0)
  const a_max = a0 + 1.0
  const b_min = Math.max(0.1, b0 - 1.0)
  const b_max = b0 + 1.0
  let best2 = best
  for (let i = 0; i <= 40; i++){
    const a = a_min + i * (a_max - a_min) / 40.0
    for (let j = 0; j <= 40; j++){
      const b = b_min + j * (b_max - b_min) / 40.0
      const c90 = betaCdfNumeric(0.9, a, b, 400)
      const c60 = betaCdfNumeric(0.6, a, b, 400)
      const err = (c90 - target_cdf_90) ** 2 + (c60 - target_cdf_60) ** 2
      if (err < best2[0]) best2 = [err, a, b]
    }
  }
  // Further refine with a continuous local optimizer (Nelder-Mead) to
  // produce smooth responses to small input changes.
  function _obj_xy(xy){
    const a = Math.max(0.01, xy[0])
    const b = Math.max(0.01, xy[1])
    const c90 = betaCdfNumeric(0.9, a, b, 800)
    const c60 = betaCdfNumeric(0.6, a, b, 800)
    return (c90 - target_cdf_90) ** 2 + (c60 - target_cdf_60) ** 2
  }

  function nelderMeadOptimize(f, x0, opts = {}){
    const maxIter = opts.maxIter || 100
    const tol = opts.tol || 1e-8
    const alpha = 1, gamma = 2, rho = 0.5, sigma = 0.5
    const n = x0.length
    // initial simplex
    const scale = opts.scale || 0.2
    const simplex = [x0.slice()]
    for (let i = 0; i < n; i++){
      const xi = x0.slice()
      xi[i] = xi[i] * (1 + scale)
      if (xi[i] === x0[i]) xi[i] = x0[i] + scale
      simplex.push(xi)
    }
    const vals = simplex.map(s => f(s))
    for (let iter = 0; iter < maxIter; iter++){
      // sort simplex
      const idx = vals.map((v,i)=>[v,i]).sort((a,b)=>a[0]-b[0]).map(x=>x[1])
      const bestIdx = idx[0], worstIdx = idx[n], secondWorstIdx = idx[n-1]
      const best = simplex[bestIdx], worst = simplex[worstIdx]
      // centroid of all but worst
      const centroid = new Array(n).fill(0)
      for (let k = 0; k <= n; k++){
        if (k === worstIdx) continue
        for (let d = 0; d < n; d++) centroid[d] += simplex[k][d]
      }
      for (let d = 0; d < n; d++) centroid[d] /= n
      // reflection
      const xr = centroid.map((c,d) => c + alpha * (c - worst[d]))
      const fxr = f(xr)
      if (fxr < vals[bestIdx]){
        // expansion
        const xe = centroid.map((c,d) => c + gamma * (xr[d] - c))
        const fxe = f(xe)
        if (fxe < fxr){ simplex[worstIdx] = xe; vals[worstIdx] = fxe } else { simplex[worstIdx] = xr; vals[worstIdx] = fxr }
      } else if (fxr < vals[secondWorstIdx]){
        simplex[worstIdx] = xr; vals[worstIdx] = fxr
      } else {
        // contraction
        if (fxr < vals[worstIdx]){
          const xc = centroid.map((c,d) => c + rho * (xr[d] - c))
          const fxc = f(xc)
          if (fxc <= fxr){ simplex[worstIdx] = xc; vals[worstIdx] = fxc }
          else {
            // shrink
            for (let k = 0; k <= n; k++){
              if (k === bestIdx) continue
              simplex[k] = simplex[bestIdx].map((bv,d) => bv + sigma * (simplex[k][d] - bv))
              vals[k] = f(simplex[k])
            }
          }
        } else {
          const xc = centroid.map((c,d) => c + rho * (worst[d] - c))
          const fxc = f(xc)
          if (fxc < vals[worstIdx]){ simplex[worstIdx] = xc; vals[worstIdx] = fxc }
          else {
            for (let k = 0; k <= n; k++){
              if (k === bestIdx) continue
              simplex[k] = simplex[bestIdx].map((bv,d) => bv + sigma * (simplex[k][d] - bv))
              vals[k] = f(simplex[k])
            }
          }
        }
      }
      // check convergence by std dev of vals
      const meanVal = vals.reduce((s,v)=>s+v,0)/(vals.length)
      const sd = Math.sqrt(vals.reduce((s,v)=>s+Math.pow(v-meanVal,2),0)/vals.length)
      if (sd < tol) break
    }
    // return best point
    let bestI = 0; for (let i = 1; i < vals.length; i++) if (vals[i] < vals[bestI]) bestI = i
    return { x: simplex[bestI], fx: vals[bestI] }
  }

  const start = [best2[1], best2[2]]
  try{
    const res = nelderMeadOptimize(_obj_xy, start, { maxIter: 120, tol: 1e-9, scale: 0.1 })
    const aOpt = Math.max(0.01, res.x[0])
    const bOpt = Math.max(0.01, res.x[1])
    return [aOpt, bOpt]
  }catch(e){
    return [best2[1], best2[2]]
  }
}

// Fit beta parameters to match exact discrete counts in a dataset of size n.
// This uses the cached sampled mapping to evaluate how many mapped values
// fall into the A range (>=0.9) and F range (<0.6) and minimizes squared
// error on counts. Returns [a,b].
export function fitBetaToCounts(A_pct, F_pct, n, mean_target = null, seed = null, samples = 10001){
  // use fractional desired counts (not rounded) so small percentage changes
  // affect the objective even when integer rounding would be constant
  const desiredA = (A_pct / 100.0) * n
  const desiredF = (F_pct / 100.0) * n
  const desiredF_frac = (F_pct / 100.0)
  // Compute a simple lower bound on achievable mean (%) when exactly
  // `desiredF_frac` of mass must map below 60%: in the extreme case the
  // F mass is at 0 and the rest at 60, giving mean_min = 60*(1 - desiredF_frac).
  // If the user asks for a mean below this, it's infeasible; we'll use an
  // effective mean in the objective to avoid feedback loops.
  const minPossibleMeanPercent = 60.0 * (1.0 - desiredF_frac)
  // build percentile array for dataset
  const pArr = new Array(n)
  for (let i = 0; i < n; i++) pArr[i] = (i + 1) / (n + 1)

  // objective: squared error on discrete counts (and optional mean penalty)
  function obj_ab(ab){
    const a = Math.max(0.01, ab[0])
    const b = Math.max(0.01, ab[1])
    const mapped = mapPercentilesToBeta(a, b, pArr, samples)
    let cntA = 0, cntF = 0
    let meanMapped = 0
    for (let i = 0; i < mapped.length; i++){
      const v = mapped[i]
      if (v >= 0.9) cntA++
      if (v < 0.6) cntF++
      meanMapped += v
    }
    meanMapped = (meanMapped / mapped.length) * 100
    // discrete-count squared error (using fractional targets)
    let err = Math.pow(cntA - desiredA, 2) + Math.pow(cntF - desiredF, 2)
    // small continuous-CDF penalty at the thresholds to make the
    // objective sensitive to small percentage/mean edits that don't
    // immediately change integer counts.
    const target_cdf_90 = 1.0 - (A_pct / 100.0)
    const target_cdf_60 = (F_pct / 100.0)
    const c90 = betaCdfNumeric(0.9, a, b, 400)
    const c60 = betaCdfNumeric(0.6, a, b, 400)
    const cdfPenalty = 0.1 * ((c90 - target_cdf_90) * (c90 - target_cdf_90) + (c60 - target_cdf_60) * (c60 - target_cdf_60))
    err += cdfPenalty
    if (mean_target !== null && mean_target !== undefined){
      // If the requested mean is infeasible given the F% constraint,
      // use an effective mean equal to the feasible lower bound to avoid
      // optimizer feedback where pushing mean below feasible causes more
      // points to be assigned to F and destabilizes the fit.
      const effectiveMean = Math.max(mean_target, minPossibleMeanPercent)
      if (effectiveMean !== mean_target){
        // optional: provide a console warning to help debugging in dev
        if (typeof console !== 'undefined' && console.warn){
          console.warn(`fitBetaToCounts: requested mean ${mean_target} < feasible minimum ${minPossibleMeanPercent.toFixed(3)} given F%=${F_pct}; using ${effectiveMean.toFixed(3)} as target.`)
        }
      }
      const mErr = (meanMapped - effectiveMean)
      // stronger mean penalty to encourage satisfying mean when feasible
      err += 0.2 * mErr * mErr
    }
    return err
  }

  // initial guess: try seeded values, or fall back to continuous fit
  let init = null
  if (seed && seed.a && seed.b){ init = [Math.max(0.01, seed.a), Math.max(0.01, seed.b)] }
  if (!init){
    try{ const [a0,b0] = fitBetaFromConstraints(A_pct, F_pct, mean_target); init = [a0, b0] }catch(e){ init = [2,5] }
  }

  // small Nelder-Mead optimizer (reused from fitBetaFromConstraints)
  function nelder(f, x0, opts = {}){
    const maxIter = opts.maxIter || 80
    const tol = opts.tol || 1e-6
    const alpha = 1, gamma = 2, rho = 0.5, sigma = 0.5
    const nDim = x0.length
    const scale = opts.scale || 0.2
    const simplex = [x0.slice()]
    for (let i = 0; i < nDim; i++){
      const xi = x0.slice(); xi[i] = xi[i] * (1 + scale); if (xi[i] === x0[i]) xi[i] = x0[i] + scale; simplex.push(xi)
    }
    const vals = simplex.map(s => f(s))
    for (let iter = 0; iter < maxIter; iter++){
      const order = vals.map((v,i)=>[v,i]).sort((a,b)=>a[0]-b[0]).map(x=>x[1])
      const best = order[0], worst = order[nDim], second = order[nDim-1]
      const centroid = new Array(nDim).fill(0)
      for (let k = 0; k <= nDim; k++){ if (k === worst) continue; for (let d=0; d<nDim; d++) centroid[d] += simplex[k][d] }
      for (let d=0; d<nDim; d++) centroid[d] /= nDim
      const xr = centroid.map((c,d) => c + alpha * (c - simplex[worst][d]))
      const fxr = f(xr)
      if (fxr < vals[best]){
        const xe = centroid.map((c,d) => c + gamma * (xr[d] - c)); const fxe = f(xe)
        if (fxe < fxr){ simplex[worst] = xe; vals[worst] = fxe } else { simplex[worst] = xr; vals[worst] = fxr }
      } else if (fxr < vals[second]){ simplex[worst] = xr; vals[worst] = fxr }
      else {
        const xc = centroid.map((c,d) => c + rho * (simplex[worst][d] - c)); const fxc = f(xc)
        if (fxc < vals[worst]){ simplex[worst] = xc; vals[worst] = fxc }
        else {
          for (let k=0;k<=nDim;k++){ if (k===order[0]) continue; simplex[k] = simplex[order[0]].map((bv,d)=> bv + sigma * (simplex[k][d] - bv)); vals[k] = f(simplex[k]) }
        }
      }
      const meanVal = vals.reduce((s,v)=>s+v,0)/vals.length
      const sd = Math.sqrt(vals.reduce((s,v)=>s+Math.pow(v-meanVal,2),0)/vals.length)
      if (sd < tol) break
    }
    let bi = 0; for (let i=1;i<vals.length;i++) if (vals[i] < vals[bi]) bi = i
    return { x: simplex[bi], fx: vals[bi] }
  }

  try{
    const res = nelder(obj_ab, init, { maxIter: 120, tol: 1e-6, scale: 0.2 })
    return [Math.max(0.01, res.x[0]), Math.max(0.01, res.x[1])]
  }catch(e){
    return init
  }
}

export function invNorm(p){
  if (p <= 0) return -Infinity
  if (p >= 1) return Infinity
  const a1 = -39.6968302866538
  const a2 = 220.946098424521
  const a3 = -275.928510446969
  const a4 = 138.357751867269
  const a5 = -30.6647980661472
  const a6 = 2.50662827745924
  const b1 = -54.4760987982241
  const b2 = 161.585836858041
  const b3 = -155.698979859887
  const b4 = 66.8013118877197
  const b5 = -13.2806815528857
  const c1 = -0.00778489400243029
  const c2 = -0.322396458041136
  const c3 = -2.40075827716184
  const c4 = -2.54973253934373
  const c5 = 4.37466414146497
  const c6 = 2.93816398269878
  const d1 = 0.00778469570904146
  const d2 = 0.32246712907004
  const d3 = 2.445134137143
  const d4 = 3.75440866190742
  const p_low = 0.02425
  const p_high = 1 - p_low
  let q, r
  if (p < p_low){
    q = Math.sqrt(-2 * Math.log(p))
    return (((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / ((((d1 * q + d2) * q + d3) * q + d4) * q + 1)
  }
  if (p <= p_high){
    q = p - 0.5
    r = q * q
    return (((((a1 * r + a2) * r + a3) * r + a4) * r + a5) * r + a6) * q / (((((b1 * r + b2) * r + b3) * r + b4) * r + b5) * r + 1)
  }
  q = Math.sqrt(-2 * Math.log(1 - p))
  return -(((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / ((((d1 * q + d2) * q + d3) * q + d4) * q + 1)
}

export function kdeGaussian(samples, xs, bandwidth=0.08){
  if (!samples || samples.length === 0) return xs.map(()=>0)
  const n = samples.length
  const dens = xs.map(x=>0)
  for (let i=0;i<xs.length;i++){
    let s = 0
    for (let j=0;j<n;j++){
      const z = (xs[i] - samples[j])
      s += Math.exp(-0.5 * (z*z) / (bandwidth*bandwidth)) / (Math.sqrt(2*Math.PI) * bandwidth)
    }
    dens[i] = s / n
  }
  return dens
}

export function linearShift(values, shift){
  return values.map(v => Math.min(100, Math.max(0, v + shift)))
}
