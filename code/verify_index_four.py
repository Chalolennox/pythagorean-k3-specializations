#!/usr/bin/env python3
"""The index-four obstruction on C : y^2 = x^3 - 2x^2 + 2x, P = (1,1): exact identities, the descent lemma, and a scan.

Setting.  f(t) = t^6 - 30 t^4 - 24 t^2 - 1 (even: roots +-tau_j, tau_j^2 = roots of g(s) = s^3 - 30 s^2 - 24 s - 1).  Two counts of 'qualifying' roots t in F_p:
   T_p  (the original definition):  chi(2t(1-t^2)) = 1 and chi((1-t)(1+t^2)) = 1, arguments nonzero;
   S_p  : (1-t) is a nonzero square and (1-t)(1+t^2) is a square (the point with x = 1 - t exists and x is a square).
We prove below that T_p = 6 implies S_p = 6 and p = 1 (mod 24); the converse is false (145 primes with S_p = 6 versus 28 with T_p = 6 up to 1.5e7).
For p = 1 (mod 8) put i = sqrt(-1), chi = Legendre symbol, eta = chi(1+i), d_p = [C(F_p) : <P>], D_p = number of qualifying candidate points in 2C(F_p).

Checks:
  1. exact identities in Q(a,i)/(quartic): the two squares behind Theorem A      (sympy)
  2. the descent lemma: delta(2-torsion) and delta(P) for p = 1 (mod 8)           (direct computation, primes below 2e5)
  3. a scan of all primes <= X (default 3e6): for every prime with T_p = 6 and p = 1 (mod 8) check
       (a) prod_j chi(tau_j + i) = eta               (Theorem A)
       (b) (-1)^(D_p/2) = -eta                         (parity law)
       (c) d_p = 4  =>  eta = -1  and  D_p <= 4        (the conjecture)
Needs: python3, sympy, gcc.  Usage: python3 code/verify_index_four.py [X].   Exit status 0 = all checks pass."""
import sys, os, subprocess, tempfile, itertools, collections, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'index_four'))
import sympy
from sympy import symbols, expand, rem, I, Rational, sqrt_mod, primerange
from curve import group_order, point_order
OK = True
def check(name, cond, extra=''):
    global OK; OK &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra), flush=True)
