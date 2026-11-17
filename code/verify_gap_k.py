#!/usr/bin/env python3
"""Gaps k >= 4: the universal correspondence G_k(t,w) = Phi_{u_k}(1-t, 1-w), exact norms, candidate primes and local tests
(notes/REVIEW_2026-11-17_gap_k_classification.md).  Derived with a language model; no human has checked it.

Curve C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), f(t) = t^6 - 30t^4 - 24t^2 - 1, t_n = 1 - x(nP) or 1 - x(nP + T).
A prime p >= 5 lies in Q_n and Q_{n+k} only if p divides the exact norm N_k of Phi_{u_k}(1-t, 1-w) (cleared of denominators) on
Q[t,w]/(f(t), f(w)); N_k = D_k * O_k^2 with D_k = Res(f, G_k(t,t)) (equal parameters) and O_k an integer (the off-diagonal factors come in
symmetric pairs).  Equivalently, p is in both iff k is congruent modulo m_p = ord(P mod p) to a difference r - r' of two qualifying indices.

Checks (one PASS line each, exit status 1 on any failure; standard library only; --quick shortens the scans):
  1  N_k = D_k * O_k^2 for k = 1..7, with the factorizations of D_k and O_k listed below (k = 6, 7: O_k has one composite cofactor
     with no prime factor below 10^6 that is NOT factored; the classification for k = 6, 7 is therefore incomplete)
  2  primality: every prime of the lists for k <= 5 above 10^12 has a certificate (Pocklington p-1 / Lucas p+1 chain) that is verified here
  3  local group-law test at every prime >= 5 of the lists, k = 4: the primes with coincident qualifying points are exactly 83, 823, 4241
  4  same, k = 5: none
  5  k = 6 and 7 (partial): coincident qualifying points at 307 and 34389517 (k = 6), at 83 and 79734735126883 (k = 7), nowhere else among
     the primes found
  6  orbit membership (baby-step giant-step): the coincidences at 83, 823, 4241 (k = 4), 307 and 34389517 (k = 6), 83 (k = 7) are
     between indices n, n + k of the orbit nP or nP + T
  7  scan of the full orbits of all primes 5 <= p < LIMIT, gaps 1..12 (both branches): the hits are exactly the expected list, and every
     hit divides the exact norm N_k
"""
import math
import random
import sys
from fractions import Fraction
from math import comb, gcd

QUICK = '--quick' in sys.argv
FAILS = []

def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('  ' + detail) if detail else ''))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- exact norms of Phi_{u_k}(1-t, 1-w)
def add_q(P1, P2):
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

def uk(k):
    cur = None
    for _ in range(k):
        cur = add_q(cur, (Fraction(1), Fraction(1)))
    return cur[0]

def phi_tw(u):
    """Phi_u(1-t, 1-w) times the common denominator, as {(i, j): integer}"""
    terms = {}
    def addt(i, j, c):
        terms[(i, j)] = terms.get((i, j), 0) + c
    addt(2, 2, 1); addt(1, 2, -2 * u); addt(0, 2, u * u)
    addt(1, 1, -2 * u * u + 8 * u - 4); addt(2, 1, -2 * u); addt(0, 1, -4 * u)
    addt(2, 0, u * u); addt(1, 0, -4 * u); addt(0, 0, 4)
    out = {}
    for (i, j), c in terms.items():
        for a in range(i + 1):
            for b in range(j + 1):
                out[(a, b)] = out.get((a, b), 0) + c * comb(i, a) * (-1) ** a * comb(j, b) * (-1) ** b
    den = 1
    for v in out.values():
        den = den * v.denominator // gcd(den, v.denominator)
    return {k: int(v * den) for k, v in out.items() if v}

def reduce_pair(poly):
    Pp = dict(poly)
    while True:
        key = next(((i, j) for (i, j) in Pp if i >= 6 or j >= 6), None)
        if key is None:
            return {k: v for k, v in Pp.items() if v}
        i, j = key
        c = Pp.pop(key)
        for d, w in ((4, 30), (2, 24), (0, 1)):
            k2 = (i - 6 + d, j) if i >= 6 else (i, j - 6 + d)
            Pp[k2] = Pp.get(k2, 0) + c * w

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

