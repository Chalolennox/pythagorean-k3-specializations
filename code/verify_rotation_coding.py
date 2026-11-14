#!/usr/bin/env python3
"""F.51 (a) and (c): the rotation coding of sign F_s along 1 + x(nP) and 1 + 2/x(nP), computed from the definitions (not fitted), and its exact consequences.
  Omega = int_0^inf dx / sqrt(x^3 - 2x^2 + 2x),  u(x) = int_x^inf dx' / (2 sqrt(x'^3 - 2x'^2 + 2x')),  theta = u(1)/Omega,  rho = u(x0)/Omega,  x0 = t0 - 1,  t0 = largest real root of D(t) = t^6 - 30t^4 - 24t^2 - 1.
Checks: D irreducible with exactly two real roots +-t0; x0 the unique positive root of D(1 + X); sign F_s versus the rotation coding for 1 <= n <= 330 (exact arithmetic);
closest approach of ||n theta|| to rho for n <= 10^6; PSLQ for a relation among 2 rho, theta, 1; the 27-lag disagreement frequency 2||27 theta||; the mean (1 - 4 rho)/3;
the identity  eps(1-x_n) eps(1-2/x_n) eps(1+x_n) eps(1+2/x_n) = -(-1)^n s_n s'_n  for 3 <= n <= 150.   Usage: python3 code/verify_rotation_coding.py   (full run about 2 minutes; --quick: the product identity only for 3 <= n <= 40 and the exact sign check only to n <= 120, about 30 s; exit 0 = all pass).  Needs sympy, mpmath, numpy."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mpmath import mp, mpf, quad, sqrt, inf, floor, pslq
from sympy import symbols, Poly, factor_list, real_roots
from mirror_projection_eps import eps, orbit
mp.dps = 40; OK = True; QUICK = '--quick' in sys.argv
def check(name, cond):
    global OK; OK = OK and bool(cond); print('%-4s %s' % ('OK' if cond else 'FAIL', name), flush=True)
t0_ = time.time()
f = lambda x: 1/(2*sqrt(x**3 - 2*x**2 + 2*x)); u = lambda x: quad(f, [x, x + 1, x + 10, x + 1000, inf])
Om = 2*quad(f, [0, 1, inf]); theta = u(mpf(1))/Om
T, X = symbols('t X'); D = Poly(T**6 - 30*T**4 - 24*T**2 - 1, T); Gp = Poly((1 + X)**6 - 30*(1 + X)**4 - 24*(1 + X)**2 - 1, X)
check('D(t) = t^6 - 30t^4 - 24t^2 - 1 is irreducible over Q', len(factor_list(D.as_expr())[1]) == 1)
rr = sorted(float(r) for r in real_roots(D)); check('D has exactly two real roots, +-t0 = %s' % rr, len(rr) == 2 and abs(rr[0] + rr[1]) < 1e-12)
t0 = mpf(str(max(r.evalf(40) for r in real_roots(D)))); x0 = t0 - 1; x1 = 2/x0; rho = u(x0)/Om
grr = sorted(float(r) for r in real_roots(Gp)); check('G_+(X) = D(1 + X) has exactly two real roots %s, one positive (x0 = %s)' % ([round(r, 6) for r in grr], mp.nstr(x0, 15)), len(grr) == 2 and grr[0] < 0 < grr[1])
print('     Omega = %s\n     theta = %s\n     rho   = %s\n     2 rho = %s' % (mp.nstr(Om, 25), mp.nstr(theta, 25), mp.nstr(rho, 25), mp.nstr(2*rho, 20)))
check('constants as stated in F.51 (Omega = 4.0364616539, theta = 0.29567987352534367, rho = 0.12509443218654407, 2 rho = 0.25018886)',
      abs(Om - mpf('4.0364616539')) < 1e-9 and abs(theta - mpf('0.29567987352534367')) < 1e-16 and abs(rho - mpf('0.12509443218654407')) < 1e-15 and abs(2*rho - mpf('0.25018886')) < 1e-8)
check('rho is the same along 1 + 2/x: u-length of {x < 2/x0} equals rho', abs(quad(f, [0, x1])/Om - rho) < 1e-18)
nmax = 120 if QUICK else 330; xs = orbit(nmax if not QUICK else 150)
sg = lambda t: 1 if t.numerator**6 - 30*t.numerator**4*t.denominator**2 - 24*t.numerator**2*t.denominator**4 - t.denominator**6 > 0 else -1
dist = lambda v: abs(v - floor(v + mpf(1)/2))
a1 = sum((dist(n*theta) < rho) == (sg(1 + xs[n - 1]) == 1) for n in range(1, nmax + 1)); a2 = sum((dist(n*theta - mpf(1)/2) < rho) == (sg(1 + 2/xs[n - 1]) == 1) for n in range(1, nmax + 1))
check('exact sign of F_s = rotation coding for 1 <= n <= %d: %d/%d along 1 + x(nP), %d/%d along 1 + 2/x(nP)' % (nmax, a1, nmax, a2, nmax), a1 == nmax and a2 == nmax)
th = float(theta); rh = float(rho); n = np.arange(1, 10**6 + 1); d = np.abs(((n*th + 0.5) % 1.0) - 0.5); mn = float(np.min(np.abs(d - rh)))
check('closest approach of ||n theta|| to rho for n <= 10^6: %.2e (> 0; x0 irrational of degree 6, x_n rational)' % mn, 1e-8 < mn < 1e-6)
check('PSLQ finds no integer relation a(2 rho) + b theta + c = 0 with coefficients <= 10^4', pslq([2*rho, theta, mpf(1)], maxcoeff=10**4, maxsteps=10**5) is None)
d27 = abs(27*theta - 8); check('||27 theta|| = %s < min(2 rho, 1 - 2 rho); disagreement frequency 2||27 theta|| = %s, agreement %s' % (mp.nstr(d27, 10), mp.nstr(2*d27, 10), mp.nstr(1 - 2*d27, 10)),
      d27 < min(2*rho, 1 - 2*rho) and abs(2*d27 - mpf('0.0332868')) < 1e-7)
# empirical frequencies from the coding itself (n <= 10^6)
s1 = np.where(d < rh, 1, -1); h1 = np.where(n % 3 == 0, 1, -1); e1 = h1*s1
check('empirical (n <= 10^6): mean of eps+ = %.4f vs (1 - 4 rho)/3 = %.4f; agreement of eps_n, eps_{n+27} = %.4f vs %.4f' % (e1[2:].mean(), float((1 - 4*rho)/3), (e1[:-27] == e1[27:]).mean(), float(1 - 2*d27)),
      abs(e1[2:].mean() - float((1 - 4*rho)/3)) < 2e-3 and abs((e1[:-27] == e1[27:]).mean() - float(1 - 2*d27)) < 2e-3)
cf = []; a = theta
for _ in range(10):
    ia = int(floor(a)); cf.append(ia); fr = a - ia
    if fr < mpf(10)**-20: break
    a = 1/fr
check('continued fraction of theta = %s (convergent 8/27)' % cf, cf[:9] == [0, 3, 2, 1, 1, 1, 1, 1, 1])
ok = tot = 0
NP = 40 if QUICK else 150
for m in range(3, NP + 1):
    x = xs[m - 1]; prod = eps(1 - x)*eps(1 - 2/x)*eps(1 + x)*eps(1 + 2/x); tot += 1; ok += (prod == -((-1)**m)*sg(1 + x)*sg(1 + 2/x))
check('eps(1-x_n) eps(1-2/x_n) eps(1+x_n) eps(1+2/x_n) = -(-1)^n s_n s\'_n for %d of %d values (3 <= n <= %d)' % (ok, tot, NP), ok == tot == NP - 2)
print('ALL CHECKS PASS (%.0f s)' % (time.time() - t0_) if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
