#!/usr/bin/env python3
"""Checks of the memorandum 'Translation by 18P, bad-fiber disjointness, and the infinite-nonneutral-prime obstruction' (11 Nov 2026).
Orbit Q_n = nP + T on C : y^2 = x^3 - 2x^2 + 2x, t_n = 1 - x(Q_n).  g(t) = t^6 - 30t^4 - 24t^2 - 1,  F(t) = 4a^3 + 27 b^2 c.
What is checked:  A the homogeneous identity; B,C the reduction mod 7 (Theorem 1);  D the factorization and the neutrality at n = 3 (Section 6);
  E,F,G the sign factor f(n): period 18 holds, but the memo's f(n) is the repository's f(t_{n+1}), so f(3) = -1 (not +1), W(E_{31/49}) = -1;
  H the genuine neutral anchors (t = 1 on nP + T; t = 0 and n = 9 on nP);  I Theorem 2 (fixed-gap common primes), J the recurrence of Section 5;
  K,L,M f(t_n) = +1 for every n = 0 (mod 6) (Lemma: f(t) = +1 when v_2(t-1) >= 3 and v_3(t-1) >= 2; valuations of t_n - 1);  N the anchor-avoidance statement
  Q_{M L(S) j} = T mod p for p in S, with L(S) = lcm ord_p(P)/gcd(ord_p(P), M), M = 18 and M = 6.
Needs python3, sympy; imports the local factor f(t) from code/scripts_as_run/eps.py and reads data/factorizations.json.  Exit 0 = all pass."""
import sys, os, json, re, collections, random
from fractions import Fraction as Fr
from math import gcd
sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, 'scripts_as_run'))
from eps import pieces, triple, jac
from sympy import symbols, Poly, expand, factorint, isprime, primerange
OK = True
def check(name, cond, extra=''):
    global OK; OK &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra), flush=True)
def add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) == 0: return None
    lam = (3*x1*x1 - 4*x1 + 2)/(2*y1) if x1 == x2 else (y2 - y1)/(x2 - x1)
    x3 = lam*lam + 2 - x1 - x2; return (x3, lam*(x1 - x3) - y1)
P = (Fr(1), Fr(1)); T = (Fr(0), Fr(0)); NP = {}; Q = None
for n in range(1, 80): Q = add(Q, P); NP[n] = Q
tPT = lambda n: Fr(1) if n == 0 else 1 - add(NP[n], T)[0]          # t_n for Q_n = nP + T (t_0 = 1)
tP = lambda n: 1 - NP[n][0]                                          # t_n for nP
def Fabc(t):
    u, v = t.numerator, t.denominator; a = v*v - u*u; b = 2*u*v; c = v*v + u*u; d = gcd(gcd(a, b), c)
    a, b, c = a//d, b//d, c//d; return a, b, c, 4*a**3 + 27*b*b*c
# A. homogeneous identity
u, v, t = symbols('u v t'); g = t**6 - 30*t**4 - 24*t**2 - 1
check('A  4(v^2-u^2)^3 + 27(2uv)^2(v^2+u^2) = -4 (u^6 - 30u^4v^2 - 24u^2v^4 - v^6) = -4 v^6 g(u/v)', expand(4*(v*v - u*u)**3 + 27*(2*u*v)**2*(v*v + u*u) + 4*(u**6 - 30*u**4*v**2 - 24*u**2*v**4 - v**6)) == 0)
# B, C. reduction mod 7
P3 = None
for _ in range(3): P3 = add(P3, P)
red = lambda q: (q.numerator*pow(q.denominator, -1, 7)) % 7
check('B  3P = (49/9, -287/27) and 3P = T = (0,0) mod 7', P3 == (Fr(49, 9), Fr(-287, 27)) and (red(P3[0]), red(P3[1])) == (0, 0))
def addp(A, B, p):
    if A is None: return B
    if B is None: return A
    if A[0] == B[0] and (A[1] + B[1]) % p == 0: return None
    l = ((3*A[0]*A[0] - 4*A[0] + 2)*pow(2*A[1], -1, p) if A[0] == B[0] else (B[1] - A[1])*pow(B[0] - A[0], -1, p)) % p
    x3 = (l*l + 2 - A[0] - B[0]) % p; return (x3, (l*(A[0] - x3) - A[1]) % p)
def order_p(p):
    X = (1, 1); k = 1
    while X is not None: X = addp(X, (1, 1), p); k += 1
    return k
check('B  ord_7(P) = 6, so 6kP = O mod 7 (the memo\'s strengthening) and 18kP = O mod 7', order_p(7) == 6)
g7 = Poly(g, t, modulus=7)
check('C  g mod 7 = (t-3)(t+3)(t^2-2t+2)(t^2+2t+2) is squarefree and coprime to (1-t)(1+t^2)',
      len(g7.factor_list()[1]) == 4 and all(e == 1 for _, e in g7.factor_list()[1]) and g7.gcd(Poly((1 - t)*(1 + t**2), t, modulus=7)).degree() == 0)
