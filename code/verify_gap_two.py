#!/usr/bin/env python3
"""Gap-two coincidences of the qualifying-prime sets (notes/REVIEW_2026-11-17_gap_two_dossier.md).

Curve C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), f(t) = t^6 - 30t^4 - 24t^2 - 1, t_n = 1 - x(nP) or 1 - x(nP + T).
A prime p >= 5 is in Q_n if p | F_n and (a_n b_n / p) = +1; necessary and checked here: t_n mod p is a *qualifying root*
(F.57 Definitions: 1 + a^2 != 0, q(a) and r(a) non-zero squares, and 1 - a a square when (2/p) = +1).

Checks (one PASS line each, exit status 1 on any failure; standard library only):
  1  the gap-two relation G2(t,u) from the consecutive relation Psi holds exactly for (t_n, t_{n+2}), n = 0..8, both branches
  2  G2(t,t) = 16 t (t+1) (t^2 - 4t + 5)  (the 2-torsion midpoint mechanism)
  3  exact norm of G2 on Q[t,u]/(f(t), f(u)) = 2^42 3^27 47^2 947^2 18637 36997^2 2325076196570957^2
  4  H(2+i) = 20 - 772i, norm 2^5 * 18637; the numerator of f(3/4) is -23 * 4241
  5  p = 18637: order 9368, the points at n = 4683, 4685 on the branch P+T, 2-torsion midpoint, qualifying indices exactly {4683, 4685}
  6  p = 47, 947, 36997: no gap-two pair (47 and 947: no qualifying index at all; 36997: only 606 and 17730, a reflection pair)
  7  p = 2325076196570957: two roots of f in F_p, neither qualifying (root finder validated against brute force)
  8  the qualifying primes <= 100000 at n = 4683 and 4685 on the branch P+T are {397, 2969, 18637} and {18637, 93053}
  9  no gap-one and no gap-two coincidence for any prime 5 <= p < LIMIT (LIMIT = 10000; 2000 with --quick), full orbits, both branches
"""
import random
import sys

QUICK = '--quick' in sys.argv
FAILS = []

def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('  ' + detail) if detail else ''))
    if not ok:
        FAILS.append(name)

# ---------------------------------------------------------------- curve arithmetic mod p
def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

def f_mod(t, p):
    return (pow(t, 6, p) - 30 * pow(t, 4, p) - 24 * t * t - 1) % p

def add(P1, P2, p):
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2:
        if (y1 + y2) % p == 0:
            return None
        lam = (3 * x1 * x1 - 4 * x1 + 2) * pow(2 * y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam + 2 - x1 - x2) % p
    return (x3, (lam * (x1 - x3) - y1) % p)

def mul(n, Pt, p):
    R, A = None, Pt
    if n < 0:
        n, A = -n, (None if Pt is None else (Pt[0], (-Pt[1]) % p))
    while n:
        if n & 1:
            R = add(R, A, p)
        A = add(A, A, p)
        n >>= 1
    return R

P0, T0 = (1, 1), (0, 0)

def qualifying_root(t, p):
    if f_mod(t, p) != 0 or (1 + t * t) % p == 0:
        return False
    q = 2 * t * (1 - t * t) * pow((1 + t * t) ** 2, -1, p) % p
    r = (1 - t) * (1 + t * t) % p
    if legendre(q, p) != 1 or legendre(r, p) != 1:
        return False
    return not (legendre(2, p) == 1 and legendre(1 - t, p) != 1)

def qualifies(Pt, p):
    return Pt is not None and qualifying_root((1 - Pt[0]) % p, p)

def orbit(p, eps):
    pts, cur = [], (T0 if eps else None)
    while True:
        pts.append(cur)
        cur = add(cur, P0, p)
        if cur == (T0 if eps else None):
            return pts

def primes_upto(N, lo=5):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b'\x00\x00'
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(lo, N + 1) if s[i]]

# ---------------------------------------------------------------- bivariate integer polynomials
def padd(a, b, s=1):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + s * v
        if r[k] == 0:
            del r[k]
    return r

def pmul(a, b):
    r = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            r[(i + k, j + l)] = r.get((i + k, j + l), 0) + v * w
    return {k: v for k, v in r.items() if v}

