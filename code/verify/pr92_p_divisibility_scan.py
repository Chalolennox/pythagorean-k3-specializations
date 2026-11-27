#!/usr/bin/env python3
"""A1 experiment: 2-power divisibility of P=(1,1) on J: y^2=x^3-2x^2+2x over F_p.

Pure standard library.  For primes p == 1 (mod 8) it computes
  m_p = largest m with J[2^m] contained in J(F_p)       (torsion splitting level)
  d_p = largest d <= m_p with P in 2^d J(F_p).
Method (x-coordinates only; roots e = 0, 1+i, 1-i of x^3-2x^2+2x):
  Q in 2J(F_p)  iff  x(Q)-e_j are all squares in F_p.
  The x-coordinates of the halves of Q are x(Q) + s1 s2 + s1 s3 + s2 s3, s_j^2 = x(Q)-e_j.
  If J[2^m] is rational, then for j<=m, Q in 2^j J(F_p) iff Q in 2J(F_p) and ONE (any)
  half lies in 2^(j-1) J(F_p) (the halves differ by J[2] inside 2^(j-1)J(F_p)).
  J[2^(k+1)] is rational iff J[2^k] is and the 2-torsion points T1=(0,0), T2=(1+i,0)
  lie in 2^k J(F_p).
Selftest compares against brute-force group enumeration for small p.
"""
import sys, argparse, time
from multiprocessing import Pool

