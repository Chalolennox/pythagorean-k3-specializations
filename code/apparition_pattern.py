#!/usr/bin/env python3
"""Which primes can divide F_n = 4a^3 + 27 b^2 c = -4 (X^6 - 30 X^4 Y^2 - 24 X^2 Y^4 - Y^6),  X = psi_{n-1} psi_{n+1},  Y = psi_n^2   (psi_n = psi_n(P), P = (1,1) on C: y^2 = x^3 - 2x^2 + 2x).
For a prime p >= 5 let r = r_p be the order of P in C(F_p) and Z_p = {Q in C(F_p) : H(1 - x(Q)) = 0}, H(t) = t^6 - 30 t^4 - 24 t^2 - 1 (the F_p-rational points among the twelve points over the roots of H).
Claims checked here (the equivalence is a one-line proof, see notes/apparition_pattern_F_n.md; the rest follow from it):
  (A) for every n >= 2:  p | F_n  <=>  (n mod r) in N_p := {n mod r : nP in Z_p}                                  [exact F_n for n <= NMAX, all primes 5 <= p < PEXACT]
  (B) N_p = -N_p, |N_p| is even, |N_p| <= |Z_p| <= 12, and N_p contains none of the classes 0, +-1, r/2 (so p | F_n implies p does not divide psi_{n-1} psi_n psi_{n+1} psi_{2n})   [all primes 5 <= p < PMAX]
  (C) p | F_n and p | G_n (G_n: the same sextic along nP + T) is impossible: Z_p and Z_p + T are disjoint in <P> for p < PMAX; the three primes 7, 103, 519521 where H and its T-translate have a common root are checked separately
  (D) statistics: the number of primes < PMAX that divide some F_n, the distribution of |N_p| and of r_p / |N_p|; cross-checks with the paper's 358 primes below 3*10^4, p = 23 (2 classes mod 10), p = 83 (4 classes mod 39).
Usage: python3 code/apparition_pattern.py [--quick]   (full: PMAX = 30000, about a minute or two; --quick: PMAX = 3000; exit 0 = all checks pass).  Needs numpy and sympy.
"""
import sys, time
import numpy as np
from sympy import factorint, primerange, sqrt_mod
QUICK = '--quick' in sys.argv
PMAX = 3000 if QUICK else 30000; PEXACT = 2000 if QUICK else 6000; NMAX = 120
OK = True
def check(name, cond):
    global OK; OK = OK and bool(cond); print('%-4s %s' % ('OK' if cond else 'FAIL', name), flush=True)
def add(P, Q, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2:
        if (y1 + y2) % p == 0: return None
        lam = (3*x1*x1 - 4*x1 + 2) * pow(2*y1, -1, p) % p
    else: lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam*lam + 2 - x1 - x2) % p; return (x3, (lam*(x1 - x3) - y1) % p)
def mul(k, P, p):
    R = None
    while k:
        if k & 1: R = add(R, P, p)
        P = add(P, P, p); k >>= 1
    return R
def count_points(p):
    x = np.arange(p, dtype=np.int64); rhs = (x*x % p * x - 2*x*x + 2*x) % p
    sq = np.zeros(p, bool); sq[(x*x) % p] = True
    return 1 + int(np.sum(np.where(rhs == 0, 1, np.where(sq[rhs], 2, 0))))
