"""Image of tau_{E,2^k} for k = 3, 4, 5, ... by successive refinement, in ONE fixed frame (beta_k, A_k, B_k).   Usage: python3 levels.py a c kk [kmax]
E : y^2 = x^3 + a x^2 + b x, alpha = (c, c kk), b = c kk^2 - a c - c^2   (Liang-Rouse parametrisation).

Level 3: descent from Gamma_0^o(2) through maximal subgroups with the coset criterion of image.py; when a coset g M passes, the image lies in g M g^-1 and we continue with that subgroup.
Level k -> k+1: P = full preimage of the level-k image I in AGL_2(Z/2^(k+1)), K = ker(P -> I).  The image I' of level k+1 maps onto I, so if I' != P it lies in a maximal subgroup M of P with M not containing K.
   Such M are tested with the coset criterion for the left cosets gM, g in n * P/M with n over lifts of N(I)/I (N(I) = normaliser of I; only g with g mod 2^k in N(I) can occur, because M mod 2^k = I).
   On a pass, I' lies in g M g^-1, and the descent continues inside it.  If I' = P (no descent) the image is the full preimage of I, which by the Frattini argument of Liang-Rouse (Theorem 4) persists at all higher levels: STABLE.
Finally the density of odd-order reductions is computed from the stable level (Liang-Rouse, Section 5) with class densities by p mod 2^r."""
import sys, time, random, json
from fractions import Fraction
from mpmath import mp, mpf
from image import *
from density import density, mu, agl_size
from descend import class_densities
a, c, kk = map(int, sys.argv[1:4]); kmax = int(sys.argv[4]) if len(sys.argv) > 4 else 5
rng = random.Random(1); t0 = time.time()
def log(*x): print("[%5.0fs]" % (time.time() - t0), *x, flush=True)
def coset_reps(G, S, q):
    """representatives of the left cosets  g G  inside the set S (S a union of left cosets of G)"""
    seen = set(); reps = []; Gl = list(G)
    for s in S:
        if s in seen: continue
        reps.append(s)
        for h in Gl: seen.add(compose(s, h, q))
    return reps
# ------------------------------------------------------------------ level 3
C = Curve(a, c, kk, 3); q = 8; AGL = agl_elements(q); Y3 = {g: C.Y(g) for g in AGL}
I = {g for g in AGL if g[4] % 2 == 0}
while True:
    maxes, ngen = maximal_subgroups(I, q, rng); found = None
    for M in maxes:
        ok, g, val = passes(C, M, AGL, Y3)
        if ok: found = (M, g); break
    if not found: break
    M, g = found; I = conjugate_set(M, g, q)
log("level 3 (mod 8): |I| = 2^%d" % (len(I).bit_length() - 1))
k = 3; history = {3: I}
while k < kmax:
    qp = 2**k; q = 2*qp; Ck = Curve(a, c, kk, k + 1)
    # normaliser of I in AGL_2(Z/qp): at k = 3 brute force; later only lifts of the previous normaliser need to be tried
    gens = []; S = {IDENT}
    while len(S) < len(I):
        g = rng.choice(list(I))
        if g not in S: gens.append(g); S = generate(gens, qp)
    if k == 3: cand = agl_elements(qp)
    else: cand = [tuple((x + qprev_*bits) % qp for x, bits in zip(n, lb)) for n in Nprev for lb in LB]
    N = [g for g in cand if all(compose(compose(g, h, qp), inverse(g, qp), qp) in I for h in gens)]
    Nreps = coset_reps(I, N, qp)
    log("level %d -> %d: |I| = 2^%d, |N(I)| = 2^%d, %d cosets of I in N(I)" % (k, k + 1, len(I).bit_length() - 1, len(N).bit_length() - 1, len(Nreps)))
    LB = [(b0, b1, b2, b3, b4, b5) for b0 in (0, 1) for b1 in (0, 1) for b2 in (0, 1) for b3 in (0, 1) for b4 in (0, 1) for b5 in (0, 1)]
    P = {tuple((x + qp*bits) % q for x, bits in zip(g, lb)) for g in I for lb in LB}
    Kern = {g for g in P if all((x - y) % qp == 0 for x, y in zip(g, IDENT))}
    # lifts of the level-k normaliser (as tuples mod q) for the next round are the same tuples read mod q
    ok, g0, v0 = passes_reps(Ck, P, [tuple(n) for n in Nreps]); assert ok, "sanity check failed: P must contain a conjugate of the image"
    cur = P
    while True:
        maxes, ngen = maximal_subgroups(cur, q, rng)
        Kc = {g for g in Kern if g in cur}
        cands = [M for M in maxes if not Kc <= M]
        log("   |H| = 2^%d: %d maximal subgroups, %d not containing the kernel part" % (len(cur).bit_length() - 1, len(maxes), len(cands)))
        found = None
        for M in cands:
            Pcos = coset_reps(M, P, q)                                   # cosets of M in the full preimage P
            reps = [compose(n, r, q) for n in Nreps for r in Pcos]
            ok, g, val = passes_reps(Ck, M, reps)
            if ok: found = (M, g); break
        if not found: break
        M, g = found; cur = conjugate_set(M, g, q); log("      one passes -> |H| = 2^%d" % (len(cur).bit_length() - 1))
    Inew = cur; stable = (len(Inew) == len(P))
    log("level %d (mod %d): |I| = 2^%d (full preimage: 2^%d)%s" % (k + 1, q, len(Inew).bit_length() - 1, len(P).bit_length() - 1, "  -> FULL PREIMAGE: stable from here on" if stable else ""))
    history[k + 1] = Inew
    Nprev, qprev_ = N, qp
    if stable: I = Inew; k += 1; break
    I = Inew; k += 1
r = k - 1 if len(history[k]) == 64*len(history[k - 1]) else k          # stable: the level-k image is the full preimage of level k-1, so use level k-1; otherwise use the last level computed
Ir = history[r]
dens = density(Ir, r)
stable_proved = (len(history[k]) == 64*len(history[k - 1]))
log("%s level 2^%d: density of odd-order reductions = %s = %.6f%s" % ("PROVED-STABLE image from", r, dens, float(dens), "") if stable_proved else
    "image NOT yet shown stable (the descent stopped at kmax); density computed ASSUMING the image at level 2^%d is the full preimage of the level-2^%d image: %s = %.6f" % (r + 1, r, dens, float(dens)))
for j, (aj, pj) in class_densities(Ir, r).items(): print("   p = %2d mod %d (prob %s): predicted fraction %s = %.5f" % (j, 2**r, pj, aj, float(aj)), flush=True)
json.dump({str(kk_): sorted(S_) for kk_, S_ in history.items()}, open('images_%d_%d_%d.json' % (a, c, kk), 'w'))
