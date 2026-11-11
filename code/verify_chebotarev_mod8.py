#!/usr/bin/env python3
"""Checks of the deterministic claims of 'A Chebotarev density calculation for y^2 = x^3 - 2x^2 + 2x' (independent-review draft, 11 Nov 2026) on every prime p = 7 (mod 8).
 f(X) = X^8 - 40X^6 + 128X^5 - 232X^4 + 256X^3 - 160X^2 + 16.  For p = 7 (mod 8), N = #C(F_p), r = v_2(N), e = v_2(ord of P = (1,1) mod p):
   (A) f mod p has cycle type 1^4 2^2 or 4^2 (Section 4)                       (B) f has a root mod p  <=>  8 | N (Section 5)
   (C) P is in 2C(F_p) (Addendum A):  e <= r-1                                   (D) Theorem B:  8 | N  <=>  P in 4C(F_p)  (e <= r-2)
   (E) Addendum C: the level-16 analogue fails (p = 31), and the census tables for p <= 10^5 (2x2 table, r-distribution, odd-order counts).
Usage: python3 code/verify_chebotarev_mod8.py [LIMIT]  (default 300000).  Needs sympy.  Exit 0 = all pass."""
import sys, os, collections, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index_four'))
from sympy import symbols, Poly, primerange, factorint, discriminant
from curve import group_order, point_order, mul, add
X = symbols('X'); f = X**8 - 40*X**6 + 128*X**5 - 232*X**4 + 256*X**3 - 160*X**2 + 16
ramified = set(factorint(int(discriminant(f, X))))
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
v2 = lambda n: (n & -n).bit_length() - 1
rows = []; types = collections.Counter(); bad = collections.Counter()
for p in primerange(7, LIMIT):
    if p % 8 != 7 or p in ramified: continue
    N = group_order(p); assert len(N) == 1, (p, N); N = N[0]; o = point_order((1, 1), N, p); r, e = v2(N), v2(o)
    degs = tuple(sorted(g.degree() for g, m in Poly(f, X, modulus=p).factor_list()[1] for _ in range(m)))
    types[degs] += 1; hasroot = 1 in degs
    if degs not in ((1, 1, 1, 1, 2, 2), (4, 4)): bad['A'] += 1
    if hasroot != (r >= 3): bad['B'] += 1
    if not e <= r - 1: bad['C'] += 1
    if (r >= 3) != (e <= r - 2): bad['D'] += 1
    rows.append((p, N, r, e))
print("primes p = 7 mod 8, p < %d (unramified; ramified set of f: %s): %d" % (LIMIT, sorted(ramified), len(rows)))
print("cycle types of f mod p:", dict(types))
for k, name in (('A', "cycle type is 1^4 2^2 or 4^2"), ('B', "f has a root mod p  <=>  8 | #C(F_p)"), ('C', "P in 2C(F_p) for every such p (e <= r-1)"), ('D', "Theorem B: 8 | #C(F_p)  <=>  P in 4C(F_p)")):
    print("%-4s %s: %s" % ("OK" if bad[k] == 0 else "FAIL", name, "no exception" if bad[k] == 0 else "%d exceptions" % bad[k]))
r8 = sum(1 for _, _, r, _ in rows if r >= 3); print("fraction of p = 7 mod 8 with 8 | N: %d/%d = %.5f (claimed conditional density 1/2)" % (r8, len(rows), r8/len(rows)))
# Addendum C: p = 31 and the 2x2 table for p <= 10^5;  Addendum D: r-distribution and odd order
N31 = group_order(31)[0]; P2 = mul(2, (1, 1), 31); P4 = mul(4, (1, 1), 31); P8 = mul(8, (1, 1), 31)
print("p = 31: #C = %d, 2P = %s, 4P = %s, 8P = %s  (Addendum C: 32, (8,11), (0,0), O)  %s" % (N31, P2, P4, P8, "OK" if (N31, P2, P4, P8) == (32, (8, 11), (0, 0), None) else "MISMATCH"))
sub = [(p, N, r, e) for p, N, r, e in rows if p <= 100000]
tab = collections.Counter((r >= 4, e <= r - 3) for p, N, r, e in sub)
print("p <= 10^5, p = 7 mod 8: %d primes; table [16 | N] x [P in 8C]:  (16|N, P in 8C) %d, (16|N, not) %d, (16 not|N, P in 8C) %d, (16 not|N, not) %d   (Addendum C: 301, 294, 307, 1497)" %
      (len(sub), tab[(True, True)], tab[(True, False)], tab[(False, True)], tab[(False, False)]))
dist = collections.Counter(r for _, _, r, _ in sub); odd = collections.Counter(r for _, _, r, e in sub if e == 0)
print("r : number of primes / odd-order  =", {r: (dist[r], odd[r]) for r in sorted(dist)}, " total odd:", sum(odd.values()), "(Addendum D: 412 of 2399)")

# Addendum D, separate conjecture Pr(P in 2^j C | p = 7 mod 8) = 2^-(j-1):  P in 2^j C  <=>  e <= max(r - j, 0)  (cyclic 2-Sylow of order 2^r; odd order P lies in every 2^j C).  If P has odd order it lies in every 2^j C, so Pr >= Pr(odd order).
freq = {j: sum(1 for _, _, r, e in rows if e <= max(r - j, 0))/len(rows) for j in range(1, 7)}
print("fraction of p = 7 mod 8 with P in 2^j C(F_p), j = 1..6:", {j: round(v, 4) for j, v in freq.items()}, " fraction with P of odd order: %.4f" % (sum(1 for _, _, r, e in rows if e == 0)/len(rows)))
print("   conjecture 2^-(j-1) gives 1, 0.5, 0.25, 0.125, 0.0625, 0.03125; the image gives 1, 1/2, 1/4, 3/16 = 0.1875, 11/64 = 0.1719 for j = 1..5 (see image_densities.py)")
assert freq[4] > 0.15 and freq[5] > 0.15, "the conjecture 2^-(j-1) would predict 0.125 and 0.0625"
print("ALL DETERMINISTIC CLAIMS HOLD" if not bad else "SOME CLAIM FAILS"); sys.exit(0 if not bad else 1)
