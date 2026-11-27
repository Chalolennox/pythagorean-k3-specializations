#!/usr/bin/env python3
"""A2 experiment: 2-adic Kummer data of the module M = <P, U_1..U_6> over the primes p = 1 mod 8 completely split in K.

K = Q(D), D = the 12 points (x_j, +-y_j) on J: y^2 = x^3-2x^2+2x with h(x_j) = 0, h = x^6-6x^5-15x^4+100x^3-189x^2+162x-54.
p is completely split in K iff h has 6 roots mod p and all f(x_j) = x_j^3-2x_j^2+2x_j are squares (all 12 points of D rational).
For each such p (p = 1 mod 8, so p is split in L0 = K(i, sqrt 2) iff split in K) the script records
  m_p                  torsion level, J[2^m] in J(F_p);
  depths               d(Q) = max k <= min(m_p, CAP) with Q in 2^k J(F_p), for Q in
                       P, U_1..U_6, U_a + U_b, U_a - U_b (15 pairs each), P + U_j, P - U_j;
  descent characters   (chi(x), chi(x-1-i)) of P, U_1..U_6 (first-level Kummer classes).
The roots x_1..x_6 are ordered so that (x_1,x_2), (x_3,x_4), (x_5,x_6) are the pairs {x, 2-x}.
Chebotarev: for a combination point R = sum c_i Q_i and k <= m, the fraction of such primes with R in 2^k J(F_p) is 1/|image of the Kummer
group of M over L(J[2^k]) under h -> sum c_i h_i|, which is how the sizes of the images are estimated in pr92_kummer_lattice_analysis.py.
Usage: python3 -I pr92_kummer_lattice_scan.py --B 500000000 [--lo 1000] --out FILE [--procs 2] [--check]
"""
import sys, os, time, argparse
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pr92_p_divisibility_scan import make_ctx, sqrt_mod, halves, depth, level, small_primes

CAP = 6
Hc = [-54, 162, -189, 100, -15, -6, 1]   # h, low -> high

def sqr_mod_h(a, p):
    pr = [0] * 11
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(a):
                pr[i + j] += ai * bj
    for k in range(10, 5, -1):
        c = pr[k] % p
        if c:
            for j in range(6):
                pr[k - 6 + j] -= c * Hc[j]
    return [x % p for x in pr[:6]]

def mulx_mod_h(a, p):
    # a * X mod h
    top = a[5]
    r = [0] + a[:5]
    if top:
        r = [(r[j] - top * Hc[j]) % p for j in range(6)]
    return r

def h_splits(p):
    """True iff X^p = X mod h, i.e. h splits into distinct linear factors mod p (p not dividing disc h)"""
    r = [0, 1, 0, 0, 0, 0]
    for b in bin(p)[3:]:
        r = sqr_mod_h(r, p)
        if b == "1":
            r = mulx_mod_h(r, p)
    return r == [0, 1, 0, 0, 0, 0]

# ---- generic polynomial arithmetic mod p (for root finding) ----
def ptrim(a):
    while a and a[-1] == 0: a.pop()
    return a
def pmod(a, b, p):
    a = a[:]; ib = pow(b[-1], -1, p)
    while len(a) >= len(b):
        c = a[-1] * ib % p
        if c:
            for j in range(len(b)):
                a[len(a) - len(b) + j] = (a[len(a) - len(b) + j] - c * b[j]) % p
        a.pop()
        ptrim(a)
    return a
def pmul(a, b, p):
    if not a or not b: return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] = (r[i + j] + x * y) % p
    return ptrim(r)
def pgcd(a, b, p):
    a, b = ptrim(a[:]), ptrim(b[:])
    while b: a, b = b, pmod(a, b, p)
    if a:
        ia = pow(a[-1], -1, p); a = [x * ia % p for x in a]
    return a
def ppowmod(base, e, mod, p):
    r = [1]
    while e:
        if e & 1: r = pmod(pmul(r, base, p), mod, p)
        base = pmod(pmul(base, base, p), mod, p); e >>= 1
    return r
