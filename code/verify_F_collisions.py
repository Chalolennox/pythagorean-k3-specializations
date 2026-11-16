#!/usr/bin/env python3
"""Exact checks for the remark at the end of F.54 (values F(t) and F(t_n)).

Checks (one line each; exit status 0 if all pass, 1 otherwise):
 1. F(t) - F(u) = -4 (t^2 - u^2) Q(t^2, u^2) / ((1+t^2)^3 (1+u^2)^3)  (exact, random rationals)
 2. the degree-2 parametrisation x = A0/B0, y = -C0/D0 satisfies Q = 0 and G(x) = G(y)
 3. Q(x, x) = 3 (x - 1)(11 x + 7)(x + 1)^2
 4. along t_n = 1 - x(nP), P = (1,1) on y^2 = x^3 - 2x^2 + 2x, 1 <= n <= N:
    (a) the values F(t_n) are pairwise distinct and t_m != +-t_n for m != n
    (b) the denominator of F(t_n) is (U_n^2 + V_n^2)^3 (t_n = U_n/V_n)
    (c) the odd part of U_n^2 + V_n^2 grows by a factor > 4 at every step
 4d. the integers F(t_n) = -4 Phi(U_n, V_n) of Appendix F are pairwise distinct as well
 5. no rational t = a/b >= 0 with a, b <= B has F(t) = F(u) for another u >= 0 with a, b <= B
Usage: python3 code/verify_F_collisions.py [--quick]   (full run about 15 s; --quick about 2 s)
Only the Python standard library is used.
"""
import math, random, sys
from fractions import Fraction as Fr

QUICK = "--quick" in sys.argv
N = 40 if QUICK else 120      # orbit length
B = 300 if QUICK else 1500    # height bound of the direct search
results = []

def check(name, ok, extra=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (("  " + extra) if extra else ""))

def F(t):
    return -4 * (t**6 - 30 * t**4 - 24 * t**2 - 1) / (1 + t * t) ** 3

def g(s):
    return s**3 - 30 * s**2 - 24 * s - 1

def Q(x, y):
    return (33 * x * x * y * y + 27 * x * x * y + 27 * x * y * y + 2 * x * x
            + 2 * y * y - 16 * x * y - 27 * x - 27 * y - 21)

A0 = lambda m: m * m - 108 * m + 2019
B0 = lambda m: m * m - 465
C0 = lambda m: 23 * m * m - 1242 * m + 16143
D0 = lambda m: 31 * m * m - 1674 * m + 22359

random.seed(257)

# 1
ok = True
for _ in range(200):
    t = Fr(random.randint(-60, 60), random.randint(1, 9))
    u = Fr(random.randint(-60, 60), random.randint(1, 9))
    lhs = F(t) - F(u)
    rhs = -4 * (t * t - u * u) * Q(t * t, u * u) / ((1 + t * t) ** 3 * (1 + u * u) ** 3)
    ok &= lhs == rhs
check("1 identity F(t)-F(u) = -4(t^2-u^2)Q/(...)", ok)

# 2
ok = True
for _ in range(200):
    m = Fr(random.randint(-300, 300), random.randint(1, 13))
    if B0(m) == 0 or D0(m) == 0:
        continue
    x, y = A0(m) / B0(m), -C0(m) / D0(m)
    ok &= Q(x, y) == 0 and (1 + x) != 0 and (1 + y) != 0 and \
        -4 * g(x) / (1 + x) ** 3 == -4 * g(y) / (1 + y) ** 3
check("2 parametrisation: Q(x(m), y(m)) = 0 and G(x) = G(y)", ok)

# 3
ok = all(Q(x, x) == 3 * (x - 1) * (11 * x + 7) * (x + 1) ** 2
         for x in (Fr(random.randint(-40, 40), random.randint(1, 7)) for _ in range(60)))
check("3 Q(x,x) = 3(x-1)(11x+7)(x+1)^2", ok)

# 4 the orbit
a2, a4 = -2, 2
def add(P, R):
    if P is None: return R
    if R is None: return P
    x1, y1 = P; x2, y2 = R
    if x1 == x2:
        if y1 == -y2: return None
        l = (3 * x1 * x1 + 2 * a2 * x1 + a4) / (2 * y1)
    else:
        l = (y2 - y1) / (x2 - x1)
    x3 = l * l - a2 - x1 - x2
    return (x3, l * (x1 - x3) - y1)

P = (Fr(1), Fr(1))
assert P[1] ** 2 == P[0] ** 3 - 2 * P[0] ** 2 + 2 * P[0]
R = None; ts = {}; Fs = {}
for n in range(1, N + 1):
    R = add(R, P)
    ts[n] = 1 - R[0]
    Fs[n] = F(ts[n])
distinct = len(set(Fs.values())) == N
pm = all(abs(ts[m]) != abs(ts[n]) for n in ts for m in ts if m < n)
check("4a F(t_n) pairwise distinct, t_m != +-t_n  (1 <= n <= %d)" % N, distinct and pm)

okb = True
for n in range(1, N + 1):
    U, V = ts[n].numerator, ts[n].denominator
    okb &= Fs[n].denominator == (U * U + V * V) ** 3
check("4b den F(t_n) = (U^2+V^2)^3", okb)

def odd(c):
    while c % 2 == 0: c //= 2
    return c
oc = [odd(ts[n].numerator ** 2 + ts[n].denominator ** 2) for n in range(1, N + 1)]
minratio = min(oc[i + 1] / oc[i] for i in range(N - 1)) if N > 1 else 0
check("4c odd part of U^2+V^2 grows by a factor > 4 at every step", all(oc[i + 1] > 4 * oc[i] for i in range(N - 1)),
      "(smallest ratio %.3g)" % minratio)

ints = [-4 * (ts[n].numerator**6 - 30 * ts[n].numerator**4 * ts[n].denominator**2
              - 24 * ts[n].numerator**2 * ts[n].denominator**4 - ts[n].denominator**6) for n in range(1, N + 1)]
cube_ok = all(ints[n - 1] == Fs[n] * (ts[n].numerator ** 2 + ts[n].denominator ** 2) ** 3 for n in range(1, N + 1))
check("4d integers F(t_n) = -4 Phi(U_n,V_n) = c_n^3 F^o(t_n) pairwise distinct", len(set(ints)) == N and cube_ok)

# 5 direct search over t = a/b >= 0
seen = {}
coll = []
for b in range(1, B + 1):
    b2 = b * b; b4 = b2 * b2; b6 = b4 * b2
    for a in range(0, B + 1):
        if math.gcd(a, b) != 1: continue
        a2_ = a * a; a4_ = a2_ * a2_; a6 = a4_ * a2_
        num = -4 * (a6 - 30 * a4_ * b2 - 24 * a2_ * b4 - b6)
        den = (a2_ + b2) ** 3
        gg = math.gcd(num, den)
        key = (num // gg, den // gg)
        if key in seen: coll.append((seen[key], (a, b)))
        else: seen[key] = (a, b)
check("5 no F(t) = F(u), 0 <= t < u, heights <= %d (%d values)" % (B, len(seen)), not coll, str(coll[:3]) if coll else "")

sys.exit(0 if all(results) else 1)
