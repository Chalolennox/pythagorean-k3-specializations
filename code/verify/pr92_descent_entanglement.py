#!/usr/bin/env python3
"""2-descent entanglement and the constant C in the sieve dimension kappa = C/2 (PR #92).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Observed numerics plus one rigorous finite computation (Part 1); the rest is heuristic.  No claim about Problem H.

Background.  J: y^2 = x(x^2 - 2x + 2) has the 2-descent homomorphism delta(Q) = x(Q) mod squares (delta(T) = 2 for T = (0,0)).  Since delta(P) = 1 for P = (1,1), every multiple nP has x(nP) a
square mod p (when nonzero): P lies in a subgroup of index 2 of J(F_p) whenever delta is nontrivial on J(F_p).  This is the one entanglement between the eligible points and <P> visible at the first
descent level.  If U is uniform on J(F_p) and independent of P then E[[G:<P>] * 1_{U in <P>}] = 1 whatever the distribution of P, so the entanglement matters for the constant C only if the
ELIGIBILITY conditions (Y square, g square) are correlated with the class of x(U) mod squares.
Part 1 (PROOF GIVEN, finite computation): in L*/L*^2, L = Q[x]/(h), the classes of 2, x, 1-x, 2-x and x^2-2x+2 are independent (rank 5 over F_2 on degree-one primes).  Hence x, Y = x(x^2-2x+2)
and g(1-x) = 2(1-x)x(2-x) are independent in L*/L*^2, and by Chebotarev the triple of Legendre symbols (chi(x), chi(Y), chi(g)) at the roots of h is equidistributed on {+-1}^3: eligibility says
nothing about chi(x).
Part 2 (observed): among eligible points the fraction with x a square mod p is about 1/2; every accessible eligible point (nP in D_p^+) has x a square (consistency with delta(P) = 1).
Usage: python3 code/verify/pr92_descent_entanglement.py [B]   (default B = 300000, about 25 s)
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
B = int(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else 300000
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v
import pr92_sieve_second_moment as sm

ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok = ok and cond


def leg(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)


def rank_f2(rows):
    basis = {}
    for r in rows:
        while r:
            hb = r.bit_length() - 1
            if hb in basis:
                r ^= basis[hb]
            else:
                basis[hb] = r
                break
    return len(basis)


def main():
    # Part 1
    gens = [lambda x, p: 2, lambda x, p: x, lambda x, p: 1 - x, lambda x, p: 2 - x, lambda x, p: x * x - 2 * x + 2]
    names = ["2", "x", "1-x", "2-x", "x^2-2x+2"]
    rows = []
    for p in v.primes_upto(3000):
        if p < 5 or p == 23:
            continue
        for x in v.roots_mod_p(p):
            sy = [leg(g(x, p), p) for g in gens]
            if 0 in sy:
                continue
            rows.append(sum(1 << i for i, s in enumerate(sy) if s == -1))
    rk = rank_f2(rows)
    check("Part 1: rank of {%s} in L*/L*^2 on %d degree-one primes of L is %d (independent iff 5)" % (", ".join(names), len(rows), rk), rk == 5)
    # Part 2
    tot = sq = acc = acc_sq = 0
    joint = {}
    for p in v.primes_upto(B):
        if p < 7 or p == 23:
            continue
        allp, elig = sm.points(p)
        for x in v.roots_mod_p(p):
            Y, g = v.Yc(x) % p, v.gc((1 - x) % p) % p
            if x % p and Y and g:
                key = (leg(x, p), leg(Y, p), leg(g, p))
                joint[key] = joint.get(key, 0) + 1
        if not elig:
            continue
        xs = {e[0] for e in elig}
        for x in xs:
            tot += 1
            sq += leg(x, p) == 1
        add, neg, mul = sm.group(p)
        P = (1, 1)
        L = math.isqrt(4 * p) + 6
        cur = P
        Eset = set(elig)
        for n in range(1, L + 1):
            if cur is None:
                break
            if cur in Eset:
                acc += 1
                acc_sq += leg(cur[0], p) == 1
            cur = add(cur, P)
    print("\nPart 2 (primes 7 <= p <= %d): joint distribution of (chi(x), chi(Y), chi(g)) over roots of h:" % B)
    n = sum(joint.values())
    for k in sorted(joint):
        print("   %s: %.4f" % (k, joint[k] / n))
    check("Part 2: the 8 joint classes each have frequency within 0.02 of 1/8 (Chebotarev)", all(abs(joint.get(k, 0) / n - 0.125) < 0.02 for k in [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]))
    print("   eligible points with x a square mod p: %d of %d (%.3f)" % (sq, tot, sq / tot))
    check("Part 2: fraction of eligible x-values that are squares is within 0.03 of 1/2", abs(sq / tot - 0.5) < 0.03)
    print("   accessible eligible points seen (n up to the walk length) with x a square: %d of %d" % (acc_sq, acc))
    check("Part 2: every accessible eligible point has x a square (delta(P) = 1)", acc == acc_sq and acc > 0)
    print("DONE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