def const(c):
    return {(0, 0): c} if c else {}

tt, uu = {(1, 0): 1}, {(0, 1): 1}
A1, B1, C1 = pmul(tt, tt), padd(const(4), pmul(const(-2), tt)), padd(pmul(const(4), tt), const(-3))
A2, B2, C2 = pmul(uu, uu), padd(const(4), pmul(const(-2), uu)), padd(pmul(const(4), uu), const(-3))
# Psi(t,s) = t^2 s^2 + (4 - 2t) s + (4t - 3) and Psi(s,u): eliminate s (resultant of two quadratics)
X = padd(pmul(A1, C2), pmul(A2, C1), -1)
Y = padd(pmul(A1, B2), pmul(A2, B1), -1)
Z = padd(pmul(B1, C2), pmul(B2, C1), -1)
G = padd(pmul(X, X), pmul(Y, Z), -1)

def div_u_minus_t(poly):
    degu = max(j for (_, j) in poly)
    cs = [dict() for _ in range(degu + 1)]
    for (i, j), v in poly.items():
        cs[j][i] = v
    q, carry = [None] * degu, {}
    for k in range(degu, 0, -1):
        cur = dict(cs[k])
        for i, v in carry.items():
            cur[i + 1] = cur.get(i + 1, 0) + v
        cur = {i: v for i, v in cur.items() if v}
        q[k - 1], carry = cur, cur
    rem = dict(cs[0])
    for i, v in carry.items():
        rem[i + 1] = rem.get(i + 1, 0) + v
    if any(rem.values()):
        return None
    return {(i, k): v for k, cp in enumerate(q) for i, v in cp.items()}

G1 = div_u_minus_t(G)
G2 = div_u_minus_t(G1) if G1 is not None else None

def peval(poly, a, b):
    return sum(c * a ** i * b ** j for (i, j), c in poly.items())

def add_q(P1, P2):   # exact rational curve arithmetic
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2:
        if y1 + y2 == 0:
            return None
        lam = (3 * x1 * x1 - 4 * x1 + 2) / (2 * y1)
    else:
        lam = (y2 - y1) / (x2 - x1)
    x3 = lam * lam + 2 - x1 - x2
    return (x3, lam * (x1 - x3) - y1)

# ---------------------------------------------------------------- check 1, 2
from fractions import Fraction
ok1 = G2 is not None
if ok1:
    Pq, Tq = (Fraction(1), Fraction(1)), (Fraction(0), Fraction(0))
    for eps in (0, 1):
        pts, cur = [], (Tq if eps else None)
        for n in range(11):
            pts.append(cur)
            cur = add_q(cur, Pq)
        for n in range(9):
            if pts[n] is not None and pts[n + 2] is not None:
                ok1 &= peval(G2, 1 - pts[n][0], 1 - pts[n + 2][0]) == 0
check('1 G2(t_n, t_{n+2}) = 0 exactly, n = 0..8, both branches ((t-u)^2 divides the resultant)', ok1)

diag = {}
if G2 is not None:
    for (i, j), c in G2.items():
        diag[i + j] = diag.get(i + j, 0) + c
    diag = {k: v for k, v in diag.items() if v}
check('2 G2(t,t) = 16 t (t+1) (t^2 - 4t + 5)', diag == {1: 80, 2: 16, 3: -48, 4: 16})

# ---------------------------------------------------------------- check 3: exact norm
def reduce_pair(poly):
    P = dict(poly)
    while True:
        key = next(((i, j) for (i, j) in P if i >= 6 or j >= 6), None)
        if key is None:
            return {k: v for k, v in P.items() if v}
        i, j = key
        c = P.pop(key)
        for d, w in ((4, 30), (2, 24), (0, 1)):
            k2 = (i - 6 + d, j) if i >= 6 else (i, j - 6 + d)
            P[k2] = P.get(k2, 0) + c * w

def bareiss(M):
    n, M, sign, prev = len(M), [r[:] for r in M], 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for r in range(k + 1, n):
                if M[r][k] != 0:
                    M[k], M[r] = M[r], M[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]

