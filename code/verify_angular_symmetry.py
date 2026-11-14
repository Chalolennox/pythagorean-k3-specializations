#!/usr/bin/env python3
"""Angular Haar symmetry on C: y^2 = x^3 - 2x^2 + 2x (note: angular_symmetry_proof.md).  z(Q) = (1+it)/(1-it), t = 1 - x(Q), z(Q+T) = -i conj z(Q).
Exact: the identity for rational t, x(Q+T) = 2/x on the group law, swap of O and T.  Numerical: explicit density, symmetry, moments mu_1..mu_4, orbit averages along nP."""
from fractions import Fraction as Fr
import random, warnings, numpy as np
warnings.filterwarnings("ignore")
from scipy.special import ellipj, ellipk
fails = 0
def check(n, ok, e=''):
    global fails; fails += (not ok); print(('PASS ' if ok else 'FAIL ')+n+(' '+e if e else ''))
random.seed(1)
def zt(t): d = 1+t*t; return ((1-t*t)/d, 2*t/d)
ok = True
for _ in range(2000):
    t = Fr(random.randint(-50, 50), random.randint(1, 50))
    if t == 1: continue
    a, b = zt(t); c, d = zt(-(1+t)/(1-t)); ok &= (c == -b and d == -a)
check('z(tau(t)) = -i conj z(t) exactly on 2000 random rationals', ok)
def add(P, Q):
    if P is None: return Q
    if Q is None: return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2:
        if y1+y2 == 0: return None
        l = (3*x1*x1-4*x1+2)/(2*y1)
    else: l = (y2-y1)/(x2-x1)
    x3 = l*l+2-x1-x2; return (x3, l*(x1-x3)-y1)
P = (Fr(1), Fr(1)); T = (Fr(0), Fr(0)); Q = P; ok = add(P, P) == (Fr(1, 4), Fr(-5, 8)); ok2 = True
for n in range(1, 25):
    S = add(Q, T); ok2 &= (S[0]*Q[0] == 2); Q = add(Q, P)
check('2P = (1/4,-5/8) (non-integral, so P and 2P are not torsion by Lutz-Nagell)', ok)
check('x(nP+T) x(nP) = 2 for n = 1..24', ok2)
check('endpoints: z(O) = -1, z(T) = i, and -i conj z(O) = i, -i conj z(T) = -1', (-1j*np.conj(-1+0j) == 1j) and (-1j*np.conj(1j) == -1+0j))
k2 = (2+np.sqrt(2))/4; K = ellipk(k2); Om = 2*K/2**0.25
g = lambda th: 1/(2**1.25*Om*np.sqrt(np.cos(th/2)*np.cos(th/2+np.pi/4)))
from scipy.integrate import quad
def integ(fun):                       # integrable 1/sqrt endpoint singularities at -pi and pi/2: QUADPACK handles them
    kw = dict(epsabs=1e-13, epsrel=1e-13, limit=400)
    return quad(lambda x: fun(x).real, -np.pi, np.pi/2, **kw)[0]+1j*quad(lambda x: fun(x).imag, -np.pi, np.pi/2, **kw)[0]
mass = integ(lambda x: g(x)+0j).real; check('density g integrates to 1', abs(mass-1) < 1e-10, '(%.13f)' % mass)
pts = np.array([-3.0, -2.2, -1.0, 0.3, 1.2]); check('g(theta) = g(-theta - pi/2)', np.allclose(g(pts), g(-pts-np.pi/2)))
mu = {k: integ(lambda x: g(x)*np.exp(1j*k*x)) for k in range(1, 7)}
quoted = {1: -0.03492019045+0.03492019045j, 2: 0.28677307940j, 3: -0.25037057779-0.25037057779j, 4: 0.22436879093}
check('mu_1..mu_4 reproduce the quoted values', all(abs(mu[k]-quoted[k]) < 2e-10 for k in quoted), 'max dev %.1e' % max(abs(mu[k]-quoted[k]) for k in quoted))
check('mu_k = (-i)^k conj(mu_k) for k = 1..6', all(abs(mu[k]-(-1j)**k*np.conj(mu[k])) < 1e-10 for k in mu))
print('  mu_5 = %.10f%+.10fi   mu_6 = %.10f%+.10fi' % (mu[5].real, mu[5].imag, mu[6].real, mu[6].imag))
theta = 0.29567987352534367
for N in (10**4, 10**6):
    n = np.arange(1, N+1); d = np.abs(((n*theta+0.5) % 1.0)-0.5); cn = ellipj(4*K*d, k2)[1]
    xs = np.sqrt(2)*(1+cn)/(1-cn); zz = (1+1j*(1-xs))/(1-1j*(1-xs))
    dev = max(abs(np.mean(zz**k)-mu[k]) for k in (1, 2, 3, 4)); check('orbit averages (N = %d) approach mu_k' % N, dev < (3e-4 if N == 10**4 else 5e-6), 'max dev %.1e' % dev)
print('Not tested and not claimed: any pointwise symmetry of the finite orbit, any root-number consequence.')
print('FAILURES: %d' % fails); raise SystemExit(1 if fails else 0)