BASIS = [(i, j) for i in range(6) for j in range(6)]
IDX = {b: k for k, b in enumerate(BASIS)}
def norm_of(G):
    M = [[0] * 36 for _ in range(36)]
    for col, (i, j) in enumerate(BASIS):
        for key, c in reduce_pair({(a + i, b + j): c for (a, b), c in G.items()}).items():
            M[IDX[key]][col] = c
    return abs(bareiss(M))

def diag_norm(G):
    dg = {}
    for (i, j), c in G.items():
        dg[i + j] = dg.get(i + j, 0) + c
    cols = []
    for j in range(6):
        a = [0] * j + [dg.get(i, 0) for i in range(max(dg) + 1)]
        while len(a) > 6:
            c = a.pop()
            kk = len(a)
            for e, w in ((4, 30), (2, 24), (0, 1)):
                a[kk - 6 + e] += c * w
        cols.append(a + [0] * (6 - len(a)))
    return abs(bareiss([[cols[j][i] for j in range(6)] for i in range(6)]))

# factorizations (D_k: diagonal part; O_k: square root of the off-diagonal part)
FACT = {
    1: ({2: 6, 3: 4, 7: 1, 103: 1, 113: 1}, {2: 6, 3: 13, 113: 1, 13085561: 1}),
    2: ({2: 30, 3: 3, 18637: 1}, {2: 6, 3: 12, 47: 1, 947: 1, 36997: 1, 2325076196570957: 1}),
    3: ({2: 6, 3: 15, 7: 2, 19427: 1, 206215327: 1},
        {2: 6, 3: 15, 71: 1, 397: 1, 4919: 1, 8887: 1, 286414695690956651258188903406027: 1, 49831710601: 1}),
    4: ({2: 43, 3: 3, 5: 12, 23: 1, 823: 1, 2141: 1, 4241: 1, 5304889: 1},
        {2: 6, 3: 12, 83: 1, 4211: 1, 18329: 1, 239375709346878300069090981344249202541713126418974522959813: 1, 5473007569: 1,
         110873747: 1, 110840087: 1}),
    5: ({2: 6, 3: 3, 7: 1, 11: 12, 17: 12, 151: 1, 8849: 1, 11393: 1, 24337: 1, 2136952387: 1, 6164369: 1},
        {2: 6, 3: 12, 47: 1, 67: 1, 137: 1, 631: 1, 1009: 1, 19391: 1,
         14804809328194960612031186071270721071612332326006472447005610496619217105373041927635455685201: 1,
         52679765626351: 1, 11513351653907: 1, 33898211: 1}),
    6: ({2: 30, 3: 15, 7: 12, 23: 1, 41: 12, 83: 1, 307: 1, 7592142411209066382317: 1, 2060749: 1, 7743563: 1},
        {2: 6, 3: 15, 83: 1, 113: 1, 748523: 1, 998651: 1, 312938568179: 1, 34389517: 1, 9907529: 1}),
    7: ({2: 6, 3: 3, 7: 2, 47: 12, 83: 1, 233: 12, 7079455478499553: 1, 31414608791327: 1, 79734735126883: 1, 2420264834891: 1},
        {2: 6, 3: 12, 244219: 1, 6544706200163: 1}),
}
def prod(d):
    r = 1
    for q, e in d.items():
        r *= q ** e
    return r

NORMS, ok1, info1 = {}, True, []
for k in range(1, 13):
    NORMS[k] = norm_of(phi_tw(uk(k)))                     # all k <= 12, used for divisibility in check 7
