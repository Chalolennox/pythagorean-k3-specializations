"""Find im tau_{E,2^k} up to conjugacy by descent from Gamma_0^o(2), then its density of odd-order reductions.
Usage: python3 descend.py a c kk k        (curve y^2 = x^3 + a x^2 + b x, alpha = (c, c*kk), b = c kk^2 - a c - c^2; Liang-Rouse parametrisation)"""
import sys, time, random
from fractions import Fraction
from mpmath import mpf
from image import Curve, agl_elements, maximal_subgroups, passes
from density import density, mu, agl_size
import json
def run(a, c, kk, k, seed=1, verbose=True):
    rng = random.Random(seed); t0 = time.time()
    C = Curve(a, c, kk, k); q = C.q; AGL = agl_elements(q); Ycache = {g: C.Y(g) for g in AGL}
    H = {g for g in AGL if g[4] % 2 == 0}
    ok, _, _ = passes(C, H, AGL, Ycache); assert ok, "sanity check failed: Gamma_0^o(2) must contain a conjugate of the image"
    chain = [len(H)]
    while True:
        maxes, ngen = maximal_subgroups(H, q, rng); found = None
        for M in maxes:
            ok, g, val = passes(C, M, AGL, Ycache)
            if ok: found = M; break
        if verbose: print("   |H| = 2^%d, %d maximal subgroups tested%s  (%.0fs)" % (len(H).bit_length() - 1, len(maxes), " -> one passes" if found else " -> none passes: image found", time.time() - t0), flush=True)
        if not found: break
        H = found; chain.append(len(H))
    dens = density(H, k)
    return H, chain, dens
def class_densities(H, r):
    """odd-order density within each class of primes p mod 2^r (det M = p mod 2^r): a_j = sum_{g in H, det g = j} mu(g) / P(class j),  P(class j) = #{g in H: det = j}/|H|"""
    from collections import defaultdict
    m = agl_size(r)//len(H); tot = defaultdict(Fraction); cnt = defaultdict(int); q = 2**r
    for g in H:
        j = (g[2]*g[5] - g[3]*g[4]) % q
        tot[j] += mu(r, (g[0], g[1]), ((g[2], g[3]), (g[4], g[5])), m); cnt[j] += 1
    return {j: (tot[j]*len(H)/cnt[j], Fraction(cnt[j], len(H))) for j in sorted(tot)}
if __name__ == '__main__':
    a, c, kk, k = map(int, sys.argv[1:5])
    H, chain, dens = run(a, c, kk, k)
    print("curve [a,c,k] = [%d,%d,%d], level 2^%d:  |im tau mod 2^%d| = 2^%d  (index %d in Gamma_0^o(2)); density of odd-order reductions = %s = %.6f" %
          (a, c, kk, k, k, len(H).bit_length() - 1, 2**(6*k - 3)//len(H), dens, float(dens)))
    for j, (aj, pj) in class_densities(H, k).items(): print("   primes p = %d mod %d (probability %s): predicted odd-order fraction %s = %.5f" % (j, 2**k, pj, aj, float(aj)))
    json.dump(sorted(H), open('image_%d_%d_%d_k%d.json' % (a, c, kk, k), 'w'))
