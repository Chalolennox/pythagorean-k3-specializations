#!/usr/bin/env python3
"""Test the conjectural 2-adic Kummer lattice H* (numerical) against pr92_kummer_lattice_scan.py data.

Hypothesis H* (Lambda' = {v in T_2 J = Z_2^2 : v mod 2 in <T>}, index 2; T = (0,0)):
  H* = { (h_P ; x_1,y_1 ; x_2,y_2 ; x_3,y_3) in (T_2 J)^7 :  h_P in 4 Lambda',  x_i in Lambda',  y_i - x_i in 2 T_2 J,
         t(x_1) + t(x_2) + t(x_3) = 0 }   where t: Lambda'/2 T_2 J = F_2.
Coordinates: P, then U_1..U_6 with (U_1,U_2), (U_3,U_4), (U_5,U_6) the pairs {x, 2-x}.  Index of H* in Z_2^14 is 2^15.
Predicted fraction of K-split primes with J[2^k] rational (given m_p >= k+shift) for which the following lie in 2^k J(F_p):
  single U_j                      2^-(2k-1)
  partner sum / difference        4^-(k-1)
  non-partner sum / difference    2^-(2k-1)
  both U_a, U_b of a partner pair 2^-(4k-3)
  two different pairs             2^-(4k-2)
  one representative from each of the three pairs   2^-(6k-4)
  all six                         2^-(12k-10)
Usage: pr92_kummer_lattice_model.py scan.tsv [shift]
"""
import sys, math, itertools
sys.path.insert(0, __import__("os").path.dirname(__file__))
from pr92_kummer_lattice_analysis import load

rows = load(sys.argv[1]); shift = int(sys.argv[2]) if len(sys.argv) > 2 else 0
pairs = list(itertools.combinations(range(6), 2))
part = [i for i, ab in enumerate(pairs) if ab in ((0, 1), (2, 3), (4, 5))]
non = [i for i in range(15) if i not in part]

def line(name, k, count_fn, pred):
    sub = [r for r in rows if r["m"] >= k + shift]
    n_tot = 0; c = 0
    for r in sub:
        cc, nn = count_fn(r, k)
        c += cc; n_tot += nn
    if n_tot == 0: return None
    f = c / n_tot; se = math.sqrt(max(pred * (1 - pred), 1e-12) / n_tot)
    z = (f - pred) / se
    return "  k=%d  %-34s %7d/%-7d obs %.5f  pred %.5f  z=%+5.2f" % (k, name, c, n_tot, f, pred, z)

tests = [
    ("single U_j (6 pooled)", lambda r, k: (sum(1 for j in range(6) if r["d"][1 + j] >= k), 6), lambda k: 2.0 ** -(2 * k - 1)),
    ("partner sum U_a+U_b", lambda r, k: (sum(1 for i in part if r["ps"][i] >= k), 3), lambda k: 4.0 ** -(k - 1)),
    ("partner difference U_a-U_b", lambda r, k: (sum(1 for i in part if r["pd"][i] >= k), 3), lambda k: 4.0 ** -(k - 1)),
    ("non-partner sum", lambda r, k: (sum(1 for i in non if r["ps"][i] >= k), 12), lambda k: 2.0 ** -(2 * k - 1)),
    ("non-partner difference", lambda r, k: (sum(1 for i in non if r["pd"][i] >= k), 12), lambda k: 2.0 ** -(2 * k - 1)),
    ("P +- U_j (12 pooled)", lambda r, k: (sum(1 for j in range(6) if r["us"][j] >= k) + sum(1 for j in range(6) if r["ud"][j] >= k), 12), lambda k: 2.0 ** -(2 * k - 1)),
    ("both of a partner pair (3 pairs)", lambda r, k: (sum(1 for a in (1, 3, 5) if r["d"][a] >= k and r["d"][a + 1] >= k), 3), lambda k: 2.0 ** -(4 * k - 3)),
    ("two different pairs (12 combos)", lambda r, k: (sum(1 for a in (1, 2) for b in (3, 4) if r["d"][a] >= k and r["d"][b] >= k) + sum(1 for a in (1, 2) for b in (5, 6) if r["d"][a] >= k and r["d"][b] >= k) + sum(1 for a in (3, 4) for b in (5, 6) if r["d"][a] >= k and r["d"][b] >= k), 12), lambda k: 2.0 ** -(4 * k - 2)),
    ("one rep. from each pair (8 combos)", lambda r, k: (sum(1 for a in (1, 2) for b in (3, 4) for c in (5, 6) if r["d"][a] >= k and r["d"][b] >= k and r["d"][c] >= k), 8), lambda k: 2.0 ** -(6 * k - 4)),
    ("all six U_j", lambda r, k: (1 if all(d >= k for d in r["d"][1:]) else 0, 1), lambda k: 2.0 ** -(12 * k - 10)),
]
print("conditioning on m_p >= k + %d;  %d K-split primes" % (shift, len(rows)))
worst = 0
for k in (1, 2, 3, 4):
    for name, fn, pr in tests:
        s = line(name, k, fn, pr(k))
        if s: print(s)
    print()
# alternative couplings for the one-representative-per-pair statistic at k=2 (p-values in the printed lines above)
print("one representative from each pair at k=2: H* predicts 2^-8 = %.5f; independent U_j would give 2^-9 = %.5f; a coupling mod 4 (x_3 forced by x_1, x_2) would give 2^-6 = %.5f" % (2.0 ** -8, 2.0 ** -9, 2.0 ** -6))
print("note: at shift 0 the k=1 rows use primes with m_p = 1, where the extra class (1+i) is not yet trivial (rank 3); use shift 1 for the k=1 triple rows.")
