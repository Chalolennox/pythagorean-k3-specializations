#!/usr/bin/env python3
"""Rao-Blackwellised numerical estimator of the 2-local factor C_2 of the sieve constant C (PR #92).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  NUMERICAL EVIDENCE ONLY: no theorem, no claim about Problem H.

Definition.  For a prime p let J(F_p)[2^inf] = G_2 (order 2^nu), N = #J(F_p) = 2^nu * m, P_2 = mP, Q_2 = mQ (the 2-primary components), and for an eligible rational point Q in D_p^+ put
    w(p, Q) = 1[Q_2 in <P_2>] * 2^nu / |<P_2>|.
If the odd-primary components of Q behave like uniform points independent of P (true in the Kummer model for the odd primes l with M l-saturated; shown for l = 3, 23 under the attested group),
then E[1[Q in <P>] / d_p] = w(p, Q) / N, so
    C_2 := lim  sum_{p <= B} sum_{Q in D_p^+} w(p,Q)/N_p  /  sum_{p <= B} |D_p^+|/N_p      (slope ratio; the loglog B normalisation cancels)
and the sieve constant is C = C_2 * prod_{l odd} C_l with C_l = 1 under the hypotheses above.  Replacing the odd part of the indicator by its conditional expectation removes the heavy-tailed
fluctuation caused by small odd orders d_p.  For p <= --fullB the script also computes the full indicator a_p / d_p (a_p = #(D_p^+ ∩ <P>), d_p = ord P) to test the uniform-odd-part hypothesis:
the paired differences a_p/d_p - sum_Q w/N_p must average to 0 within their standard error.
Usage: python3 -I code/verify/pr92_c2_estimator.py [--B 5000000] [--fullB 400000] [--out FILE] [--procs 2]
Output: one TSV line per prime with a non-empty D_p^+: p N nu alpha beta vP nelig n_in2 sumw d hits   (d, hits = 0, -1 above fullB); alpha, beta from 8 random points (alpha = nu - beta).
"""
import math
import os
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
B = 5000000
FULLB = 400000
OUT = None
PROCS = 2
for i, a in enumerate(sys.argv):
    if a == "--B":
        B = int(sys.argv[i + 1])
    elif a == "--fullB":
        FULLB = int(sys.argv[i + 1])
    elif a == "--out":
        OUT = sys.argv[i + 1]
    elif a == "--procs":
        PROCS = int(sys.argv[i + 1])
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v  # noqa: E402
import pr92_sieve_second_moment as sm  # noqa: E402


def leg(a, p):
    return pow(a % p, (p - 1) // 2, p)


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def point_order(p, pt, add, neg, mul):
    cur = pt
    for n in range(1, 40):
        if cur is None:
            return n
        cur = add(cur, pt)
    return sm.order_bsgs(p, pt, add, neg, mul)


def in_cyclic2(P2, vP, Q2, add, neg, mul):
    """is Q2 in the cyclic 2-group <P2> of order 2^vP ?"""
    if vP == 0:
        return Q2 is None
    half = mul(1 << (vP - 1), P2)
    cur = Q2
    for i in range(vP):
        T = mul(1 << (vP - 1 - i), cur)
        if T is None:
            continue
        if T == half:
            cur = add(cur, neg(mul(1 << i, P2)))
        else:
            return False
    return cur is None


def work(p):
    allp, elig = sm.points(p)
    if not elig:
        return None
    rng = random.Random(p * 7919 + 13)
    add, neg, mul = sm.group(p)
    P = (1, 1)
    pts = [P] + elig[:3]
    e = 1
    for pt in pts:
        o = point_order(p, pt, add, neg, mul)
        e = e * o // math.gcd(e, o)
    lo, hi = p + 1 - math.isqrt(4 * p) - 2, p + 1 + math.isqrt(4 * p) + 2
    N = None
    for _ in range(14):
        cands = list(range((lo + e - 1) // e * e, hi + 1, e))
        if len(cands) == 1:
            N = cands[0]
            break
        while True:
            x = rng.randrange(p)
            Y = v.Yc(x) % p
            if Y and leg(Y, p) == 1:
                break
        o = point_order(p, (x, v.sqrt_mod(Y, p)), add, neg, mul)
        e = e * o // math.gcd(e, o)
    if N is None and p < 30000:
        N = 1
        for x in range(p):
            Y = (x * (x * x - 2 * x + 2)) % p
            N += 1 if Y == 0 else (2 if pow(Y, (p - 1) // 2, p) == 1 else 0)
    if N is None:
        return (p, -1, 0, 0, 0, 0, len(elig), 0, 0.0, 0, -1)
    nu = v2(N)
    m = N >> nu
    # beta from random points (alpha = nu - beta)
    be = 0
    for _ in range(8):
        while True:
            x = rng.randrange(p)
            Y = v.Yc(x) % p
            if Y and leg(Y, p) == 1:
                break
        R = mul(m, (x, v.sqrt_mod(Y, p)))
        k = 0
        while R is not None:
            R = add(R, R)
            k += 1
        be = max(be, k)
    P2 = mul(m, P)
    vP = 0
    R = P2
    while R is not None:
        R = add(R, R)
        vP += 1
    n_in2 = 0
    for Q in elig:
        if in_cyclic2(P2, vP, mul(m, Q), add, neg, mul):
            n_in2 += 1
    sumw = n_in2 * 2.0 ** (nu - vP)
    d, hits = 0, -1
    if p <= FULLB:
        n = N
        f, t = {}, N
        q = 2
        while q * q <= t:
            while t % q == 0:
                f[q] = 1
                t //= q
            q += 1 if q == 2 else 2
        if t > 1:
            f[t] = 1
        for q in f:
            while n % q == 0 and mul(n // q, P) is None:
                n //= q
        d = n
        hits = sum(1 for Q in elig if sm.dlog(P, d, Q, add, neg, mul) is not None)
    return (p, N, nu, nu - be, be, vP, len(elig), n_in2, sumw, d, hits)


def main():
    primes = [p for p in v.primes_upto(B) if p >= 7 and p != 23]
    out = open(OUT, "w") if OUT else None
    cnt = 0
    with Pool(PROCS) as pool:
        for r in pool.imap(work, primes, chunksize=64):
            if r is None:
                continue
            cnt += 1
            line = "%d %d %d %d %d %d %d %d %.1f %d %d" % r
            if out:
                out.write(line + "\n")
                out.flush()
            else:
                print(line)
    print("primes with non-empty D_p^+ processed: %d (up to %d)" % (cnt, B), file=sys.stderr)


if __name__ == "__main__":
    main()
