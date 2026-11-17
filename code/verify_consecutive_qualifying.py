#!/usr/bin/env python3
"""Checks for F.57: consecutive qualifying-prime sets and the candidate density.
 (a) the relation Psi(t_n, t_{n+1}) = 0 on both branches nP and nP+T, and Phi = t^2 Psi;
 (b) the iterated resultant D = Res_t(H, Res_u(Phi, H(u))) exactly: D = 2^18 3^30 7 103 113^3 13085561^2;
 (c) the orbit of P modulo 7, 103, 113 and 13085561 (exact): which n have p | N_n and p | N_{n+1}, and (ab/p) there;
 (d) the necessary conditions for a prime to lie in some Q_n (qualifying roots);
 (e) the counts of primes with a qualifying root, and with a qualifying root in the orbit (dossier Part C).
Standard library only.  Usage: python3 verify_consecutive_qualifying.py [--quick]
Full run: about 1-2 minutes (the full orbit modulo 13085561 has 3272847 steps per branch); --quick about 3 s."""
import sys
from fractions import Fraction as Fr
QUICK = "--quick" in sys.argv
results = []
def report(name, ok):
    results.append(ok); print(("PASS " if ok else "FAIL ") + name)

# ---------------- exact orbit over Q
def addQ(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2:
        if y1 + y2 == 0: return None
        lam = (3*x1*x1 - 4*x1 + 2) / (2*y1)
    else: lam = (y2 - y1) / (x2 - x1)
    x3 = lam*lam + 2 - x1 - x2
    return (x3, lam*(x1 - x3) - y1)
P0 = (Fr(1), Fr(1)); T0 = (Fr(0), Fr(0))
Psi = lambda t, u: t*t*u*u - 2*t*u + 4*(t + u) - 3
Phi = lambda t, u: (t*t*u - t + 2)**2 - 4*(1 - t)*(1 + t*t)
NQ = 25 if QUICK else 45
ok = True
for br in (0, 1):
    Q = T0 if br else None
    pts = []
    for n in range(NQ):
        Q = addQ(Q, P0)
        pts.append(Q)
    for a, b in zip(pts, pts[1:]):
        if a is None or b is None: continue
        if Psi(1 - a[0], 1 - b[0]) != 0 or Phi(1 - a[0], 1 - b[0]) != 0: ok = False
ok &= all(Phi(Fr(t), Fr(u)) == Fr(t)**2 * Psi(Fr(t), Fr(u)) for t in range(-4, 5) for u in range(-4, 5))
report("Psi(t_n,t_{n+1}) = 0 = Phi(t_n,t_{n+1}) on nP and nP+T, and Phi = t^2 Psi", ok)

# ---------------- exact resultant
def det(M):
    n = len(M); M = [r[:] for r in M]; sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for i in range(k + 1, n):
                if M[i][k] != 0: M[k], M[i] = M[i], M[k]; sign = -sign; break
            else: return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j]*M[k][k] - M[i][k]*M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n-1][n-1]
def sylv(f, g):
    m = len(f) - 1; n = len(g) - 1; N = m + n; M = []
    for i in range(n): M.append([0]*i + f + [0]*(N - m - 1 - i))
    for i in range(m): M.append([0]*i + g + [0]*(N - n - 1 - i))
    return det(M)
Hc = [1, 0, -30, 0, -24, 0, -1]
def R_at(t0):
    return sylv([t0**4, 2*t0*t0*(2 - t0), (2 - t0)**2 - 4*(1 - t0)*(1 + t0*t0)], Hc)
xs = list(range(0, 34)); ys = [R_at(x) for x in xs]
def interp(xs, ys):
    n = len(xs); coef = [Fr(0)]*n
    for i in range(n):
        b = [Fr(1)]; den = Fr(1)
        for j in range(n):
            if j == i: continue
            nb = [Fr(0)]*(len(b) + 1)
            for k, c in enumerate(b): nb[k] += c*(-xs[j]); nb[k+1] += c
            b = nb; den *= xs[i] - xs[j]
        for k, c in enumerate(b): coef[k] += ys[i]*c/den
    return coef