def chi(a, p):
    a %= p; return 0 if a == 0 else (1 if pow(a, (p - 1)//2, p) == 1 else -1)

# ---- 1. exact identities ------------------------------------------------------------------------------------------------------
a = symbols('a'); i = I
quart = a**4 - 60*a**2 - 8*a + 996                      # a = -(sum of the roots of a 'face' F with prod(F) = -1)
b = (a**2 - 30)/2
h = lambda x: x**3 + a*x**2 + b*x + 1                    # h_F(t) = prod_{r in F} (t - r);  f(t) = -h_F(t) h_F(-t) modulo the quartic
t = symbols('t')
check('f(t) = -h(t) h(-t) modulo the quartic in a', rem(expand(-h(t)*h(-t) - (t**6 - 30*t**4 - 24*t**2 - 1)), quart, a) == 0)
check('face with prod(F) = -1:   -h(1) h(-i) (1+i) = w^2,  w = 1 - 14i + a + (i/2) a^2',
      rem(expand((1 - 14*i + a + (i/2)*a**2)**2 - expand(-h(1)*h(-i)*(1 + i))), quart, a) == 0)
check("face with prod(F) = +1:   -h(-1) h(i) (1+i) * 3 = w'^2,  w' = (9-4i) + (16/3) i a + (i/6) a^2 - (i/6) a^3  (F = -F', h = h_F')",
      rem(expand(((9 - 4*i) + Rational(16, 3)*i*a + Rational(1, 6)*i*a**2 - Rational(1, 6)*i*a**3)**2 - 3*expand(-h(-1)*h(i)*(1 + i))), quart, a) == 0)

# ---- 2. the descent lemma ---------------------------------------------------------------------------------------------------------
bad = 0; n = 0; seen_eta = set()
for p in primerange(17, 200000):
    if p % 8 != 1: continue
    n += 1; ii = sqrt_mod(p - 1, p); e1 = (1 + ii) % p; e2 = (1 - ii) % p; eta = chi(1 + ii, p); seen_eta.add(eta)
    roots = (0, e1, e2)
    def delta(x, y):                                       # (x - r1, x - r2, x - r3) with the usual rule at the 2-torsion points
        comps = [(x - r) % p for r in roots]
        if y % p == 0:
            k = roots.index(x % p); others = [(roots[k] - r) % p for j, r in enumerate(roots) if j != k]
            comps[k] = others[0]*others[1] % p
        return tuple(chi(c_, p) for c_ in comps)
    ok = (delta(0, 0) == (1, eta, eta) and delta(e1, 0) == (eta, eta, 1) and delta(e2, 0) == (eta, 1, eta) and delta(1, 1) == (1, 1, 1))
    bad += (not ok)
check('descent: delta(T0, T1, T2) = (1,eta,eta), (eta,eta,1), (eta,1,eta) and delta(P) trivial, at all %d primes p = 1 (mod 8) below 2e5 (both signs of eta occur: %s)' % (n, sorted(seen_eta)), bad == 0)

# ---- 3. the scan ----------------------------------------------------------------------------------------------------------------------
X = int(sys.argv[1]) if len(sys.argv) > 1 else 3000000
tmp = tempfile.mkdtemp(prefix='idx4_'); exe = os.path.join(tmp, 'scan')
subprocess.run(['gcc', '-O2', '-o', exe, os.path.join(HERE, 'index_four', 'scan.c')], check=True)
lines = subprocess.run([exe, str(X)], capture_output=True, text=True).stdout.split('\n')
rows = [tuple(map(int, l.split())) for l in lines if l.strip()]
q6 = [r for r in rows if r[2] == 6 and r[0] % 8 == 1]        # S_p = 6
t6 = [r for r in rows if r[3] == 6]                            # T_p = 6 (original definition)
def process(sel):
  results = []
  for (p, ta, tb, tc, c0, c1, c2) in sel:
    N = group_order(p)
    assert len(N) == 1, (p, N)
    N = N[0]; o = point_order((1, 1), N, p); d = N//o; ii = sqrt_mod(p - 1, p); eta = chi(1 + ii, p)
    D = 2*sum(1 for c_ in (c0, c1, c2) if c_ == 1)
    results.append((p, N, o, d, D, eta, c0*c1*c2))
  return results
results = process(q6)
resultsT = process(t6)
print('     primes p <= %d with p = 1 (mod 8): S_p = 6 at %d primes, T_p = 6 (original definition) at %d primes' % (X, len(results), len(resultsT)))
check('T_p = 6 implies S_p = 6 and p = 1 (mod 24)  (proved in the note, section 2.3)', all(r[0] in {x[0] for x in results} and r[0] % 24 == 1 for r in resultsT))
for label, res in (('S_p = 6', results), ('T_p = 6 (original definition)', resultsT)):
    check('[%s] (a) prod_j chi(tau_j + i) = eta = chi(1+i) at all %d primes (Theorem A)' % (label, len(res)), all(r[6] == r[5] for r in res))
    check('[%s] (b) parity law (-1)^(D_p/2) = -eta' % label, all(((-1)**(r[4]//2)) == -r[5] for r in res))
    check('[%s] (c) d_p = 4 implies eta = -1 and D_p <= 4 (D_p in {0, 4}); %d primes have d_p = 4' % (label, sum(1 for r in res if r[3] == 4)), all(r[5] == -1 and r[4] <= 4 for r in res if r[3] == 4))
    check('[%s] d_p/4 odd  <=>  eta = -1' % label, all(((r[3]//4) % 2 == 1) == (r[5] == -1) for r in res))
    print('     [%s] (d_p, D_p) counts:' % label, dict(sorted(collections.Counter((r[3], r[4]) for r in res).items())))
print('ALL CHECKS PASS' if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
