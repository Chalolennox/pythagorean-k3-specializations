#!/usr/bin/env python3
"""Addendum 19: first-level structure in the K-split scan data.
For each prime of notes/data/pr92_kummer_lattice_scan{,_deep}.tsv.gz (p=1 mod 8, K-split) check
 (a) chi(x_j) = +1 for all six U_j (x_j = 2 mod K*^2 and 2 square);
 (b) partner classes chi(x-1-i) agree within the pairs (U1,U2),(U3,U4),(U5,U6);
 (c) the parity of the nonsquare bits over one member of each pair equals [chi(1+i) = -1]  (owner's certificate [b1b2b3]=[1+i]);
 (d) P has chi(x)=chi(x-1-i)=+1.
Usage: python3 -I pr92_first_level_scan_check.py DATA_DIR"""
import gzip, sys, os
def leg(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
def sqrtm1(p):
    g = 2
    while True:
        r = pow(g, (p - 1) // 4, p)
        if r * r % p == p - 1: return r
        g += 1
d = sys.argv[1]; tot = 0; bad = [0, 0, 0, 0]; seen = set()
for fn in ("pr92_kummer_lattice_scan.tsv.gz", "pr92_kummer_lattice_scan_deep.tsv.gz"):
    for line in gzip.open(os.path.join(d, fn), "rt"):
        if line.startswith("#"): continue
        f = line.rstrip("\n").split("\t"); p = int(f[0])
        if p in seen: continue
        seen.add(p); ch = [int(v) for v in f[7].split(",")]
        b0 = [c & 1 for c in ch]; b1 = [(c >> 1) & 1 for c in ch]; tot += 1
        if any(b0[1:]): bad[0] += 1
        if not (b1[1] == b1[2] and b1[3] == b1[4] and b1[5] == b1[6]): bad[1] += 1
        i = sqrtm1(p); c1 = 0 if leg(1 + i, p) == 1 else 1
        if (b1[1] + b1[3] + b1[5]) % 2 != c1: bad[2] += 1
        if b0[0] or b1[0]: bad[3] += 1
print("distinct K-split primes p=1 mod 8 in the two scan files: %d" % tot)
print("violations: (a) chi(x_j)=-1: %d; (b) partner mismatch: %d; (c) coupling vs chi(1+i): %d; (d) P class nontrivial: %d" % tuple(bad))
