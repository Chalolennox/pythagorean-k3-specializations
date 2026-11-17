#!/usr/bin/env python3
"""Gap three, and all gaps in characteristic 0 (notes/REVIEW_2026-11-17_gap_three_dossier.md).

Curve C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), f(t) = t^6 - 30t^4 - 24t^2 - 1, t_n = 1 - x(nP) or 1 - x(nP + T).
A prime p >= 5 is in Q_n if p | F_n and (a_n b_n / p) = +1; necessary and checked here: t_n mod p is a *qualifying root*
(F.57 Definitions: 1 + a^2 != 0, q(a) and r(a) non-zero squares, and 1 - a a square when (2/p) = +1).
Status of everything below: derived with a language model; no human has checked it.

Checks (one PASS line each, exit status 1 on any failure; standard library only; --quick shortens the scans):
  1  x(Q + 3P) = (A(x) + 1722 y)/D(x), A = 441x^2 + 799x + 882, D = (9x - 49)^2, 3P = (49/9, -287/27)  (the dossier's formula)
  2  the dossier's resultant R_3 = Res_x(h, G0^2 - f_C G1^2) is negative and equals the reported factorization
  3  the gap-three relation G3(t,w) (two middle parameters eliminated from Psi, divided by Psi) is the symmetric biquadratic
     81t^2w^2 + 720t^2w + 720tw^2 + 1600t^2 + 1600w^2 - 4802tw + 1044t + 1044w - 1683, and G3(t_n, t_{n+3}) = 0 exactly (both branches)
  4  exact norm of G3 on Q[t,w]/(f(t), f(w)) = 2^18 3^45 7^2 71^2 397^2 4919^2 8887^2 19427 206215327 49831710601^2 pi^2,
     pi = 286414695690956651258188903406027; Res(f, G3(t,t)) = 2^6 3^15 7^2 19427 206215327
  5  307 and 7743563 (the dossier's "denominator" candidates) are not candidates: 307 * 7743563 is the numerator of f(-40/9), t(3P) = -40/9
  6  the nine candidate primes are prime (trial division below 10^12; pi by a Pocklington chain of 6 steps with the certificate in the script)
  7  local test for the nine candidates: no pair of qualifying points differing by 3P
  8  no gap-one, gap-two (other than 18637, beyond the range) or gap-three coincidence for any prime 5 <= p < LIMIT, full orbits, both branches
  9  theorem (no geometric exceptional gaps): h = f(1-x) irreducible over Q (factorization patterns mod p), N(r) = -3456 is not a
     square, so the degree-12 polynomial g(y) = m(y^2) is irreducible and D is one Galois orbit; x(2P) = 1/4 is not an integer
 10  |R_{p,eps}| <= 12; qualifying indices come in pairs n, -n (n != -n); a prime with a qualifying index n coincides with itself at the
     gap (-2n) mod m_p, so every prime with a qualifying index lies in E_L for L >= its smallest gap
"""
import random
import sys
from fractions import Fraction
from math import gcd

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



# ---------------------------------------------------------------- check 1: the dossier's formula for x(Q + 3P)
Pq, Tq = (Fraction(1), Fraction(1)), (Fraction(0), Fraction(0))
P3q = add_q(add_q(Pq, Pq), Pq)
fC = lambda x: x ** 3 - 2 * x * x + 2 * x
A3 = lambda x: 441 * x * x + 799 * x + 882
D3 = lambda x: (9 * x - 49) ** 2
orbit_pts = []
for eps in (0, 1):
    cur = Tq if eps else None
    for n in range(0, 10):
        cur = add_q(cur, Pq)
        orbit_pts.append(cur)
ok = P3q == (Fraction(49, 9), Fraction(-287, 27))
npts = 0
for Q in orbit_pts:
    if Q is None or 9 * Q[0] == 49:
        continue
    R = add_q(Q, P3q)
    if R is not None:
        ok &= R[0] == (A3(Q[0]) + 1722 * Q[1]) / D3(Q[0])
        npts += 1
# the polynomial part of the formula: 81 f_C(x) + 82369/9 + (2 - x - 49/9) D(x) = A(x) (cubic identity, 8 points)
for xv in range(-4, 4):
    xv = Fraction(xv)
    ok &= 81 * fC(xv) + Fraction(82369, 9) + (2 - xv - Fraction(49, 9)) * D3(xv) == A3(xv)
check('1 3P = (49/9, -287/27); x(Q+3P) = (A(x) + 1722 y)/D(x) at %d orbit points and as a polynomial identity' % npts, ok)

