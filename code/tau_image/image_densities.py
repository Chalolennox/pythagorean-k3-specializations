"""Chebotarev densities for C : y^2 = x^3 - 2x^2 + 2x, P = (1,1), read off the computed images I_8, I_16, I_32 of the Kummer representation (image_generators_-2_1_1.json).
For a prime p with Frobenius (v, M) in I_{2^k}:  #C(F_p) = det(I - M) mod 2^k,  p = det M mod 2^k,  and  P is in 2^j C(F_p)  iff  the affine map x -> v + xM has a fixed point mod 2^j.
Every statement below is an exact count in a finite group (Chebotarev), CONDITIONAL on the image having been computed correctly (numerical coset criterion; see README) and, for the odd-order
statements, on the density formula of Liang-Rouse (which also needs the image above the level used)."""
import json, os, sys, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from image import generate
from density import mu, agl_size
data = json.load(open(os.path.join(HERE, 'image_generators_-2_1_1.json')))
I = {k: generate([tuple(g) for g in data[str(k)]['generators']], 2**k) for k in (3, 4, 5)}
v2 = lambda n: 99 if n == 0 else (n & -n).bit_length() - 1
def det(g, q): return (g[2]*g[5] - g[3]*g[4]) % q
def detImM(g, q): return ((1 - g[2])*(1 - g[5]) - g[3]*g[4]) % q
def fixed_point(g, j):
    q = 2**j; e, f, a, b, c, d = (x % q for x in g)
    return any((e + x1*a + x2*c - x1) % q == 0 and (f + x1*b + x2*d - x2) % q == 0 for x1 in range(q) for x2 in range(q))
t0 = time.time()
# ---- 1. density of {p = 7 mod 8, 8 | #C(F_p)}   (level 8)
G = I[3]; q = 8
cls = [g for g in G if det(g, q) == 7]
n8 = sum(1 for g in cls if detImM(g, q) % 8 == 0)
print("1. level 8: |I_8| = %d, elements with det = 7 mod 8: %d; of these det(I-M) = 0 mod 8 for %d" % (len(G), len(cls), n8))
print("   density of {p = 7 mod 8 : 8 | #C(F_p)} = %s  (note: 1/8);  conditional on p = 7 mod 8: %s  (note: 1/2)" % (Fr(n8, len(G)), Fr(n8, len(cls))))
# ---- 2. distribution of r = v_2(#C(F_p)) given p = 7 mod 8   (level 32 resolves r <= 4)
G = I[5]; q = 32; cls = [g for g in G if det(g, q) % 8 == 7]
cnt = {}
for g in cls:
    r = min(v2(detImM(g, q)), 5); cnt[r] = cnt.get(r, 0) + 1
print("2. level 32, p = 7 mod 8: Pr(r = k | 7 mod 8) =", {("r>=5" if k == 5 else "r=%d" % k): str(Fr(c, len(cls))) for k, c in sorted(cnt.items())}, "  (note: 1/2, 1/4, 1/8, then 1/8 for r >= 5)")
# ---- 3. Pr(P in 2^j C | p = 7 mod 8):   j = 1, 2, 3 from I_8 (reduced mod 2^j), j = 4 from I_16, j = 5 from I_32
res = {}
for j, k in ((1, 3), (2, 3), (3, 3), (4, 4), (5, 5)):
    G = I[k]; q = 2**k; cls = [g for g in G if det(g, q) % 8 == 7]
    res[j] = Fr(sum(1 for g in cls if fixed_point(g, j)), len(cls))