cf = interp(xs, ys)
deg = max(i for i, c in enumerate(cf) if c != 0)
Rhi = [int(c) for c in cf[:deg+1]][::-1]
D = sylv(Hc, Rhi)
def is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d = n - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x*x % n
            if x == n - 1: break
        else: return False
    return True
report("D = Res_t(H, Res_u(Phi, H(u))) = 2^18 3^30 7 103 113^3 13085561^2 (exact, degree of R = 24), the four primes are prime, gcd(H,R) = 1",
       deg == 24 and abs(D) == 2**18 * 3**30 * 7 * 103 * 113**3 * 13085561**2
       and all(is_prime(p) for p in (7, 103, 113, 13085561)))

# ---------------- orbit modulo p
def leg(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1)//2, p) == 1 else -1)
def orbit_hits(p):
    """for branch nP and nP+T: order r of P, the list of n in [0,r) with H(t)=0 at the point, (t, chi=(ab/p))."""
    def add(A, B):
        if A is None: return B
        if B is None: return A
        x1, y1 = A; x2, y2 = B
        if x1 == x2:
            if (y1 + y2) % p == 0: return None
            lam = (3*x1*x1 - 4*x1 + 2) * pow(2*y1, -1, p) % p
        else: lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam*lam + 2 - x1 - x2) % p
        return (x3, (lam*(x1 - x3) - y1) % p)
    P = (1, 1); T = (0, 0)
    r = 1; S = P
    while S is not None: S = add(S, P); r += 1
    out = []
    for br in (0, 1):
        S = T if br else None; hits = []
        for n in range(r):
            if S is not None:
                a = (1 - S[0]) % p
                if (a**6 - 30*a**4 - 24*a**2 - 1) % p == 0:
                    hits.append((n, a, leg(2*a*(1 - a*a), p)))
            S = add(S, P)
        out.append(hits)
    return r, out
ok = True
for p in (7, 103, 113):
    r, (h0, h1) = orbit_hits(p)
    if h0 or h1: ok = False
report("orbit of P mod 7, 103, 113, full period, both branches: no n with p | N_n", ok)

BIG = 13085561; RBIG = 3272847
def Wmod(n, p, cache):
    if n < 0: return (-Wmod(-n, p, cache)) % p
    if n <= 4: return (0, 1, 2, 3, -20 % p)[n]
    if n in cache: return cache[n]
    m = n // 2
    if n % 2: v = (Wmod(m+2, p, cache)*pow(Wmod(m, p, cache), 3, p) - Wmod(m-1, p, cache)*pow(Wmod(m+1, p, cache), 3, p)) % p
    else:     v = Wmod(m, p, cache)*(Wmod(m+2, p, cache)*Wmod(m-1, p, cache)**2 - Wmod(m-2, p, cache)*Wmod(m+1, p, cache)**2) * pow(2, -1, p) % p
    cache[n] = v; return v
def N_chi(n, p, cache):
    U = Wmod(n-1, p, cache)*Wmod(n+1, p, cache) % p; V = Wmod(n, p, cache)**2 % p
    N = (U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6) % p
    return N, leg(2*U*V*(V*V - U*U), p)
cache = {}
spot = {n: N_chi(n, BIG, cache) for n in (1126541, 1126542, 1126543, 1126544, 1545769, 1727078, 2146304, 2146305)}
ok = (spot[1126542] == (0, -1) and spot[1126543] == (0, -1) and spot[2146304] == (0, -1) and spot[2146305] == (0, -1)
      and spot[1126541][0] != 0 and spot[1126544][0] != 0 and spot[1545769][0] == 0 and spot[1727078][0] == 0
      and Wmod(RBIG, BIG, cache) == 0)
