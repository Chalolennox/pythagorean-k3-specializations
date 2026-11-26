#!/usr/bin/env python3
"""Local factors C_l (l = 2, 3, 5, 7, 11, 13, 23) and the joint factor C_S of the sieve constant, estimated by Rao-Blackwellisation (PR #92).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  NUMERICAL EVIDENCE ONLY: no theorem, no claim about Problem H.

For a prime p, an eligible rational point Q in D_p^+ and a prime l let nu_l = v_l(#J(F_p)), P_l, Q_l the l-primary components of P = (1,1) and Q, v_l = log_l ord(P_l), and
    w_l(p, Q) = 1[Q_l in <P_l>] * l^(nu_l - v_l)          (= 1 if l does not divide #J(F_p)).
For a set S of primes, w_S = prod_{l in S} w_l.  If the l-primary components for l in S behave like independent uniform points relative to P (Kummer model), E[w_l] = 1 and E[w_S] = 1.
The local factor is C_l := lim (sum_p sum_Q w_l/N_p) / (sum_p |D_p^+|/N_p) and the joint factor C_S likewise with w_S; C = C_S * prod_{l not in S} C_l.  The joint factor tests the product structure
(cross-prime entanglement through Q(sqrt -6, sqrt 69) in Q(zeta_552)).
Usage: python3 -I code/verify/pr92_c_local_factors.py [--B 10000000] [--out FILE] [--procs 2]
Output: one TSV line per prime with non-empty D_p^+:  p N nelig  w_2 w_3 w_5 w_7 w_11 w_13 w_23 w_S   (each w = sum over the eligible Q at p)
"""
import math
import os
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
B = 10000000
OUT = None
PROCS = 2
for i, a in enumerate(sys.argv):
    if a == "--B":
        B = int(sys.argv[i + 1])
    elif a == "--out":
        OUT = sys.argv[i + 1]
    elif a == "--procs":
        PROCS = int(sys.argv[i + 1])
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v  # noqa: E402
import pr92_sieve_second_moment as sm  # noqa: E402

LS = (2, 3, 5, 7, 11, 13, 23)


def leg(a, p):
    return pow(a % p, (p - 1) // 2, p)


def point_order(p, pt, add, neg, mul):
    cur = pt
    for n in range(1, 40):
        if cur is None:
            return n
        cur = add(cur, pt)
    return sm.order_bsgs(p, pt, add, neg, mul)


def in_cyclic(l, Pl, v_, Ql, add, neg, mul):
    """is Ql in the cyclic l-group <Pl> of order l^v_ ?"""
    if v_ == 0:
        return Ql is None
    H = mul(l ** (v_ - 1), Pl)
    hs = [mul(j, H) for j in range(1, l)]
    cur = Ql
    for i in range(v_):
        T = mul(l ** (v_ - 1 - i), cur)
        if T is None:
            continue
        for j in range(1, l):
            if T == hs[j - 1]:
                cur = add(cur, neg(mul(j * l ** i, Pl)))
                break
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
    e = 1
    for pt in [P] + elig[:3]:
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
        return None
    ws = []
    prod = [1.0] * len(elig)
    for l in LS:
        nu, t = 0, N
        while t % l == 0:
            t //= l
            nu += 1
        if nu == 0:
            ws.append(float(len(elig)))
            continue
        m = N // l ** nu
        Pl = mul(m, P)
        v_ = 0
        R = Pl
        while R is not None:
            R = mul(l, R)
            v_ += 1
        tot = 0.0
        for k, Q in enumerate(elig):
            if in_cyclic(l, Pl, v_, mul(m, Q), add, neg, mul):
                w = float(l ** (nu - v_))
                tot += w
                prod[k] *= w
            else:
                prod[k] = 0.0
        ws.append(tot)
    return (p, N, len(elig)) + tuple(ws) + (sum(prod),)


def main():
    primes = [p for p in v.primes_upto(B) if p >= 7 and p != 23]
    out = open(OUT, "w") if OUT else sys.stdout
    cnt = 0
    with Pool(PROCS) as pool:
        for r in pool.imap(work, primes, chunksize=64):
            if r is None:
                continue
            cnt += 1
            out.write("%d %d %d %s\n" % (r[0], r[1], r[2], " ".join("%.1f" % x for x in r[3:])))
            out.flush()
    print("primes processed: %d (up to %d)" % (cnt, B), file=sys.stderr)


if __name__ == "__main__":
    main()