def make_ctx(p):
    # i = sqrt(-1), a nonresidue z for Tonelli-Shanks
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    i = pow(z, (p - 1) // 4, p)
    assert i * i % p == p - 1
    q = p - 1; s = 0
    while q % 2 == 0:
        q //= 2; s += 1
    return (p, z, i, q, s)

def sqrt_mod(a, ctx):
    p, z, _, q, s = ctx
    a %= p
    if a == 0:
        return 0
    if s == 1 or p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    M = s; c = pow(z, q, p); t = pow(a, q, p); R = pow(a, (q + 1) // 2, p)
    while t != 1:
        t2 = t; k = 0
        while t2 != 1:
            t2 = t2 * t2 % p; k += 1
        b = pow(c, 1 << (M - k - 1), p)
        M = k; c = b * b % p; t = t * c % p; R = R * b % p
    return R

def halves(x0, ctx):
    """x-coordinates of the halves of a point with x-coordinate x0, or None if not in 2J(F_p)."""
    p, _, i, _, _ = ctx
    u = (x0 % p, (x0 - 1 - i) % p, (x0 - 1 + i) % p)
    for a in u:
        if a and pow(a, (p - 1) // 2, p) != 1:
            return None
    s1, s2, s3 = (sqrt_mod(a, ctx) for a in u)
    out = []
    for e2 in (1, -1):
        for e3 in (1, -1):
            a, b, c = s1, e2 * s2, e3 * s3
            out.append((x0 + a * b + a * c + b * c) % p)
    return out

def depth(x0, cap, ctx):
    """number of successive halvings possible, up to cap (single path; valid when J[2^cap] rational)"""
    d = 0; x = x0
    while d < cap:
        h = halves(x, ctx)
        if h is None:
            break
        x = h[0]; d += 1
    return d

def level(ctx, cap=12):
    p, _, i, _, _ = ctx
    m = 1
    while m < cap:
        if depth(0, m, ctx) >= m and depth((1 + i) % p, m, ctx) >= m:
            m += 1
        else:
            break
    return m

def analyse(p):
    ctx = make_ctx(p)
    m = level(ctx)
    return m, depth(1, m, ctx)

# ---------------- sieve of the progression 1 mod 8 ----------------
def small_primes(n):
    sv = bytearray([1]) * (n + 1); sv[0] = sv[1] = 0
    for a in range(2, int(n ** 0.5) + 1):
        if sv[a]:
            sv[a * a::a] = bytearray(len(sv[a * a::a]))
    return [a for a in range(n + 1) if sv[a]]

def segment_primes(lo_t, hi_t, sp):
    seg = bytearray([1]) * (hi_t - lo_t)
    for q in sp:
        if q == 2:
            continue
        t0 = (-pow(8, -1, q)) % q
        st = lo_t + ((t0 - lo_t) % q)
        # do not strike the prime itself
        if 1 + 8 * st == q:
            st += q
        seg[st - lo_t::q] = bytearray(len(seg[st - lo_t::q]))
    return [1 + 8 * (lo_t + k) for k in range(hi_t - lo_t) if seg[k]]

def work(args):
    lo_t, hi_t, sp, keep_min = args
    rows = []; hist = {}
    for p in segment_primes(lo_t, hi_t, sp):
        m, d = analyse(p)
        hist[(m, d)] = hist.get((m, d), 0) + 1
        if m >= keep_min:
            rows.append((p, m, d))
    return rows, hist

def selftest():
    # brute force on small primes p == 1 mod 8
    def add(P, Q, p):
        if P is None: return Q
        if Q is None: return P
        x1, y1 = P; x2, y2 = Q
        if x1 == x2 and (y1 + y2) % p == 0: return None
        if P == Q: lam = (3 * x1 * x1 - 4 * x1 + 2) * pow(2 * y1, -1, p) % p
        else: lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam + 2 - x1 - x2) % p
        return (x3, (lam * (x1 - x3) - y1) % p)
    bad = 0; tested = 0
    for p in small_primes(1500):
        if p % 8 != 1: continue
        pts = [None] + [(x, y) for x in range(p) for y in range(p) if (y * y - (x ** 3 - 2 * x * x + 2 * x)) % p == 0]
        # level
        def mul(n, Q):
            R = None
            for _ in range(n): R = add(R, Q, p)
            return R
        def dbl_set(S): return {add(Q, Q, p) for Q in S}
        m_bf = 0
        while True:
            n = 2 ** (m_bf + 1)
            cnt = sum(1 for Q in pts if _mulpow(Q, m_bf + 1, p, add) is None)
            if cnt == 4 ** (m_bf + 1): m_bf += 1
            else: break
            if m_bf >= 6: break
        S = set(pts); d_bf = 0; Pt = (1, 1)
        while d_bf < m_bf:
            S = dbl_set(S)
            if Pt in S: d_bf += 1
            else: break
        m, d = analyse(p)
        tested += 1
        if (m, d) != (m_bf, d_bf):
            bad += 1; print("MISMATCH", p, (m, d), (m_bf, d_bf))
    print("selftest: %d primes tested, %d mismatches" % (tested, bad))
    return bad

def _mulpow(Q, k, p, add):
    for _ in range(k): Q = add(Q, Q, p)
    return Q

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lo", type=int, default=1000)
    ap.add_argument("--B", type=int, default=10**7)
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--seg", type=int, default=400000)
    ap.add_argument("--keep", type=int, default=3)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.selftest:
        sys.exit(1 if selftest() else 0)
    sp = small_primes(int(a.B ** 0.5) + 2)
    t_lo = (a.lo - 1) // 8 + 1; t_hi = (a.B - 1) // 8 + 1
    jobs = [(t, min(t + a.seg, t_hi), sp, a.keep) for t in range(t_lo, t_hi, a.seg)]
    t0 = time.time(); rows = []; hist = {}
    with Pool(a.procs) as pool:
        for r, h in pool.imap_unordered(work, jobs):
            rows += r
            for k, v in h.items(): hist[k] = hist.get(k, 0) + v
    rows.sort()
    if a.out:
        with open(a.out, "w") as f:
            f.write("# p\tm_p\td_p   (primes p=1 mod 8, %d<=p<%d, m_p>=%d)\n" % (a.lo, a.B, a.keep))
            for p, m, d in rows: f.write("%d\t%d\t%d\n" % (p, m, d))
    tot = sum(hist.values())
    print("primes p=1 mod 8 in [%d,%d): %d   time %.1fs" % (a.lo, a.B, tot, time.time() - t0))
    for m in range(1, 9):
        n = sum(v for (mm, d), v in hist.items() if mm >= m)
        if n: print("  m_p >= %d : %d primes (fraction of p=1 mod 8: %.3e)" % (m, n, n / tot))
    for m in range(2, 8):
        n = sum(v for (mm, d), v in hist.items() if mm >= m)
        if n < 1: continue
        for k in range(1, m + 1):
            c = sum(v for (mm, d), v in hist.items() if mm >= m and min(d, m) >= k)
            print("  m=%d: P in 2^%d J(F_p) for %d of %d  (%.4f)" % (m, k, c, n, c / n))
