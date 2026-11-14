#!/usr/bin/env python3
"""The sign of F_n = 4a^3 + 27 b^2 c = -4 Phi(psi_{n-1} psi_{n+1}, psi_n^2) as an exact coding of the rotation by theta on C(R) / (Omega Z), made fully explicit.
Normalisation of F.51 (a):  omega = dx/(2y),  Omega = int_0^oo dx / sqrt(x^3 - 2x^2 + 2x),  u(x) = int_x^oo dx'/(2 sqrt(x'^3 - 2x'^2 + 2x')),  lambda(Q) = +-u(x(Q)) in R/Omega Z,  theta = u(1)/Omega.
New here:  t0 = largest real root of H(t) = t^6 - 30t^4 - 24t^2 - 1,  c1 = 1 + t0 = 6.548041...,  rho1 = u(c1)/Omega;  closed forms with the modulus k = cos(pi/8):
    Omega = 2 K(k) / 2^(1/4),    u(c)/Omega = F(phi_c, k) / (4 K(k)),    cos(phi_c) = (c - sqrt 2)/(c + sqrt 2).
Statements checked (n >= 2, ||.|| = distance to the nearest integer, theta_n = ||n theta||, theta'_n = ||n theta + 1/2|| = 1/2 - theta_n):
  (1) sign F_n = -1  <=>  theta_n < rho1;   sign G_n = -1  <=>  theta'_n < rho1  (G_n the same sextic along nP + T);   the two never occur together;
  (2) the four real classes (sign U, sign(V + U), sign F_s) of t_n = U/V:  theta_n > theta: (+,+,-);  1/2 - theta < theta_n < theta: (-,+,-);  rho1 < theta_n < 1/2 - theta: (-,-,-);  theta_n < rho1: (-,-,+);  the same for t'_n with theta'_n;
  (3) the breakpoints are theta (x = 1), 1/2 - theta (x = 2, the half-turn: u(2)/Omega = 1/2 - theta), rho1 (x = c1), and 1/2 - rho1 is the image of c1 under x -> 2/x;
  (4) first returns of {n : F_n < 0}: at most three gap values (three-distance theorem), computed exactly.
Usage: python3 code/rotation_coding_F_n.py [--quick]   (about a minute; --quick about 10 s; exit 0 = all checks pass).  Needs mpmath, sympy, numpy and code/mirror_projection_eps.py.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mpmath import mp, mpf, quad, sqrt, inf, ellipk, ellipf, acos, floor
from sympy import symbols, Poly, real_roots
mp.dps = 40; QUICK = '--quick' in sys.argv; OK = True
def check(name, cond):
    global OK; OK = OK and bool(cond); print('%-4s %s' % ('OK' if cond else 'FAIL', name), flush=True)
t_start = time.time(); sys.set_int_max_str_digits(0)
f = lambda x: 1/(2*sqrt(x**3 - 2*x**2 + 2*x)); u = lambda c: quad(f, [c, c + 1, c + 10, c + 1000, inf])
Om = 2*quad(f, [0, 1, inf]); theta = u(mpf(1))/Om
T = symbols('t'); rr = sorted(real_roots(Poly(T**6 - 30*T**4 - 24*T**2 - 1, T))); t0 = mpf(str(rr[-1].evalf(40))); c1 = 1 + t0; rho1 = u(c1)/Om
check('H has exactly two real roots +-t0, t0 = %s; D(1 - X) has the unique positive root X = c1 = 1 + t0 = %s' % (mp.nstr(t0, 15), mp.nstr(c1, 15)), len(rr) == 2)
# closed forms
m = (2 + sqrt(2))/4; K = ellipk(m); A = sqrt(2); ph = lambda c: acos((c - A)/(c + A)); uc = lambda c: ellipf(ph(c), m)/(4*K)
check('closed forms with k = cos(pi/8): Omega = 2K(k)/2^(1/4) = %s, theta = F(phi_1,k)/(4K) = %s, rho1 = F(phi_c1,k)/(4K) = %s' % (mp.nstr(Om, 20), mp.nstr(theta, 20), mp.nstr(rho1, 20)),
      abs(Om - 2*K/mpf(2)**mpf('0.25')) < 1e-20 and abs(theta - uc(mpf(1))) < 1e-20 and abs(rho1 - uc(c1)) < 1e-20)
check('half-turn as an identity: cos(phi_2) = -cos(phi_1) (phi_c: x = c), hence u(2)/Omega = 1/2 - theta = %s; and u(2/c1)/Omega = 1/2 - rho1 = %s' % (mp.nstr(mpf(1)/2 - theta, 15), mp.nstr(mpf(1)/2 - rho1, 15)),
      abs(ph(mpf(2)) + ph(mpf(1)) - mp.pi) < 1e-30 and abs(u(mpf(2))/Om - (mpf(1)/2 - theta)) < 1e-20 and abs(u(2/c1)/Om - (mpf(1)/2 - rho1)) < 1e-20)
order = [rho1, mpf(1)/2 - theta, theta, mpf(1)/2]; check('breakpoints in ||n theta|| (0 < ... < 1/2): rho1 = %s < 1/2 - theta = %s < theta = %s; rho1 < 1/4 (so the arcs of F_n < 0 and G_n < 0 are disjoint)' % tuple(mp.nstr(v, 10) for v in order[:3]),
      all(order[i] < order[i + 1] for i in range(3)) and rho1 < mpf(1)/4)
# exact signs
from mirror_projection_eps import orbit
NV = 60 if QUICK else 400; W = {0: 0, 1: 1, 2: 2, 3: 3, 4: -20}
def psi(n):
    if n < 0: return -psi(-n)
    if n in W: return W[n]
    if n % 2: j = (n - 1)//2; W[n] = psi(j + 2)*psi(j)**3 - psi(j - 1)*psi(j + 1)**3
    else: j = n//2; W[n] = psi(j)*(psi(j + 2)*psi(j - 1)**2 - psi(j - 2)*psi(j + 1)**2)//2
    return W[n]
Phi = lambda X, Y: X**6 - 30*X**4*Y**2 - 24*X**2*Y**4 - Y**6
sg = lambda v: 1 if v > 0 else -1
dist = lambda v: abs(v - floor(v + mpf(1)/2))
bad_sign = bad_cls = both_neg = nneg = nGneg = nprod = 0; seq = []
for n in range(2, NV + 1):
    U, V = psi(n - 1)*psi(n + 1), psi(n)**2; Aa = V - U; U2, V2 = Aa - 2*V, Aa      # t_n = U/V; t'_n = (A - 2B^2)/A with A = V - U, B^2 = V
    Fn = -4*Phi(U, V); Gn = -4*Phi(U2, V2); th_n = dist(n*theta); th2 = dist(n*theta + mpf(1)/2)
    assert Fn == 4*(V*V - U*U)**3 + 27*(2*U*V)**2*(V*V + U*U)                                  # d_n = 1 and F_n = 4a^3 + 27b^2c
    bad_sign += ((sg(Fn) == -1) != (th_n < rho1)) + ((sg(Gn) == -1) != (th2 < rho1)); both_neg += (Fn < 0 and Gn < 0); nneg += (Fn < 0); nGneg += (Gn < 0); nprod += (Fn*Gn < 0); seq.append(Fn < 0)
    def pred(d): return (1, 1, -1) if d > theta else (-1, 1, -1) if d > mpf(1)/2 - theta else (-1, -1, -1) if d > rho1 else (-1, -1, 1)
    bad_cls += (pred(th_n) != (sg(U), sg(V + U), sg(Phi(U, V)))) + (pred(th2) != (sg(U2), sg(V2 + U2), sg(Phi(U2, V2))))
check('exact: sign F_n = -1 iff theta_n < rho1, and sign G_n = -1 iff theta\'_n < rho1, for 2 <= n <= %d (%d disagreements); F_n < 0 and G_n < 0 never together (%d cases)' % (NV, bad_sign, both_neg), bad_sign == 0 and both_neg == 0)
check('exact: the four real classes (sign U, sign(V + U), sign F_s) of t_n and t\'_n agree with the position of theta_n (resp. theta\'_n) relative to rho1 < 1/2 - theta < theta, 2 <= n <= %d (%d disagreements)' % (NV, bad_cls), bad_cls == 0)
check('exact densities for 2 <= n <= %d: F_n < 0 for %d of %d (%.4f), 2 rho1 = %.4f; G_n < 0 for %d (%.4f); F_n G_n < 0 for %d (%.4f), 4 rho1 = %.4f' % (NV, nneg, NV - 1, nneg/(NV - 1), float(2*rho1), nGneg, nGneg/(NV - 1), nprod, nprod/(NV - 1), float(4*rho1)),
      abs(nneg/(NV - 1) - float(2*rho1)) < 0.03 and abs(nprod/(NV - 1) - float(4*rho1)) < 0.04)
print('     F_n < 0 for n in', [n for n, b in zip(range(2, NV + 1), seq) if b][:16], '...')
# closest approach to the breakpoints (floating point coding is reliable if the distance is far above 1e-12)
N = 10**6; nn = np.arange(1, N + 1); d = np.abs(((nn*float(theta) + 0.5) % 1.0) - 0.5); bp = [float(rho1), float(mpf(1)/2 - theta), float(theta)]
mins = [float(np.min(np.abs(d[1:] - b))) for b in bp]
check('closest approach of theta_n to the breakpoints rho1, 1/2 - theta, theta for 2 <= n <= 10^6: %s (all > 1e-9, no boundary case; x = 1 and x = 2 are not x(nP), n >= 2, and c1 is irrational)' % ['%.1e' % v for v in mins], all(v > 1e-9 for v in mins))
# first returns to the arc theta_n < rho1: exact breakpoints
th_f = theta; r_f = rho1; pts = {mpf(-1)*r_f, r_f}
for k in range(1, 60):
    for s in (-1, 1): pts.add((s*r_f - k*th_f + mpf(1)/2) % 1 - mpf(1)/2)
inside = sorted(v for v in pts if -r_f <= v <= r_f); gaps = {}
def first_return(x):
    for k in range(1, 400):
        if dist(x + k*th_f) < r_f: return k
for a, b in zip(inside, inside[1:]):
    if b - a > mpf(10)**-25: g = first_return((a + b)/2); gaps[g] = gaps.get(g, 0) + (b - a)/(2*r_f)
gl = sorted(gaps); check('first returns to {theta_n < rho1}: exactly %d gap values %s with frequencies %s' % (len(gl), gl, [mp.nstr(gaps[g], 8) for g in gl]), len(gl) <= 3 and abs(sum(gaps.values()) - 1) < 1e-20)
check('three-distance theorem: the largest gap is the sum of the other two (%s)' % gl, len(gl) == 3 and gl[2] == gl[0] + gl[1])
s_all = np.where(d < float(rho1))[0] + 1; dg = np.diff(s_all); emp = {int(g): float((dg == g).mean()) for g in np.unique(dg)}
check('empirical gap frequencies for the coding up to n <= 10^6: %s (theory %s)' % ({g: round(v, 5) for g, v in emp.items()}, {g: round(float(gaps[g]), 5) for g in gl}), set(emp) == set(gl) and all(abs(emp[g] - float(gaps[g])) < 2e-3 for g in gl))
ex = [n for n, b in zip(range(2, NV + 1), seq) if b]; exg = sorted(set(np.diff(ex).tolist())); check('exact gaps between consecutive n with F_n < 0 (n <= %d): %s' % (NV, exg), set(exg) <= set(gl))
cf = []; a = theta
for _ in range(12):
    ia = int(floor(a)); cf.append(ia); fr = a - ia
    if fr < mpf(10)**-25: break
    a = 1/fr
q = [1, cf[1]]
for a_ in cf[2:]: q.append(a_*q[-1] + q[-2])
print('     continued fraction of theta = %s; convergent denominators q_k = %s' % (cf, q))
print('     Omega = %s\n     theta = %s\n     rho1  = %s   (2 rho1 = %s, 4 rho1 = %s)\n     1/2 - theta = %s' % (mp.nstr(Om, 25), mp.nstr(theta, 25), mp.nstr(rho1, 25), mp.nstr(2*rho1, 12), mp.nstr(4*rho1, 12), mp.nstr(mpf(1)/2 - theta, 20)))
print('ALL CHECKS PASS (%.0f s)' % (time.time() - t_start) if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
