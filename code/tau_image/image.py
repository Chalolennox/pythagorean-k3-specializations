"""Image of the arboreal representation tau_{E,2^k} for E : y^2 = x^3 + a x^2 + b x (rational 2-torsion point T = (0,0)) and alpha = (c, c*kk), b = c kk^2 - a c - c^2,
by the method of Liang-Rouse (Section 4) / Dokchitser-Dokchitser: a subgroup H of AGL_2(Z/2^k) contains a conjugate of im tau  iff  some left-coset sum
    zeta_{gH} = sum_{h in H} Y^{g h},   Y = x(beta_2 + A) x(beta_2 + B) x(beta_2 + A + B)^2,
is an integer (the zeta are algebraic integers).  Starting from Gamma_0^o(2) and descending through maximal (= index 2) subgroups, the image is the last subgroup that passes.
Points are computed numerically (mpmath, 100 digits) by repeated halving; the basis of E[2^k] is chosen with 2^(k-1) B = T (so the image lies in Gamma_0(2)) and 2^(k-1) A = another 2-torsion point.
Elements of AGL_2(Z/2^k) are tuples (e, f, a, b, c, d): the map x -> (e,f) + x M on row vectors, M = [[a,b],[c,d]]; the Galois action is sigma(A) = aA + bB, sigma(B) = cA + dB, sigma(beta_k) = beta_k + eA + fB."""
import sys, random, time, itertools
from mpmath import mp, mpf, mpc, sqrt, polyroots, nint
mp.dps = 100
EPS = mpf(10)**(-60)
class Curve:
    def __init__(s, a, c, kk, k):
        s.a = mpf(a); s.c = c; s.kk = kk; s.b = mpf(c*kk*kk - a*c - c*c); s.k = k; s.q = 2**k
        s.build()
    # ---- elliptic curve arithmetic over C (None = point at infinity)
    def add(s, P, Q):
        if P is None: return Q
        if Q is None: return P
        x1, y1 = P; x2, y2 = Q
        if abs(x1 - x2) < EPS:
            if abs(y1 + y2) < EPS: return None
            lam = (3*x1**2 + 2*s.a*x1 + s.b)/(2*y1)
        else: lam = (y2 - y1)/(x2 - x1)
        x3 = lam**2 - s.a - x1 - x2; return (x3, lam*(x1 - x3) - y1)
    def neg(s, P): return None if P is None else (P[0], -P[1])
    def mul(s, n, P):
        R = None
        while n:
            if n & 1: R = s.add(R, P)
            P = s.add(P, P); n >>= 1
        return R
    def same(s, P, Q):
        if P is None or Q is None: return P is None and Q is None
        return abs(P[0] - Q[0]) < EPS and abs(P[1] - Q[1]) < EPS
    def halves(s, P):
        """the four points Q with 2Q = P"""
        x0, y0 = P
        if abs(y0) < EPS:                                              # 2-torsion point (r, 0): quartic is (x^2 - 2 r x + w)^2
            w = -s.b - 2*s.a*x0 - 2*x0*x0; sq = sqrt(x0*x0 - w); xs = [x0 + sq, x0 - sq]
        else:
            xs = polyroots([1, -4*x0, -2*s.b - 4*s.a*x0, -4*s.b*x0, s.b**2], maxsteps=500, extraprec=400)
        out = []
        for x in xs:
            y2 = x**3 + s.a*x**2 + s.b*x; y = sqrt(y2)
            for Q in ((x, y), (x, -y)):
                if s.same(s.add(Q, Q), P) and not any(s.same(Q, R) for R in out): out.append(Q)
        assert len(out) == 4, len(out)
        return out
    def build(s):
        k, q = s.k, s.q
        disc = sqrt(s.a*s.a - 4*s.b); r1 = (-s.a + disc)/2
        T = (mpc(0), mpc(0)); T1 = (r1, mpc(0))
        B = [None, T]; A = [None, T1]
        for j in range(1, k): B.append(s.halves(B[j])[0]); A.append(s.halves(A[j])[0])
        alpha = (mpc(s.c), mpc(s.c*s.kk)); beta = [alpha]
        for j in range(1, k + 1): beta.append(s.halves(beta[j - 1])[0])
        s.A, s.B, s.beta = A[k], B[k], beta
        assert s.same(s.mul(2**k, beta[k]), alpha) and s.same(s.mul(2**(k - 1), A[k]), T1) and s.same(s.mul(2**(k - 1), B[k]), T)
        # table X[(u, w)] = x(beta_k + u A + w B)   (the points beta_k + r1 A + r2 B have x-coordinates integral over Z[a,c,k]; built from beta_2 = 2^(k-2) beta_k the coset sums
        # acquire denominators such as 3 and are therefore not algebraic integers -- that variant is wrong)
        mA = [None]; mB = [None]
        for u in range(1, q): mA.append(s.add(mA[-1], s.A)); mB.append(s.add(mB[-1], s.B))
        s.X = {}
        for u in range(q):
            for w in range(q):
                P = s.add(s.add(beta[k], mA[u]), mB[w]); s.X[(u, w)] = P[0]
        s.shift = 1
    def Y(s, g):
        e, f, a, b, c, d = g; q = s.q; sh = s.shift
        X = s.X
        return X[((sh*e + a) % q, (sh*f + b) % q)] * X[((sh*e + c) % q, (sh*f + d) % q)]**2 * X[((sh*e + a + c) % q, (sh*f + b + d) % q)]**3
