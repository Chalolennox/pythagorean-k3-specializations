#!/usr/bin/env python3
"""Independent check of identities in notes/ADDITIVE_DESCENT_RIGIDITY.md (PR #92).

Written by Claude (a language model), independent of the PR author's scripts.
No human has checked it.  Stdlib only, exact integer/Fraction arithmetic.  Runtime: under 2 seconds.

CHECKS for coprime 1<=m,D<=59, curve J: y^2=x^3-2x^2+2x, x=m^2/D^2, l^2=m^4-2m^2D^2+2D^4:
 (1) N = D^12 H(1-m^2/D^2) is an integer, equals l^6-33 l^4 D^4+39 l^2 D^8-8 D^12 (l^2 as integer).
 (2) N = (m^2-D^2)^6 mod D^4.
 (3) when l is an integer: U=l-m^2+D^2, V=l+m^2-D^2 satisfy UV=D^4 and
     64N = U^6-126U^5V+111U^4V^2-36U^3V^3+111U^2V^4-126UV^5+V^6.
 (4) when l is an integer: x(2Q) and x(3Q) from the group law equal the squares of the
     duplication/triplication square-root formulas in section 3.
DOES NOT CHECK: the 2-adic/odd-prime valuation propagation, Hensel/sixth-power statements,
the Magma grids, or any claim about oriented r,s propagation.  Only the rational points with
integer l found in the range (count printed) test (3),(4); (1),(2) run on all coprime pairs.
"""
from fractions import Fraction as F
from math import gcd, isqrt
H = lambda t: t**6 - 30*t**4 - 24*t**2 - 1
def add(P, Q):
    s = (3*P[0]**2 - 4*P[0] + 2)/(2*P[1]) if P == Q else (Q[1]-P[1])/(Q[0]-P[0])
    x3 = s*s + 2 - P[0] - Q[0]
    return (x3, -(P[1] + s*(x3-P[0])))
pairs = pts = 0
for m in range(1, 60):
    for D in range(1, 60):
        if gcd(m, D) != 1: continue
        L2 = m**4 - 2*m*m*D*D + 2*D**4
        N = D**12 * H(1 - F(m*m, D*D)); assert N.denominator == 1; N = int(N)
        assert N == L2**3 - 33*L2**2*D**4 + 39*L2*D**8 - 8*D**12
        assert (N - (m*m-D*D)**6) % D**4 == 0
        pairs += 1
        l = isqrt(L2)
        if l*l != L2: continue
        U = l - m*m + D*D; V = l + m*m - D*D
        assert U*V == D**4
        assert 64*N == U**6-126*U**5*V+111*U**4*V**2-36*U**3*V**3+111*U**2*V**4-126*U*V**5+V**6
        P = (F(m*m, D*D), F(m*l, D**3)); P2 = add(P, P); P3 = add(P2, P)
        assert P2[0] == F(m**4-2*D**4, 2*m*D*l)**2
        r = F(m**9-12*m**5*D**4+16*m**3*D**6-12*m*D**8, 3*m**8*D-8*m**6*D**3+12*m**4*D**5-4*D**9)
        assert P3[0] == r*r
        pts += 1; print("rational point m=%d D=%d l=%d U=%d V=%d" % (m, D, l, U, V))
print("checks (1),(2) passed for", pairs, "pairs; (3),(4) for", pts, "rational points")
