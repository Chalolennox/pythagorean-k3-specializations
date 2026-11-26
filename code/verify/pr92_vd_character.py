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

# Comparison with the owner-attested exact Galois computation (PR #83 comment 7201408002, Magma V2.30-1): |G| = 1536, trace histogram of chi_V
# at -6,-4,-2,0,2,4,6 equal to 1,6,159,1204,159,6,1.  By Chebotarev the observed trace frequencies should match these proportions.
OWNER = {-6: 1, -4: 6, -2: 159, 0: 1204, 2: 159, 4: 6, 6: 1}
obs = Counter()
for (nr, S), c in cnt.items():
    obs[S] += c
chi2 = 0.0
print("\ntrace   observed frequency   owner group frequency")
for t in sorted(OWNER):
    e = OWNER[t] / 1536
    chi2 += (obs[t] - n * e) ** 2 / (n * e)
    print("%5d   %.5f              %.5f" % (t, obs[t] / n, e))
print("chi-square statistic (6 degrees of freedom): %.2f" % chi2)
six = sum(c for (nr, S), c in cnt.items() if nr == 6) / n
print("fraction of primes with 6 rational roots: %.4f (1/24 = %.4f for the owner's group acting on 6 pairs through a quotient of order 24)" % (six, 1 / 24))
ok2 = chi2 < 16.8 and set(nr for (nr, S) in cnt) <= {0, 2, 6}  # 99 percent point of chi-square with 6 d.o.f. is 16.81
print(("ok   " if ok2 else "FAIL ") + "observed trace distribution consistent with the owner's group (chi-square below the 99% point); root counts only 0, 2, 6")

# R(z) = prod (z^2 - Y(x_i)) over the roots of h, computed exactly as the characteristic polynomial of multiplication by Y on Q[x]/(h)
from fractions import Fraction as Fr
hh = [Fr(c) for c in v.FC]


def mulmod(a, b):
    r = [Fr(0)] * 11
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    for k in range(10, 5, -1):
        c = r[k]
        if c:
            for i in range(7):
                r[k - 6 + i] -= c * hh[i]
    return r[:6]


Ycoef = [Fr(0), Fr(2), Fr(-2), Fr(1), Fr(0), Fr(0)]
cols = []
for j in range(6):
    e = [Fr(0)] * 6
    e[j] = Fr(1)
    cols.append(mulmod(Ycoef, e))
Mx = [[cols[j][i] for j in range(6)] for i in range(6)]
I6 = [[Fr(int(i == j)) for j in range(6)] for i in range(6)]


def mm(A, Bm):
    return [[sum(A[i][k] * Bm[k][j] for k in range(6)) for j in range(6)] for i in range(6)]


cp, Mk = [Fr(1)], I6
for k in range(1, 7):
    if k > 1:
        Mk = [[mm(Mx, Mk)[i][j] + cp[-1] * I6[i][j] for j in range(6)] for i in range(6)]
    AM = mm(Mx, Mk)
    cp.append(-sum(AM[i][i] for i in range(6)) / k)
OWNER_R = [1, -66, -29922, 73214, -62559, 22032, -3456]  # R(z) = z^12 - 66 z^10 - 29922 z^8 + 73214 z^6 - 62559 z^4 + 22032 z^2 - 3456, in w = z^2
ok3 = [int(c) for c in cp] == OWNER_R
print(("ok   " if ok3 else "FAIL ") + "char poly of Y mod h equals the owner's R(w), w = z^2: %s" % [int(c) for c in cp])
sys.exit(0 if (ok and ok2 and ok3) else 1)