# D. n = 3
t3 = tPT(3); a, b, c, F3 = Fabc(t3); fac = factorint(F3)
check('D  t_3 = 31/49, (a,b,c) = (720,1519,1681), F = 106217185707 = 3^3 23 83 2060749, all three Legendre symbols (ab/p) = -1  (B_3 empty, s(3) = 0)',
      t3 == Fr(31, 49) and (a, b, c) == (720, 1519, 1681) and F3 == 106217185707 and fac == {3: 3, 23: 1, 83: 1, 2060749: 1} and isprime(2060749) and all(jac(a*b, p) == -1 for p in (23, 83, 2060749)))
# E, F, G. the sign factor
fc = {n: pieces(tPT(n))[0] for n in range(0, 61)}
check('E  the local factor f(t_n) along nP + T has period 18 (n = 1..60)', all(fc[n] == fc[n + 18] for n in range(1, 43)))
w3 = [1, -1, 1, 1, 1, 1, -1, 1, 1]; memo = lambda n: -((-1)**n)*w3[n % 9]
check("F  the memo's f(n) = -(-1)^n w3(n mod 9) equals the repository's f(t_{n+1}) for n = 0..59 (index shift by one) and NOT f(t_n) (differs at n = 3, 4, 5, 8, 9, ...)",
      all(memo(n) == fc[n + 1] for n in range(0, 60)) and memo(3) == +1 and fc[3] == -1)
sc = sum(1 for p in fac if p >= 5 and jac(a*b, p) == 1); W3 = fc[3]*(-1)**sc
check('G  f(t_3) = -1, s(3) = 0, hence W(E_{31/49}) = -1 (not +1)', fc[3] == -1 and sc == 0 and W3 == -1)
paper = re.sub(r'\s+', ' ', open(os.path.join(ROOT, 'paper', 'paper.md'), encoding='utf-8').read())
check("G  the paper's table already records 3P + T = 31/49: '23 N, 83 N, 2060749 N | 0 (f = -1) | -1'", '23 N, 83 N, 2060749 N | 0 (f = −1) | −1' in paper)
# H. anchors
a0, b0, c0, F0 = Fabc(Fr(1)); a1, b1, c1, F1 = Fabc(Fr(0))
check('H  Q_0 = T (t = 1): F = 27, no prime >= 5, f(t_0) = +1, so W(E_1) = +1 (recorded in the paper); f = +1 also at n = 18, 36, 54',
      F0 == 27 and fc[0] == 1 and all(fc[n] == 1 for n in (18, 36, 54)))
check('H  nP orbit: t_1 = 0 has F = 4 (no prime >= 5); f(t_n) = +1 for all n = 1..60 (Appendix B)', F1 == 4 and all(pieces(tP(n))[0] == 1 for n in range(1, 61)))
data = json.load(open(os.path.join(ROOT, 'data', 'factorizations.json')))['entries']; anchors = []
for e in data:
    if e['status'] != 'complete' or e['n'] > 12: continue
    tt = tPT(e['n']) if e['orbit'] == 'nP+T' else tP(e['n']); aa, bb, cc, _ = Fabc(tt); ff = pieces(tt)[0]
    s = sum(1 for p in map(int, e['primes']) if p >= 5 and jac(aa*bb, p) == 1)
    if ff == 1 and s == 0: anchors.append((e['orbit'], e['n']))
check('H  among the complete factorizations (n <= 12) the indices with f = +1 and s = 0 are exactly: %s  (none on nP + T)' % anchors, anchors == [('nP', 9)])
# I. Theorem 2: common primes at fixed gaps (orbit nP + T)
def supp(N):
    N = abs(N)
    for p in (2, 3):
        while N % p == 0: N //= p
    return N
Fv = lambda n: (lambda tt: tt.numerator**6 - 30*tt.numerator**4*tt.denominator**2 - 24*tt.numerator**2*tt.denominator**4 - tt.denominator**6)(tPT(n))
common = {}
for j in (1, 2, 3):
    cs = set()
    for n in range(0, 40):
        if n + 18*j > 79: break
        gg = gcd(supp(Fv(n)), supp(Fv(n + 18*j)))
        if gg > 1: cs |= set(factorint(gg))
    common[j] = sorted(cs)
