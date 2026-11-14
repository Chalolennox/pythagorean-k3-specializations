#!/usr/bin/env python3
"""Periodic part eps = L * (ab/N) of the root number along the four sequences  t = 1 - x(nP), 1 - x(nP+T)  (paper, proved laws)  and  t = 1 + x(nP), 1 + x(nP+T)  (the 'mirror' projection),
on C : y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), x(nP + T) = 2/x(nP).   For t = U/V:  F_s(U,V) = U^6 - 30U^4V^2 - 24U^2V^4 - V^6,  N = part of |F_s| prime to 6,  L = -w2*w3*(2/c) (paper section 4),
eps = L * Jacobi(ab, N)  (a Jacobi symbol: no factorisation needed).  Then W(E_t) = eps * delta * kappa with delta = Liouville sign of N (paper F.24), so eps is exactly the part of the sign that is NOT a coin.
Checks: the control sequences must reproduce the proved laws  eps_n = +1 iff n = 0, 1, 5 (mod 6) along nP and iff 3 | n along nP + T (n >= 2).   OBSERVED LAW (checked here for 3 <= n <= nmax, and for 16 values of n in 156..271 including five within 0.01 of the threshold): along the mirror sequences
    eps_n = h(n) * s_n,    h(n) = +1 iff 3 | n (1 + x(nP)),  h(n) = -1 iff 3 | n (1 + x(nP+T)),   s_n = sign F_s = +1 iff ||n*theta|| < rho (1 + x(nP)) resp. ||n*theta - 1/2|| < rho (1 + x(nP+T)),
with theta = u(P)/Omega = 0.2956798735... the rotation number of P on the real component of C (u = elliptic logarithm, Omega the real period) and rho = 0.1250944321... = u(x_0)/Omega, x_0 = t_0 - 1 where t_0 = 5.548...
is the largest real root of t^6 - 30t^4 - 24t^2 - 1.  Since theta is irrational, eps is NOT periodic (a period-3 pattern times a Sturmian rotation sequence), unlike the proved laws along 1 - x(nP), 1 - x(nP+T):
there t < 1, the real place is trivial and no sign appears.  Needs mpmath for theta and rho (a sympy dependency).
Usage: python3 mirror_projection_eps.py [nmax, default 72]   (exit 0 iff the control laws and the rotation law all hold for 3 <= n <= nmax)"""
import sys
from fractions import Fraction as Fr
from math import gcd
from sympy import jacobi_symbol
S2 = {(0, 1), (1, 0), (4, 9), (8, 1), (9, 4), (12, 9), (15, 0), (15, 8)}
def eps(t):
    U, V = t.numerator, t.denominator
    d = gcd(gcd(V*V - U*U, 2*U*V), V*V + U*U); a, b, c = (V*V - U*U)//d, (2*U*V)//d, (V*V + U*U)//d
    Fs = U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6; N = abs(Fs)
    while N % 2 == 0: N //= 2
    while N % 3 == 0: N //= 3
    J = jacobi_symbol((a*b) % N, N) if N > 1 else 1
    A9, B9 = (a*pow(c, -1, 9)) % 9, (b*pow(c, -1, 9)) % 9; A16, B16 = (a*pow(c, -1, 16)) % 16, (b*pow(c, -1, 16)) % 16
    w3 = -1 if (A9, B9) == (3, 8) else 1; w2 = -1 if (A16, B16) in S2 else 1
    return -w2*w3*jacobi_symbol(2, c)*J
def orbit(nmax):
    a2, a4 = -2, 2; P0 = (Fr(1), Fr(1)); Q = None; xs = []
    for n in range(1, nmax + 1):
        if Q is None: Q = P0
        else:
            (x1, y1), (x2, y2) = Q, P0
            lam = (3*x1*x1 + 2*a2*x1 + a4)/(2*y1) if Q == P0 else (y2 - y1)/(x2 - x1)
            x3 = lam*lam - a2 - x1 - x2; Q = (x3, lam*(x1 - x3) - y1)
        xs.append(Q[0])
    return xs
def rotation_constants():
    from mpmath import mp, mpf, quad, sqrt, inf, polyroots
    mp.dps = 30; f = lambda x: 1/(2*sqrt(x**3 - 2*x**2 + 2*x)); Om = 2*quad(f, [0, 1, inf]); theta = quad(f, [1, 2, 11, inf])/Om
    t0 = max(r.real for r in polyroots([1, 0, -30, 0, -24, 0, -1], maxsteps=200, extraprec=200) if abs(r.imag) < 1e-20)
    return theta, quad(f, [t0 - 1, t0, t0 + 10, inf])/Om
def law_eps(n, which, theta, rho):
    """eps_n = h(n) * s_n along the mirror sequences; which = 'P' for 1 + x(nP), 'PT' for 1 + x(nP+T)"""
    from mpmath import floor
    v = n*theta - (0 if which == 'P' else 0.5); dist = abs(v - floor(v + 0.5))
    s = 1 if dist < rho else -1; hh = (1 if n % 3 == 0 else -1)
    return hh*s if which == 'P' else -hh*s
def period(seq, start=2):
    s = seq[start - 1:]
    for p in range(1, len(s)//2 + 1):
        if all(s[i] == s[i + p] for i in range(len(s) - p)): return p
    return None
if __name__ == '__main__':
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 72
    xs = orbit(nmax)
    seqs = {'1 - x(nP)':     [eps(1 - x) for x in xs], '1 - x(nP+T)':  [eps(1 - 2/x) for x in xs],
            '1 + x(nP)':     [eps(1 + x) for x in xs], '1 + x(nP+T)':  [eps(1 + 2/x) for x in xs]}
    ok1 = all((seqs['1 - x(nP)'][n-1] == 1) == (n % 6 in (0, 1, 5)) for n in range(2, nmax + 1)); ok2 = all((seqs['1 - x(nP+T)'][n-1] == 1) == (n % 3 == 0) for n in range(2, nmax + 1))
    print('control: proved law along nP (+1 iff n = 0,1,5 mod 6) holds for 2 <= n <= %d: %s;  along nP+T (+1 iff 3 | n): %s' % (nmax, ok1, ok2))
    for k, s in seqs.items():
        print('%-14s eps_n, n = 1..%d: %s   least period (n >= 2): %s   mean over n >= 2: %+.3f' % (k, nmax, ''.join('+' if e == 1 else '-' for e in s), period(s), sum(s[1:])/(nmax - 1)))
    theta, rho = rotation_constants()
    ok3 = all(seqs['1 + x(nP)'][n-1] == law_eps(n, 'P', theta, rho) for n in range(3, nmax + 1)); ok4 = all(seqs['1 + x(nP+T)'][n-1] == law_eps(n, 'PT', theta, rho) for n in range(3, nmax + 1))
    print('rotation law eps_n = h(n)*s_n  (theta = %.10f, rho = %.10f): holds for 3 <= n <= %d along 1 + x(nP): %s;  along 1 + x(nP+T): %s' % (theta, rho, nmax, ok3, ok4))
    sys.exit(0 if (ok1 and ok2 and ok3 and ok4) else 1)
