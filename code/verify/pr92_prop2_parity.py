#!/usr/bin/env python3
"""Independent check of Proposition 2 of notes/ARITHMETIC_CARDINALITY_PRESSURE.md (PR #92).

Written by Claude (a language model), independent of the PR author's scripts.
No human has checked it.  Stdlib only, exact integer arithmetic.  Runtime: about 4 seconds.

CHECKS (for all coprime u,v with 1<=u,v<=BOUND, and the sign flip u -> -u):
 (1) 4a^3+27b^2c = -4*D(u,v) for (a,b,c)=(v^2-u^2,2uv,u^2+v^2), D=u^6-30u^4v^2-24u^2v^4-v^6.
 (2) For primes p>=5 dividing D: Euler-criterion eligibility (ab/p)=1 for the triple (u,v)
     (ab computed from the primitive triple) agrees with (G(u/v)/p)=1, G(t)=2t(1-t^2).
 (3) s(u,v)+s(-u,v) == #{p>=5, p|D, p=3 mod 4} (mod 2), s = number of eligible primes.
 (4) For u=0 mod 6, v=1 mod 6, v<u/6, D squarefree: D>0, D=3 mod 4, gcd(D,6)=1 and exactly
     one of the two signs has odd s (instances of the Theorem's final step).
DOES NOT CHECK: the Chebotarev/CRT existence of primes, Greaves/Lemke Oliver-Thorne squarefree
sieve statement, density claims, or anything about the B=1000 Magma/SAT experiments.
"""
from math import gcd

def D(u, v): return u**6 - 30*u**4*v**2 - 24*u**2*v**4 - v**6

def factor(n):
    n = abs(n); f = {}; p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1; n //= p
        p += 1 if p == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def leg(x, p):
    x %= p
    if x == 0: return 0
    r = pow(x, (p - 1) // 2, p)
    return -1 if r == p - 1 else r

def s_count(u, v):
    a, b, c = v*v - u*u, 2*u*v, u*u + v*v
    d = gcd(gcd(a, b), c)
    assert d in (1, 2), (u, v, d)
    assert 4*a**3 + 27*b*b*c == -4*D(u, v)
    ap, bp = a // d, b // d
    n = 0
    for p in factor(D(u, v)):
        if p < 5: continue
        e1 = leg(ap * bp, p) == 1
        # G(u/v) = 2u(v^2-u^2)/v^3 ; character of 2u v (v^2-u^2) * v^-4 ... use u*v^-1 representative
        vi = pow(v, -1, p)
        t = u * vi % p
        e2 = leg(2 * t * (1 - t * t), p) == 1
        assert e1 == e2, (u, v, p)
        n += e1
    return n

BOUND = 40
cases = 0
for u in range(1, BOUND + 1):
    for v in range(1, BOUND + 1):
        if gcd(u, v) != 1 or D(u, v) == 0: continue
        s1, s2 = s_count(u, v), s_count(-u, v)
        n3 = sum(1 for p in factor(D(u, v)) if p >= 5 and p % 4 == 3)
        assert (s1 + s2 - n3) % 2 == 0, (u, v, s1, s2, n3)
        cases += 1
print("checks (1)-(3) passed for", cases, "coprime pairs (u,v) up to", BOUND)

inst = 0
for v in range(1, 20, 6):
    for u in range(6, 160, 6):
        if not (6 * v < u): continue
        d = D(u, v)
        f = factor(d)
        if any(e > 1 for e in f.values()): continue
        assert d > 0 and d % 4 == 3 and gcd(d, 6) == 1 and gcd(u, v) == 1
        s1, s2 = s_count(u, v), s_count(-u, v)
        assert (s1 + s2) % 2 == 1, (u, v, s1, s2)
        inst += 1
        if inst <= 5: print("instance u=%d v=%d D=%d s(t)=%d s(-t)=%d" % (u, v, d, s1, s2))
print("check (4) passed for", inst, "squarefree instances")
