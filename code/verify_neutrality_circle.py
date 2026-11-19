#!/usr/bin/env python3
"""Neutral points on the rational unit circle (19 November 2026).

t = u/v in lowest terms, (a,b,c) = ((v^2-u^2)/d, 2uv/d, (v^2+u^2)/d), d = gcd in {1,2}, F = 4a^3 + 27 b^2 c, D = a b.
A circle point is NEUTRAL if no prime p >= 5 dividing F has (D/p) = +1 (equivalently every local root number at p >= 5, p | F is +1).
The reflection t -> -t changes b to -b, so D to -D, and leaves F unchanged.

Checks (all asserted):
  1. Reproduces the summary of an independent Magma V2.30 run (u+v odd, v <= 40): 662 points, 174 neutral, pairs 20 / 71 / 63 / 177
     (both / only B+ / only B- / neither); B+ neutral: 71 with a prime = 3 mod 4 among the candidates, 20 with all candidates = 1 mod 4.
  2. Proposition: both reflected points are neutral  <=>  every prime p >= 5 dividing F has p = 1 mod 4 and (D/p) = -1.
  3. Sharp necessary congruence: with F = 2^al 3^e m, both neutral forces m = 1 mod 4, hence
       u+v odd:  a = (-1)^e (mod 4);     u, v both odd (d = 2):  e is odd  (F = 3 mod 4 because c = 1 mod 4).
  4. Prime-value family: along t = 1/(12k) the symbol (ab/N) is -1 for every k (N = part of |F| prime to 6), so F prime  =>  neutral;
     along t = u = 6w the symbol depends only on u mod 24 (-1 for u = 0, 12; +1 for u = 6, 18).  Counts of prime values and neutral points.
  5. Orbit: on both branches nP, nP + T (n <= 40) the denominator of t = 1 - x is a perfect square and t <= 1; the orbit members of the
     complete factorizations (data/factorizations.json) with Q_n empty are nP, n = 9 and nP + T, n = 3.
  6. The negative result: t = 1/(12k), t = 12k, t = -12k, t = -1/(12k) are never of the form 1 - x(Q), Q in C(Q); the only integral t on C
     with |t| <= 2*10^5 are -7, -1, 0, 1.  Criterion: t = u/v is 1 - x(Q) iff v = s^2 and (s^2-u)(s^4+u^2) is a square.
Standard library only.  Default run about 1 second; --quick is smaller.  Derived with a language model; no human check;
no consequence for Problem H (neutral on the circle does not give neutral on the orbit)."""
import sys, math, random, json, os
from fractions import Fraction as Fr
QUICK = "--quick" in sys.argv
random.seed(1)

# ---------- number theory helpers
def is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d = n - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):     # deterministic below 3.3e24, probable above
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def rho(n):
    if n % 2 == 0: return 2
    while True:
        c = random.randrange(1, n); x = y = random.randrange(2, n); d = 1
        while d == 1:
            x = (x * x + c) % n; y = (y * y + c) % n; y = (y * y + c) % n; d = math.gcd(abs(x - y), n)
        if d != n: return d
