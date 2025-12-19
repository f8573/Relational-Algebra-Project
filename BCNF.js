const Rel = ["P","E","N","R","T","K","H","D","M"];

const FDs = {
  "E": ["N","R","D"],
  "T": ["K"],
  "D": ["M"],
  "P,E,T": ["H"]
};

// ---------- Normalize FDs into [{lhs:Set, rhs:Set, lhsArr, rhsArr, keyStr}, ...]
const rules = Object.entries(FDs).map(([lhs, rhs]) => {
  const lhsArr = lhs.split(",").map(s => s.trim()).filter(Boolean);
  const rhsArr = rhs.slice();
  return {
    lhs: new Set(lhsArr),
    rhs: new Set(rhsArr),
    lhsArr,
    rhsArr,
    keyStr: `${lhsArr.slice().sort().join(",")}->${rhsArr.slice().sort().join(",")}`
  };
});

// ---------- Set helpers
function isSubset(a, b) { // a ⊆ b ?
  for (const x of a) if (!b.has(x)) return false;
  return true;
}
function unionSet(a, b) {
  const s = new Set(a);
  for (const x of b) s.add(x);
  return s;
}
function setsEqual(a, b) {
  if (a.size !== b.size) return false;
  for (const x of a) if (!b.has(x)) return false;
  return true;
}
function intersectSize(a, b) {
  let cnt = 0;
  for (const x of a) if (b.has(x)) cnt++;
  return cnt;
}

// ---------- Closure
function closure(attrs, rules) {
  const res = new Set(attrs);
  let changed = true;
  while (changed) {
    changed = false;
    for (const { lhs, rhs } of rules) {
      if (isSubset(lhs, res)) {
        for (const y of rhs) {
          if (!res.has(y)) {
            res.add(y);
            changed = true;
          }
        }
      }
    }
  }
  return res;
}

// ---------- BCNF Decompose (order-sensitive: picks first violating FD in `allRules` order)
function projectRulesToRelation(relSet, orderedRules) {
  // Keep only rules whose lhs and rhs are fully inside the relation
  return orderedRules.filter(r =>
    isSubset(r.lhs, relSet) && [...r.rhs].every(x => relSet.has(x))
  );
}

function decompose(relArr, violation) {
  const { lhsArr, rhsArr } = violation;

  // R1 = X ∪ Y
  const r1Set = new Set([...lhsArr, ...rhsArr]);

  // R2 = R - (Y - X)  (keep X, remove RHS attrs not in LHS)
  const lhsSet = new Set(lhsArr);
  const rhsSet = new Set(rhsArr);
  const r2 = relArr.filter(a => !rhsSet.has(a) || lhsSet.has(a));

  return [[...r1Set], r2];
}

function bcnfDecompose(initialRel, orderedRules) {
  const result = [];
  const queue = [initialRel.slice()];

  while (queue.length) {
    const rel = queue.shift();
    const Rset = new Set(rel);

    const projected = projectRulesToRelation(Rset, orderedRules);

    let found = null;
    for (const r of projected) {
      const cl = closure(r.lhsArr, projected);
      if (!setsEqual(cl, Rset)) {
        found = r; // first violating FD in this order
        break;
      }
    }

    if (!found) {
      result.push(rel);
    } else {
      const [r1, r2] = decompose(rel, found);
      queue.push(r1, r2);
    }
  }

  return result;
}

// ---------- Canonicalize a decomposition (so we can dedupe outcomes)
function canonicalizeDecomp(decomp) {
  // sort attrs inside each relation; sort relations lexicographically
  const rels = decomp.map(r => [...new Set(r)].sort());
  rels.sort((a, b) => {
    const sa = a.join(",");
    const sb = b.join(",");
    return sa < sb ? -1 : sa > sb ? 1 : 0;
  });
  return rels;
}
function signatureOfDecomp(decomp) {
  const canon = canonicalizeDecomp(decomp);
  return canon.map(r => `{${r.join(",")}}`).join(" | ");
}

