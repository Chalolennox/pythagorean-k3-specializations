#!/usr/bin/env python3
"""Check the statements about the fibre configuration of S_c used in F.43 and F.47.

S_c : Y^2 = X^3 + 4(1 - t^4) N_c(t)^2 X - 16 t (1 + t^2)^2 N_c(t)^3,  N_c(t) = c(c^2 - 4)t^2 - 16t + c^3 + 4c.
Exact (sympy):   discriminant, resultants, absence of rational roots, fibre valuations, the cases c = 0, +-2 at t = infinity,
                 and the 18 values of c of F.44-F.46.
Numerical (mpmath, 40 digits):   at one root of each collision polynomial, the vanishing of delta and of 3r^2 + 4(1 - alpha^4).
Needs: python3, sympy, mpmath.  Exit status 0 = every check passes.  Takes a few seconds."""
import sys, warnings
warnings.filterwarnings('ignore')
import sympy, mpmath as mp
from sympy import symbols, Poly, resultant, discriminant, expand, factor, gcd, Rational, degree, factor_list
t, c = symbols('t c')
ok = True
def check(name, cond, extra=''):
    global ok; ok &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra))

N = c*(c**2 - 4)*t**2 - 16*t + c**3 + 4*c
f = t**6 - 30*t**4 - 24*t**2 - 1
A = 4*(1 - t**4)*N**2; B = -16*t*(1 + t**2)**2*N**3
check('4A^3 + 27B^2 = -256 N_c^6 (1+t^2)^3 f(t)   (so Delta has the fibres of N_c^6, (1+t^2)^3 and f)',
      expand(4*A**3 + 27*B**2 + 256*N**6*(1 + t**2)**3*f) == 0)
check('f is squarefree, f(+-i) != 0', Poly(gcd(f, f.diff(t)), t).degree() == 0 and Poly(gcd(f, t**2 + 1), t).degree() == 0, '(f(i) = %s)' % f.subs(t, sympy.I))

R_f = factor(resultant(N, f, t)); R_i = factor(resultant(N, t**2 + 1, t)); D_N = factor(discriminant(N, t))
check('Res_t(N_c, f) = 64 (c^6+9c^4-16)^2 (c^6+36c^4-1024)', expand(R_f - 64*(c**6 + 9*c**4 - 16)**2*(c**6 + 36*c**4 - 1024)) == 0)
check('Res_t(N_c, t^2+1) = 64 (c^2+4)', expand(R_i - 64*(c**2 + 4)) == 0)
check('disc_t N_c = -4 (c^6 - 16c^2 - 64)', expand(D_N + 4*(c**6 - 16*c**2 - 64)) == 0)
for nm, expr in (('Res_t(N_c, f)', R_f), ('Res_t(N_c, t^2+1)', R_i), ('disc_t N_c', D_N)):
    rr = Poly(expr, c).ground_roots()
    check('%s has no rational root in c' % nm, rr == {}, '(degree %d)' % Poly(expr, c).degree())
check('each of the polynomials c^6+9c^4-16, c^6+36c^4-1024, c^6-16c^2-64, c^2+4 has no rational root (all of the above, factor by factor)',
      all(Poly(p, c).ground_roots() == {} for p in (c**6 + 9*c**4 - 16, c**6 + 36*c**4 - 1024, c**6 - 16*c**2 - 64, c**2 + 4)))

# valuations at t = +-i for generic c: a4 = 4(1-t^4)N^2, a6 = -16 t (1+t^2)^2 N^3 and N(+-i) != 0 (resultant != 0)
def mult(poly, factor_poly):
    k = 0; p = Poly(poly, t); q = Poly(factor_poly, t)
    while True:
        quo, rem = sympy.div(p, q)
        if rem.is_zero: k += 1; p = quo
        else: return k
check('at t = +-i: v(a4) = 1, v(a6) = 2, v(Delta) = 3  (type III)', (mult(A, t**2 + 1), mult(B, t**2 + 1), mult(expand(4*A**3 + 27*B**2), t**2 + 1)) == (1, 2, 3))

