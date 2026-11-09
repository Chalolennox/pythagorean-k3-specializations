#!/usr/bin/env python3
"""The local sign at a prime dividing F_n as a quadratic character of t_n.

Definition.  For t = u/v in lowest terms and a prime p >= 5 with p | F(u,v) (F(u,v) = u^6 - 30u^4v^2 - 24u^2v^4 - v^6, so p does not divide v), the local root number of E_t at p
(multiplicative reduction) is  sigma_p = -(ab/p)  with  a = v^2 - u^2,  b = 2uv   (paper, section 4.1: w_p = -(-c_6/p) = -(ab/p)).   chi = Legendre symbol mod p, tau = t mod p.
Claim.  For p >= 5 dividing F(U_n, V_n) with t_n = 1 - x(nP) = U_n/V_n:
      sigma_p = -chi(-6) chi(tau)         (orbit nP),
and for the translated orbit t'_n = 1 - x(nP + T) = 1 - 2/x(nP):      sigma_p = -chi(-3) chi(tau').
Derivation (orbit nP): ab = 2 v^4 tau (1 - tau^2) mod p, so (ab/p) = chi(2 tau (1-tau)(1+tau)).  x = 1 - t_n = x(nP) is a rational square, so chi(1 - tau) = 1;  y^2 = x(1 + t^2) gives chi(1 + tau^2) = 1;
f(tau) = 0 and (1-t^2)^3 + 27 t^2 (1+t^2) = -f(t) give chi(1 - tau^2) = chi(-3) chi(1 + tau^2), hence chi(1 + tau) = chi(-3).  So (ab/p) = chi(2) chi(-3) chi(tau).
(Orbit nP + T: x' = 2/x is 2 times a square, so chi(1 - tau') = chi(2), chi(1 + tau'^2) = chi(2), chi(1 + tau') = chi(-3).)
Checks: (1) the formula at every prime of the complete factorizations (n = 2..12, both orbits); (2) at every prime p < 3e5 dividing F(U_n, V_n) for n = 2..40 (both orbits);
(3) the intermediate facts.   Needs python3 only.  Exit 0 = all pass."""
import sys, os, json, collections
from fractions import Fraction as Fr
sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OK = True
def check(name, cond, extra=''):
    global OK; OK &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra), flush=True)
def leg(a, p):
    a %= p; return 0 if a == 0 else (1 if pow(a, (p - 1)//2, p) == 1 else -1)
def add(P, Q):
    x1, y1 = P; x2, y2 = Q
    lam = (3*x1*x1 - 4*x1 + 2)/(2*y1) if x1 == x2 else (y2 - y1)/(x2 - x1)
    x3 = lam*lam + 2 - x1 - x2; return (x3, lam*(x1 - x3) - y1)
NMAX = 40
P = (Fr(1), Fr(1)); Q = P; pts = {1: P}
for n in range(2, NMAX + 1): Q = add(Q, P); pts[n] = Q
def tvalue(orbit, n):
    x = pts[n][0]; return 1 - x if orbit == 'nP' else 1 - 2/x
def sigma_crit(t, p):
    u, v = t.numerator, t.denominator; return -leg((v*v - u*u)*(2*u*v), p)
def sigma_form(orbit, t, p):
    u, v = t.numerator, t.denominator; tp = u*pow(v, -1, p) % p
    return (-leg(-6, p) if orbit == 'nP' else -leg(-3, p))*leg(tp, p)
def facts(orbit, t, p):
    u, v = t.numerator, t.denominator; tp = u*pow(v, -1, p) % p; x = (1 - tp) % p
    c1m = leg(1 - tp, p); c1p = leg(1 + tp, p); cq = leg(1 + tp*tp, p)
    if orbit == 'nP': return c1m == 1 and cq == 1 and c1p == leg(-3, p) and leg(1 - tp*tp, p) == leg(-3, p)
    return c1m == leg(2, p) and cq == leg(2, p) and c1p == leg(-3, p)
# (1) complete factorizations
data = json.load(open(os.path.join(ROOT, 'data', 'factorizations.json')))['entries']; cnt = collections.Counter(); ok1 = True; ok3 = True
for e in data:
    if e['status'] != 'complete' or not (2 <= e['n'] <= 12): continue
    t = tvalue(e['orbit'], e['n'])
    for ps in e['primes']:
        p = int(ps)
        if p < 5: continue
        ok1 &= (sigma_crit(t, p) == sigma_form(e['orbit'], t, p)); ok3 &= facts(e['orbit'], t, p); cnt[e['orbit']] += 1
check('(1) formula = criterion at every prime p >= 5 of the complete factorizations (n = 2..12): %s' % dict(cnt), ok1)
# (2) all primes p < 3e5 dividing F(U_n, V_n), n = 2..40
LIM = 300000; sieve = bytearray([1])*(LIM + 1); primes = []
for i in range(2, LIM + 1):
    if sieve[i]:
        primes.append(i)
        for j in range(i*i, LIM + 1, i): sieve[j] = 0
cnt2 = collections.Counter(); ok2 = True; byclass = collections.Counter(); ok4 = True
for orbit in ('nP', 'nP+T'):
    for n in range(2, NMAX + 1):
        t = tvalue(orbit, n); u, v = t.numerator, t.denominator
        N = u**6 - 30*u**4*v**2 - 24*u**2*v**4 - v**6
        for p in primes:
            if p < 5 or N % p: continue
            ok2 &= (sigma_crit(t, p) == sigma_form(orbit, t, p)); ok4 &= facts(orbit, t, p); cnt2[orbit] += 1; byclass[p % 24] += 1
check('(2) formula = criterion at every prime p in [5, 3e5) dividing F(U_n, V_n), n = 2..%d: %s; residues mod 24 occurring: %s' % (NMAX, dict(cnt2), sorted(byclass)), ok2)
check('(3) the intermediate facts (chi(1-tau), chi(1+tau^2), chi(1+tau) = chi(-3)) at all these primes', ok3 and ok4)
# the two candidates of a pair: chi(-tau) = chi(tau) for p = 1 (mod 4), so sigma(tau) = sigma(-tau) when both are candidates (formula only; no data needed)
print('ALL CHECKS PASS' if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
