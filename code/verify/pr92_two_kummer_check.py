#!/usr/bin/env python3
"""Independent finite-field check of notes/KUMMER_TWO_ADIC_FIRST_LEVEL.md (first-level 2-Kummer rank over L0 = K(i, sqrt 2)).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  No claim about Problem H.  The owner's Magma square-class test at degree 96 is NOT re-run here.

What is checked.
 (1) The witness p = 125329 of the note: p = 1 mod 8, h has the six stated roots, all Y_j and all x_j are squares, the character bits of B_j = x_j - 1 - i are (1,0,0,0,0,1) for either square root of -1,
     the roots pair up under x -> 2 - x, and the bits are constant on the pairs (so the evaluation on the three pair classes is a unit vector).
 (2) The algebraic identities behind the pairing: h(2-x) = h(x); B(2-x) = -(x-1+i); and, at every totally split prime found, B(x_j) and B(2-x_j) have the same quadratic character (as the identity predicts when x_j is a square).
 (3) A necessary condition for the owner certificate: at every prime p = 1 mod 8 completely split in K (all 12 points rational) up to the bound, all six x_j are squares mod p (probability 2^-6 per prime if x were
     a non-square class); and the same test at primes completely split in K but p != 1 mod 8, where non-squares should occur (so that L0 is really needed).
 (4) Statistics of the pair-evaluation vectors at those primes (weights 0..3); the rank-3 argument needs only one weight-1 vector plus transitivity of Galois on the three pairs (h irreducible).
Usage: python3 -I code/verify/pr92_two_kummer_check.py [--B 3000000]   (default 3000000, about 1-2 minutes).  Exit 0 iff all checks pass.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
B = 3000000
if "--B" in sys.argv:
    B = int(sys.argv[sys.argv.index("--B") + 1])
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v  # noqa: E402

ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok = ok and cond


def leg(a, p):
    return pow(a % p, (p - 1) // 2, p)  # 1 square, p-1 nonsquare, 0 zero


def main():
    # (2) symbolic identity h(2-x) = h(x)
    def hval(x, p):
        t = (1 - x) % p
        return (t ** 6 - 30 * t ** 4 - 24 * t ** 2 - 1) % p
    check("h(2-x) = h(x): H is even, so h(2-x) = H(x-1) = H(1-x) (spot-checked at 1000 integers)", all(hval(2 - x, 10 ** 9 + 7) == hval(x, 10 ** 9 + 7) for x in range(1000)))

    # (1) witness prime
    p = 125329
    check("(1) p = 125329 is prime and p = 1 mod 8", v.primes_upto(p)[-1] == p and p % 8 == 1)
    xs = sorted(v.roots_mod_p(p))
    check("(1) roots of h mod p are 10263,37280,45627,79704,88051,115068: %s" % xs, xs == [10263, 37280, 45627, 79704, 88051, 115068])
    check("(1) all Y_j = x(x^2-2x+2) and all x_j are nonzero squares mod p (K completely split, and x_j square)", all(leg(v.Yc(x), p) == 1 and leg(x, p) == 1 for x in xs))
    i1 = v.sqrt_mod(p - 1, p)
    for ii in (i1, p - i1):
        bits = [0 if leg(x - 1 - ii, p) == 1 else 1 for x in xs]
        check("(1) with i = %d the bits of B_j = x_j-1-i are %s" % (ii, bits), bits == [1, 0, 0, 0, 0, 1])
    pairs_ok = all((xs[j] + xs[5 - j]) % p == 2 for j in range(6))
    check("(1) roots pair as x + x' = 2: (10263,115068), (37280,88051), (45627,79704)", pairs_ok)
    pv = [[1 if leg(xs[j] - 1 - i1, p) != 1 else 0 for j in (0, 1, 2)]]
    check("(1) pair vector (bits on the three pairs) = %s, a unit vector" % pv[0], pv[0] == [1, 0, 0])

    # (3), (4) scan
    n8 = bad8 = 0
    nother = nonsq_other = 0
    weights = {0: 0, 1: 0, 2: 0, 3: 0}
    sym_fail = 0
    for p in v.primes_upto(B):
        if p < 11 or p in (23,):
            continue
        rts = v.roots_mod_p(p)
        if len(rts) != 6:
            continue
        if any(leg(v.Yc(x), p) != 1 for x in rts):
            continue  # not completely split in K
        sq = [leg(x, p) == 1 for x in rts]
        if p % 8 == 1:
            n8 += 1
            if not all(sq):
                bad8 += 1
            ii = v.sqrt_mod(p - 1, p)
            bit = {x: (0 if leg(x - 1 - ii, p) == 1 else 1) for x in rts}
            # pairs
            rs = set(rts)
            seen, vec = set(), []
            for x in rts:
                if x in seen:
                    continue
                x2 = (2 - x) % p
                seen |= {x, x2}
                if x2 not in rs or bit[x] != bit[x2]:
                    sym_fail += 1
                vec.append(bit[x])
            weights[sum(vec)] += 1
        else:
            nother += 1
            if not all(sq):
                nonsq_other += 1
    print("   primes p = 1 mod 8 completely split in K, p <= %d: %d; with some x_j a nonsquare: %d" % (B, n8, bad8))
    check("(3) every such prime has all six x_j squares (owner certificate necessary condition; chance of this by accident about 64^-%d)" % n8, n8 >= 10 and bad8 == 0)
    print("   primes completely split in K with p != 1 mod 8: %d; with some x_j a nonsquare: %d" % (nother, nonsq_other))
    check("(3) at p != 1 mod 8 non-squares do occur, so adjoining i and sqrt 2 is needed", nonsq_other > 0)
    check("(2) at all those primes the roots pair under x -> 2-x and the B-bits agree on each pair (failures: %d)" % sym_fail, sym_fail == 0)
    print("   (4) weight distribution of the pair vectors over the three pairs: %s" % weights)
    check("(4) a weight-1 vector occurs (so the rank-3 argument is not an accident of one prime)", weights[1] > 0)
    print("DONE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
