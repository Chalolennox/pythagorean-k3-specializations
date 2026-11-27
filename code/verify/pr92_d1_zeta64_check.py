#!/usr/bin/env python3
"""Check of the owner's exact identity sqrt(x(S)) in T_64, T_32(sqrt d1) = T_32(zeta_64)  (KUMMER_P_EXACT_INDEX_2026-11-27.md, step 4):
at every prime p with J[32] rational (m_p >= 5), d1 = x(S) is a square mod p at all 16 quarter points iff zeta_64 is in F_p, i.e. p = 1 mod 64.
Reads the P-divisibility scan (p, m_p, d_p) and recomputes the 16 quarter-point x-coordinates by x-only halving.
Usage: pr92_d1_zeta64_check.py pr92_p_divisibility_scan.tsv.gz"""
import sys, gzip, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pr92_p_divisibility_scan import make_ctx, halves
tab = collections.Counter(); bad = 0; n = 0
for line in (gzip.open(sys.argv[1], "rt") if sys.argv[1].endswith(".gz") else open(sys.argv[1])):
    if line.startswith("#"): continue
    p, m, d = map(int, line.split())
    if m < 5: continue
    ctx = make_ctx(p)
    xs = [x2 for x1 in halves(1, ctx) for x2 in halves(x1, ctx)]
    chi = {1 if pow(x, (p - 1) // 2, p) == 1 else -1 for x in xs}
    z64 = (p % 64 == 1)
    key = (m >= 6, z64, tuple(sorted(chi)))
    tab[key] += 1; n += 1
    if len(chi) != 1 or (chi == {1}) != z64: bad += 1
for k in sorted(tab): print("m_p>=6: %-5s  p=1 mod 64: %-5s  character of d1 over the 16 quarter points: %-8s  %d primes" % (k[0], k[1], list(k[2]), tab[k]))
print("primes with J[32] rational: %d;  violations of [d1 square at all 16 points] <=> [p = 1 mod 64]: %d" % (n, bad))
sys.exit(1 if bad else 0)