def factor(n):
    f = {}
    for p in (2, 3, 5, 7, 11, 13):
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
    st = [n] if n > 1 else []
    while st:
        m = st.pop()
        if m == 1: continue
        if is_prime(m): f[m] = f.get(m, 0) + 1; continue
        d = rho(m); st += [d, m // d]
    return f
def leg(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
def jac(a, n):
    a %= n; r = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): r = -r
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: r = -r
        a %= n
    return r if n == 1 else 0
def isq(n): r = math.isqrt(n); return n >= 0 and r * r == n

def abc(u, v):
    d = 1 if (u + v) % 2 else 2
    a = (v * v - u * u) // d; b = 2 * u * v // d; c = (v * v + u * u) // d
    assert a * a + b * b == c * c and math.gcd(math.gcd(abs(a), abs(b)), c) == 1
    return a, b, c
def info(u, v, full=True):
    a, b, c = abc(u, v); F = 4 * a ** 3 + 27 * b * b * c
    fa = factor(abs(F)); cand = [p for p in fa if p >= 5]; D = a * b
    return dict(a=a, b=b, c=c, F=F, fa=fa, cand=cand,
                nB=all(leg(D, p) == -1 for p in cand), nM=all(leg(-D, p) == -1 for p in cand))
def symbolN(u, v):                                     # Jacobi (ab / N), N = part of |F| prime to 6
    a, b, c = abc(u, v); N = abs(4 * a ** 3 + 27 * b * b * c)
    for p in (2, 3):
        while N % p == 0: N //= p
    return (jac(a * b, N) if N > 1 else 1), N

# ---------- 1, 2: the Magma summary and the proposition (u+v odd, v <= 40)
rows = {}
for v in range(2, 41):
    for u in range(1, v):
        if math.gcd(u, v) == 1 and (u + v) % 2: rows[(u, v)] = info(u, v)
assert len(rows) == 331
both = sum(r['nB'] and r['nM'] for r in rows.values()); oB = sum(r['nB'] and not r['nM'] for r in rows.values())
oM = sum(r['nM'] and not r['nB'] for r in rows.values()); nei = sum(not r['nB'] and not r['nM'] for r in rows.values())
assert (both, oB, oM, nei) == (20, 71, 63, 177) and 2 * both + oB + oM == 174
has3 = lambda r: any(p % 4 == 3 for p in r['cand'])
assert sum(r['nB'] and has3(r) for r in rows.values()) == 71 and sum(r['nB'] and not has3(r) for r in rows.values()) == 20
assert all((r['nB'] and r['nM']) == (r['nB'] and all(p % 4 == 1 for p in r['cand'])) for r in rows.values())
assert all((r['F'] // 4 - r['a']) % 4 == 0 for r in rows.values())                  # F/4 = a mod 4 for u + v odd
print("1-2 OK: 662 points, 174 neutral (0.2628); pairs both/B+/B-/neither = 20/71/63/177; proposition holds on all 331 pairs")

# ---------- 3: sharp congruence, both parity classes, and the neutral fractions
H3 = 60 if QUICK else 100
viol = 0
for H in (40, H3):
    for par in ("u+v odd", "u,v odd"):
        pairs = pts = bo = 0
        for v in range(2, H + 1):
            for u in range(1, v):
                if math.gcd(u, v) != 1 or ((u + v) % 2 == 1) != (par == "u+v odd"): continue
                r = info(u, v); pairs += 1; pts += r['nB'] + r['nM']
                if r['nB'] and r['nM']:
                    bo += 1; e = r['fa'].get(3, 0)
                    viol += not ((r['a'] % 4 == (1 if e % 2 == 0 else 3)) if par == "u+v odd" else (e % 2 == 1))
        print("   v <= %d, %s: pairs %d, neutral points %d of %d = %.4f, both-neutral pairs %d" % (H, par, pairs, pts, 2 * pairs, pts / (2 * pairs), bo))
assert viol == 0
print("3 OK: sharp congruence (a = (-1)^e mod 4, resp. e odd) holds for every both-neutral pair")

# ---------- 4: prime-value families
for k in range(1, 3001 if not QUICK else 600):
    assert symbolN(1, 12 * k)[0] == -1
tab = {}
for w in range(1, 4000 if not QUICK else 1000):
    u = 6 * w; tab.setdefault(u % 24, set()).add(symbolN(u, 1)[0])
assert tab == {0: {-1}, 12: {-1}, 6: {1}, 18: {1}}, tab
K = 6000 if not QUICK else 1500
pr = sum(1 for k in range(1, K) if is_prime(symbolN(1, 12 * k)[1])); assert pr > 0
W = 20000 if not QUICK else 5000; prime_u = neutral_u = 0
for w in range(1, W + 1):
    s, N = symbolN(6 * w, 1)
    if is_prime(N): prime_u += 1; neutral_u += (s == -1)
print("4 OK: t = 1/(12k): symbol -1 for all k; F'' prime for %d of %d values of k, all neutral. t = 6w <= %d: F'' prime for %d, neutral for %d (u = 0 mod 12)" % (pr, K - 1, 6 * W, prime_u, neutral_u))

# ---------- 5: orbit
def add(A, B):
    if A is None: return B
    if B is None: return A
    x1, y1 = A; x2, y2 = B
    if x1 == x2 and y1 + y2 == 0: return None
    l = (3 * x1 * x1 - 4 * x1 + 2) / (2 * y1) if A == B else (y2 - y1) / (x2 - x1)
    x3 = l * l + 2 - x1 - x2; return (x3, l * (x1 - x3) - y1)
P = (Fr(1), Fr(1)); T = (Fr(0), Fr(0)); Q = None
tp = {}
for n in range(1, 41):
    Q = add(Q, P)
    for br, R in (("nP", Q), ("nP+T", add(Q, T))):
        if R is None: continue
        t = 1 - R[0]; tp[(br, n)] = t
        assert isq(t.denominator) and t <= 1
print("5a OK: all %d orbit points (n <= 40, both branches) have a square denominator and t <= 1" % len(tp))
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "factorizations.json")
if os.path.exists(path):
    empty = []
    for e in json.load(open(path))['entries']:
        if e['status'] != 'complete': continue
        R = None
        for _ in range(e['n']): R = add(R, P)
        if e['orbit'] == 'nP+T': R = add(R, T)
        t = 1 - R[0]; u, v = t.numerator, t.denominator
        a, b, c = abc(u, v); ps = [int(p) for p in e['primes'] if int(p) >= 5]
        if not any(leg(a * b, p) == 1 for p in ps): empty.append((e['orbit'], e['n']))
    assert empty == [('nP', 9), ('nP+T', 3)], empty
    print("5b OK: orbit members (complete factorizations) with Q_n empty: nP n = 9 and nP+T n = 3")

# ---------- 6: the negative result
bound = 6 * (5000 if QUICK else 20000)
assert not [s for s in range(6, bound, 6) if isq((s * s - 1) * (s ** 4 + 1))]
assert {((s * s - 1) * (s ** 4 + 1)) % 3 for s in range(3, 300, 3)} == {2}           # 3 | s: product = 2 mod 3, not a square
assert not [s for s in range(6, bound, 6) if isq((s * s + 1) * (s ** 4 + 1))]          # t = -1/(12k)
assert not [u for u in range(12, 10 ** 6, 12) if isq((1 + u) * (1 + u * u))]            # t = -12k
assert all((1 - 12 * k) * (144 * k * k + 1) < 0 for k in range(1, 1000))                # t = 12k: x < 0, y^2 < 0
ints = [t for t in range(-200000, 2) if isq((1 - t) * (t * t + 1))]
assert ints == [-7, -1, 0, 1], ints
print("6 OK: 1 - x(Q) = 1/(12k), 12k, -12k, -1/(12k) have no solution Q in C(Q); integral t on C with |t| <= 2e5: %s" % ints)
print("OK")