for k in range(1, 8):
    Dk = diag_norm(phi_tw(uk(k)))
    Dd, Oo = FACT[k]
    ok1 &= prod(Dd) == Dk
    off2 = NORMS[k] // Dk
    Ok = math.isqrt(off2)
    ok1 &= NORMS[k] == Dk * off2 and Ok * Ok == off2
    cof, r = divmod(Ok, prod(Oo))
    ok1 &= r == 0
    if k <= 5:
        ok1 &= cof == 1
    else:
        ok1 &= cof > 10 ** 100
        info1.append('k=%d: unfactored composite cofactor of %d digits' % (k, len(str(cof))))
check('1 N_k = D_k * O_k^2 and the factorizations of D_k, O_k (k = 1..7; complete for k <= 5)', ok1, '(' + '; '.join(info1) + ')')

# ---------------------------------------------------------------- check 2: primality certificates
CERTS = {
    2641917343453: ('pock', [(12950575213, 1)], {12950575213: 2}),
    3772899186241: ('pock', [(3930103319, 1)], {3930103319: 2}),
    5756675826953: ('pock', [(113167, 1), (107773, 1)], {113167: 2, 107773: 2}),
    11513351653907: ('pock', [(5756675826953, 1)], {5756675826953: 2}),
    52679765626351: ('pock', [(372426763, 1)], {372426763: 2}),
    181099160939569: ('pock', [(3772899186241, 1)], {3772899186241: 2}),
    1420431019453601: ('pock', [(623214733, 1)], {623214733: 2}),
    2173189931274829: ('pock', [(181099160939569, 1)], {181099160939569: 2}),
    2325076196570957: ('pock', [(206930953771, 1)], {206930953771: 2}),
    6087967349378133887: ('pock', [(1420431019453601, 1)], {1420431019453601: 2}),
    1490373654868277728201: ('pock', [(2173189931274829, 1)], {2173189931274829: 2}),
    2556946286738816232541: ('pock', [(6087967349378133887, 1)], {6087967349378133887: 2}),
    1081840417044928050054133: ('pock', [(2641917343453, 1)], {2641917343453: 2}),
    286414695690956651258188903406027: ('pock', [(2556946286738816232541, 1)], {2556946286738816232541: 2}),
    39090964075753344274635165434556691: ('pock', [(1081840417044928050054133, 1)], {1081840417044928050054133: 2}),
    32066786922909377348614521827952068307593: ('pock', [(39090964075753344274635165434556691, 1)], {39090964075753344274635165434556691: 2}),
    39943240112845630092010750031829037606979: ('pock', [(1490373654868277728201, 1)], {1490373654868277728201: 2}),
    3355232169479032927728903002673639158986237: ('pock', [(39943240112845630092010750031829037606979, 1)], {39943240112845630092010750031829037606979: 2}),
    388047625887519318814728811421887750353372658917462173: ('pock', [(32066786922909377348614521827952068307593, 1)], {32066786922909377348614521827952068307593: 2}),
    47232776114222237582693563801154144147930766854572715659: ('pock', [(3355232169479032927728903002673639158986237, 1)], {3355232169479032927728903002673639158986237: 2}),
    239375709346878300069090981344249202541713126418974522959813: ('pock', [(47232776114222237582693563801154144147930766854572715659, 1)], {47232776114222237582693563801154144147930766854572715659: 2}),
    154748277960138255063653234239856671516599858217894064606035513: ('lucas', 3, 5, [(2, 1), (199393409, 1), (388047625887519318814728811421887750353372658917462173, 1)]),
    5297301560745126215092811500755495969556358793347764950769236993482218825781993: ('pock', [(154748277960138255063653234239856671516599858217894064606035513, 1)], {154748277960138255063653234239856671516599858217894064606035513: 2}),
    14804809328194960612031186071270721071612332326006472447005610496619217105373041927635455685201: ('lucas', 1, 3, [(2, 1), (3, 3), (11, 1), (17, 1), (223, 1), (1297, 1), (956903, 1), (5297301560745126215092811500755495969556358793347764950769236993482218825781993, 1)]),
}
def jacobi(a, n):
    a %= n
    r = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                r = -r
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            r = -r
        a %= n
    return r if n == 1 else 0

