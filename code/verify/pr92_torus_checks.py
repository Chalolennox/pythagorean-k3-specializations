#!/usr/bin/env python3
"""Independent check for PR #92 notes ARITHMETIC_TORUS_COVERING.md and DE_BRUIJN_ARITHMETIC_COVER.md.
Written by Claude (a language model), independent of the PR author's scripts. No human has checked it.
Stdlib only, exact integer arithmetic. Runtime: about 5 seconds.
Checks: (1) p=2131 row of the odd-torus table: #J, ord(P), qualifying indices, x(Q)=442;
 (2) the de Bruijn 4x4 reference code table and its 8 marked vertices;
 (3) the generalized-CRT intersection-lattice formula (index r*b) against brute-force
     group sizes for random pairs e1,e2 coprime to 6;
 (4) the arithmetic of the union-bound figures 1-4C and 1-4C-1/16 for the three quoted C values.
Does NOT check: Magma transcripts, other table primes, seed 72/360/2520 data, dependency components,
or the claim that components are isolated (needs the unarchived group sizes per seed)."""
import random
from math import gcd
p = 2131
def add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0: return None
    l = (3*x1*x1 - 4*x1 + 2) * pow(2*y1, -1, p) % p if P == Q else (y2-y1) * pow(x2-x1, -1, p) % p
    x3 = (l*l + 2 - x1 - x2) % p
    return (x3, (l*(x1-x3) - y1) % p)
n = 1 + sum(1 for x in range(p) for y in range(p) if (y*y - (x**3 - 2*x*x + 2*x)) % p == 0)
pts = {}; Q = None
for k in range(1, 3000):
    Q = add(Q, (1, 1))
    if Q is None: order = k; break
    pts[k] = Q
def qual(Q):
    t = (1 - Q[0]) % p
    if (t**6 - 30*t**4 - 24*t*t - 1) % p: return False
    v = 2*t*(1-t*t) % p
    return v != 0 and pow(v, (p-1)//2, p) == 1
qk = [k for k in pts if qual(pts[k])]
print("p=2131 #J", n, "ord P", order, "qualifying indices", qk, "x", [pts[k][0] for k in qk])
M = [[1,1,1,0],[1,1,0,1],[0,1,0,0],[1,0,0,0]]
codes = [[8*M[i][j]+4*M[i][(j+1)%4]+2*M[(i+1)%4][j]+M[(i+1)%4][(j+1)%4] for j in range(4)] for i in range(4)]
print("de Bruijn codes", codes, "all16 distinct", sorted(sum(codes, [])) == list(range(16)), "marked", sum(map(sum, M)))
def lat(e):
    r = 1; x = 2 % e
    while x != 1: x = x*2 % e; r += 1
    pw = {pow(2, a, e): a for a in range(r)}
    b = 1
    while pow(3, b, e) not in pw: b += 1
    return r, pw[pow(3, b, e)], b
random.seed(1); bad = 0; tested = 0
pool = [x for x in range(5, 400) if gcd(x, 6) == 1]
for _ in range(300):
    e1, e2 = random.choice(pool), random.choice(pool)
    r1, a1, b1 = lat(e1); r2, a2, b2 = lat(e2)
    r = r1*r2//gcd(r1, r2); b0 = b1*b2//gcd(b1, b2)
    c1, c2 = a1*b0//b1, a2*b0//b2
    g = gcd(r1, r2); k = g//gcd(g, abs(c1-c2)); b = b0*k
    S = {(1, 1)}; fr = [(1, 1)]
    while fr:
        nf = []
        for x, y in fr:
            for m in (2, 3):
                t = (x*m % e1, y*m % e2)
                if t not in S: S.add(t); nf.append(t)
        fr = nf
    tested += 1
    if len(S) != r*b: bad += 1
print("intersection index r*b == joint group size: tested", tested, "failures", bad)
for C in (0.0107838811974069, 0.0336780314980923, 0.0124110799153279):
    print("C", C, "1-4C", round(1-4*C, 15), "1-4C-1/16", round(1-4*C-1/16, 15))
