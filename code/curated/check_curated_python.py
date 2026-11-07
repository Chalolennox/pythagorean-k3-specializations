#!/usr/bin/env python3
"""Python/sympy re-implementation of every part of the curated CAS scripts (01-10) that can be checked
without Sage, Magma or PARI.  Needs: python3, sympy, numpy.   Exit status 0 = every check passes.
The CAS scripts themselves are NOT run by this file; see README_INTEGRATION.md for what that means."""
import sys, os, itertools, warnings
warnings.filterwarnings('ignore')
from fractions import Fraction as Fr
import sympy
from sympy import symbols, Poly, groebner, expand, factor, gcd, resultant, discriminant, factor_list
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # code/ec.py
from ec import Curve, gram, det3
ok = True
def check(name, cond, extra=''):
    global ok; ok &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra))

# ---- 03 and 07: the circle sequence ((3+4i)/5)^n, two different recurrences -------------------------------------------
s = Fr(1, 2); t = Fr(0); a, b = 1, 0; good = True
for n in range(1, 13):
    t = (t + s) / (1 - s*t)                       # script 03
    A = (1 - t*t) / (1 + t*t); B = 2*t / (1 + t*t)
    a, b = 3*a - 4*b, 4*a + 3*b                   # script 07
    good &= (A*A + B*B == 1) and (a*a + b*b == 25**n) and (A == Fr(a, 5**n)) and (B == Fr(b, 5**n))
check('03 + 07: t_n from the half-angle recurrence gives A_n + i B_n = ((3+4i)/5)^n, n = 1..12, and a_n^2 + b_n^2 = 25^n', good,
      '(n=12: a=%d, b=%d)' % (a, b))

# ---- 08: the integral model used in the PARI script ------------------------------------------------------------------
good = True; a, b = 1, 0
for n in range(0, 12):
    A = Fr(a, 5**n); B = Fr(b, 5**n); u = 5**n
    good &= (4*A*u**4 == 4*a*5**(3*n)) and (-8*B*u**6 == -8*b*5**(5*n)) and (4*(4*a*5**(3*n))**3 + 27*(8*b*5**(5*n))**2 != 0)
    a, b = 3*a - 4*b, 4*a + 3*b
check('08: [0,0,0,4a5^(3n),-8b5^(5n)] is E_n scaled by u = 5^n, and is nonsingular, n = 0..11', good)

# ---- 01/02: the sixteen parameters give nonsingular curves; list the curves ------------------------------------------
vals = [Fr(-46,9), Fr(-12,11), Fr(-17,31), Fr(15,8), Fr(-7), Fr(-4), Fr(8), Fr(-4,3), Fr(-1,3), Fr(4,3), Fr(-7,4), Fr(2,5), Fr(-5,7), Fr(1,9), Fr(1,2), Fr(1)]
good = True
for t in vals:
    A = (1 - t*t)/(1 + t*t); B = 2*t/(1 + t*t); good &= (4*(4*A)**3 + 27*(8*B)**2 != 0)
check('01/02: the 16 parameters give nonsingular curves (ranks are NOT computed here)', good)

# ---- 05: constant-x cover ----------------------------------------------------------------------------------------------
c, t_ = symbols('c t')
N = c*(c**2-4)*t_**2 - 16*t_ + c**3 + 4*c
D = factor(discriminant(N, t_)); Rs = factor(resultant(N, t_**2 + 1, t_))
check('05: disc_t N_c = -4(c^6 - 16c^2 - 64)', expand(D - (-4*(c**6 - 16*c**2 - 64))) == 0, '  (printed by the script as the factorization %s)' % D)
check('05: Res_t(N_c, t^2+1) = 64(c^2+4)  (= |N_c(i)|^2, N_c(i) = 8c - 16i)', expand(Rs - 64*(c**2+4)) == 0)
u = symbols('u'); sq = True
for cc in [0, 1, 2, 4, -3]:
    F = sympy.expand((u*u + 1)*(cc*(cc*cc-4)*u*u - 16*u + cc**3 + 4*cc)); sq &= (Poly(gcd(F, F.diff(u)), u).degree() == 0)
check('05: (u^2+1)N_c(u) squarefree for c = 0, 1, 2, 4, -3', sq)

