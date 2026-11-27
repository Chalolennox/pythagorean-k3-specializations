#!/usr/bin/env python3
"""Sieve / second-moment experiment around the geometric Sidon bound (PR #92).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Observed numerics only: no theorem, no claim about Problem H.

Setting.  C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), D_p^+ = {Q in C(F_p): H(1-x(Q)) = 0, g(1-x(Q)) a nonzero square mod p} (as in verify_eligible_triples.py),
d_p = ord(P mod p), A_p = {n mod d_p : nP in D_p^+}, so that p is in Q(n) iff n mod d_p is in A_p.  X_B(n) = #{p <= B : n mod d_p in A_p}.

Part 1 (Sidon, direct).  For every prime 7 <= p <= B and every nonzero translation R = a - b (a, b in D_p^+, resp. D_p) we record max |S ∩ (S+R)|, where S = D_p^+ (all
rational eligible points), D_p (all rational points of the discriminant divisor) and S_p = D_p^+ ∩ <P mod p> (the orbit-accessible part).  PR #92 claims <= 2 for S_p
and D_p^+ with the single exception p = 519521, R = T for D_p^+ (size 4), and <= 4 for D_p.
Part 2 (sieve).  For n in [1, N] compute X_B(n) and compare, at cutoffs B, the observed fraction of n with X_B(n) = 0 with the independent-model product
prod_p (1 - c_p), c_p = #{n <= N : n mod d_p in A_p}/N, and compare Var X_B / E X_B with 1 (Poisson).  The d_p are not pairwise coprime, so exact independence is not expected.
Usage: python3 code/verify/pr92_sieve_second_moment.py [--B 100000] [--N 1000000]    (defaults B = 100000, N = 1000000, about 10 s; --quick: B = 20000, N = 200000, about 1 s;
--B 2000000 reproduces notes/data/pr92_sieve_second_moment_output.txt in about 3 minutes).  Always exits 0 unless the Sidon check (part 1) fails.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import verify_eligible_triples as v

B = 100000
N = 1000000
if "--quick" in sys.argv:
    B, N = 20000, 200000
if "--B" in sys.argv:
    B = int(sys.argv[sys.argv.index("--B") + 1])
if "--N" in sys.argv:
    N = int(sys.argv[sys.argv.index("--N") + 1])


def group(p):
    def add(A, Bq):
        if A is None:
            return Bq
        if Bq is None:
            return A
        x1, y1 = A
        x2, y2 = Bq
        if x1 == x2:
            if (y1 + y2) % p == 0:
                return None
            lam = (3 * x1 * x1 - 4 * x1 + 2) * pow(2 * y1, -1, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam + 2 - x1 - x2) % p
        return (x3, (-(lam * (x3 - x1) + y1)) % p)

    def neg(A):
        return None if A is None else (A[0], (-A[1]) % p)

    def mul(k, A):
        R = None
        while k:
            if k & 1:
                R = add(R, A)
            A = add(A, A)
            k >>= 1
        return R

    return add, neg, mul


def factor(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def order_bsgs(p, P, add, neg, mul):
    """order of P assuming it exceeds 4 sqrt(p) (small orders are caught by the walk)."""
    w = math.isqrt(4 * p) + 2
    lo, hi = p + 1 - w, p + 1 + w
    s = math.isqrt(hi - lo) + 1
    base = {}
    A = None
    for j in range(s + 1):
        base.setdefault(A, []).append(j)
        A = add(A, P)
    G = mul(s, P)
    cur = mul(lo, P)
    g = 0
    for i in range(s + 1):
        nc = neg(cur)
        if nc in base:
            for j in base[nc]:
                m = lo + i * s + j
                g = math.gcd(g, m) if g else m
        cur = add(cur, G)
    n = g
    for q in factor(g):
        while n % q == 0 and mul(n // q, P) is None:
            n //= q
    return n


def dlog(P, n, X, add, neg, mul):
    s = math.isqrt(n) + 1
    baby = {}
    A = None
    for j in range(s):
        baby.setdefault(A, j)
        A = add(A, P)
    G = neg(mul(s, P))
    cur = X
    for i in range(s + 1):
        if cur in baby:
            return (i * s + baby[cur]) % n
        cur = add(cur, G)
    return None


def points(p):
    """(D_p all rational points, D_p^+ eligible rational points)."""
    allp, elig = [], []
    for x in v.roots_mod_p(p):
        y = v.sqrt_mod(v.Yc(x), p)
        if y is None or y == 0:
            continue
        pts = [(x, y), (x, (-y) % p)]
        allp += pts
        gg = v.gc((1 - x) % p) % p
        if gg and pow(gg, (p - 1) // 2, p) == 1:
            elig += pts
    return allp, elig


def max_shift(S, add, neg):
    """max over nonzero R of |S ∩ (S+R)| = max multiplicity of a difference a - b != O."""
    cnt = {}
    for a in S:
        for b in S:
            r = add(a, neg(b))
            if r is not None:
                cnt[r] = cnt.get(r, 0) + 1
    return max(cnt.values()) if cnt else 0, cnt


def main():
    sidon = {"D": (0, None), "D+": (0, None), "S": (0, None)}
    viol = []
    data = []  # (p, d_p, A_p)
    for p in v.primes_upto(B):
        if p < 7:
            continue
        allp, elig = points(p)
        if not elig and len(allp) < 2:
            continue
        add, neg, mul = group(p)
        P, T = (1, 1), (0, 0)
        # orbit data
        A = set()
        d = None
        if elig:
            L = math.isqrt(4 * p) + 6
            cur = P
            Eset = set(elig)
            hits = []
            for n in range(1, L + 1):
                if cur is None:
                    d = n
                    break
                if cur in Eset:
                    hits.append(n)
                cur = add(cur, P)
            if d is not None:
                A = {n for n in hits if n < d}
            else:
                d = order_bsgs(p, P, add, neg, mul)
                A = set()
                for e in elig:
                    k = dlog(P, d, e, add, neg, mul)
                    if k is not None:
                        A.add(k)
            if A:
                data.append((p, d, sorted(A)))
        # Sidon: all rational eligible/all points
        for name, S in (("D", allp), ("D+", elig)):
            if len(S) < 2:
                continue
            m, cnt = max_shift(S, add, neg)
            if m > sidon[name][0]:
                sidon[name] = (m, p)
            if name == "D+" and m > 2:
                viol.append((p, m, [r for r, c in cnt.items() if c == m][:2]))
        # orbit-accessible part S_p = D_p^+ ∩ <P>: points with discrete log
        if A:
            Sp = [mul(k, P) for k in A]
            if len(Sp) >= 2:
                m, _ = max_shift(Sp, add, neg)
                if m > sidon["S"][0]:
                    sidon["S"] = (m, p)
    print("Part 1 (Sidon, primes 7 <= p <= %d): max |S ∩ (S+R)| over nonzero R" % B)
    print("   D_p   (all rational points of the divisor):  max = %d (first at p = %s)" % sidon["D"])
    print("   D_p^+ (eligible rational points):             max = %d (first at p = %s);  primes with max > 2: %s" % (sidon["D+"] + (viol,)))
    print("   S_p   (eligible and in <P>):                  max = %d (first at p = %s)" % sidon["S"])
    ok = sidon["S"][0] <= 2 and all(pv == 519521 for pv, _, _ in viol)
    print(("ok   " if ok else "FAIL ") + "orbit bound <= 2 and the only eligible violation is p = 519521 (if within range)")

    # Part 2: sieve over n in [1, N]
    data.sort()
    cov = bytearray(N + 1)  # 0 = survivor so far
    cnt = [0] * (N + 1)
    checkpoints = sorted({int(10 ** (2 + 0.5 * k)) for k in range(0, 30) if 10 ** (2 + 0.5 * k) < B} | {B})
    prod = 1.0
    sum_c = 0.0
    sum_c2 = 0.0
    idx = 0
    print("\nPart 2 (sieve, n in [1, %d]): primes with nonempty A_p up to B: %d" % (N, len(data)))
    print("   B        #primes  survivors/N   product(1-c_p)  E[X]     Var/E     kappa_eff = d E[X] / d loglog B (previous row to this)")
    prev = None
    for cp in checkpoints:
        while idx < len(data) and data[idx][0] <= cp:
            p, d, A = data[idx]
            idx += 1
            hit = 0
            for a in A:
                for n in range(a, N + 1, d):
                    cnt[n] += 1
                    hit += 1
                    cov[n] = 1
            c = hit / N
            prod *= 1 - c
            sum_c += c
            sum_c2 += c * (1 - c)
        surv = (N - sum(cov[1:])) / N
        mean = sum(cnt[1:]) / N
        var = sum((x - mean) ** 2 for x in cnt[1:]) / N
        kap = (sum_c - prev[1]) / (math.log(math.log(cp)) - math.log(math.log(prev[0]))) if prev else float("nan")
        prev = (cp, sum_c)
        print("   %-8d %-8d %-13.5f %-15.5f %-8.4f %-8.4f %.3f" % (cp, idx, surv, prod, mean, var / mean if mean else float("nan"), kap))
    # shared-factor structure: how far from pairwise coprime are the periods
    ds = [d for _, d, _ in data]
    sample = ds[:400]
    nonc = sum(1 for i in range(len(sample)) for j in range(i) if math.gcd(sample[i], sample[j]) > 1)
    tot = len(sample) * (len(sample) - 1) // 2
    print("   fraction of pairs among the first 400 periods d_p with gcd > 1: %.3f" % (nonc / tot))
    print("DONE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
