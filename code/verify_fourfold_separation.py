#!/usr/bin/env python3
"""Verification of the fourfold coprimality of F.50: for x_n = x(nP) on C : y^2 = x^3 - 2x^2 + 2x, P = (1,1), the four integers F(t), t = 1 - x_n, 1 + x_n, 1 - 2/x_n, 1 + 2/x_n,
F(t) = 4a^3 + 27 b^2 c, are pairwise coprime away from 2 and 3 (primes p >= 5) for every n.   Method (no Magma needed):
 (1) exact identity 4(v^2-u^2)^3 + 27(2uv)^2(v^2+u^2) = -4 v^6 H(u/v), H(t) = t^6 - 30t^4 - 24t^2 - 1;  G_-(X) = H(1-X), G_+(X) = H(1+X), J_-(X) = X^6 G_-(2/X), J_+(X) = X^6 G_+(2/X) as stated;
 (2) the six resultants and the set E of primes >= 5 dividing one of them;  leading/constant coefficients (1,1,-54,-54), (-54,-54,64,64) are nonzero mod every p >= 5;
 (3) for every p in E: order of P mod p, all common roots in F_p of the six pairs, and the number of orbit points (x-coordinates of <P mod p>) that are common roots (must be 0);
 (4) brute force: no pair of the four integers shares a prime >= 5 for 1 <= n <= NMAX (default 120).   Usage: python3 code/verify_fourfold_separation.py [NMAX]   Exit 0 = all checks pass.  sympy only."""
import sys
from math import gcd
from fractions import Fraction as Fr
from sympy import symbols, Poly, expand, resultant, factorint
X, u, v = symbols('X u v'); NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 120
H = lambda s: s**6 - 30*s**4 - 24*s**2 - 1
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print('%-4s %s' % ('OK' if cond else 'FAIL', name))
check('identity 4(v^2-u^2)^3 + 27(2uv)^2(v^2+u^2) = -4 v^6 H(u/v)', expand(4*(v**2-u**2)**3 + 27*(2*u*v)**2*(v**2+u**2) + 4*v**6*H(u/v)) == 0)
Gm, Gp = expand(H(1-X)), expand(H(1+X)); Jm, Jp = expand(X**6*Gm.subs(X, 2/X)), expand(X**6*Gp.subs(X, 2/X))
polys = {'G-': Gm, 'G+': Gp, 'J-': Jm, 'J+': Jp}; names = list(polys); pairs = [(a, b) for i, a in enumerate(names) for b in names[i+1:]]
stated = {'G-': [1, -6, -15, 100, -189, 162, -54], 'G+': [1, 6, -15, -100, -189, -162, -54], 'J-': [-54, 324, -756, 800, -240, -192, 64], 'J+': [-54, -324, -756, -800, -240, 192, 64]}
check('the four polynomials G-, G+, J-, J+ are as stated in F.50', all(Poly(polys[k], X).all_coeffs() == stated[k] for k in names))
res = {pr: abs(int(resultant(polys[pr[0]], polys[pr[1]], X))) for pr in pairs}
claimed = {('G-', 'G+'): {2: 13, 3: 9, 7: 2, 66601: 2}, ('G-', 'J-'): {2: 17, 7: 1, 103: 1, 519521: 2}, ('G-', 'J+'): {2: 15, 3: 12, 7: 2, 79: 2, 113: 1, 13327: 2},
           ('G+', 'J-'): {2: 15, 3: 12, 7: 2, 79: 2, 113: 1, 13327: 2}, ('G+', 'J+'): {2: 17, 7: 1, 103: 1, 519521: 2}, ('J-', 'J+'): {2: 49, 3: 9, 7: 2, 66601: 2}}
check('the six resultants are as stated', all(factorint(res[pr]) == claimed[pr] for pr in pairs))
E = sorted({p for r in res.values() for p in factorint(r) if p >= 5}); check('exceptional primes E = %s' % E, E == [7, 79, 103, 113, 13327, 66601, 519521])
check('leading coefficients (1, 1, -54, -54) and constant coefficients (-54, -54, 64, 64) are units mod every p >= 5', all(c % p for c in (1, -54, 64) for p in (5, 7, 11, 13) + tuple(E)))
# (3) finite fields
def orbit_mod(p):
    def add(A, B):
        if A is None: return B
        if B is None: return A
        (x1, y1), (x2, y2) = A, B
        if x1 == x2 and (y1 + y2) % p == 0: return None
        lam = ((3*x1*x1 - 4*x1 + 2)*pow(2*y1, -1, p)) % p if A == B else ((y2 - y1)*pow(x2 - x1, -1, p)) % p
        x3 = (lam*lam + 2 - x1 - x2) % p; return (x3, (lam*(x1 - x3) - y1) % p)
    P = (1, 1); pts = []; Q = P
    while Q is not None: pts.append(Q); Q = add(Q, P)
    return len(pts) + 1, {q[0] for q in pts}
orders = {7: 6, 79: 22, 103: 54, 113: 14, 13327: 3358, 66601: 8366, 519521: 698}; summary = []
for p in E:
    m, xs = orbit_mod(p); cf = {k: [int(c) % p for c in Poly(polys[k], X).all_coeffs()] for k in names}
    def roots(k):
        c = cf[k]; return {x for x in range(p) if (lambda s: s)(__import__('functools').reduce(lambda s, a: (s*x + a) % p, c, 0)) == 0}
    R = {k: roots(k) for k in names}; common = {pr: R[pr[0]] & R[pr[1]] for pr in pairs}
    ncom = sum(len(c) for c in common.values()); coll = sum(len(c & xs) for c in common.values())
    check('p = %6d: ord(P) = %5d, common roots in F_p of the six pairs: %2d, orbit points that are common roots: %d' % (p, m, ncom, coll), m == orders[p] and coll == 0)
# (4) brute force
a2, a4 = -2, 2
def addQ(A, B):
    if A is None: return B
    (x1, y1), (x2, y2) = A, B
    lam = (3*x1*x1 + 2*a2*x1 + a4)/(2*y1) if A == B else (y2 - y1)/(x2 - x1)
    x3 = lam*lam - a2 - x1 - x2; return (x3, lam*(x1 - x3) - y1)
def D(name, r, s): return sum(c*r**(6 - k)*s**k for k, c in enumerate(stated[name]))
Q = None; P0 = (Fr(1), Fr(1)); bad = []
for n in range(1, NMAX + 1):
    Q = addQ(Q, P0); r, s = Q[0].numerator, Q[0].denominator; vals = {k: D(k, r, s) for k in names}
    for a, b in pairs:
        g = gcd(vals[a], vals[b])
        for q in (2, 3):
            while g and g % q == 0: g //= q
        if abs(g) != 1: bad.append((n, a, b))
check('1 <= n <= %d, all six pairs: no common prime factor >= 5 (so the statement holds for p >= 5, not only p > 5)' % NMAX, not bad)
sys.exit(0 if ok else 1)
