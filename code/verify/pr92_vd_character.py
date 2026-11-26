#!/usr/bin/env python3
"""Character of the signed permutation representation V_D of Gal(Q(D)/Q) on the 12 points of D (PR #92 sieve dimension).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Observed numerics (Chebotarev averages); the irreducibility is NOT certified by this script.
V_D has basis e_1..e_6 (one for each pair {U, -U} of D) and sigma(e_j) = +-e_{sigma(j)}, sign + if sigma U_j = U_k and - if sigma U_j = -U_k.  For a prime p of good reduction
unramified in Q(D), the trace of Frob_p on V_D is  chi_V(p) = sum over roots x of h in F_p of the Legendre symbol (Y(x)/p)  (+1 if Frobenius fixes U, -1 if it maps U to -U; pairs not fixed contribute 0).
By Chebotarev  <chi_V, 1> = mean of chi_V  and  <chi_V, chi_V> = mean of chi_V^2.  <chi,1> = 0 means no trivial constituent (this is rigorous from 'Y is a non-square in L', see
pr92_sieve_dimension.py); <chi,chi> = 1 means irreducible over C, while a decomposition into k >= 2 constituents would give <chi,chi> >= k >= 2.
Usage: python3 code/verify/pr92_vd_character.py [B]  (default 300000, about 15 s)
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
B = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
import verify_eligible_triples as v


def leg(a, p):
    return 1 if pow(a % p, (p - 1) // 2, p) == 1 else -1


n = s1 = s2 = 0
cnt = Counter()
for p in v.primes_upto(B):
    if p < 5 or p == 23:
        continue
    roots = v.roots_mod_p(p)
    S = sum(leg(v.Yc(x), p) for x in roots)
    n += 1
    s1 += S
    s2 += S * S
    cnt[(len(roots), S)] += 1
print("primes used: %d (5 <= p <= %d, p != 23)" % (n, B))
print("<chi_V, 1>     = %.4f   (0 expected: no trivial constituent)" % (s1 / n))
print("<chi_V, chi_V> = %.4f   (1 = irreducible; a reducible V_D would give at least 2)" % (s2 / n))
print("(#rational roots of h, chi_V) -> number of primes:", sorted(cnt.items()))
ok = abs(s1 / n) < 0.05 and abs(s2 / n - 1) < 0.1
print(("ok   " if ok else "FAIL ") + "chi_V has mean ~ 0 and mean square ~ 1")
sys.exit(0 if ok else 1)
