#!/usr/bin/env python3
"""Pooled local-factor estimates with delta-method standard errors, from the output of pr92_c_local_factors.py.  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Numerical evidence only; no claim about Problem H.
Usage: python3 -I code/verify/pr92_c_local_analysis.py FILE [FILE ...]      (plain or .gz; several ranges are merged)
Columns of the input: p N nelig w_2 w_3 w_5 w_7 w_11 w_13 w_23 w_S  (sums over the eligible points at p).  Estimate = (sum w/N)/(sum nelig/N) over p >= LO; the standard error treats
40 consecutive blocks of primes as independent: se = sqrt(sum_b (n_b - R d_b)^2) / sum d.
"""
import gzip
import math
import sys

LS = ["2", "3", "5", "7", "11", "13", "23", "S"]
rows = []
for fn in sys.argv[1:]:
    for l in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        t = l.split()
        rows.append((int(t[0]), int(t[1]), int(t[2])) + tuple(float(x) for x in t[3:]))
rows.sort()
print("%d primes with non-empty D_p^+, largest p = %d" % (len(rows), rows[-1][0]))


def est(sel, col, nb=40):
    num = sum(r[col] / r[1] for r in sel)
    den = sum(r[2] / r[1] for r in sel)
    R = num / den
    k = len(sel) // nb
    bl = [(sum(r[col] / r[1] for r in sel[i * k:(i + 1) * k]), sum(r[2] / r[1] for r in sel[i * k:(i + 1) * k])) for i in range(nb)]
    return R, math.sqrt(sum((n - R * d) ** 2 for n, d in bl)) / den


for lo in (30000, 1000000, 10000000):
    sel = [r for r in rows if r[0] >= lo]
    if len(sel) < 400:
        continue
    print("\np >= %d (%d primes):  l: estimate +- se (z from 1)" % (lo, len(sel)))
    prod, var = 1.0, 0.0
    vals = {}
    for k, l in enumerate(LS):
        R, se = est(sel, 3 + k)
        vals[l] = (R, se)
        print("   C_%-2s = %.4f +- %.4f  (z = %+.1f)" % (l, R, se, (R - 1) / se))
    # product of the individual factors for l in {2,3,5,7,11,13,23}
    p_ = 1.0
    v_ = 0.0
    for l in LS[:-1]:
        p_ *= vals[l][0]
        v_ += (vals[l][1] / vals[l][0]) ** 2
    print("   product of the seven individual factors = %.4f (se about %.4f, ignoring covariances); joint factor C_S = %.4f +- %.4f" % (p_, p_ * math.sqrt(v_), vals["S"][0], vals["S"][1]))
print("DONE")
