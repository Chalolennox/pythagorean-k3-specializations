#!/usr/bin/env python3
"""Checks for F.56: coprimality of ab with the part of F prime to 6, the identity
4a^3+27b^2c = -4F(U,V)/d^3, (ab/p) = (-3bc/p), the parity functions h, h~ and the
disagreement sign kappa = (-1)^D, and the reciprocity expansion of (ab/M).
Standard library only.  Usage: python3 verify_jacobi_identities.py [--quick]
Also scans n <= NN and primes 5 <= p < PP for p^2 | F_n (EDS recurrence mod p^3)."""
import sys
from math import gcd
QUICK = "--quick" in sys.argv
B = 14 if QUICK else 30          # |u|, v <= B
NN, PP = (300, 600) if QUICK else (2000, 8000)

def jac(a, n):
    assert n > 0 and n % 2 == 1
    a %= n; r = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): r = -r
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: r = -r
        a %= n
    return r if n == 1 else 0

def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1 if p == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

Phi = lambda u, v: u**6 - 30*u**4*v**2 - 24*u**2*v**4 - v**6
ok = {k: True for k in "ABCDEFG"}
cases = primes_seen = squareful = 0
for v in range(1, B + 1):
    for u in range(-B, B + 1):
        if u == 0 or gcd(u, v) != 1 or abs(u) == v: continue
        d = 2 if (u % 2 and v % 2) else 1
        a, b, c = (v*v - u*u)//d, 2*u*v//d, (v*v + u*u)//d
        if gcd(a, b) != 1 or a*a + b*b != c*c: ok["A"] = False
        if d**3 * (4*a**3 + 27*b*b*c) != -4*Phi(u, v): ok["A"] = False
        M = abs(Phi(u, v))
        for p in (2, 3):
            while M % p == 0: M //= p
        if M == 1: continue
        cases += 1
        if gcd(a*b, M) != 1: ok["B"] = False
        f = factor(M)
        lam = (-1)**sum(f.values()); J = jac(a*b, M)
        h = ht = 1; D = 0
        for p, e in f.items():
            primes_seen += 1
            chi = jac(a*b, p)
            if chi == 0 or chi != jac(-3*b*c, p): ok["C"] = False
            h *= -chi; ht *= (-chi)**e
            if e % 2 == 0 and chi == 1: D += 1
        rad = 1
        for p in f: rad *= p
        if h != (-1)**len(f) * jac(a*b, rad): ok["D"] = False       # h = (-1)^omega (ab/R)
        if ht != lam * J: ok["D"] = False                           # h~ = lambda(M) (ab/M)
        if h * ht != (-1)**D: ok["E"] = False                       # h h~ = (-1)^D
        # G: local evaluation of (M/l) for the odd primes l | ab, in the orbit situation M = |Phi|
        Ph = Phi(u, v)
        if Ph % 2 and Ph % 3:
            sg = 1 if Ph > 0 else -1
            q2 = abs(a*b)
            while q2 % 2 == 0: q2 //= 2
            for l, el in factor(q2).items():
                if a % l == 0:   want = jac(-6*sg, l)
                elif u % l == 0: want = jac(-sg, l)
                else:            want = jac(sg, l)
                if jac(M, l) != want: ok["G"] = False
            ok_prod = 1
            for l, el in factor(q2).items():
                ok_prod *= jac(M, l)**el
            if jac(M, q2) != ok_prod: ok["G"] = False
        if any(e % 2 == 0 for e in f.values()): squareful += 1
        # reciprocity expansion
        ab = a*b; eps = 1 if ab > 0 else -1; q = abs(ab); k = 0
        while q % 2 == 0: q //= 2; k += 1
        rhs = jac(eps % M, M) * jac(2, M)**k * (-1)**(((q-1)//2)*((M-1)//2)) * jac(M, q)
        if rhs != J: ok["D"] = False
print("pairs with M>1: %d, prime factors tested: %d, with a square prime factor: %d"
      % (cases, primes_seen, squareful))
# F: scan of p^2 | F_n along the orbit
primes = [p for p in range(5, PP) if all(p % q for q in range(2, int(p**.5) + 1))]
hits = []
for p in primes:
    Mod = p**3; i2 = pow(2, -1, Mod)
    W = [0, 1, 2, 3, -20 % Mod] + [0]*(NN + 2)
    for n in range(5, NN + 2):
        m = n // 2
        if n % 2: W[n] = (W[m+2]*W[m]**3 - W[m-1]*W[m+1]**3) % Mod
        else:     W[n] = W[m]*(W[m+2]*W[m-1]**2 - W[m-2]*W[m+1]**2)*i2 % Mod
    for n in range(2, NN + 1):
        U = W[n-1]*W[n+1] % Mod; V = W[n]*W[n] % Mod
        if Phi(U, V) % (p*p) == 0: hits.append((n, p))
ns = sorted(set(n for n, p in hits))
print("n <= %d, 5 <= p < %d: %d values of n with p^2 | F_n (%.4f); primes %s"
      % (NN, PP, len(ns), len(ns)/(NN - 1), sorted(set(p for n, p in hits))))
# p = 23: the hits lie in classes modulo p*r, r = rank of apparition of 23 (order of P mod 23)
def rank_of_apparition(p):
    W = [0, 1, 2, 3, -20 % p]
    for n in range(5, 4*p + 8):
        m = n // 2
        if n % 2: W.append((W[m+2]*W[m]**3 - W[m-1]*W[m+1]**3) % p)
        else:     W.append(W[m]*(W[m+2]*W[m-1]**2 - W[m-2]*W[m+1]**2)*pow(2, -1, p) % p)
    return next(k for k in range(1, len(W)) if W[k] == 0)
r23 = rank_of_apparition(23)
cl = sorted(set(n % (23*r23) for n, p in hits if p == 23))
print("rank of apparition of 23: %d; classes of n mod %d with 23^2 | F_n: %s" % (r23, 23*r23, cl))
ok["F"] = len(cl) <= 2 and 32 % (23*r23) in cl or QUICK
res = {"A": "identity 4a^3+27b^2c = -4F/d^3 and primitivity", "B": "gcd(ab, M) = 1",
       "C": "(ab/p) = (-3bc/p) for p | M, p >= 5, and chi_p != 0",
       "D": "h = (-1)^omega(R) (ab/R), h~ = lambda(M)(ab/M), reciprocity expansion",
       "E": "h h~ = (-1)^D",
       "G": "(M/l) for l | ab from the local table, (M/q) as a product", "F": "scan of p^2 | F_n; classes mod p*r for p = 23"}
allok = True
for k in "ABCDEFG":
    s = ok[k]; allok &= s
    print(("PASS " if s else "FAIL ") + res[k])
sys.exit(0 if allok else 1)