def roots_of(poly, p, rng):
    poly = ptrim(poly[:])
    if len(poly) == 1: return []
    if len(poly) == 2: return [(-poly[0]) * pow(poly[1], -1, p) % p]
    while True:
        a = rng.randrange(p)
        g = ppowmod([a, 1], (p - 1) // 2, poly, p)
        g = g + [0] * (1 - len(g)) if g else [0]
        g[0] = (g[0] - 1) % p
        d = pgcd(poly, ptrim(g), p)
        if 1 < len(d) < len(poly):
            q = pdiv(poly, d, p)
            return roots_of(d, p, rng) + roots_of(q, p, rng)
def pdiv(a, b, p):
    a = a[:]; ib = pow(b[-1], -1, p); q = [0] * (len(a) - len(b) + 1)
    while len(a) >= len(b):
        c = a[-1] * ib % p; q[len(a) - len(b)] = c
        for j in range(len(b)): a[len(a) - len(b) + j] = (a[len(a) - len(b) + j] - c * b[j]) % p
        a.pop()
    return q

def K_split_data(p, ctx):
    import random
    rng = random.Random(p)
    xs = sorted(roots_of(Hc[:], p, rng))
    if len(xs) != 6: return None
    pts = []
    for x in xs:
        fx = (x * x * x - 2 * x * x + 2 * x) % p
        if fx == 0 or pow(fx, (p - 1) // 2, p) != 1: return None
        y = sqrt_mod(fx, ctx)
        pts.append((x, min(y, p - y)))
    # order into partner pairs {x, 2-x}
    idx = {x: j for j, x in enumerate(xs)}
    order = []; used = set()
    for j, x in enumerate(xs):
        if j in used: continue
        pj = idx.get((2 - x) % p)
        assert pj is not None and pj != j, "partner pair missing"
        used |= {j, pj}; order += [j, pj]
    return [pts[j] for j in order]

def add(P, Q, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0: return None
    if P == Q: lam = (3 * x1 * x1 - 4 * x1 + 2) * pow(2 * y1, -1, p) % p
    else: lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam + 2 - x1 - x2) % p
    return (x3, (lam * (x1 - x3) - y1) % p)
def neg(P, p): return None if P is None else (P[0], (-P[1]) % p)

def chars(P, ctx):
    p, i = ctx[0], ctx[2]
    def ch(a):
        a %= p
        if a == 0: return 0
        return 0 if pow(a, (p - 1) // 2, p) == 1 else 1
    return ch(P[0]) | (ch(P[0] - 1 - i) << 1)

def dep(R, cap, ctx):
    if R is None: return cap
    return depth(R[0], cap, ctx)

def record(p):
    ctx = make_ctx(p)
    pts = K_split_data(p, ctx)
    if pts is None: return None
    m = level(ctx)
    cap = min(m, CAP)
    P = (1, 1); U = pts
    singles = [P] + U
    d_single = [dep(Q, cap, ctx) for Q in singles]
    pair_s = []; pair_d = []
    for a in range(6):
        for b in range(a + 1, 6):
            pair_s.append(dep(add(U[a], U[b], p), cap, ctx))
            pair_d.append(dep(add(U[a], neg(U[b], p), p), cap, ctx))
    pu_s = [dep(add(P, u, p), cap, ctx) for u in U]
    pu_d = [dep(add(P, neg(u, p), p), cap, ctx) for u in U]
    ch = [chars(Q, ctx) for Q in singles]
    return (p, m, d_single, pair_s, pair_d, pu_s, pu_d, ch)

def job(args):
    lo_t, hi_t, sp, M = args
    from pr92_p_divisibility_scan import segment_primes
    out = []; tested = 0
    for p in segment_primes(lo_t, hi_t, sp, M):
        if pow(3, (p - 1) // 2, p) != 1 or pow(23, (p - 1) // 2, p) != 1:   # (3/p) = (23/p) = 1, necessary for K-split with p = 1 mod 8
            continue
        tested += 1
        if not h_splits(p): continue
        r = record(p)
        if r: out.append(r)
    return out, tested

def fmt(r):
    p, m, ds, ps, pd, us, ud, ch = r
    return "\t".join(map(str, [p, m] + [",".join(map(str, v)) for v in (ds, ps, pd, us, ud, ch)]))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lo", type=int, default=1000); ap.add_argument("--B", type=int, default=10**7)
    ap.add_argument("--procs", type=int, default=2); ap.add_argument("--seg", type=int, default=500000)
    ap.add_argument("--out", default=None)
    ap.add_argument("--mod", type=int, default=8, help="scan only p = 1 mod MOD (MOD = 32 loses nothing for primes with J[16] rational: m_p >= 4 forces p = 1 mod 32)")
    a = ap.parse_args()
    M = a.mod
    sp = small_primes(int(a.B ** 0.5) + 2)
    t_lo = (a.lo - 1) // M + 1; t_hi = (a.B - 1) // M + 1
    jobs = [(t, min(t + a.seg, t_hi), sp, M) for t in range(t_lo, t_hi, a.seg)]
    t0 = time.time(); res = []; tested = 0
    with Pool(a.procs) as pool:
        for out, nt in pool.imap_unordered(job, jobs):
            res += out; tested += nt
    res.sort()
    if a.out:
        with open(a.out, "w") as f:
            f.write("# p\tm_p\tdepth[P,U1..U6]\tdepth[U_a+U_b, 15 pairs]\tdepth[U_a-U_b]\tdepth[P+U_j]\tdepth[P-U_j]\tchars[P,U1..U6] (bit0: x nonsquare, bit1: x-1-i nonsquare)   (p=1 mod %d, K-split, %d<=p<%d)\n" % (M, a.lo, a.B))
            for r in res: f.write(fmt(r) + "\n")
    print("range [%d,%d): %d primes (p = 1 mod %d) passed the quadratic filter, %d completely K-split; %.0fs" % (a.lo, a.B, tested, M, len(res), time.time() - t0))
