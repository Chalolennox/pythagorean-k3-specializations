#!/usr/bin/env python3
"""Sieve dimension of the eligible-prime coverage by Chebotarev, with finite checks of each step.  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Rigorous parts are labelled PROOF GIVEN (they use only the finite computations printed here);
the passage from the Frobenius average to the sieve dimension of the coverage sums is CONDITIONAL / HEURISTIC and tested numerically.  No claim about Problem H.

Setting.  h(x) = H(1-x) = x^6-6x^5-15x^4+100x^3-189x^2+162x-54, Y(x) = x^3-2x^2+2x, g(1-x) = 2(1-x)(1-(1-x)^2) = 2(1-x)x(2-x).  L = Q[x]/(h).
X~ = {(x, y, w) : h(x) = 0, y^2 = Y(x), w^2 = g(1-x)}  (24 geometric points).  A prime p >= 5 not dividing disc(h) = 2^6 3^18 23^2 has
#X~(F_p) = 2 |D_p^+|, #X(F_p) = |D_p| for X = {(x,y)} (12 points), #roots(h mod p) = number of F_p-rational x.

Step 1 (PROOF GIVEN).  h is irreducible over Q: mod 11 it factors as 3+3 and mod 29 as 2+4 (computed below); any factorization over Q would refine both patterns, forcing degrees 6.
Step 2 (PROOF GIVEN).  Y, g(1-x) and Y g(1-x) are non-squares in L: a square in L would be a square mod every prime ideal of degree one (every root x in F_p); the script finds
roots x mod p where each of the three is a non-square.  Hence L[y, w]/(y^2-Y, w^2-g) is a field of degree 4 over L, X~ is a single Galois orbit (24 points), X is a single orbit (12 points) and
Spec L is a single orbit (6 points).
Step 3 (Chebotarev, PROOF GIVEN from Steps 1-2).  The mean over primes of #roots, |D_p|, |D_p^+| is 1, 1, 1/2 (mean number of fixed points of Frobenius = number of orbits; |D_p^+| = #X~(F_p)/2).
Step 4 (CONDITIONAL).  The coverage weight of p is a_p / d_p with a_p = |D_p^+ ∩ <P mod p>|, d_p = ord(P mod p).  If the points of D_p^+ behave like random points of J(F_p) with respect
to the cyclic group <P> (Kummer-type independence; an Artin-type constant C may enter), then sum_{p <= B} a_p/d_p ~ C * (1/2) * log log B, i.e. the sieve dimension is kappa = C/2, and C = 1 if there is no entanglement.
Numerics below test Step 4: they compare sum a_p/d_p with sum |D_p^+|/p and display the drift of the difference.

Usage: python3 code/verify/pr92_sieve_dimension.py [--B 300000]  (default 300000, about 15 s; --B 2000000 about 3 minutes).  Exit 0 iff Steps 1-3 checks and the mean checks pass.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import verify_eligible_triples as v

B = 300000
if "--B" in sys.argv:
    B = int(sys.argv[sys.argv.index("--B") + 1])
sys.argv = [sys.argv[0]]  # keep the imported module's own option parser quiet
import pr92_sieve_second_moment as sm  # noqa: E402

ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok = ok and cond


def dd_pattern(p):
    """factor degrees of h mod p for squarefree reduction (distinct-degree factorization)."""
    f = v.pnorm([c % p for c in v.FC])
    degs = []
    g = f[:]
    cur = [0, 1]
    for k in range(1, 7):
        if len(g) <= 1:
            break
        cur = v.ppowx_shift(cur, p, g, p)
        d = cur + [0] * (2 - len(cur))
        d = d[:]
        d[1] = (d[1] - 1) % p
        d = v.pnorm(d)
        G = g[:] if not d else v.pgcd(g, d, p)
        if len(G) > 1:
            degs += [k] * ((len(G) - 1) // k)
            q = [0] * (len(g) - len(G) + 1)
            r = g[:]
            ig = pow(G[-1], -1, p)
            for i in range(len(q) - 1, -1, -1):
                c = r[i + len(G) - 1] * ig % p
                q[i] = c
                for j in range(len(G)):
                    r[i + j] = (r[i + j] - c * G[j]) % p
            g = v.pnorm(q)
            cur = v.pmod(cur, g, p) if len(g) > 1 else cur
    return degs


def main():
    # Step 1
    d11, d29 = dd_pattern(11), dd_pattern(29)
    check("Step 1: h mod 11 has factor degrees %s (expected [3, 3]) and h mod 29 has %s (expected [2, 4]); hence h is irreducible over Q" % (d11, d29), d11 == [3, 3] and d29 == [2, 4])
    # Step 2
    wit = {"Y": None, "g": None, "Yg": None}
    for p in v.primes_upto(2000):
        if p < 5 or p in (23,):
            continue
        for x in v.roots_mod_p(p):
            Y = v.Yc(x) % p
            gg = v.gc((1 - x) % p) % p
            if Y == 0 or gg == 0:
                continue
            sq = lambda a: pow(a, (p - 1) // 2, p) == 1
            if wit["Y"] is None and not sq(Y):
                wit["Y"] = (p, x)
            if wit["g"] is None and not sq(gg):
                wit["g"] = (p, x)
            if wit["Yg"] is None and not sq(Y * gg % p):
                wit["Yg"] = (p, x)
        if all(wit.values()):
            break
    check("Step 2: non-square witnesses (p, root x mod p) for Y, g(1-x), Y*g(1-x): %s" % wit, all(wit.values()))
    check("Step 2/3: so L[y,w]/(y^2-Y, w^2-g) is a field of degree 4 over L; X~ has one Galois orbit of 24 points, X one orbit of 12, Spec L one orbit of 6", all(wit.values()) and d11 == [3, 3] and d29 == [2, 4])

    # Step 3 numerics + Step 4 numerics
    nprime = 0
    s_roots = s_D = s_Dp = 0
    sum_a_d = 0.0   # sum a_p / d_p
    sum_Dp_p = 0.0  # sum |D_p^+| / p
    marks = sorted({int(10 ** (3 + 0.5 * k)) for k in range(0, 30) if 10 ** (3 + 0.5 * k) < B} | {B})
    mi = 0
    rows = []
    for p in v.primes_upto(B):
        if p < 7 or p == 23:
            continue
        nprime += 1
        roots = v.roots_mod_p(p)
        allp, elig = sm.points(p)
        s_roots += len(roots)
        s_D += len(allp)
        s_Dp += len(elig)
        sum_Dp_p += len(elig) / p
        if elig:
            add, neg, mul = sm.group(p)
            P = (1, 1)
            L = math.isqrt(4 * p) + 6
            cur = P
            Eset = set(elig)
            hits = 0
            d = None
            for n in range(1, L + 1):
                if cur is None:
                    d = n
                    break
                if cur in Eset:
                    hits += 1
                cur = add(cur, P)
            if d is None:
                d = sm.order_bsgs(p, P, add, neg, mul)
                hits = sum(1 for e in elig if sm.dlog(P, d, e, add, neg, mul) is not None)
            sum_a_d += hits / d
        while mi < len(marks) and p >= marks[mi]:
            rows.append((marks[mi], nprime, s_roots / nprime, s_D / nprime, s_Dp / nprime, sum_a_d, sum_Dp_p))
            mi += 1
    while mi < len(marks):
        rows.append((marks[mi], nprime, s_roots / nprime, s_D / nprime, s_Dp / nprime, sum_a_d, sum_Dp_p))
        mi += 1
    print("\nStep 3 numerics (primes 7 <= p <= B, p != 23): means of #roots, |D_p|, |D_p^+| should tend to 1, 1, 0.5 (Chebotarev error about 1/sqrt(#primes))")
    print("Step 4 numerics: S_A = sum a_p/d_p, S_D = sum |D_p^+|/p, and kappa_eff = d S / d loglog B between rows")
    print("   B         #primes  mean|roots|  mean|D_p|  mean|D_p^+|   S_A      S_D      S_A-S_D   kappa_A  kappa_D")
    prev = None
    for r in rows:
        if prev:
            dl = math.log(math.log(r[0])) - math.log(math.log(prev[0]))
            kA, kD = (r[5] - prev[5]) / dl, (r[6] - prev[6]) / dl
        else:
            kA = kD = float("nan")
        print("   %-9d %-8d %-12.4f %-10.4f %-13.4f %-8.4f %-8.4f %-9.4f %-8.3f %-8.3f" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[5] - r[6], kA, kD))
        prev = r
    last = rows[-1]
    se = 1 / math.sqrt(last[1])
    check("Step 3 numerics: means %.3f, %.3f, %.3f within 0.05 of 1, 1, 0.5" % (last[2], last[3], last[4]), abs(last[2] - 1) < 0.05 and abs(last[3] - 1) < 0.05 and abs(last[4] - 0.5) < 0.05)
    big = [r for r in rows if r[0] >= 30000]
    if len(big) >= 2:
        dl = math.log(math.log(big[-1][0])) - math.log(math.log(big[0][0]))
        kA = (big[-1][5] - big[0][5]) / dl
        kD = (big[-1][6] - big[0][6]) / dl
        print("   over B in [%d, %d]: kappa_A = %.3f, kappa_D = %.3f, ratio C = %.3f" % (big[0][0], big[-1][0], kA, kD, kA / kD))
    print("DONE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
