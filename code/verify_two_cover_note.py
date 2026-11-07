#!/usr/bin/env python3
"""Checks of the claims in 'constant_x_two_cover_independent_review.md' (fixed pair of distinct constant-x covers).
Needs: python3, sympy, numpy, mpmath.  Exit status 0 = every expected check passes.  Takes about a minute."""
import sys, itertools, random, warnings
warnings.filterwarnings('ignore')
from fractions import Fraction as Fr
from math import gcd
import numpy as np, sympy, mpmath as mp
from sympy import symbols, Poly, resultant, discriminant, expand, factor, gcd as sgcd, Rational, sqf_list
t, a, b, c, x = symbols('t a b c x')
ok = True
def check(name, cond, extra=''):
    global ok; ok &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra))
N = lambda cc: cc*(cc**2 - 4)*t**2 - 16*t + cc**3 + 4*cc
f6 = t**6 - 30*t**4 - 24*t**2 - 1

# --- sections 1-2: single cover ------------------------------------------------------------------------------------
check('disc_t N_c = 4(64 + 16c^2 - c^6)', expand(discriminant(N(c), t) - 4*(64 + 16*c**2 - c**6)) == 0)
check('Res_t(N_c, 1+t^2) = 64(c^2+4)', expand(resultant(N(c), 1 + t**2, t) - 64*(c**2 + 4)) == 0)
check('c^6 - 16c^2 - 64 has no rational root', Poly(c**6 - 16*c**2 - 64, c).ground_roots() == {})
check('2-adic argument: c odd gives 1 mod 4; c = 2k gives 64(k^6-k^2-1) with k^6-k^2-1 odd',
      all((cc**6 - 16*cc**2 - 64) % 4 == 1 for cc in range(1, 60, 2)) and all((k**6 - k**2 - 1) % 2 == 1 for k in range(0, 60)))
for cc in (0, 2, -2):
    P = Poly(sympy.expand((1 + t**2)*N(cc)), t)
    check('c = %2d: (1+t^2)N_c has degree 3 and distinct roots, so the branch set is {i, -i, root, infinity}' % cc, P.degree() == 3 and Poly(sgcd(P.as_expr(), P.as_expr().diff(t)), t).degree() == 0,
          '(finite root %s)' % sympy.solve(N(cc), t))

# --- section 3: distinct square classes for a != b --------------------------------------------------------------------
def Mpoly(cc): return Poly(sympy.expand((1 + t**2)*N(Rational(cc))), t)
def is_square_class(P):          # constant times a square in Qbar[t]?  all multiplicities even and even degree
    _, fl = sqf_list(P.as_expr(), t); return P.degree() % 2 == 0 and all(m % 2 == 0 for _, m in fl)
vals = sorted({Fr(p, q) for p in range(-9, 10) for q in range(1, 6)})
vals = [v for v in vals if abs(v) <= 6][:60]
bad = []; sanity = True
for u, v in itertools.combinations(vals, 2):
    if is_square_class(Mpoly(u)*Mpoly(v)): bad.append((u, v))