print("3. Pr(P in 2^j C(F_p) | p = 7 mod 8):", {j: str(res[j]) for j in res}, "  (note: j = 1: 1, j = 2: 1/2 (Theorem B), j = 3: 1/4, conjecture 2^-(j-1))   [%.0fs]" % (time.time() - t0), flush=True)
# ---- 4. joint law of (odd order, r)  via the Liang-Rouse weights at level 32 (assumes the image above level 32 is the full preimage: NOT proved)
G = I[5]; q = 32; m = agl_size(5)//len(G); cls = [g for g in G if det(g, q) % 8 == 7]
tot = {}; num = {}
for g in cls:
    r = min(v2(detImM(g, q)), 5); w = mu(5, (g[0], g[1]), ((g[2], g[3]), (g[4], g[5])), m)
    tot[r] = tot.get(r, 0) + 1; num[r] = num.get(r, 0) + w
print("4. Pr(odd order | r = k, p = 7 mod 8) from the level-32 image:", {("r>=5" if k == 5 else "r=%d" % k): "%s = %.5f" % (num[k]*len(G)/tot[k], float(num[k]*len(G)/tot[k])) for k in sorted(tot)}, "  (note: 0, 1/2, 1/4, ...)")
allodd = sum(num.values())*len(G)/len(cls)
print("   Pr(odd order | p = 7 mod 8) = %s = %.6f  (note: conjectured 1/6)   [%.0fs]" % (allodd, float(allodd), time.time() - t0))

# ---- 5. Theorem B as a statement about the finite group:  for EVERY Frobenius class (v, M) in I_8 with det M = 7 mod 8:  8 | det(I-M)  <=>  the affine map has a fixed point mod 4  (P in 4C(F_p)).
#         Every element of the image is the Frobenius of infinitely many primes (Chebotarev), so this is exactly the equivalence for all unramified p = 7 mod 8, conditional on the image I_8.
G = I[3]; q = 8; cls = [g for g in G if det(g, q) == 7]
mism = sum(1 for g in cls if (detImM(g, q) % 8 == 0) != fixed_point(g, 2))
print("5. level 8, %d classes with det = 7 mod 8: Theorem B (8 | #C <=> P in 4C) fails for %d of them" % (len(cls), mism))
G = I[4]; q = 16; cls = [g for g in G if det(g, q) % 8 == 7]
mism16 = [g for g in cls if (detImM(g, q) % 16 == 0) != fixed_point(g, 3)]
print("   level 16 analogue (16 | #C <=> P in 8C): fails for %d of %d classes with det = 7 mod 8  (so the analogue is false, as in Addendum C)" % (len(mism16), len(cls)))
assert mism == 0 and len(mism16) > 0

# ---- 6. matrix part (the image of rho_{C,2^k}) versus translation part
import math
for k in (3, 4, 5):
    q = 2**k; G = I[k]; mats = {g[2:] for g in G}; ker = {g for g in G if g[2:] == (1, 0, 0, 1)}
    print("6. level 2^%d: |I| = 2^%d; image of rho: order 2^%d, index %d in GL_2(Z/2^%d); translations (M = I): 2^%d of 2^%d, index %d" %
          (k, len(G).bit_length() - 1, int(math.log2(len(mats))), 3*2**(4*k - 3)//len(mats), k, len(ker).bit_length() - 1, 2*k, 2**(2*k)//len(ker)))
print("   Rouse-Zureick-Brown: for non-CM E/Q the index of the 2-adic image divides 64 or 96 and the image is determined mod 32. C has j = 128 (not a CM j-invariant), so the index-96 image found at level 32 is the 2-adic image of C.")
# ---- 7. the sequence a_j = Pr(P in 2^j C | p = 7 mod 8): 1/4, 3/16, 11/64 = 1/6 + (1/12) 4^-(j-3)
a = {3: Fr(1, 4), 4: Fr(3, 16), 5: Fr(11, 64)}
print("7. a_j = Pr(P in 2^j C | 7 mod 8) for j = 3, 4, 5 =", {j: str(v) for j, v in a.items()}, "= 1/6 + (1/12) 4^-(j-3):", all(a[j] == Fr(1, 6) + Fr(1, 12)/4**(j - 3) for j in a), "(a pattern fitted to three points; its limit 1/6 is the odd-order density)")