// ---------- Candidate keys (brute force, fine for <= 12-15 attrs)
function candidateKeys(allAttrsArr, allRules) {
  const allSet = new Set(allAttrsArr);
  const n = allAttrsArr.length;
  const keys = [];

  // Enumerate subsets by increasing size
  for (let k = 1; k <= n; k++) {
    const idx = Array.from({ length: k }, (_, i) => i);

    while (true) {
      const subset = idx.map(i => allAttrsArr[i]);
      const cl = closure(subset, allRules);
      if (setsEqual(cl, allSet)) {
        // minimality check: no existing key is subset of this
        const subsetSet = new Set(subset);
        let minimal = true;
        for (const key of keys) {
          if (isSubset(key, subsetSet)) { minimal = false; break; }
        }
        if (minimal) keys.push(subsetSet);
      }

      // next combination
      let i = k - 1;
      while (i >= 0 && idx[i] === i + (n - k)) i--;
      if (i < 0) break;
      idx[i]++;
      for (let j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
    }

    // early stop: if we found keys of size k, no need to search larger for minimal keys
    if (keys.length) break;
  }

  return keys;
}

// ---------- Scoring heuristic (lower is better)
function scoreDecomposition(decomp, orderedRules, allRules, allAttrsArr, candKeys) {
  const canon = canonicalizeDecomp(decomp);
  const relSets = canon.map(r => new Set(r));

  // H1: FD locality / preservation: each original FD X∪Y must appear in some relation
  let missingFDs = 0;
  for (const r of allRules) {
    const need = new Set([...r.lhsArr, ...r.rhsArr]);
    const ok = relSets.some(S => isSubset(need, S));
    if (!ok) missingFDs++;
  }

  // H3: pairwise overlap score
  let overlap = 0;
  for (let i = 0; i < relSets.length; i++) {
    for (let j = i + 1; j < relSets.length; j++) {
      overlap += intersectSize(relSets[i], relSets[j]);
    }
  }

  // Total attribute duplication (how many “extra” attribute appearances beyond |Rel|)
  const totalAttrsAcross = canon.reduce((sum, r) => sum + r.length, 0);
  const duplication = totalAttrsAcross - allAttrsArr.length;

  // Key replication: how many relations contain (at least one) candidate key
  let keyCopies = 0;
  for (const S of relSets) {
    if (candKeys.some(K => isSubset(K, S))) keyCopies++;
  }

  // Weighted score: make missingFDs dominate (you can tweak weights)
  return (
    missingFDs * 1_000_000 + // preserve if possible
    overlap * 1_000 +
    duplication * 100 +
    keyCopies
  );
}

// ---------- Permutations (iterative Heap’s algorithm)
function* permutations(arr) {
  const a = arr.slice();
  const n = a.length;
  const c = new Array(n).fill(0);
  yield a.slice();
  let i = 0;
  while (i < n) {
    if (c[i] < i) {
      const swapWith = i % 2 === 0 ? 0 : c[i];
      [a[i], a[swapWith]] = [a[swapWith], a[i]];
      yield a.slice();
      c[i]++;
      i = 0;
    } else {
      c[i] = 0;
      i++;
    }
  }
}

// ---------- Run all FD orderings
const allAttrsArr = Rel.slice();
const candKeys = candidateKeys(allAttrsArr, rules);

const indices = rules.map((_, i) => i);
const seen = new Map(); // signature -> {score, order, decomp}

let best = null;

for (const perm of permutations(indices)) {
  const orderedRules = perm.map(i => rules[i]);
  const decomp = bcnfDecompose(Rel, orderedRules);
  const sig = signatureOfDecomp(decomp);

  const sc = scoreDecomposition(decomp, orderedRules, rules, allAttrsArr, candKeys);

  const prev = seen.get(sig);
  if (!prev || sc < prev.score) {
    seen.set(sig, { score: sc, order: perm.slice(), decomp: canonicalizeDecomp(decomp) });
  }

  if (!best || sc < best.score) {
    best = { score: sc, order: perm.slice(), decomp: canonicalizeDecomp(decomp), sig };
  }
}

console.log("Unique decompositions found:", seen.size);
console.log("Best signature:", best.sig);
console.log("Best score:", best.score);
console.log("Best FD order:", best.order.map(i => rules[i].keyStr));
console.log("Best decomposition:", best.decomp);