# ---------------------------------------------------------------- check 2: the dossier's resultant R_3
hco = [-54, 162, -189, 100, -15, -6, 1]       # h(x) = f(1 - x), low -> high
def zadd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]
def zscale(a, c):
    return [c * v for v in a]
def zmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            r[i + j] += u * v
    return r
def zmodh(a):
    a = a[:]
    while len(a) > 6:
        c = a.pop()
        k = len(a)
        for e, w in ((5, 6), (4, 15), (3, -100), (2, 189), (1, -162), (0, 54)):   # x^6 = 6x^5 + 15x^4 - 100x^3 + 189x^2 - 162x + 54
            a[k - 6 + e] += c * w
    return a + [0] * (6 - len(a))
fCco = [0, 2, -2, 1]
def rmul(u, v):
    (a0, a1), (b0, b1) = u, v
    return (zmodh(zadd(zmul(a0, b0), zmul(zmul(a1, b1), fCco))), zmodh(zadd(zmul(a0, b1), zmul(a1, b0))))
def radd(u, v):
    return (zmodh(zadd(u[0], v[0])), zmodh(zadd(u[1], v[1])))
def rscale(u, c):
    return (zmodh(zscale(u[0], c)), zmodh(zscale(u[1], c)))
def rpow(u, k):
    r = ([1], [0])
    for _ in range(k):
        r = rmul(r, u)
    return r
