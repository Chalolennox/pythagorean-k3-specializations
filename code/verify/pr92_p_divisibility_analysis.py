#!/usr/bin/env python3
"""Analyse the output of pr92_p_divisibility_scan.py.

Prediction H(P): P = 4R' with R' in J(T_16) and the Kummer image of R' is full, i.e.
Prob(P in 2^k J(F_p) | J[2^m] in J(F_p)) = 4^-(k-2) for 2 <= k <= m.  We report the data against
this and against the alternatives that the image at level 8 has order 1 or 2.
"""
import sys, math, re
tsv, outtxt = sys.argv[1], sys.argv[2]
total = None
for line in open(outtxt):
    mo = re.match(r"primes p=1 mod 8 in \[(\d+),(\d+)\): (\d+)", line)
    if mo: total = int(mo.group(3)); lo, hi = int(mo.group(1)), int(mo.group(2))
import gzip
rows = []
for line in (gzip.open(tsv, "rt") if tsv.endswith(".gz") else open(tsv)):
    if line.startswith("#"): continue
    p, m, d = map(int, line.split()); rows.append((p, m, min(d, m)))
print("primes p = 1 mod 8 in [%d, %d): %d" % (lo, hi, total))
print("\nTorsion splitting level m_p (J[2^m] in J(F_p)); fraction of primes p=1 mod 8, ratio to previous level")
prev = None
for m in range(3, 12):
    n = sum(1 for r in rows if r[1] >= m)
    if n == 0: break
    f = n / total
    print("  m>=%d: %9d   %.4e   %s" % (m, n, f, ("ratio %.2f" % (prev / f)) if prev else ""))
    prev = f
print("\nDivisibility of P: observed fraction with P in 2^k J(F_p) among primes with m_p >= m, versus 4^-(k-2)")
print("  (z = (obs-pred)/sd, binomial; the rate 1/2^(k-2) and 1 are shown for comparison at k=3)")
print("   m  k   count/total   obs     pred    z      z_if_pred=1/2   z_if_pred=1")
worst = 0
for m in range(3, 9):
    sub = [r for r in rows if r[1] >= m]
    n = len(sub)
    if n < 5: continue
    for k in range(3, m + 1):
        c = sum(1 for r in sub if min(r[2], m) >= k)
        pred = 4.0 ** (-(k - 2))
        z = (c - n * pred) / math.sqrt(n * pred * (1 - pred))
        extra = ""
        if k == 3:
            z2 = (c - n * 0.5) / math.sqrt(n * 0.25)
            extra = "   %8.1f        (pred=1 impossible if c<n)" % z2
        pred2 = 2.0 * pred
        z3 = (c - n * pred2) / math.sqrt(n * pred2 * (1 - pred2))
        if m <= 5: worst = max(worst, abs(z))
        else: worst = max(worst, abs(z3))
        print("  %2d  %d  %6d/%-6d  %.4f  %.4f  %+5.2f   [alt 2^-(2k-5)=%.4f: z=%+5.2f]%s" % (m, k, c, n, c / n, pred, z, pred2, z3, extra))
print("\nlargest |z| using 4^-(k-2) for m<=5 and 2^-(2k-5) for m>=6: %.2f" % worst)
print("\nAlways P in 4J(F_p) when m_p >= 3: %s" % all(r[2] >= 2 for r in rows))
