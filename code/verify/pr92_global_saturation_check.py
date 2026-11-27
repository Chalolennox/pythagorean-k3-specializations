#!/usr/bin/env python3
"""Independent check of notes/KUMMER_GLOBAL_ODD_SATURATION.md (owner proof of odd saturation of M over K by a height argument), PR #92.  Stdlib only.

Written by Claude (a language model), 27 November 2026; no human has checked it.  Does NOT use PARI/Magma and does NOT re-run the owner's nfinit; it re-derives every ingredient that can be checked by finite arithmetic:
 (1) the Bezout identity (12x^2-16x+16)A + (-3x^3-2x^2+10x+8)B = 64 for the duplication x(2Q) = A/B;
 (2) that f(y) = y^12 - 66y^10 - ... - 3456 is the field polynomial of the 12 points (number of roots of f mod p = |D_p| for many primes);
 (3) at p = 7, 23, 71: number of SIMPLE roots of f mod p (each gives an unramified degree-one place of F = Q(y(U)), hence a place with residue field F_p), #J(F_p) and #J(F_p) | 60;
     this uses only unramified places, so it does not depend on the ramified places over 3;
 (4) the exact arithmetic of the height inequality: D = prod p^(2 c_p), 2^k < D, lambda = k (2/3)/12, H(V) > (lambda - 3)/3600, H(U) < 7, hence l <= l_max;
 (5) the finite exclusions: for every odd prime l <= max(137, l_max) a prime p with l | #J(F_p) and [N/l]Q != O, for Q = U (a rational point of D_p at a simple root of f, N even so [N/l]T = O for the 2-torsion T) and for Q = P;
 (6) no odd torsion in J(F) from gcd of the orders #J(F_p) at the unramified places.
Not checked: the Galois sign-flip reduction and the trace K -> F (taken from the owner notes; the trace step is elementary since [K:F] = 128), the formal group fact (valuation of x of a formal group point <= -2), and
the local heights at the archimedean places (re-derived on paper below).
Usage: python3 -I code/verify/pr92_global_saturation_check.py [--out FILE]   (about 1 minute).  Exit 0 iff all checks pass.
"""
import cmath
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v  # noqa: E402

ok_all = True
lines = []


def check(name, cond):
    global ok_all
    s = ("ok   " if cond else "FAIL ") + name
    print(s)
    lines.append(s)
    ok_all = ok_all and cond


def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


