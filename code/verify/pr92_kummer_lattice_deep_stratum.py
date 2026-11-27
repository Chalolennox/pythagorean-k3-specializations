#!/usr/bin/env python3
"""Deep torsion stratum (m_p >= 4) of the Kummer-lattice scans: tests hypothesis H* of pr92_kummer_lattice_model.py.
Usage: pr92_kummer_lattice_deep_stratum.py scan.tsv scan_deep.tsv [MINM]   (rows with m_p >= MINM, default 4, from both files)."""
import sys, math, collections, itertools, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pr92_kummer_lattice_analysis import load
minm = int(sys.argv[3]) if len(sys.argv) > 3 else 4
a = [r for r in load(sys.argv[1]) if r['m'] >= minm]
b = [r for r in load(sys.argv[2]) if r['m'] >= minm]
rows = a + b
print("K-split primes with m_p >= %d: %d (first scan %d, deep scan %d); by m_p: %s" % (minm, len(rows), len(a), len(b), sorted(collections.Counter(min(r['m'], 8) for r in rows).items())))
part = [0, 9, 14]; non = [i for i in range(15) if i not in part]
def rep(name, k, cnt, tot, pred):
    f = cnt / tot; se = math.sqrt(pred * (1 - pred) / tot)
    z = (f - pred) / se if se > 0 else 0.0
    print("  k=%d %-30s %6d/%-7d %.5f  H* %.5f  z=%+5.2f" % (k, name, cnt, tot, f, pred, z))
n = len(rows)
for k in (1, 2, 3, 4):
    rep("single U_j", k, sum(1 for r in rows for j in range(6) if r['d'][1 + j] >= k), 6 * n, 2.0 ** -(2 * k - 1))
    rep("partner sum", k, sum(1 for r in rows for i in part if r['ps'][i] >= k), 3 * n, 4.0 ** -(k - 1))
    rep("partner difference", k, sum(1 for r in rows for i in part if r['pd'][i] >= k), 3 * n, 4.0 ** -(k - 1))
    rep("non-partner sum", k, sum(1 for r in rows for i in non if r['ps'][i] >= k), 12 * n, 2.0 ** -(2 * k - 1))
    rep("non-partner difference", k, sum(1 for r in rows for i in non if r['pd'][i] >= k), 12 * n, 2.0 ** -(2 * k - 1))
    rep("P +- U_j", k, sum(1 for r in rows for j in range(6) if r['us'][j] >= k) + sum(1 for r in rows for j in range(6) if r['ud'][j] >= k), 12 * n, 2.0 ** -(2 * k - 1))
    rep("both of a partner pair", k, sum(1 for r in rows for a_ in (1, 3, 5) if r['d'][a_] >= k and r['d'][a_ + 1] >= k), 3 * n, 2.0 ** -(4 * k - 3))
    rep("two different pairs (12)", k, sum(1 for r in rows for x in (1, 2) for y in (3, 4) if r['d'][x] >= k and r['d'][y] >= k) + sum(1 for r in rows for x in (1, 2) for y in (5, 6) if r['d'][x] >= k and r['d'][y] >= k) + sum(1 for r in rows for x in (3, 4) for y in (5, 6) if r['d'][x] >= k and r['d'][y] >= k), 12 * n, 2.0 ** -(4 * k - 2))
    rep("one rep from each pair (8)", k, sum(1 for r in rows for x in (1, 2) for y in (3, 4) for z in (5, 6) if r['d'][x] >= k and r['d'][y] >= k and r['d'][z] >= k), 8 * n, 2.0 ** -(6 * k - 4))
    print()