basis = [(i, j) for i in range(6) for j in range(6)]
idx = {b: k for k, b in enumerate(basis)}
M = [[0] * 36 for _ in range(36)]
for col, (i, j) in enumerate(basis):
    for key, c in reduce_pair({(a + i, b + j): c for (a, b), c in G2.items()}).items():
        M[idx[key]][col] = c
# sanity of the matrix build: norm of (u - t) must be 0 and norm of t must be 1
Mt = [[0] * 36 for _ in range(36)]
for col, (i, j) in enumerate(basis):
    for key, c in reduce_pair({(i + 1, j): 1}).items():
        Mt[idx[key]][col] = c
N = abs(bareiss(M))
expected = 2 ** 42 * 3 ** 27 * 47 ** 2 * 947 ** 2 * 18637 * 36997 ** 2 * 2325076196570957 ** 2
check('3 exact norm of G2 on Q[t,u]/(f(t),f(u)) = 2^42 3^27 47^2 947^2 18637 36997^2 2325076196570957^2',
      N == expected and bareiss(Mt) == 1, '(candidate primes >= 5: 47, 947, 18637, 36997, 2325076196570957)')

# ---------------------------------------------------------------- check 4
def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def cpow(a, k):
    r = (1, 0)
    for _ in range(k):
        r = cmul(r, a)
    return r
z = (2, 1)
z2, z4, z6 = cpow(z, 2), cpow(z, 4), cpow(z, 6)
Hz = (z6[0] - 30 * z4[0] - 24 * z2[0] - 1, z6[1] - 30 * z4[1] - 24 * z2[1])
v34 = Fraction(3, 4) ** 6 - 30 * Fraction(3, 4) ** 4 - 24 * Fraction(3, 4) ** 2 - 1
check('4 H(2+i) = 20 - 772i, norm 2^5 * 18637; f(3/4) = -97543/4096 = -23 * 4241 / 4096',
      Hz == (20, -772) and Hz[0] ** 2 + Hz[1] ** 2 == 32 * 18637 and v34 == Fraction(-97543, 4096) and 23 * 4241 == 97543)

# ---------------------------------------------------------------- check 5
p = 18637
o0, o1 = orbit(p, 0), orbit(p, 1)
m = len(o0)
q0 = [n for n in range(m) if qualifies(o0[n], p)]
q1 = [n for n in range(m) if qualifies(o1[n], p)]
mid = add(mul(4684, P0, p), T0, p)
check('5 p = 18637: order 9368, 4683P+T = (3765,7534), 4685P+T = (3765,11103), 4684P+T = (14872,0) of order 2, '
      'qualifying indices {} on nP and {4683, 4685} on nP+T',
      m == 9368 and o1[4683] == (3765, 7534) and o1[4685] == (3765, 11103) and mid == (14872, 0)
      and q0 == [] and q1 == [4683, 4685],
      '(mean 2341/2342 of the local sign h over a period)')

# ---------------------------------------------------------------- check 6
def gap_pairs(p):
    out = {}
    for eps in (0, 1):
        pts = orbit(p, eps)
        mm = len(pts)
        qual = [n for n in range(mm) if qualifies(pts[n], p)]
        s = set(qual)
        out[eps] = (mm, qual, [n for n in qual if (n + 2) % mm in s], [n for n in qual if (n + 1) % mm in s])
    return out
ok6 = True
for pp, expect in ((47, ([], [])), (947, ([], [])), (36997, ([], [606, 17730]))):
    r = gap_pairs(pp)
    ok6 &= r[0][1] == expect[0] and r[1][1] == expect[1]
    ok6 &= all(r[e][2] == [] and r[e][3] == [] for e in (0, 1))
    if expect[1]:
        ok6 &= sum(expect[1]) == r[1][0]    # reflection pair n + n' = m
check('6 p = 47, 947, 36997: no gap-two pair (36997: indices 606, 17730 on nP+T sum to the order 18336)', ok6)

# ---------------------------------------------------------------- check 7: polynomial root finding over F_P for the large prime
def trim(a, p):
    a = [c % p for c in a]
    while a and a[-1] == 0:
        a.pop()
    return a
def pmod(a, mod, p):
    a, inv = trim(a, p), pow(mod[-1], -1, p)
    while len(a) >= len(mod):
        c, s = a[-1] * inv % p, len(a) - len(mod)
        for i, y in enumerate(mod):
            a[s + i] = (a[s + i] - c * y) % p
        a = trim(a, p)
    return a