# at t = infinity, weights 8, 12, 24
def inf_data(cv):
    Ncv = Poly(N.subs(c, cv), t); Acv = Poly(expand(A.subs(c, cv)), t); Bcv = Poly(expand(B.subs(c, cv)), t); Dcv = Poly(expand((4*A**3 + 27*B**2).subs(c, cv)), t)
    return 8 - Acv.degree(), 12 - Bcv.degree(), 24 - Dcv.degree()
check('t = infinity, generic c (c = 1, 3): (v(a4), v(a6), v(Delta)) = (0, 1, 0), smooth fibre', all(inf_data(cv) == (0, 1, 0) for cv in (1, 3)))
check('t = infinity, c = 0, 2, -2: (v(a4), v(a6), v(Delta)) = (2, 4, 6), type I0*', all(inf_data(cv) == (2, 4, 6) for cv in (0, 2, -2)),
      '(%s)' % [inf_data(cv) for cv in (0, 2, -2)])

# the 18 values of c of F.44-F.46
cs = [Rational(x) for x in '2 13/9 -11/5 14/45 1 4 1/4 1/3 2/3 3/4 5/4 7/4 9/4 5/2 3 10/3 5 11/2'.split()]
check('the 18 values of c of F.44-F.46 avoid all collision polynomials',
      all(P.subs(c, cv) != 0 for cv in cs for P in (R_f, R_i, D_N)))

# numerical check of the collision structure (40 digits)
mp.mp.dps = 40
fn = lambda x: x**6 - 30*x**4 - 24*x**2 - 1
delta = lambda cc, a: -3*cc**2*(1 + a**2)**2 - 16*(1 - a**4)
r_res = lambda cc, a: 3*(cc*(1 + a**2))**2 + 4*(1 - a**4)
def alphas(cc): return mp.polyroots([cc*(cc**2 - 4), -16, cc**3 + 4*cc], maxsteps=300, extraprec=300)
def best(cc, fun):  # the root alpha of N_c at which |f| is smallest
    return min(alphas(cc), key=lambda a: abs(fn(a)))
c1 = mp.polyroots([1, 0, 36, 0, 0, 0, -1024], maxsteps=300, extraprec=300)[0]
a1 = best(c1, fn)
check('c^6+36c^4-1024 = 0: a root alpha of N_c is a root of f and delta(alpha) = 0', abs(fn(a1)) < 1e-30 and abs(delta(c1, a1)) < 1e-30, '(|f| = %.1e, |delta| = %.1e)' % (abs(fn(a1)), abs(delta(c1, a1))))
c2 = mp.polyroots([1, 0, 9, 0, 0, 0, -16], maxsteps=300, extraprec=300)[0]
a2 = best(c2, fn)
check('c^6+9c^4-16 = 0: a root alpha of N_c is a root of f and r = c(1+alpha^2) is a double root of the residue cubic (3r^2 + 4(1-alpha^4) = 0)',
      abs(fn(a2)) < 1e-30 and abs(r_res(c2, a2)) < 1e-30 and abs(delta(c2, a2)) > 1, '(|f| = %.1e, |3r^2+4(1-a^4)| = %.1e, |delta| = %.1e)' % (abs(fn(a2)), abs(r_res(c2, a2)), abs(delta(c2, a2))))
c3 = mp.mpc(0, 2); a3 = min(alphas(c3), key=lambda a: abs(a**2 + 1))
check('c^2+4 = 0 (c = 2i): a root alpha of N_c is i and delta(alpha) = 0, 3r^2+4(1-alpha^4) = 0', abs(a3**2 + 1) < 1e-30 and abs(delta(c3, a3)) < 1e-30 and abs(r_res(c3, a3)) < 1e-30)
print('ALL CHECKS PASS' if ok else 'SOME CHECK FAILED'); sys.exit(0 if ok else 1)