report("p = 13085561 (EDS mod p): p | N_n and p | N_{n+1} at n = 1126542 and 2146304 with (ab/p) = -1 at both; W_3272847 = 0", ok)
if not QUICK:
    r, (h0, h1) = orbit_hits(BIG)
    cons = [(n, (n + 1) % r) for n, _, _ in h0 if any(m == (n + 1) % r for m, _, _ in h0)]
    ok = (r == RBIG and [n for n, _, _ in h0] == [1126542, 1126543, 1545769, 1727078, 2146304, 2146305]
          and not h1 and all(c == -1 for n, _, c in h0 if n in (1126542, 1126543, 2146304, 2146305)) and len(cons) == 2)
    report("p = 13085561, full orbit (3272847 steps per branch): six hits on nP, none on nP+T, two consecutive pairs, all with (ab/p) = -1", ok)

# ---------------- necessary conditions and counts
def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b"\x00\x00"
    for i in range(2, int(n**.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]
def qualifying_xs(p):
    two = leg(2, p) == 1; xs = set(); any_ = False
    for a in range(p):
        a2 = a*a % p
        if (a2**3 - 30*a2*a2 - 24*a2 - 1) % p: continue
        den = (1 + a2) % p
        if den == 0: continue
        qq = 2*a*(1 - a2) % p; rr = (1 - a) * den % p
        if qq == 0 or rr == 0 or leg(qq, p) != 1 or leg(rr, p) != 1: continue
        if two and leg(1 - a, p) != 1: continue
        xs.add((1 - a) % p)
    return xs
PN = 300 if QUICK else 1500
bad = checked = qual = 0
for p in primes_upto(PN):
    if p < 5: continue
    r, (h0, h1) = orbit_hits(p)
    for hits in (h0, h1):
        for n, a, chi in hits:
            checked += 1
            if chi == 1:
                qual += 1
                if not (leg((1 - a)*(1 + a*a), p) == 1 and (leg(2, p) != 1 or leg(1 - a, p) == 1)): bad += 1
report("every p | N_n with (ab/p) = +1 meets the qualifying conditions (p < %d: %d hits, %d with (ab/p) = +1)" % (PN, checked, qual), bad == 0 and qual > 0)

LIM = 2000 if QUICK else 20000
tot = ne = orb = 0
for p in primes_upto(LIM):
    if p < 5: continue
    tot += 1
    xs_ = qualifying_xs(p)
    if not xs_: continue
    ne += 1
    # orbit membership: any point nP or nP+T with x in xs_
    def addp(A, B):
        if A is None: return B
        if B is None: return A
        x1, y1 = A; x2, y2 = B
        if x1 == x2:
            if (y1 + y2) % p == 0: return None
            lam = (3*x1*x1 - 4*x1 + 2) * pow(2*y1, -1, p) % p
        else: lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam*lam + 2 - x1 - x2) % p
        return (x3, (lam*(x1 - x3) - y1) % p)
    S = None; hit = False
    while True:
        if S is not None and S[0] in xs_: hit = True
        ST = addp(S, (0, 0))
        if ST is not None and ST[0] in xs_: hit = True
        S = addp(S, (1, 1))
        if S is None or hit: break
    orb += hit
print("primes 5 <= p <= %d: %d, with a qualifying root: %d, with a qualifying root in the orbit: %d" % (LIM, tot, ne, orb))
if QUICK: report("counts for p <= 2000 (regression values)", (tot, ne, orb) == (301, 38, 28))
else:     report("counts for p <= 20000 equal the dossier's 2260, 348, 263 (excluded by the orbit: 85)", (tot, ne, orb) == (2260, 348, 263))

report("prod (1 + u_i) = -g(-1) = 8 for the roots u_i of g(U) = U^3 - 30U^2 - 24U - 1 (so sqrt(2) lies in L)", -((-1)**3 - 30*(-1)**2 - 24*(-1) - 1) == 8)
sys.exit(0 if all(results) else 1)