check('M_a * M_b is never a square class for distinct a, b among %d rationals (%d pairs); degree-drop cases c = 0, +-2 included' % (len(vals), len(vals)*(len(vals)-1)//2), not bad, str(bad[:3]))
check('sanity: M_a * M_a is a square class', all(is_square_class(Mpoly(u)*Mpoly(u)) for u in vals[:10]))

# --- section 4: genus of the biquadratic cover, two methods ------------------------------------------------------------------
def genus_two_ways(u, v):
    Mu, Mv = Mpoly(u), Mpoly(v)
    g_ = Poly(sgcd(Mu.as_expr(), Mv.as_expr()), t).degree()
    finite = Mu.degree() + Mv.degree() - g_
    inf = 1 if (Mu.degree() % 2 or Mv.degree() % 2) else 0
    m = finite + inf; g1 = m - 3                                   # Riemann-Hurwitz as in the note
    Nu, Nv = Poly(N(Rational(u)), t), Poly(N(Rational(v)), t)    # genus of the three quotients: C_a, C_b (genus 1 each) and u^2 = N_a N_b
    prod = Nu*Nv; _, fl = sqf_list(prod.as_expr(), t)
    odd_finite = sum(Poly(fac, t).degree() for fac, mult in fl if mult % 2 == 1)
    k = odd_finite + (1 if prod.degree() % 2 else 0); g2 = 1 + 1 + (k//2 - 1)
    return g1, g2, m
rows = [genus_two_ways(u, v) for u, v in itertools.combinations(vals[::3], 2)]
check('genus m - 3 equals g(C_a) + g(C_b) + g(u^2 = N_a N_b) for %d pairs; values seen: %s' % (len(rows), sorted({r[0] for r in rows})), all(r[0] == r[1] for r in rows) and {r[0] for r in rows} <= {2, 3})
special = [(Fr(0), Fr(2)), (Fr(2), Fr(-2)), (Fr(0), Fr(-2)), (Fr(1), Fr(3))]
print('     genus of D_{a,b} for', [(str(p), str(q), genus_two_ways(p, q)[0]) for p, q in special], '(the first three share the moving root at infinity)')
check('all pairs among c in {0, 2, -2} have genus 2', all(genus_two_ways(p, q)[0] == 2 for p, q in [(0, 2), (2, 0), (0, -2), (-2, 0), (2, -2), (-2, 2)]))

# --- section 6: the resultant, the circle point, the cubic ----------------------------------------------------------------------
R = factor(resultant(N(a), N(b), t))
Fab = a**2*b**2*(a + b)**2 + 4*((a**2 + a*b + b**2)**2 - 16)
check('Res_t(N_a, N_b) = 64 (a-b)^2 F(a,b)', expand(R - 64*(a - b)**2*Fab) == 0)
A_ = -(a**2 + a*b + b**2)/4; B_ = -a*b*(a + b)/8
check('64 (A^2 + B^2 - 1) = F(a,b) for A = -(a^2+ab+b^2)/4, B = -ab(a+b)/8', sympy.simplify(64*(A_**2 + B_**2 - 1) - Fab) == 0)
check('x^3 + 4Ax - 8B = (x-a)(x-b)(x+a+b)', expand(x**3 + 4*A_*x - 8*B_ - (x - a)*(x - b)*(x + a + b)) == 0)
check('F(a,a) = F(a,-2a) = 4(a^6 + 9a^4 - 16)  (repeated-root cases)', expand(Fab.subs(b, a) - 4*(a**6 + 9*a**4 - 16)) == 0 and expand(Fab.subs(b, -2*a) - 4*(a**6 + 9*a**4 - 16)) == 0)
check('a^6 + 9a^4 - 16 (the collision polynomial of F.47) has no rational root, so no repeated-root solution of F = 0 over Q', Poly(a**6 + 9*a**4 - 16, a).ground_roots() == {})
check('f(t) = t^6-30t^4-24t^2-1 has no rational root; (1+t^2) f(t) is squarefree of degree 8 (genus 3)',
      Poly(f6, t).ground_roots() == {} and Poly(sgcd(sympy.expand((1 + t**2)*f6), sympy.expand((1 + t**2)*f6).diff(t)), t).degree() == 0 and Poly((1 + t**2)*f6, t).degree() == 8)
tt = symbols('tt'); At = (1 - tt**2)/(1 + tt**2); Bt = 2*tt/(1 + tt**2)
check('Delta = 16 * (cubic discriminant) = 4096 f(t)/(1+t^2)^3, so the cubic discriminant is a square iff (1+t^2) f(t) is a square',
      sympy.simplify(16*(-4*(4*At)**3 - 27*(8*Bt)**2) - 4096*f6.subs(t, tt)/(1 + tt**2)**3) == 0)

# numerical check of the correspondence F(a,b) = 0  <->  circle point with split cubic, at generic real solutions
mp.mp.dps = 30; good = True; cnt = 0
random.seed(1)
for _ in range(12):
    a0 = mp.mpf(random.uniform(-3, 3))
    poly_b = Poly(Fab.subs(a, sympy.Float(str(a0), 30)), b)
    for r_ in sympy.Poly(poly_b, b).nroots(n=25):
        if abs(sympy.im(r_)) < 1e-12:
            b0 = mp.mpf(str(sympy.re(r_))); A0 = -(a0**2 + a0*b0 + b0**2)/4; B0 = -a0*b0*(a0 + b0)/8
            if abs(A0**2 + B0**2 - 1) > 1e-15: good = False
            if abs(A0 + 1) > 1e-6:
                t0 = B0/(1 + A0); z2 = (1 + t0**2)*(t0**6 - 30*t0**4 - 24*t0**2 - 1)
                roots_ok = all(abs(rt**3 + 4*A0*rt - 8*B0) < 1e-12 for rt in (a0, b0, -a0 - b0))
                zz = (1 + t0**2)**2*(a0 - b0)*(2*a0 + b0)*(a0 + 2*b0)/16     # z with z^2 = (1+t0^2) f(t0) when the cubic splits
                good &= roots_ok and abs(zz**2 - z2) < 1e-15*(1 + abs(z2))
                cnt += 1
check('at %d generic real solutions of F(a,b) = 0: A^2+B^2 = 1, t0 = B/(1+A), and a, b, -a-b are the roots of the cubic at t0, and (1+t0^2) f(t0) = z^2 with z = (1+t0^2)^2 (a-b)(2a+b)(a+2b)/16' % cnt, good and cnt > 0)

# bounded search for rational solutions of F(a,b) = 0 and for rational points of z^2 = (1+t^2) f(t)
sols = set()
for d in range(1, 81):
    p = np.arange(-250, 251, dtype=np.int64)[:, None]; r = np.arange(-250, 251, dtype=np.int64)[None, :]
    val = p**2*r**2*(p + r)**2 + 4*d*d*(p*p + p*r + r*r)**2 - 64*d**6
    for i, j in zip(*np.nonzero(val == 0)):
        pa, ra = int(p[i, 0]), int(r[0, j])
        if Fr(pa, d) != Fr(ra, d): sols.add((Fr(pa, d), Fr(ra, d)))
expected = {(Fr(u), Fr(v)) for u in (-2, 0, 2) for v in (-2, 0, 2) if u != v}
print('     rational solutions (a, b), a != b, of F(a,b) = 0 with |numerator| <= 250, denominator <= 80:', len(sols))
check('the only solutions found are the 6 ordered pairs from {-2, 0, 2}, which come from t = infinity (A, B) = (-1, 0)', sols == expected)
def issq(n):
    if n < 0: return False
    s = int(sympy.integer_nthroot(n, 2)[0]); return s*s == n
found = [(u, v) for v in range(1, 301) for u in range(-600, 601) if gcd(abs(u), v) == 1 and issq((u*u + v*v)*(u**6 - 30*u**4*v**2 - 24*u**2*v**4 - v**6))]
check('no rational point (finite t = u/v, |u| <= 600, v <= 300) on z^2 = (1+t^2) f(t), so no t with full rational 2-torsion in that range', found == [])
print('ALL EXPECTED CHECKS PASS' if ok else 'SOME CHECK FAILED'); sys.exit(0 if ok else 1)
