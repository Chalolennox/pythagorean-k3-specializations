#!/usr/bin/env python3
"""Analyse pr92_kummer_lattice_scan.py output.  Fraction of K-split primes with J[2^k] rational and Q in 2^k J(F_p) equals 1/|image of the Kummer group of Q over K(J[2^k])| (Chebotarev)."""
import sys, math, itertools, collections

def load(fn):
    import gzip
    rows = []
    for line in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        if line.startswith("#"): continue
        f = line.rstrip("\n").split("\t")
        ints = lambda s: list(map(int, s.split(",")))
        rows.append(dict(p=int(f[0]), m=int(f[1]), d=ints(f[2]), ps=ints(f[3]), pd=ints(f[4]), us=ints(f[5]), ud=ints(f[6]), ch=ints(f[7])))
    return rows

def rank(vs):
    basis = []
    for v in vs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis), basis

def bits(r):  # 14-bit vector of first-level descent characters of P,U1..U6
    v = 0
    for i, c in enumerate(r["ch"]): v |= c << (2 * i)
    return v

SHIFT = 0
def frac(rows, k, pred):
    sub = [r for r in rows if r["m"] >= k + SHIFT]
    n = len(sub); c = sum(1 for r in sub if pred(r, k))
    return c, n

def fmtf(c, n):
    if n == 0: return "   -   "
    f = c / n
    se = math.sqrt(max(f * (1 - f), 1e-9) / n)
    return "%5d/%-5d %.4f+-%.4f" % (c, n, f, se)

if __name__ == "__main__":
    rows = load(sys.argv[1])
    if len(sys.argv) > 2: SHIFT = int(sys.argv[2])
    print("conditioning on m_p >= k + %d (SHIFT)" % SHIFT)
    print("K-split primes p = 1 mod 8: %d  (largest %d)" % (len(rows), rows[-1]["p"]))
    cnt = collections.Counter(min(r["m"], 8) for r in rows)
    print("torsion level m_p: " + ", ".join("m=%d: %d" % (m, cnt[m]) for m in sorted(cnt)))
    for mm in (1, 2, 3, 4):
        sub = [r for r in rows if r["m"] >= mm]
        rk, basis = rank([bits(r) for r in sub])
        print("first-level (k=1) F_2-rank of the descent-character vectors of (P, U_1..U_6) over the %d primes with m_p >= %d: %d" % (len(sub), mm, rk))
    # which coordinates
    sub1 = [r for r in rows if r["m"] >= 1]
    print("P descent characters over all primes: %s" % sorted(collections.Counter(r["ch"][0] for r in sub1).items()))
    names = ["P"] + ["U%d" % (j + 1) for j in range(6)]
    print("\nFraction of primes with J[2^k] rational in which Q is in 2^k J(F_p)  [1/fraction = size of the Kummer image of Q mod 2^k]")
    for k in (1, 2, 3, 4):
        print("\n--- k = %d ---" % k)
        c, n = frac(rows, k, lambda r, k: r["d"][0] >= k)
        print("  P            : " + fmtf(c, n))
        c = sum(sum(1 for r in rows if r["m"] >= k + SHIFT and r["d"][1 + j] >= k) for j in range(6))
        nn = 6 * frac(rows, k, lambda r, k: True)[1]
        print("  U_j (all 6 pooled): " + fmtf(c, nn))
        for j in range(6):
            c, n = frac(rows, k, lambda r, k, j=j: r["d"][1 + j] >= k)
            print("     U%d: %s" % (j + 1, fmtf(c, n)))
        pairs = list(itertools.combinations(range(6), 2))
        part = [i for i, (a, b) in enumerate(pairs) if (a, b) in ((0, 1), (2, 3), (4, 5))]
        non = [i for i in range(15) if i not in part]
        for lab, key in (("U_a+U_b", "ps"), ("U_a-U_b", "pd")):
            for grp, ids in (("partner pairs {x,2-x}", part), ("other pairs", non)):
                c = sum(sum(1 for r in rows if r["m"] >= k + SHIFT and r[key][i] >= k) for i in ids)
                n = len(ids) * frac(rows, k, lambda r, k: True)[1]
                print("  %s, %-22s: %s" % (lab, grp, fmtf(c, n)))
        for lab, key in (("P+U_j", "us"), ("P-U_j", "ud")):
            c = sum(sum(1 for r in rows if r["m"] >= k + SHIFT and r[key][j] >= k) for j in range(6))
            n = 6 * frac(rows, k, lambda r, k: True)[1]
            print("  %s (pooled)        : %s" % (lab, fmtf(c, n)))
        # joint events
        c, n = frac(rows, k, lambda r, k: all(d >= k for d in r["d"][1:]))
        print("  all of U_1..U_6 in 2^k J : " + fmtf(c, n))
        c, n = frac(rows, k, lambda r, k: all(d >= k for d in r["d"]))
        print("  all of P,U_1..U_6 in 2^k J: " + fmtf(c, n))
        for (a, b) in ((1, 2), (1, 3), (3, 5)):
            c, n = frac(rows, k, lambda r, k, a=a, b=b: r["d"][a] >= k and r["d"][b] >= k)
            fa = frac(rows, k, lambda r, k, a=a: r["d"][a] >= k); fb = frac(rows, k, lambda r, k, b=b: r["d"][b] >= k)
            exp = fa[0] / fa[1] * fb[0] / fb[1]
            print("  U%d and U%d both: %s   (product of marginals %.4f)" % (a, b, fmtf(c, n), exp))
