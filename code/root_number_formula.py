#!/usr/bin/env python3
"""Global root number W(E_t) of E_t : y^2 = x^3 + 4A x - 8B, A = (1-t^2)/(1+t^2), B = 2t/(1+t^2), t = u/v, from the closed formula of paper section 4 (proved there):
    W(E_t) = -w2 * w3 * (2/c) * (-1)^{omega(R_F)} * (ab / R_F),     (a, b, c) the primitive Pythagorean triple of t, F = 4a^3 + 27 b^2 c = -4 F_s(u, v)/d^3,
    F_s(u, v) = u^6 - 30 u^4 v^2 - 24 u^2 v^4 - v^6,  R_F = product of the primes p >= 5 dividing F,
    w3 = -1 iff (A, B) = (3, 8) mod 9;   w2 = -1 iff (A, B) mod 16 lies in S2 = {(0,1),(1,0),(4,9),(8,1),(9,4),(12,9),(15,0),(15,8)};   (2/c) Jacobi symbol.
Usage as a module: W(Fraction or (u, v)) -> +-1 ; parts(u, v) -> dict.  Run as a script: validates against independent Magma values (paired-root-numbers note) and the paper's table."""
from fractions import Fraction
from math import gcd
from sympy import factorint, jacobi_symbol
S2 = {(0, 1), (1, 0), (4, 9), (8, 1), (9, 4), (12, 9), (15, 0), (15, 8)}
def parts(u, v):
    if isinstance(u, Fraction): u, v = u.numerator, u.denominator
    g = gcd(u, v); u, v = u//g, v//g
    if v < 0: u, v = -u, -v
    d = gcd(gcd(v*v - u*u, 2*u*v), v*v + u*u)
    a, b, c = (v*v - u*u)//d, (2*u*v)//d, (v*v + u*u)//d
    Fs = u**6 - 30*u**4*v**2 - 24*u**2*v**4 - v**6
    assert 4*a**3 + 27*b*b*c == -4*Fs//d**3 and (4*Fs) % d**3 == 0   # F = 4a^3 + 27b^2c = -4 F_s(u, v)/d^3
    fac = {p: e for p, e in factorint(abs(Fs)).items() if p >= 5}
    R = 1
    for p in fac: R *= p
    A9, B9 = (a*pow(c, -1, 9)) % 9, (b*pow(c, -1, 9)) % 9; A16, B16 = (a*pow(c, -1, 16)) % 16, (b*pow(c, -1, 16)) % 16
    w3 = -1 if (A9, B9) == (3, 8) else 1; w2 = -1 if (A16, B16) in S2 else 1
    two_c = jacobi_symbol(2, c); y = (-1)**len(fac); J = jacobi_symbol((a*b) % R, R) if R > 1 else 1
    return dict(a=a, b=b, c=c, d=d, Fs=Fs, fac=fac, w2=w2, w3=w3, two_c=two_c, Y=y, J=J, W=-w2*w3*two_c*y*J)
def W(t, v=None): return parts(*((t, v) if v is not None else (t, 1)))['W']
if __name__ == '__main__':
    F = Fraction
    # independent Magma V2.30-1 values (paired-root-numbers review draft, section 6): W(E_{t_n}) for t_n = t(nP) and W(E_{R(t_n)}), R(t_n) = t(nP + T), n = 1..6 (n = 7, 8 need larger t)
    tn = [F(0), F(3, 4), F(-40, 9), F(-561, 400), F(34440, 34969), F(-2047837, 2965284)]; Wn = [1, -1, -1, -1, -1, 1]
    tp = [F(-1), F(-7), F(31, 49), F(161, 961), F(-69409, 529), F(-917447, 5013121)]; Wp = [-1, 1, -1, -1, -1, -1]
    bad = 0
    for t, w in list(zip(tn, Wn)) + list(zip(tp, Wp)):
        got = W(t); bad += (got != w); print('t = %-18s Magma %+d  formula %+d  %s' % (t, w, got, 'ok' if got == w else 'MISMATCH'))
    # the paper's list of orbit members and signs (section 6): t = 0, 1, -1, 3/4, -7, -40/9, 31/49, -561/400, 161/961, 34440/34969, -69409/529
    print('mismatches:', bad)
    raise SystemExit(1 if bad else 0)