def fdet(M):
    n, M, d = len(M), [[Fraction(v) for v in r] for r in M], Fraction(1)
    for k in range(n):
        piv = next((r for r in range(k, n) if M[r][k] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != k:
            M[k], M[piv] = M[piv], M[k]
            d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            c = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= c * M[k][j]
    return d
Dx, Ax = [2401, -882, 81], [882, 799, 441]
W = (zmodh(zadd(Dx, zscale(Ax, -1))), zmodh([-1722]))          # W = D - A - 1722 y  (the y-part is -1722)
Dr = (zmodh(Dx), [0] * 6)
Gx = radd(radd(rpow(W, 6), rscale(rmul(rpow(W, 4), rpow(Dr, 2)), -30)),
          radd(rscale(rmul(rpow(W, 2), rpow(Dr, 4)), -24), rscale(rpow(Dr, 6), -1)))
Nx = zmodh(zadd(zmul(Gx[0], Gx[0]), zscale(zmul(zmul(Gx[1], Gx[1]), fCco), -1)))
Mx = [zmodh(zmul(Nx, [0] * j + [1])) for j in range(6)]
R3 = fdet([[Mx[j][i] for j in range(6)] for i in range(6)])
PI = 286414695690956651258188903406027
reported = 2 ** 18 * 3 ** 45 * 7 ** 2 * 71 ** 2 * 307 ** 12 * 397 ** 2 * 4919 ** 2 * 8887 ** 2 * 19427 * 7743563 ** 12 \
    * 206215327 * 49831710601 ** 2 * PI ** 2
check('2 dossier resultant R_3 = Res_x(h, G0^2 - f_C G1^2): negative, |R_3| = 2^18 3^45 7^2 71^2 307^12 397^2 4919^2 8887^2 19427 7743563^12 '
      '206215327 49831710601^2 pi^2', R3 < 0 and abs(int(R3)) == reported)

# ---------------------------------------------------------------- check 3: G3 from Psi
def coeffs_in_second(poly):
    out = {0: {}, 1: {}, 2: {}}
    for (i, j), c in poly.items():
        out[j][(i, 0)] = out[j].get((i, 0), 0) + c
    return out
cg = coeffs_in_second(G2)
a2, a1, a0 = cg[2], cg[1], cg[0]
b2, b1, b0 = {(0, 2): 1}, padd(const(4), {(0, 1): -2}), padd({(0, 1): 4}, const(-3))       # Psi(s, w) as a quadratic in s
Xr = padd(pmul(a2, b0), pmul(b2, a0), -1)
Yr = padd(pmul(a2, b1), pmul(b2, a1), -1)
Zr = padd(pmul(a1, b0), pmul(b1, a0), -1)
R3tw = padd(pmul(Xr, Xr), pmul(Yr, Zr), -1)                      # Res_s(G2(t,s), Psi(s,w))
Psi = {(2, 2): 1, (0, 1): 4, (1, 1): -2, (1, 0): 4, (0, 0): -3}
def div_by_psi(num):
    q, rem = {}, dict(num)
    while rem:
        dn = max(j for _, j in rem)
        if dn < 2:
            break
        ln = {(i, 0): c for (i, j), c in rem.items() if j == dn}
        if any(i < 2 for (i, _) in ln):
            return None
        qt = {(i - 2, dn - 2): c for (i, _), c in ln.items()}
        q = padd(q, qt)
        rem = padd(rem, pmul(qt, Psi), -1)
    return q if not rem else None
G3 = div_by_psi(R3tw)
G3_expected = {(2, 2): 81, (2, 1): 720, (1, 2): 720, (2, 0): 1600, (0, 2): 1600, (1, 1): -4802, (1, 0): 1044, (0, 1): 1044, (0, 0): -1683}
ok3 = G3 == G3_expected
if G3 is not None:
    for eps in (0, 1):
        pts, cur = [], (Tq if eps else None)
        for n in range(13):
            pts.append(cur)
            cur = add_q(cur, Pq)
        for n in range(10):
            if pts[n] is not None and pts[n + 3] is not None:
                ok3 &= peval(G3, 1 - pts[n][0], 1 - pts[n + 3][0]) == 0
check('3 G3 = Res_s(G2(t,s), Psi(s,w)) / Psi(t,w) is the symmetric biquadratic above; G3(t_n, t_{n+3}) = 0 exactly (n = 0..9, both branches)', ok3)

# ---------------------------------------------------------------- check 4: exact norms
basis = [(i, j) for i in range(6) for j in range(6)]
idx = {b: k for k, b in enumerate(basis)}
M3 = [[0] * 36 for _ in range(36)]
for col, (i, j) in enumerate(basis):
    for key, c in reduce_pair({(a + i, b + j): c for (a, b), c in G3_expected.items()}).items():
        M3[idx[key]][col] = c
N3 = abs(bareiss(M3))
exp3 = 2 ** 18 * 3 ** 45 * 7 ** 2 * 71 ** 2 * 397 ** 2 * 4919 ** 2 * 8887 ** 2 * 19427 * 206215327 * 49831710601 ** 2 * PI ** 2
diag3 = {}
for (i, j), c in G3_expected.items():
    diag3[i + j] = diag3.get(i + j, 0) + c
dl = [diag3.get(k, 0) for k in range(5)]                        # 81t^4 + 1440t^3 - 1602t^2 + 2088t - 1683
def reduce_f(poly):                                             # poly in t as list low->high, modulo t^6 = 30t^4 + 24t^2 + 1
    a = poly[:]
    while len(a) > 6:
        c = a.pop()
        k = len(a)
        for e, w in ((4, 30), (2, 24), (0, 1)):
            a[k - 6 + e] += c * w
    return a + [0] * (6 - len(a))
Md = [reduce_f([0] * j + dl) for j in range(6)]
Rd = fdet([[Md[j][i] for j in range(6)] for i in range(6)])
check('4 exact norm of G3 on Q[t,w]/(f(t),f(w)) = 2^18 3^45 7^2 71^2 397^2 4919^2 8887^2 19427 206215327 49831710601^2 pi^2; '
      'diagonal G3(t,t) = %s, Res(f, G3(t,t)) = 2^6 3^15 7^2 19427 206215327' % '81t^4+1440t^3-1602t^2+2088t-1683',
      N3 == exp3 and dl == [-1683, 2088, -1602, 1440, 81] and abs(Rd) == 2 ** 6 * 3 ** 15 * 7 ** 2 * 19427 * 206215327)

# ---------------------------------------------------------------- check 5: pole artifacts 307, 7743563
v = Fraction(-40, 9)
num = 40 ** 6 - 30 * 40 ** 4 * 81 - 24 * 40 ** 2 * 9 ** 4 - 9 ** 6        # 9^6 f(-40/9)
check('5 t(3P) = 1 - 49/9 = -40/9; 9^6 f(-40/9) = %d = 307 * 7743563 (pole of the relation, not a coincidence prime)' % num,
      v == 1 - P3q[0] and num == -2377273841 and 307 * 7743563 == 2377273841 and Fraction(num, 9 ** 6) == v ** 6 - 30 * v ** 4 - 24 * v ** 2 - 1)

CANDS = [7, 71, 397, 4919, 8887, 19427, 206215327, 49831710601, PI]
# ---------------------------------------------------------------- check 6: primality of the candidates
SMALL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
def strong_probable_prime(n):
    for q in SMALL:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in SMALL:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True
# Pocklington certificate for pi: n -> ([(q, e)] with prod q^e dividing n - 1 and (prod q^e)^2 > n, {q: witness a})
POCK = {
    286414695690956651258188903406027: ([(2556946286738816232541, 1)], {2556946286738816232541: 2}),
    2556946286738816232541: ([(6087967349378133887, 1)], {6087967349378133887: 2}),
    6087967349378133887: ([(1420431019453601, 1)], {1420431019453601: 2}),
    1420431019453601: ([(623214733, 1)], {623214733: 2}),
    623214733: ([(1059889, 1)], {1059889: 2}),
    1059889: ([(311, 1), (71, 1)], {311: 2, 71: 2}),
}
def proved_prime(n):
    if n < 10 ** 12:
        return n > 1 and all(n % q for q in range(2, int(n ** 0.5) + 1))
    if n not in POCK:
        return False
    used, wit = POCK[n]
    F = 1
    for q, e in used:
        F *= q ** e
    if (n - 1) % F != 0 or F * F <= n:
        return False
    for q, e in used:
        a = wit[q]
        if pow(a, n - 1, n) != 1 or gcd(pow(a, (n - 1) // q, n) - 1, n) != 1 or not proved_prime(q):
            return False
    return True
check('6 the nine candidate primes are prime (all below 10^12 by trial division; pi = %d by a Pocklington chain of 6 steps; every candidate '
      'also passes a strong probable prime test to 25 bases)' % PI,
      all(proved_prime(c) for c in CANDS) and all(strong_probable_prime(c) for c in CANDS) and proved_prime(307) and proved_prime(7743563))

# ---------------------------------------------------------------- check 7: local group-law test for the candidates
random.seed(3)
def sqrt_mod(a, p):
    a %= p
    if a == 0:
        return 0
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legendre(z, p) != -1:
        z += 1
    m, c, t_, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t_ != 1:
        i, t2 = 0, t_
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t_, r = i, b * b % p, t_ * b * b % p, r * b % p
    return r
ok7, info7 = True, []
for pc in CANDS:
    rts = roots_of(f_poly(pc), pc)
    qual = [a for a in rts if qualifying_root(a, pc)]
    pairs = both = 0
    for a in rts:
        rr = (1 - a) * (1 + a * a) % pc
        if legendre(rr, pc) != 1:
            continue
        y = sqrt_mod(rr, pc)
        for Qp in (((1 - a) % pc, y), ((1 - a) % pc, (-y) % pc)):
            for sg in (1, -1):
                R = add(Qp, mul(sg * 3, P0, pc), pc)
                if R is None:
                    continue
                tp = (1 - R[0]) % pc
                if f_mod(tp, pc) == 0:
                    pairs += 1
                    if a in qual and qualifying_root(tp, pc):
                        both += 1
    ok7 &= both == 0
    info7.append('%s: %d roots, %d qualifying' % (pc if pc < 10 ** 12 else 'pi', len(rts), len(qual)))
check('7 local test: for each of the nine candidates no pair of qualifying points Q, Q +- 3P', ok7, '(' + '; '.join(info7) + ')')

# ---------------------------------------------------------------- check 8: full-orbit scan, gaps 1, 2, 3
def orbit_data(p):
    out = {}
    for eps in (0, 1):
        pts = orbit(p, eps)
        mm = len(pts)
        qual = [n for n in range(mm) if qualifies(pts[n], p)]
        out[eps] = (mm, qual)
    return out
LIMIT = 3000 if QUICK else 10000
hits, data = {}, {}
for pp in primes_upto(LIMIT):
    data[pp] = orbit_data(pp)
    for eps in (0, 1):
        mm, qual = data[pp][eps]
        s = set(qual)
        for gap in (1, 2, 3):
            if any((n + gap) % mm in s for n in qual):
                hits.setdefault(pp, []).append((eps, gap))
ctrl = orbit_data(18637)          # positive control: the scan logic must see the known gap-two coincidence
cm, cq = ctrl[1]
control = ctrl[0][1] == [] and cq == [4683, 4685] and any((n + 2) % cm in set(cq) for n in cq) \
    and not any((n + g) % cm in set(cq) for n in cq for g in (1, 3))
check('8 no gap-one, gap-two or gap-three coincidence for any prime 5 <= p < %d (full orbits, both branches; the gap-two prime 18637 is beyond; '
      'control: the scan logic finds the gap-two pair at 18637 and no gap one or three there)' % LIMIT,
      not hits and control, str(hits) if hits else '')
#

# ---------------------------------------------------------------- check 9: the theorem (no geometric exceptional gaps)
def charpoly(Mat):
    n = len(Mat)
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    c, Mk = [Fraction(1)], [[0] * n for _ in range(n)]
    for k in range(1, n + 1):
        AM = mm(Mat, Mk)
        Mk = [[AM[i][j] + c[-1] * I[i][j] for j in range(n)] for i in range(n)]
        AM = mm(Mat, Mk)
        c.append(Fraction(-sum(AM[i][i] for i in range(n)), k))
    return [int(x) for x in c]                                  # high -> low
Mf = [zmodh(zmul(fCco, [0] * j + [1])) for j in range(6)]       # multiplication by f_C(x) = y^2 on Q[x]/(h)
cp = charpoly([[Mf[j][i] for j in range(6)] for i in range(6)])
gco = [0] * 13
for i, co in enumerate(cp):
    gco[2 * (6 - i)] = co                                        # g(y) = m(y^2), low -> high
def ddf_pattern(poly, p):
    f, out, xp, d = trim(poly, p), [], [0, 1], 0
    while len(f) - 1 >= 2 * (d + 1):
        d += 1
        xp = ppowmod(xp, p, f, p)
        diff = list(xp) + [0, 0]
        diff[1] = (diff[1] - 1) % p
        diff = trim(diff, p)
        gcd = pgcd(f, diff, p) if diff else f
        if len(gcd) > 1:
            out.append((d, (len(gcd) - 1) // d))
            f = pdiv(f, gcd, p)
            xp = pmod(xp, f, p) if len(f) > 1 else xp
    if len(f) > 1:
        out.append((len(f) - 1, 1))
    return tuple(sorted(out))
seen = {}
for pp in primes_upto(300 if QUICK else 600):
    hp = trim(hco, pp)
    if len(pgcd(hp, trim([(i * hco[i]) % pp for i in range(1, 7)], pp), pp)) > 1:
        continue                                                 # h has a repeated factor mod p
    pt = ddf_pattern(hco, pp)
    seen[pt] = seen.get(pt, 0) + 1
# h cannot split over Q as 1+5, 1+1+4, ..., 2+4, 3+3, ...: a rational factor of degree d is a product of factors mod p whose degrees sum to d
def partition_sums(pattern):
    degs = [d for d, mult in pattern for _ in range(mult)]
    sums = {0}
    for d in degs:
        sums |= {s + d for s in sums}
    return sums
possible = set(range(1, 6))
for pt in seen:
    possible &= partition_sums(pt)
P2q = add_q(Pq, Pq)
check('9 theorem premises: h = f(1-x) irreducible over Q (no degree 1..5 factor is compatible with the patterns mod p: %s); '
      'minimal polynomial of y^2 = f_C(x) over Q is s^6 - 66s^5 - 29922s^4 + 73214s^3 - 62559s^2 + 22032s - 3456, N(r) = -3456 < 0 is not a square; '
      '2P = (1/4, -5/8) (infinite order by Nagell-Lutz)' % ', '.join('%s x%d' % (k, v) for k, v in sorted(seen.items())),
      not possible and cp == [1, -66, -29922, 73214, -62559, 22032, -3456] and cp[-1] < 0
      and P2q == (Fraction(1, 4), Fraction(-5, 8)) and P2q[0].denominator != 1)

# ---------------------------------------------------------------- check 10: |R| <= 12, reflection pairs, forced coincidences at the gap -2n
ok10, with_index, maxR, mingaps = True, 0, 0, {}
for pp, dd in data.items():
    for eps in (0, 1):
        mm, qual = dd[eps]
        maxR = max(maxR, len(qual))
        ok10 &= len(qual) <= 12 and len(qual) % 2 == 0
        s = set(qual)
        for n in qual:
            ok10 &= (-n) % mm in s and (-n) % mm != n
            gap = (-2 * n) % mm
            ok10 &= gap != 0 and (n + gap) % mm in s
            mingaps[pp] = min(mingaps.get(pp, mm), gap)
    if any(dd[e][1] for e in (0, 1)):
        with_index += 1
check('10 for all primes 5 <= p < %d: |R_{p,eps}| <= 12 (maximum seen %d), |R| even, qualifying n gives qualifying -n != n, hence a coincidence '
      'at the gap (-2n) mod m_p' % (LIMIT, maxR), ok10,
      '(%d of %d primes have a qualifying index; smallest gap over these primes between %d and %d)'
      % (with_index, len(data), min(mingaps.values()), max(mingaps.values())))

print()
print('FAILED: ' + ', '.join(FAILS) if FAILS else 'all checks passed')
sys.exit(1 if FAILS else 0)