# ---- group AGL_2(Z/q)
def compose(g, h, q):
    """g o h : x -> g(h(x))"""
    eg, fg, ag, bg, cg, dg = g; eh, fh, ah, bh, ch, dh = h
    return ((eg + eh*ag + fh*cg) % q, (fg + eh*bg + fh*dg) % q,
            (ah*ag + bh*cg) % q, (ah*bg + bh*dg) % q, (ch*ag + dh*cg) % q, (ch*bg + dh*dg) % q)
IDENT = (0, 0, 1, 0, 0, 1)
def agl_elements(q):
    return [(e, f, a, b, c, d) for a in range(q) for b in range(q) for c in range(q) for d in range(q) if (a*d - b*c) % 2 == 1 for e in range(q) for f in range(q)]
def generate(gens, q):
    S = {IDENT}; frontier = [IDENT]
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = compose(x, g, q)
                if y not in S: S.add(y); new.append(y)
        frontier = new
    return S
def maximal_subgroups(H, q, rng):
    """all index-2 subgroups of the 2-group H (a set of elements).  Returns a list of sets."""
    Hl = list(H); gens = []; S = {IDENT}
    while len(S) < len(H):
        g = rng.choice(Hl)
        if g not in S: gens.append(g); S = generate(gens, q)
    s = len(gens); label = {IDENT: 0}; relations = []; frontier = [IDENT]
    while frontier:
        new = []
        for x in frontier:
            for i, g in enumerate(gens):
                y = compose(x, g, q); v = label[x] ^ (1 << i)
                if y not in label: label[y] = v; new.append(y)
                elif label[y] != v: relations.append(label[y] ^ v)
        frontier = new
    # characters chi in F_2^s orthogonal to all relation vectors
    basis = []
    for v in relations:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    chars = []
    for chi in range(1, 2**s):
        if all(bin(chi & b).count('1') % 2 == 0 for b in basis): chars.append(chi)
    out = []
    for chi in chars:
        out.append({h for h in Hl if bin(label[h] & chi).count('1') % 2 == 0})
    # distinct subgroups (different chi give different kernels once relations are factored out)
    uniq = {}
    for M in out: uniq[frozenset(M)] = M
    return list(uniq.values()), len(gens)
def passes(curve, H, AGL, Ycache):
    """does some left coset sum  sum_{h in H} Y^{g h}  come out as an integer?"""
    q = curve.q; seen = set(); best = None
    Hl = list(H)
    for g in AGL:
        if g in seen: continue
        tot = mpc(0)
        for h in Hl:
            x = compose(g, h, q); seen.add(x); tot += Ycache[x]
        if abs(tot.imag) < mpf(10)**(-40) and abs(tot.real - nint(tot.real)) < mpf(10)**(-40): return True, g, tot.real
    return False, None, None
if __name__ == '__main__':
    a, c, kk, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    t0 = time.time(); C = Curve(a, c, kk, k); q = C.q
    print("curve y^2 = x^3 + (%d) x^2 + (%d) x,  alpha = (%d, %d);  numeric setup done in %.1fs" % (a, C.b, c, c*kk, time.time() - t0), flush=True)
    AGL = agl_elements(q); Ycache = {g: C.Y(g) for g in AGL}
    H0 = {g for g in AGL if g[4] % 2 == 0}
    ok, g, val = passes(C, H0, AGL, Ycache)
    print("sanity check: the coset sums over Gamma_0^o(2) contain an integer:", ok, val, "(%.1fs)" % (time.time() - t0), flush=True)

# ---- helpers for the level-16 refinement ----------------------------------------------------------------------------------------------------------------
def inverse(g, q):
    e, f, a, b, c, d = g; det = (a*d - b*c) % q; di = pow(det, -1, q)
    Mi = ((d*di) % q, (-b*di) % q, (-c*di) % q, (a*di) % q)
    return ((-(e*Mi[0] + f*Mi[2])) % q, (-(e*Mi[1] + f*Mi[3])) % q) + Mi
def conjugate_set(S, g, q):
    gi = inverse(g, q); return {compose(compose(g, h, q), gi, q) for h in S}
def passes_reps(curve, M, reps):
    """left cosets g M for g in reps: is some coset sum an integer?  returns (True, g, value) or (False, None, None)"""
    q = curve.q; Ml = list(M)
    for g in reps:
        tot = mpc(0)
        for h in Ml: tot += curve.Y(compose(g, h, q))
        if abs(tot.imag) < mpf(10)**(-40) and abs(tot.real - nint(tot.real)) < mpf(10)**(-40): return True, g, tot.real
    return False, None, None