def order_of_P(p):
    N = count_points(p); r = N; P = (1, 1)
    for q in factorint(N):
        while r % q == 0 and mul(r//q, P, p) is None: r //= q
    return r
def roots_of_H(p):
    t = np.arange(p, dtype=np.int64); u = t*t % p
    h = (u*u % p * u - 30*(u*u % p) - 24*u - 1) % p; return [int(v) for v in np.nonzero(h == 0)[0]]
def Zdata(p):
    """x-coordinates of Z_p (as a set) and |Z_p|"""
    X = set(); nZ = 0
    for tau in roots_of_H(p):
        x = (1 - tau) % p; rhs = (x**3 - 2*x*x + 2*x) % p
        if rhs == 0: continue
        if pow(rhs, (p - 1)//2, p) == 1: X.add(x); nZ += 2
    return X, nZ
def Np(p, r, X):
    out = []; Q = None; P = (1, 1)
    for n in range(1, r):
        Q = add(Q, P, p)
        if Q is not None and Q[0] in X: out.append(n)
    return out
if __name__ == '__main__':
    t0 = time.time(); sys.set_int_max_str_digits(0)
    # exact F_n for n <= NMAX from the elliptic divisibility sequence, with the psi-form checked
    W = {0: 0, 1: 1, 2: 2, 3: 3, 4: -20}
    def psi(n):
        if n < 0: return -psi(-n)
        if n in W: return W[n]
        if n % 2: j = (n - 1)//2; W[n] = psi(j + 2)*psi(j)**3 - psi(j - 1)*psi(j + 1)**3
        else: j = n//2; W[n] = psi(j)*(psi(j + 2)*psi(j - 1)**2 - psi(j - 2)*psi(j + 1)**2)//2
        return W[n]
    from math import gcd
    from mirror_projection_eps import orbit
    xs = orbit(NMAX + 2); Fn = {}; Gn = {}
    for n in range(2, NMAX + 1):
        X, Y = psi(n - 1)*psi(n + 1), psi(n)**2; Fn[n] = -4*(X**6 - 30*X**4*Y**2 - 24*X**2*Y**4 - Y**6)
        t = 1 - xs[n - 1]; u, v = t.numerator, t.denominator; assert (u, v) == (X, Y) and Fn[n] == 4*(v*v - u*u)**3 + 27*(2*u*v)**2*(v*v + u*u)
        tp = 1 - 2/xs[n - 1]; u2, v2 = tp.numerator, tp.denominator; Gn[n] = -4*(u2**6 - 30*u2**4*v2**2 - 24*u2**2*v2**4 - v2**6)
    check('psi-form: F_n = -4 (X^6 - 30 X^4 Y^2 - 24 X^2 Y^4 - Y^6), X = psi_{n-1} psi_{n+1}, Y = psi_n^2, equals 4a^3 + 27b^2 c with d_n = 1, for 2 <= n <= %d' % NMAX, True)
    stats = {}; classes = {}; badA = badB = badC = 0; nA = 0; dividing = []
    for p in primerange(5, PMAX):
        X, nZ = Zdata(p)
        if not X:
            if p < PEXACT:
                r = order_of_P(p); nA += NMAX - 1; badA += sum(1 for n in range(2, NMAX + 1) if Fn[n] % p == 0)
            continue
        r = order_of_P(p); N = Np(p, r, X); dividing.append(p); classes[p] = (r, N, nZ)
        S = set(N); even = len(N) % 2 == 0; sym = all((r - n) in S for n in N); excl = not ({0, 1, r - 1} & S) and (r % 2 or r//2 not in S)
        badB += (not (even and sym and excl and len(N) <= nZ <= 12 and len(N) > 0 or len(N) == 0))
        if N: stats[len(N)] = stats.get(len(N), 0) + 1
        if p < PEXACT:
            nA += NMAX - 1; badA += sum(1 for n in range(2, NMAX + 1) if (Fn[n] % p == 0) != ((n % r) in S))
        # (C): p | G_n iff nP + T in Z_p  iff  x(nP) in {2/x : x in X}
        XT = {(2 * pow(x, -1, p)) % p for x in X if x}; badC += bool(X & XT) and True
    N_div = sum(1 for p in dividing if classes[p][1])
    check('(A) p | F_n <=> n mod r_p in N_p, for all n in [2, %d] and all primes 5 <= p < %d (%d prime-index pairs, 0 disagreements: %d)' % (NMAX, PEXACT, nA, badA), badA == 0)
    check('(B) for the %d primes < %d with N_p nonempty: N_p = -N_p, |N_p| even, |N_p| <= |Z_p| <= 12, and none of the classes 0, +-1, r/2 in N_p (violations: %d)' % (N_div, PMAX, badB), badB == 0)
    # (C) the T-translate: Z_p and Z_p + T disjoint modulo p for every p < PMAX with N_p; plus the three exceptional primes
    check('(C) for p < %d: no point of <P> lies in both Z_p and Z_p + T (so p | F_n and p | G_n never occur together; %d violations)' % (PMAX, badC), badC == 0)
    ex = {}
    for p in (7, 103, 519521):
        X, nZ = Zdata(p); r = order_of_P(p); XT = {(2*pow(x, -1, p)) % p for x in X if x}
        ex[p] = (sorted(X & XT), r, nZ)
    check('(C) the primes 7, 103, 519521 where H and its T-translate share a root (Res = 2^11 * 7 * 103 * 519521^2): common x-coordinates of F_p-points in Z_p and Z_p + T: %s' % {p: v[0] for p, v in ex.items()}, True)
    if 519521 in ex and ex[519521][0]:
        Q = [(x, None) for x in ex[519521][0]]; print('     (519521: common x-coordinates', ex[519521][0], '; order of P =', ex[519521][1], '; they are not x(nP) for any n:', end=' ')
        p = 519521; X = set(ex[519521][0]); Qn = None; P = (1, 1); hit = False
        for n in range(1, ex[519521][1]):
            Qn = add(Qn, P, p)
            if Qn is not None and Qn[0] in X: hit = True; break
        print(not hit, ')'); check('(C) 519521: neither common root is x(nP) (order of P = %d)' % ex[519521][1], not hit)
    # (D) statistics and cross-checks with the paper
    n_primes = len(list(primerange(5, PMAX)))
    check('(D) %d of the %d primes 5 <= p < %d divide some F_n (all n >= 2): N_p nonempty%s' % (N_div, n_primes, PMAX, ' (the paper: 358 below 3*10^4)' if PMAX == 30000 else ''), (N_div == 358) if PMAX == 30000 else True)
    check('(D) p = 23: %s; p = 83: %s (the paper: 2 classes modulo 10; 4 classes modulo 39)' % ((classes[23][0], classes[23][1]), (classes[83][0], classes[83][1])), classes[23][0] == 10 and len(classes[23][1]) == 2 and classes[83][0] == 39 and len(classes[83][1]) == 4)
    print('     distribution of |N_p| among the %d primes < %d that divide some F_n: %s' % (N_div, PMAX, dict(sorted(stats.items()))))
    small = [(p, classes[p][0], classes[p][1]) for p in dividing if classes[p][1] and p < 200]
    print('     p, r_p, N_p for the primes < 200 that divide some F_n:'); [print('       %4d  r=%4d  N_p=%s' % s) for s in small]
    print('ALL CHECKS PASS (%.0f s)' % (time.time() - t0) if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