def pmulmod(a, b, mod, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return pmod(r, mod, p)
def ppowmod(base, e, mod, p):
    r, b = [1], pmod(base, mod, p)
    while e:
        if e & 1:
            r = pmulmod(r, b, mod, p)
        b = pmulmod(b, b, mod, p)
        e >>= 1
    return r
def pgcd(a, b, p):
    a, b = trim(a, p), trim(b, p)
    while b:
        a, b = b, pmod(a, b, p)
    inv = pow(a[-1], -1, p)
    return [c * inv % p for c in a]
def pdiv(a, b, p):
    a, inv = trim(a[:], p), pow(b[-1], -1, p)
    q = [0] * (len(a) - len(b) + 1)
    while len(a) >= len(b):
        c, s = a[-1] * inv % p, len(a) - len(b)
        q[s] = c
        for i, y in enumerate(b):
            a[s + i] = (a[s + i] - c * y) % p
        a = trim(a, p)
    return trim(q, p)
def roots_of(poly, p):
    poly = trim(poly, p)
    xp = ppowmod([0, 1], p, poly, p) + [0, 0]
    xp[1] = (xp[1] - 1) % p
    diff = trim(xp, p)
    g = pgcd(poly, diff, p) if diff else [c * pow(poly[-1], -1, p) % p for c in poly]
    out = []
    def split(g):
        if len(g) == 1:
            return
        if len(g) == 2:
            out.append((-g[0]) * pow(g[1], -1, p) % p)
            return
        while True:
            h = ppowmod([random.randrange(p), 1], (p - 1) // 2, g, p)
            hm1 = list(h) if h else [0]
            hm1[0] = (hm1[0] - 1) % p
            hm1 = trim(hm1, p)
            d = pgcd(g, hm1, p) if hm1 else g
            if 1 < len(d) < len(g):
                split(d)
                split(pdiv(g, d, p))
                return
    split(g)
    return sorted(set(out))
def f_poly(p):
    return [-1 % p, 0, -24 % p, 0, -30 % p, 0, 1]

random.seed(1)
bad = 0
for pp in primes_upto(200 if QUICK else 400):
    if roots_of(f_poly(pp), pp) != [a for a in range(pp) if f_mod(a, pp) == 0]:
        bad += 1
PB = 2325076196570957
rts = roots_of(f_poly(PB), PB)
check('7 p = 2325076196570957: root finder agrees with brute force (primes < %d), f has 2 roots in F_p, neither qualifying' % (200 if QUICK else 400),
      bad == 0 and len(rts) == 2 and all(f_mod(a, PB) == 0 for a in rts) and not any(qualifying_root(a, PB) for a in rts))

# ---------------------------------------------------------------- check 8: sieve to 100000
PR = primes_upto(100000)
def qual_list(n, eps):
    out = []
    for pp in PR:
        Qn = mul(n, P0, pp)
        if eps:
            Qn = add(Qn, T0, pp)
        if qualifies(Qn, pp):
            out.append(pp)
    return out
a, b = qual_list(4683, 1), qual_list(4685, 1)
check('8 qualifying primes <= 100000 at n = 4683 and 4685 on nP+T: {397, 2969, 18637} and {18637, 93053}; common prime 18637; sign product -1',
      a == [397, 2969, 18637] and b == [18637, 93053] and set(a) & set(b) == {18637} and (-1) ** len(a) * (-1) ** len(b) == -1)

# ---------------------------------------------------------------- check 9
LIMIT = 2000 if QUICK else 10000
hits = {}
for pp in primes_upto(LIMIT):
    r = gap_pairs(pp)
    if any(r[e][2] or r[e][3] for e in (0, 1)):
        hits[pp] = {e: (r[e][2], r[e][3]) for e in (0, 1)}
check('9 no gap-one and no gap-two coincidence for any prime 5 <= p < %d (full orbits, both branches)' % LIMIT, not hits,
      str(hits) if hits else '')

print()
print('FAILED: ' + ', '.join(FAILS) if FAILS else 'all checks passed')
sys.exit(1 if FAILS else 0)