check('I  common primes >= 5 of F(t_n), F(t_{n+18j}) for n < 40: %s  (finite and small, as in Theorem 2)' % common, all(len(v) <= 3 for v in common.values()))
# J. recurrence of Section 5
bad = tested = 0
for p in primerange(5, 60):
    r_p = order_p(p); m_p = r_p//gcd(r_p, 18)
    for r in range(0, 8):
        n1, n2 = r + 18, r + 18*(1 + m_p)
        if n2 > 79: continue
        def red_pt(n):
            R = T if n == 0 else add(NP[n], T)
            if R is None or R[0].denominator % p == 0: return 'inf'
            return (R[0].numerator*pow(R[0].denominator, -1, p) % p, R[1].numerator*pow(R[1].denominator, -1, p) % p)
        tested += 1; bad += (red_pt(n1) != red_pt(n2))
check('J  Q_{r+18(k+m_p)} = Q_{r+18k} mod p for m_p = ord_p(P)/gcd(ord_p(P), 18): %d cases, %d failures' % (tested, bad), tested > 0 and bad == 0)

# K. valuations of t_n - 1 along nP + T:  v_2 = 1 + 2 v_2(n) (n even), v_3 = 2 v_3(n) (3 | n)   (F.22: v_p(D_n) = v_p(n), x(nP + T) = 2/x(nP))
def val(q, p):
    q = Fr(q)
    if q == 0: return 10**9
    k = 0; a_, b_ = q.numerator, q.denominator
    while a_ % p == 0: a_ //= p; k += 1
    while b_ % p == 0: b_ //= p; k -= 1
    return k
check('K  v_2(t_n - 1) = 1 + 2 v_2(n) for even n and v_3(t_n - 1) = 2 v_3(n) for 3 | n (n <= 79)',
      all(val(tPT(n) - 1, 2) == 1 + 2*val(n, 2) for n in range(2, 80, 2)) and all(val(tPT(n) - 1, 3) == 2*val(n, 3) for n in range(3, 80, 3)))
# L. Lemma:  f(t) = -w2 w3 (2/|c|) = +1 whenever v_2(t-1) >= 3 and v_3(t-1) >= 2.
#    By hand: t = 1 + e;  (a/c, b/c) = (-e(1 + e/2)/(1 + e + e^2/2), (1+e)/(1+e+e^2/2)) = (-e, 1) mod 32, so (A16, B16) in {(0,1), (8,1)} (both in the list W2): w2 = -1;
#    c = v^2 (1 + e + e^2/2) = 1 mod 8: (2/|c|) = +1;  (A9, B9) = (0, 1) != (3, 8): w3 = +1;  hence f = -(-1)(+1)(+1) = +1.
random.seed(5); nsamp = 0; allone = True
for _ in range(2000):
    r = random.randint(-10**6, 10**6) or 1; sden = random.choice([k for k in range(1, 5000) if k % 2 and k % 3]); tt = 1 + Fr(72*r, sden)
    if tt.numerator == 0: continue
    nsamp += 1; allone &= (pieces(tt)[0] == 1)
check('L  Lemma f(t) = +1 for v_2(t-1) >= 3, v_3(t-1) >= 2: %d random rationals t = 1 + 72r/s, gcd(s,6) = 1, all give f = +1; just outside (t = 5 mod 8) f = -1' % nsamp,
      allone and all(pieces(1 + Fr(36*k, 5))[0] == -1 for k in (1, 3, 5, 7, 9, 11)))
check('M  hence f(t_n) = +1 for every n = 0 (mod 6) on nP + T (n = 6, 12, ..., 78): the class n = 0 (mod 18) has f = +1 without any periodicity input', all(fc[n] == 1 for n in (6, 12, 18, 24, 30, 36, 42, 48, 54, 60)) and all(pieces(tPT(n))[0] == 1 for n in range(6, 79, 6)))
# N. anchor avoidance:  Q_{M L j} = T mod p for all p in S,  L(S) = lcm_p ord_p(P)/gcd(ord_p(P), M);  t = 1 mod p and F(1) = 27, so p does not divide F
def mulp(k, A, p):
    R = None
    while k:
        if k & 1: R = addp(R, A, p)
        A = addp(A, A, p); k >>= 1
    return R
from math import lcm
okN = True; info = {}
for M_ in (18, 6):
    S = list(primerange(5, 101)); orders = {p: order_p(p) for p in S}
    L = 1
    for p in S: L = lcm(L, orders[p]//gcd(orders[p], M_))
    info[M_] = L
    for j in (1, 2):
        for p in S:
            okN &= (mulp(M_*L*j, (1, 1), p) is None)               # M L j P = O mod p, so Q = M L j P + T = T mod p, i.e. t = 1 mod p, F(1) = 27 prime to p
check('N  S = primes in [5, 100]: M L(S) j P = O mod p for all p in S (M = 18: L = %d; M = 6: L = %d; j = 1, 2), so no p in S divides F(t_{M L j}) (t = 1 mod p, F(1) = 27)' % (info[18], info[6]), okN)
print('ALL CHECKS PASS' if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