def lucasU(Pq, n, N, Q):
    D, inv2 = Pq * Pq - 4 * Q, pow(2, -1, N)
    U, V, Qk = 0, 2, 1
    for bit in bin(n)[2:]:
        U, V, Qk = U * V % N, (V * V - 2 * Qk) % N, Qk * Qk % N
        if bit == '1':
            U, V = (Pq * U + V) * inv2 % N, (D * U + Pq * V) * inv2 % N
            Qk = Qk * Q % N
    return U

def proved_prime(n):
    if n < 10 ** 12:
        return n > 1 and all(n % q for q in range(2, math.isqrt(n) + 1))
    c = CERTS.get(n)
    if c is None:
        return False
    if c[0] == 'pock':                                   # Pocklington: F | n-1 fully factored, F^2 > n, witnesses
        used, wit = c[1], c[2]
        F = 1
        for q, e in used:
            F *= q ** e
        if (n - 1) % F or F * F <= n:
            return False
        for q, e in used:
            a = wit[q]
            if pow(a, n - 1, n) != 1 or gcd(pow(a, (n - 1) // q, n) - 1, n) != 1 or not proved_prime(q):
                return False
        return True
    Pq, Q, fac = c[1], c[2], c[3]                        # Lucas: n+1 fully factored, (D/n) = -1, U_{n+1} = 0, gcd(U_{(n+1)/q}, n) = 1
    if prod(dict(fac)) != n + 1 or gcd(Q, n) != 1 or jacobi(Pq * Pq - 4 * Q, n) != -1 or lucasU(Pq, n + 1, n, Q) != 0:
        return False
    return all(gcd(lucasU(Pq, (n + 1) // q, n, Q), n) == 1 and proved_prime(q) for q, e in fac)

allprimes = {k: sorted(set(FACT[k][0]) | set(FACT[k][1])) for k in FACT}
ok2 = all(proved_prime(q) for k in range(1, 6) for q in allprimes[k])
check('2 every prime of the lists for k <= 5 is proved prime (trial division below 10^12; above: Pocklington / Lucas certificates, %d nodes)' % len(CERTS), ok2)

# ---------------------------------------------------------------- local tests
random.seed(5)
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


def local_test(p, k):
    """(#roots of f, qualifying roots, geometric pairs, coincident qualifying pairs [(a, a', sign)]) at p for the gap k"""
    rts = roots_of(f_poly(p), p)
    qual = [a for a in rts if qualifying_root(a, p)]
    pairs, co = 0, []
    for a in rts:
        rr = (1 - a) * (1 + a * a) % p
        if legendre(rr, p) != 1:
            continue
        y = sqrt_mod(rr, p)
        for Qp in (((1 - a) % p, y), ((1 - a) % p, (-y) % p)):
            for sg in (1, -1):
                R = add(Qp, mul(sg * k, P0, p), p)
                if R is None:
                    continue
                tp = (1 - R[0]) % p
                if f_mod(tp, p) == 0:
                    pairs += 1
                    if a in qual and qualifying_root(tp, p):
                        co.append((a, tp, sg))
    return rts, qual, pairs, co

def hits_at(k, plist):
    return sorted(q for q in plist if q >= 5 and local_test(q, k)[3])

h4 = hits_at(4, allprimes[4])
check('3 k = 4: Q_n and Q_{n+4} can share only the primes %s (all primes of N_4 >= 5 tested, group law at every root)' % h4,
      h4 == [83, 823, 4241])
h5 = hits_at(5, allprimes[5])
check('4 k = 5: no prime >= 5 lies in Q_n and Q_{n+5} (all %d primes of N_5 >= 5 tested; the 95-digit prime is proved prime in check 2)' % len([q for q in allprimes[5] if q >= 5]),
      h5 == [])
h6, h7 = hits_at(6, allprimes[6]), hits_at(7, allprimes[7])
check('5 k = 6, 7 (partial: composite cofactors unfactored): coincident points among the primes found: k = 6: %s, k = 7: %s' % (h6, h7),
      h6 == [307, 34389517] and h7 == [83, 79734735126883])

# ---------------------------------------------------------------- check 6: orbit membership by baby-step giant-step
def bsgs(Q, p, bound):
    s = math.isqrt(bound) + 1
    baby, cur = {}, None
    for j in range(s):
        baby.setdefault(cur, j)
        cur = add(cur, P0, p)
    step, cur = mul(-s, P0, p), Q
    for i in range(s + 1):
        if cur in baby:
            return i * s + baby[cur]
        cur = add(cur, step, p)
    return None

def orbit_pairs(p, k):
    """[(eps, n, n')]: qualifying points Q = nP + eps T and Q + kP = n'P + eps T, found from the roots; indices by discrete logarithm"""
    out = []
    bound = p + 1 + 2 * math.isqrt(p) + 2
    for a in [a for a in roots_of(f_poly(p), p) if qualifying_root(a, p)]:
        y = sqrt_mod((1 - a) * (1 + a * a) % p, p)
        for Qp in (((1 - a) % p, y), ((1 - a) % p, (-y) % p)):
            R = add(Qp, mul(k, P0, p), p)
            if R is None or not qualifying_root((1 - R[0]) % p, p):
                continue
            for eps in (0, 1):
                Q0, R0 = (Qp, R) if not eps else (add(Qp, T0, p), add(R, T0, p))
                nQ = 0 if Q0 is None else bsgs(Q0, p, bound)
                nR = 0 if R0 is None else bsgs(R0, p, bound)
                if nQ is not None and nR is not None:
                    out.append((eps, nQ, nR))
    return out

ok6, det6 = True, []
for k, p in ((4, 83), (4, 823), (4, 4241), (6, 307), (6, 34389517), (7, 83)):
    res = orbit_pairs(p, k)
    ok6 &= bool(res)
    for eps, n, n2 in res:
        Qn, Qm = mul(n, P0, p), mul(n2, P0, p)
        if eps:
            Qn, Qm = add(Qn, T0, p), add(Qm, T0, p)
        ok6 &= qualifies(Qn, p) and qualifies(Qm, p) and mul(n2 - n - k, P0, p) is None     # (n2 - n - k) P = O
    det6.append('k=%d p=%d: %d orbit pairs, e.g. %s' % (k, p, len(res), res[0] if res else None))
check('6 the coincidences at 83, 823, 4241 (k = 4), 307, 34389517 (k = 6), 83 (k = 7) are pairs of indices n, n+k of one orbit', ok6, '(' + '; '.join(det6) + ')')

# ---------------------------------------------------------------- check 7: scan, gaps 1..12
LIMIT = 3000 if QUICK else 10000
EXPECTED = [(4, 83, 0), (4, 823, 0), (4, 823, 1), (4, 4241, 0), (6, 307, 0), (7, 83, 0), (9, 673, 1), (9, 2381, 1),
            (11, 83, 0), (12, 757, 0), (12, 2549, 0), (12, 6907, 0)]
found = []
for pp in primes_upto(LIMIT):
    for eps in (0, 1):
        pts = orbit(pp, eps)
        mm = len(pts)
        qual = [n for n in range(mm) if qualifies(pts[n], pp)]
        s = set(qual)
        for g in range(1, 13):
            if any((n + g) % mm in s for n in qual):
                found.append((g, pp, eps))
found.sort()
expected = sorted(e for e in EXPECTED if e[1] < LIMIT)
check('7 scan of the full orbits of all primes 5 <= p < %d, gaps 1..12, both branches: %d hits, exactly the expected list; each hit divides N_gap' % (LIMIT, len(found)),
      found == expected and all(NORMS[g] % pp == 0 for g, pp, eps in found),
      str(found) if found != expected else '')

print()
print('FAILED: ' + ', '.join(FAILS) if FAILS else 'all checks passed')
sys.exit(1 if FAILS else 0)