# ---- 06: genus-three curve --------------------------------------------------------------------------------------------
H = sympy.expand((c**2 + 4)*(c**6 + 36*c**4 - 1024))
check('06: H(c) squarefree of degree 8 (genus 3); factorization %s' % factor(H), Poly(gcd(H, H.diff(c)), c).degree() == 0 and Poly(H, c).degree() == 8)
def is_rat_square(q):
    q = Fr(q); 
    if q < 0: return False
    r = lambda n: int(sympy.integer_nthroot(n, 2)[0])**2 == n
    return r(q.numerator) and r(q.denominator)
cs = [Fr(1,4), Fr(1,3), Fr(1,2), Fr(2,3), Fr(3,4), Fr(1), Fr(5,4), Fr(4,3), Fr(3,2), Fr(5,2), Fr(3), Fr(4)]
check('06: H(c) is not a rational square at the 12 listed c', not any(is_rat_square((x*x+4)*(x**6+36*x**4-1024)) for x in cs))

# ---- 10: section identity ---------------------------------------------------------------------------------------------
X = c*(1+t_**2)*N; Y = (1+t_**2)*N**2
check('10: P_c lies on S_c (exact identity in Q[c,t])', expand(Y**2 - (X**3 + 4*(1-t_**4)*N**2*X - 16*t_*(1+t_**2)**2*N**3)) == 0)

# ---- 04: the elimination (port of the Magma script to sympy) ----------------------------------------------------------
lam, v0, v1, v2, h = symbols('lam v0 v1 v2 h')
r = c*(1 + t_**2)
Fm = (1+t_**2)**2 + lam*(3*r**2 + 4*(1 - t_**4)) + 3*lam**2*r*N + lam**3*N**2
Vm = v0 + v1*t_ + v2*t_**2
P_ = Poly(expand(Fm - Vm**2), t_)
eqs = [P_.coeff_monomial(t_**k) for k in range(5)] + [h*lam - 1]
GB = groebner(eqs, lam, v0, v1, v2, h, c, order='lex')
G = c*(c**6 + 16*c**4 + 432*c**2 + 1472)
check('04: G(c) = c(c^6+16c^4+432c^2+1472) lies in the ideal (Groebner basis of %d elements)' % len(GB.exprs), GB.contains(G))
check('04: the last basis element is G(c)', expand(factor(GB.exprs[-1]) - G) == 0)
check('04: x^3+16x^2+432x+1472 (x = c^2) has no positive real root', all(v < 0 for v in sympy.real_roots(Poly(sympy.symbols('x')**3 + 16*sympy.symbols('x')**2 + 432*sympy.symbols('x') + 1472))))

# ---- 09: the four points at t = -46/9 ---------------------------------------------------------------------------------
t0 = Fr(-46, 9); A = (1 - t0*t0)/(1 + t0*t0); B = 2*t0/(1 + t0*t0); E = Curve(4*A, -8*B)
pts = [(Fr(-18,13), Fr(396,169)), (Fr(-242,117), Fr(6172,4563)), (Fr(-243,169), Fr(5091,2197)), (Fr(358,117), Fr(20572,4563))]
check('09: the four points lie on y^2 = x^3 + 4Ax - 8B at t = -46/9 (exact)', all(E.on(Pt) for Pt in pts))
R = E.add(E.add(pts[0], pts[2]), pts[3])
check('09: P1 + P3 + P4 = O exactly (the fourth point is the third intersection of the line P1 P3)', R is None)
G4 = gram(E, pts, 6)
regs = [det3([[G4[i][j] for j in idx] for i in idx]) for idx in itertools.combinations(range(4), 3)]
import numpy as np
eig = np.linalg.eigvalsh(np.array(G4))
check('09: Gram matrix of canonical heights has exactly one zero eigenvalue (rank 3)', sum(abs(e) < 1e-4 for e in eig) == 1 and min(e for e in eig if abs(e) > 1e-4) > 1,
      '  eigenvalues %s' % ['%.3g' % e for e in eig])
check('09: every independent triple has regulator 87.60 +- 0.02 (the value recorded in section 5 of the paper)',
      all(abs(r_ - 87.60) < 0.02 for r_ in regs if abs(r_) > 1), '  regulators %s' % ['%.3f' % r_ for r_ in regs])
print('ALL CHECKS PASS' if ok else 'SOME CHECK FAILED'); sys.exit(0 if ok else 1)
