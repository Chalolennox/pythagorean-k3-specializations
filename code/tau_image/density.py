"""Density of primes at which alpha has ODD order, from a subgroup G of AGL_2(Z/2^r)   (Liang-Rouse, arXiv 1810.10583, Sections 2 and 5).
An element is a tuple (e, f, a, b, c, d) = the affine map x -> (e,f) + x M on row vectors x of (Z/2^r)^2, M = [[a,b],[c,d]].
F(G) = sum over g in G of mu_r(g),  with mu_r given by Lemmas 6-10 of the paper (ell = 2) and m = [AGL_2(Z/2^r) : G]."""
from fractions import Fraction as Fr
import itertools, functools
def agl_size(r): return 3 * 2**(6*r - 3)
def _val(x, q):
    """2-adic valuation of x mod q (q for x = 0)"""
    x %= q
    return q.bit_length() - 1 if x == 0 else (x & -x).bit_length() - 1
def in_rowspace(na, nb, nc, nd, e, f, q):
    """is (e, f) = x * [[na, nb], [nc, nd]] solvable over Z/q (q a power of 2)?  Elimination with a pivot of minimal 2-adic valuation."""
    rows = [[na % q, nb % q], [nc % q, nd % q]]; v = [e % q, f % q]; k2 = q.bit_length() - 1
    best = None
    for i in (0, 1):
        for j in (0, 1):
            if rows[i][j] % q and (best is None or _val(rows[i][j], q) < _val(rows[best[0]][best[1]], q)): best = (i, j)
    if best is None: return v[0] == 0 and v[1] == 0
    i, j = best; piv = rows[i][j]; kv = _val(piv, q); u = piv >> kv; ui = pow(u, -1, q)
    if _val(v[j], q) < kv: return False
    t = ((v[j] >> kv) * ui) % q                                   # v - t*row_i has column j equal to 0
    v = [(v[0] - t*rows[i][0]) % q, (v[1] - t*rows[i][1]) % q]
    o = rows[1 - i]
    if _val(o[j], q) < kv: raise AssertionError("pivot not minimal")
    t2 = ((o[j] >> kv) * ui) % q if o[j] % q else 0
    o = [(o[0] - t2*rows[i][0]) % q, (o[1] - t2*rows[i][1]) % q]  # other row with column j cleared
    jj = 1 - j
    if o[jj] % q == 0: return v[jj] % q == 0
    return _val(v[jj], q) >= _val(o[jj], q)
def mu(r, v, M, m):
    q = 2**r; (a, b), (c, d) = M; e, f = v
    na, nb, nc, nd = (a - 1) % q, b % q, c % q, (d - 1) % q          # N = M - I
    # Lemma 6: v must lie in the row space of N
    inrow = in_rowspace(na, nb, nc, nd, e % q, f % q, q)
    if not inrow: return Fr(0)
    if na % 2 == 0 and nb % 2 == 0 and nc % 2 == 0 and nd % 2 == 0:                        # M = I mod 2  (then v = 0 mod 2, since v is in the row space)
        if (e % q, f % q, na, nb, nc, nd) == (0, 0, 0, 0, 0, 0):                        # Lemma 10: (v, M) = (0, I) mod 2^r
            return Fr((1*2 + 1) * m, 1 * 2**(6*r - 5) * (2**6 - 1))
        h = q // 2                                                                          # Lemma 7: reduce the level by one
        return mu(r - 1, ((e//2) % h, (f//2) % h), (((na//2 + 1) % h, (nb//2) % h), ((nc//2) % h, (nd//2 + 1) % h)), m) / Fr(2**6)
    det = (na*nd - nb*nc) % q
    if det != 0: return Fr(m, agl_size(r))                                                  # Lemma 8
    return Fr(m, 2**(6*r - 4) * 1 * 9)                                                      # Lemma 9
def density(G, r):
    """G: iterable of elements (e,f,a,b,c,d) mod 2^r (a subgroup of AGL_2(Z/2^r))."""
    G = list(G); m = Fr(agl_size(r), len(G)); assert m.denominator == 1; m = int(m)
    return sum((mu(r, (g[0], g[1]), ((g[2], g[3]), (g[4], g[5])), m) for g in G), Fr(0))
def gl2_elements(q):
    return [(a, b, c, d) for a in range(q) for b in range(q) for c in range(q) for d in range(q) if (a*d - b*c) % 2 == 1]
