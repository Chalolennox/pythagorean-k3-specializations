#!/usr/bin/env python3
"""Independent brute-force check of (m_p, d_p) from pr92_p_divisibility_scan.py for a few larger primes.
Enumerates all of J(F_p), computes the 2-power torsion by repeated doubling and 2^k J as images of doubling."""
import sys, time
def run(p):
    pts = []
    sq = bytearray(p)
    for y in range(p): sq[y * y % p] = 1
    sqrt_one = {}
    # enumerate points: for each x with f(x) a square find y
    ys = {}
    for y in range(p): ys.setdefault(y * y % p, y)
    pts = [None]
    for x in range(p):
        f = (x * x * x - 2 * x * x + 2 * x) % p
        if f == 0: pts.append((x, 0))
        elif f in ys:
            y = ys[f]; pts.append((x, y)); pts.append((x, p - y))
    def dbl(Q):
        if Q is None or Q[1] == 0: return None
        x, y = Q
        lam = (3 * x * x - 4 * x + 2) * pow(2 * y, -1, p) % p
        x3 = (lam * lam + 2 - 2 * x) % p
        return (x3, (lam * (x - x3) - y) % p)
    N = len(pts)
    # torsion level: count points killed by 2^m
    cur = pts; m = 0
    # kill counts: iterate doubling on all points; Q killed by 2^m iff doubled m times is None
    cur = list(pts); alive = N; counts = [N]
    for k in range(1, 12):
        cur = [dbl(Q) for Q in cur]
        c = sum(1 for Q in cur if Q is None)
        counts.append(c)
        if c == N: break
    # |J[2^k]| = number of Q with 2^k Q = O
    m_bf = 0
    for k in range(1, len(counts)):
        if counts[k] == 4 ** k: m_bf = k
        else: break
    # divisibility: P in 2^k J ?
    S = set(pts); d_bf = 0
    while d_bf < m_bf:
        S = {dbl(Q) for Q in S}
        if (1, 1) in S: d_bf += 1
        else: break
    return N, m_bf, d_bf

if __name__ == "__main__":
    sys.path.insert(0, __import__("os").path.dirname(__file__))
    from pr92_p_divisibility_scan import analyse
    ps = [int(a) for a in sys.argv[1:]]
    ok = True
    for p in ps:
        t = time.time()
        N, m, d = run(p)
        m2, d2 = analyse(p)
        flag = "OK" if (m, d) == (m2, d2) else "MISMATCH"
        ok &= flag == "OK"
        print("p=%d  #J=%d  brute (m,d)=(%d,%d)  x-halving scan (m,d)=(%d,%d)  %s  [%.0fs]" % (p, N, m, d, m2, d2, flag, time.time() - t))
    sys.exit(0 if ok else 1)