# (1) Bezout identity, coefficient lists low degree first
A = pmul([-2, 0, 1], [-2, 0, 1])           # (x^2-2)^2
B = [4 * c for c in [0, 2, -2, 1]]         # 4 x (x^2-2x+2) = 4 (2x - 2x^2 + x^3)
C = [16, -16, 12]
D = [8, 10, -2, -3]
S = padd(pmul(C, A), pmul(D, B))
check("(1) (12x^2-16x+16)(x^2-2)^2 + (-3x^3-2x^2+10x+8) 4x(x^2-2x+2) = %s (expected 64)" % S, S == [64, 0, 0, 0, 0, 0, 0, 0][:len(S)] and S[0] == 64 and all(c == 0 for c in S[1:]))
# duplication formula x(2Q) = (x^2-2)^2/(4 Y(x)) against the group law mod a prime
import pr92_sieve_second_moment as sm  # noqa: E402
p0 = 10007
add, neg, mul = sm.group(p0)
cnt_dup = 0
for x in range(2, 400):
    Y = (x * (x * x - 2 * x + 2)) % p0
    if Y and pow(Y, (p0 - 1) // 2, p0) == 1:
        y = v.sqrt_mod(Y, p0)
        q2 = add((x, y), (x, y))
        if q2 is not None:
            xd = (x * x - 2) ** 2 * pow(4 * Y, -1, p0) % p0
            if q2[0] != xd:
                cnt_dup = -10 ** 6
            cnt_dup += 1
check("(1) duplication x(2Q) = (x^2-2)^2/(4x(x^2-2x+2)) agrees with the group law for %d points mod %d" % (cnt_dup, p0), cnt_dup > 100)

# (2) field polynomial
def fval(y, p):
    return (pow(y, 12, p) - 66 * pow(y, 10, p) - 29922 * pow(y, 8, p) + 73214 * pow(y, 6, p) - 62559 * pow(y, 4, p) + 22032 * pow(y, 2, p) - 3456) % p


def fder(y, p):
    return (12 * pow(y, 11, p) - 660 * pow(y, 9, p) - 8 * 29922 * pow(y, 7, p) + 6 * 73214 * pow(y, 5, p) - 4 * 62559 * pow(y, 3, p) + 2 * 22032 * y) % p


bad = 0
tested = 0
dbl = []
for p in v.primes_upto(5000):
    if p < 5 or p in (23,):
        continue
    allp, elig = sm.points(p)
    simple = [y for y in range(p) if fval(y, p) == 0 and fder(y, p) != 0]
    allr = [y for y in range(p) if fval(y, p) == 0]
    tested += 1
    ys = sorted(set(y for _, y in allp))
    if simple != ys:
        bad += 1
    if len(allr) != len(simple):
        dbl.append(p)
check("(2) over %d primes up to 5000 the SIMPLE roots of f mod p are exactly the y-coordinates of the rational points of the discriminant divisor (mismatches: %d); primes where f has additional multiple roots (index primes): %s" % (tested, bad, dbl), bad == 0)

# (3) local data
def count_points(p):
    sq = bytearray(p)
    for t in range(1, p):
        sq[t * t % p] = 1
    n = 1
    for x in range(p):
        Y = (x * (x * x - 2 * x + 2)) % p
        n += 1 if Y == 0 else (2 if sq[Y] else 0)
    return n


loc = {}
for p in (3, 7, 23, 71):
    N = count_points(p)
    rts = [y for y in range(p) if fval(y, p) == 0]
    simple = [y for y in rts if fder(y, p) != 0]
    loc[p] = (N, len(rts), len(simple))
    print("     p = %2d: #J(F_p) = %2d, roots of f mod p: %d, simple roots: %d" % (p, N, len(rts), len(simple)))
check("(3) #J(F_p) = 6, 12, 20, 60 for p = 3, 7, 23, 71 and all divide 60", [loc[p][0] for p in (3, 7, 23, 71)] == [6, 12, 20, 60] and all(60 % loc[p][0] == 0 for p in loc))
cnts = {p: loc[p][2] for p in (7, 23, 71)}
check("(3) simple roots of f mod 7, 23, 71: %s (owner: 2, 2, 4 degree-one places)" % cnts, cnts == {7: 2, 23: 2, 71: 4})

# (4) arithmetic
Dm = 1
for p in (7, 23, 71):
    Dm *= p ** (2 * cnts[p])
Dfull = Dm * 3 ** 6
check("(4) D (without 3) = 7^4 23^4 71^8 = %d, D with 3^6 = %d (owner: 316299002425639143508066329)" % (Dm, Dfull), Dfull == 316299002425639143508066329)
k_m = Dm.bit_length() - 1
k_f = Dfull.bit_length() - 1
check("(4) 2^%d < D (without the places over 3) and 2^%d < D (owner: 88): exact integer comparison" % (k_m, k_f), 2 ** k_m < Dm and 2 ** k_f < Dfull and k_f >= 88)
check("(4) log 2 > 2/3 (e^2 < 8)", math.exp(2) < 8 and math.log(2) > 2 / 3)
c_up = math.log(7680) / 3
c_lo = math.log(20) / 3
check("(4) log(7680)/3 = %.4f < 3 and log(20)/3 = %.4f" % (c_up, c_lo), c_up < 3)
for tag, k in (("owner (with 3)", k_f), ("mine (without 3)", k_m)):
    lam = k * (2 / 3) / 12      # h(x(60V)) >= log D / 12 > k log2/12 > k (2/3)/12
    Hmin = (lam - 3) / 3600
    print("     %-18s: lambda >= %.4f, H(V) > %.3e" % (tag, lam, Hmin))
# H(U) bound: numerical roots of h
hc = [-54, 162, -189, 100, -15, -6, 1]
rs = [complex(0.4, 0.9) ** k for k in range(6)]
for _ in range(500):
    new = []
    for i, z in enumerate(rs):
        pz = sum(c * z ** j for j, c in enumerate(hc))
        d = 1
        for j, w in enumerate(rs):
            if j != i:
                d *= (z - w)
        new.append(z - pz / d)
    rs = new
resid = max(abs(sum(c * z ** j for j, c in enumerate(hc))) for z in rs)
mahler = sum(math.log(max(1, abs(z))) for z in rs) / 6
HU = mahler + c_lo
check("(4) roots of h: max |root| = %.3f (Cauchy bound 190), h(x(U)) = %.4f, H(U) <= %.4f < 7 (residual %.1e)" % (max(abs(z) for z in rs), mahler, HU, resid), resid < 1e-6 and HU < 7)
lam_f = k_f * (2 / 3) / 12
lmax_f = math.isqrt(int(7 / ((lam_f - 3) / 3600)))
lam_m = k_m * (2 / 3) / 12
lmax_m = math.isqrt(int(7 / ((lam_m - 3) / 3600)))
check("(4) l_max = %d with the owner's data (owner: 115, primes <= 113) and %d without the places over 3 (using H(U) < 7)" % (lmax_f, lmax_m), lmax_f == 115 and lmax_m < 10000)
LMAX = max(137, lmax_f, lmax_m)

# (5) finite exclusions
odd_primes = [q for q in v.primes_upto(LMAX) if q > 2]
needU = {q: None for q in odd_primes}
needP = {q: None for q in odd_primes}
p = 5
PLIM = 60000
while (any(x is None for x in needU.values()) or any(x is None for x in needP.values())) and p < PLIM:
    p = next(q for q in range(p + 1, PLIM + 2) if all(q % d for d in range(2, math.isqrt(q) + 1)))
    if p == 23:
        continue
    N = count_points(p)
    todo = [q for q in odd_primes if N % q == 0 and (needU[q] is None or needP[q] is None)]
    if not todo:
        continue
    add, neg, mul = sm.group(p)
    allp, elig = sm.points(p)
    Dpts = [(x, y) for x, y in allp if fval(y, p) == 0 and fder(y, p) != 0]
    for q in todo:
        if needP[q] is None and mul(N // q, (1, 1)) is not None:
            needP[q] = (p, N, mul(N // q, (1, 1)))
        if needU[q] is None:
            for Q in Dpts:
                R = mul(N // q, Q)
                if R is not None:
                    needU[q] = (p, N, Q, R)
                    break
missU = [q for q, w in needU.items() if w is None]
missP = [q for q, w in needP.items() if w is None]
check("(5) finite exclusions for U (rational point of D_p at a simple root of f, N even, [N/l]Q != O) for all %d odd primes l <= %d (missing: %s); largest prime p used %d" % (len(odd_primes), LMAX, missU, max(w[0] for w in needU.values() if w)), not missU)
check("(5) finite exclusions for P = (1,1) over Q for all odd primes l <= %d (missing: %s); largest prime p used %d" % (LMAX, missP, max(w[0] for w in needP.values() if w)), not missP)
check("(5) every witness has N even (so [N/l]T = O for the 2-torsion point T)", all(w[1] % 2 == 0 for w in list(needU.values()) + list(needP.values())))
lines.append("witness table (l: U-witness [p, N, Q, [N/l]Q]; P-witness [p, N, [N/l]P]):")
for q in odd_primes:
    lines.append("  l = %3d  U: %s   P: %s" % (q, list(needU[q]), list(needP[q])))
# (6) torsion
import functools
g = functools.reduce(math.gcd, [loc[p][0] for p in (7, 23, 71)])
check("(6) gcd of #J(F_p) over the unramified places 7, 23, 71 is %d: J(F) has no torsion of odd order (an odd torsion point of order prime to p injects into J(F_p))" % g, g == 4)
print("DONE")
if OUT:
    open(OUT, "w").write("\n".join(lines) + "\nDONE\n")
sys.exit(0 if ok_all else 1)
