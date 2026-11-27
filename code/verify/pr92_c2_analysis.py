#!/usr/bin/env python3
"""Analysis of the output of pr92_c2_estimator.py: slope ratio C_2, block standard errors, check of the uniform-odd-part hypothesis, and breakdown by Frobenius class.  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Numerical evidence only; no claim about Problem H.
Usage: python3 -I code/verify/pr92_c2_analysis.py notes/data/pr92_c2_estimator.tsv [lo] [blocks]      (lo = smallest p included in the slope, default 30000)
"""
import gzip
import math
import sys
from collections import defaultdict

fn = sys.argv[1]
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
NB = int(sys.argv[3]) if len(sys.argv) > 3 else 20
rows = []
und = 0
for l in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
    t = l.split()
    p, N, nu, al, be, vP, ne, n2 = map(int, t[:8])
    sw = float(t[8])
    d, h = int(t[9]), int(t[10])
    if N < 0:
        und += 1
        continue
    rows.append((p, N, nu, al, be, vP, ne, n2, sw, d, h))
rows.sort()
print("%d primes with non-empty D_p^+ (undetermined group order: %d), largest p = %d" % (len(rows), und, rows[-1][0]))


def ratio(sel):
    num = sum(r[8] / r[1] for r in sel)
    den = sum(r[6] / r[1] for r in sel)
    return num / den if den else float("nan"), num, den


def blocks(sel, nb):
    k = len(sel) // nb
    out = []
    for i in range(nb):
        s = sel[i * k:(i + 1) * k]
        out.append(ratio(s)[0])
    m = sum(out) / len(out)
    sd = math.sqrt(sum((x - m) ** 2 for x in out) / (len(out) - 1))
    return m, sd / math.sqrt(len(out))


sel = [r for r in rows if r[0] >= LO]
c, num, den = ratio(sel)
m, se = blocks(sel, NB)
print("\nC_2 estimate (sum w/N)/(sum |D+|/N) over p >= %d: %.4f  (block mean %.4f +- %.4f from %d blocks)" % (LO, c, m, se, NB))
print("by range:")
edges = [30000, 100000, 300000, 1000000, 3000000, 10000001]
for a, b in zip(edges, edges[1:]):
    s = [r for r in rows if a <= r[0] < b]
    if len(s) > 40:
        cc = ratio(s)[0]
        mm, ss = blocks(s, 10)
        print("   %8d <= p < %8d: %6d primes, C_2 = %.4f (block se %.4f)" % (a, b, len(s), cc, ss))

# uniform odd part check
full = [r for r in rows if r[10] >= 0 and r[9] > 0]
if full:
    dif = [r[10] / r[9] - r[8] / r[1] for r in full]
    mu = sum(dif) / len(dif)
    sd = math.sqrt(sum((x - mu) ** 2 for x in dif) / (len(dif) - 1))
    sA = sum(r[10] / r[9] for r in full)
    sR = sum(r[8] / r[1] for r in full)
    sD = sum(r[6] / r[1] for r in full)
    print("\nuniform-odd-part check on %d primes (p <= %d): sum a_p/d_p = %.4f, sum RB = %.4f, difference %.4f +- %.4f (paired standard error); ratios: full %.3f, RB %.3f (including small p)" % (len(full), full[-1][0], sA, sR, sA - sR, sd * math.sqrt(len(dif)), sA / sD, sR / sD))
    f2 = [r for r in full if r[0] >= LO]
    print("   restricted to p >= %d (%d primes): full %.4f, RB %.4f" % (LO, len(f2), sum(r[10] / r[9] for r in f2) / sum(r[6] / r[1] for r in f2), sum(r[8] / r[1] for r in f2) / sum(r[6] / r[1] for r in f2)))

# breakdown
print("\nbreakdown by p mod 8 (weights 1/N): share of sum|D+|/N, mean w per eligible point, C_2 contribution")
tot = sum(r[6] / r[1] for r in sel)
for k in (1, 3, 5, 7):
    s = [r for r in sel if r[0] % 8 == k]
    d_ = sum(r[6] / r[1] for r in s)
    n_ = sum(r[8] / r[1] for r in s)
    n2 = sum(r[7] for r in s)
    ne = sum(r[6] for r in s)
    print("   p = %d mod 8: %6d primes, share of denominator %.3f, C_2 within class %.4f, fraction of eligible points with Q_2 in <P_2>: %.4f" % (k, len(s), d_ / tot, n_ / d_, n2 / ne))
print("\nbreakdown for p = 1 mod 8 by (alpha, beta, vP): count of eligible points, fraction with Q_2 in <P_2>, mean w")
cls = defaultdict(lambda: [0, 0, 0.0])
for r in sel:
    if r[0] % 8 == 1:
        key = (min(r[3], 4), min(r[4], 6), min(r[5], 6))
        c_ = cls[key]
        c_[0] += r[6]
        c_[1] += r[7]
        c_[2] += r[8]
for key in sorted(cls):
    c_ = cls[key]
    if c_[0] >= 150:
        print("   (alpha,beta,vP) = %-12s eligible points %6d, in <P_2>: %.3f, mean w %.3f" % (key, c_[0], c_[1] / c_[0], c_[2] / c_[0]))
print("DONE")
