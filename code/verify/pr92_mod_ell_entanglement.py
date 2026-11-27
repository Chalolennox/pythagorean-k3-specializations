#!/usr/bin/env python3
"""Mod-3 and mod-23 images of J over Q, entanglement of K with Q(J[l]), and Frobenius statistics conditional on the entangled characters (PR #92).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Parts marked PROOF GIVEN use only finite computations printed here plus classical group theory (Dickson);
parts that use the owner-attested Galois group G of the 12 points (archived generators) are conditional on it.  No claim about Problem H.

(1) l >= 5 (l = 5..199): witnesses p < 8000 for the three Dickson tests on Frobenius traces a_p:  A: a_p != 0, a_p^2 - 4p a nonsquare mod l (not in Borel, not in N(split Cartan));
    B: a_p != 0, a_p^2 - 4p a nonzero square (not in N(nonsplit Cartan));  C: t = a_p^2/p not in {0,1,2,4}, t^2 - 3t + 1 != 0 (projective order > 5: not exceptional).  With det = cyclotomic character
    surjective, A, B, C give image = GL_2(F_l).  PROOF GIVEN for each l printed.  (For l > 199 the statement needs a separate argument; LMFDB reports maximal image for every odd l for the j = 128 twist class.)
(2) l = 3: enumeration of all subgroups of GL_2(F_3) and comparison of the observed (trace, det) frequencies of Frobenius with each subgroup (chi-square); evidence for the full group.
(3) PROOF GIVEN from (1)-(2) and the attested G: the solvable quotients of GL_2(F_l) factor through det (SL_2(F_l) perfect for l >= 5; for l = 3 the quotients S_3, S_4, GL_2 carry sqrt(-3) as sign character),
    and the only quadratic subfields of K are Q(sqrt -6), Q(sqrt 69), Q(sqrt -46) (Addendum 9); hence K ∩ Q(J[l]) = Q for l = 3 and l = 23 (and in fact for all l with the image GL_2).
(4) Chebotarev with the attested G: the mean number of rational points |D_p| conditional on ((-6/p), (69/p)) is predicted exactly from G (fixed points of group elements with the given sign characters) and compared
    with the observed means for 7 <= p <= 300000.  Then the coverage weights a_p/d_p vs |D_p^+|/p are split by the same classes: evidence for how the entanglement enters the constant C.
Usage: python3 -I code/verify/pr92_mod_ell_entanglement.py   (about 1 minute).  Exit 0 iff all checks pass.
"""
import itertools
import math
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v  # noqa: E402
import pr92_sieve_second_moment as sm  # noqa: E402

ok_all = True


def check(name, cond):
    global ok_all
    print(("ok   " if cond else "FAIL ") + name)
    ok_all = ok_all and cond


def leg(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)


# ---------- traces
AP_BOUND = 8000
ap = {}
for p in v.primes_upto(AP_BOUND):
    if p == 2:
        continue
    n = 1
    for x in range(p):
        Y = (x * (x * x - 2 * x + 2)) % p
        n += 1 if Y == 0 else (2 if pow(Y, (p - 1) // 2, p) == 1 else 0)
    ap[p] = p + 1 - n
check("traces a_p computed for %d odd primes below %d (e.g. a_3 = %d, a_5 = %d, a_7 = %d)" % (len(ap), AP_BOUND, ap[3], ap[5], ap[7]), len(ap) > 1000 and abs(ap[7]) <= 5)

# ---------- (1) l >= 5
fails, wit = [], {}
for l in v.primes_upto(199):
    if l < 5:
        continue
    A = B = C = None
    for p, a in ap.items():
        if p == l or p == 2:
            continue
        a %= l
        d = (a * a - 4 * p) % l
        if A is None and a != 0 and leg(d, l) == -1:
            A = p
        if B is None and a != 0 and leg(d, l) == 1:
            B = p
        if C is None:
            t = a * a * pow(p, -1, l) % l
            if t not in (0, 1, 2, 4) and (t * t - 3 * t + 1) % l != 0:
                C = p
        if A and B and C:
            break
    wit[l] = (A, B, C)
    if not (A and B and C):
        fails.append(l)
check("(1) tests A, B, C have witnesses for every prime l in [5, 199] (failures: %s); so the mod-l image is GL_2(F_l) for all of them (Dickson + surjective det)" % fails, not fails)
print("     witnesses for l = 5, 7, 13, 23, 199: %s" % {l: wit[l] for l in (5, 7, 13, 23, 199)})
check("(1) l = 23 in particular: witnesses p_A, p_B, p_C = %s" % (wit[23],), all(wit[23]))

# ---------- (2) l = 3
def mm(a, b):
    return ((a[0] * b[0] + a[1] * b[2]) % 3, (a[0] * b[1] + a[1] * b[3]) % 3, (a[2] * b[0] + a[3] * b[2]) % 3, (a[2] * b[1] + a[3] * b[3]) % 3)


GL = [m for m in itertools.product(range(3), repeat=4) if (m[0] * m[3] - m[1] * m[2]) % 3]
I3 = (1, 0, 0, 1)
subs = set()
for g in GL:
    for h in GL:
        S = {I3}
        fr = [I3]
        while fr:
            nw = []
            for x in fr:
                for s in (g, h):
                    y = mm(x, s)
                    if y not in S:
                        S.add(y)
                        nw.append(y)
            fr = nw
        subs.add(frozenset(S))
det = lambda m: (m[0] * m[3] - m[1] * m[2]) % 3
tr = lambda m: (m[0] + m[3]) % 3
cand = [S for S in subs if {det(m) for m in S} == {1, 2}]
obs = Counter((ap[p] % 3, p % 3) for p in ap if p not in (2, 3))
n = sum(obs.values())
print("     GL_2(F_3) has %d subgroups (2-generated enumeration); %d have surjective det; observed (trace, det) of Frobenius over %d primes: %s" % (len(subs), len(cand), n, dict(sorted(obs.items()))))
res = []
for S in sorted(cand, key=len):
    f = Counter((tr(m), det(m)) for m in S)
    if any(k not in f for k in obs):
        res.append((len(S), None))
        continue
    chi = sum((obs[k] - n * f[k] / len(S)) ** 2 / (n * f[k] / len(S)) for k in f)
    res.append((len(S), chi, len(f) - 1))
for r in res:
    print("       subgroup of order %2d: %s" % (r[0], "excluded (an observed (trace,det) does not occur)" if r[1] is None else "chi2 = %.1f (df %d)" % (r[1], r[2])))
full = [r for r in res if r[0] == 48][0]
check("(2) the full group GL_2(F_3) fits the observed Frobenius statistics (chi2 = %.1f, df %d); every proper subgroup with surjective det is excluded or fits with larger chi2: %s" % (full[1], full[2], [(r[0], None if r[1] is None else round(r[1], 1)) for r in res if r[0] != 48]),
      full[1] < full[2] + 4 * math.sqrt(2 * full[2]) and all(r[1] is None or r[1] > full[2] + 4 * math.sqrt(2 * full[2]) for r in res if r[0] != 48))

# rigorous exclusion of every proper subgroup with surjective det (PROOF GIVEN):
#   not in SL_2: p = 2 mod 3 occurs (det = p mod 3);  not in a Borel subgroup: a p with (trace, det) = (1, 2) mod 3 has char poly x^2 - x + 2, irreducible mod 3 (disc = 2 nonsquare), impossible in a Borel;
#   not in a Sylow-2 subgroup SD16 = N(nonsplit Cartan): a p = 1 mod 3 with #J(F_p) = 3 or 6 mod 9 gives J(F_p)[3] = Z/3, so Frobenius has eigenvalue 1, is not the identity and has det 1: unipotent of order 3.
w_det = next(p for p in ap if p % 3 == 2)
w_irr = next(p for p in ap if p not in (2, 3) and ap[p] % 3 == 1 and p % 3 == 2)
w_ord3 = next(p for p in ap if p % 3 == 1 and (p + 1 - ap[p]) % 9 in (3, 6))
check("(2) rigorous: p = %d (det 2), p = %d (char poly x^2 - x + 2 irreducible mod 3), p = %d (#J = %d, J(F_p)[3] = Z/3, Frobenius unipotent of order 3) exclude SL_2, Borel, SD16: mod-3 image = GL_2(F_3)" % (w_det, w_irr, w_ord3, w_ord3 + 1 - ap[w_ord3]), True)

# ---------- the attested group
def cyc(*cycles):
    p = list(range(13))
    for c in cycles:
        for i in range(len(c)):
            p[c[i]] = c[(i + 1) % len(c)]
    return tuple(p[1:])


GENS = [
    cyc((1, 8, 5, 3, 11, 9), (2, 12, 10), (4, 7, 6)),
    cyc((1, 11, 10), (2, 12, 9, 4, 7, 5), (3, 8, 6)),
    cyc((8, 11)), cyc((5, 9)), cyc((7, 12)), cyc((2, 4)),
    cyc((1, 9), (2, 10), (3, 5), (4, 6), (7, 12)),
    cyc((1, 3)),
    cyc((1, 6, 3, 10), (2, 9, 4, 5), (7, 12)),
    cyc((6, 10)),
]


def compose(a, b):
    return tuple(b[a[i] - 1] for i in range(12))


ident = tuple(range(1, 13))
grp = {ident}
fr = [ident]
while fr:
    nw = []
    for g in fr:
        for s in GENS:
            h = compose(g, s)
            if h not in grp:
                grp.add(h)
                nw.append(h)
    fr = nw
chars = []
for signs in itertools.product((1, -1), repeat=len(GENS)):
    eps = {ident: 1}
    fr = [ident]
    good = True
    while fr and good:
        nw = []
        for g in fr:
            for s, sg in zip(GENS, signs):
                h = compose(g, s)
                e = eps[g] * sg
                if h in eps:
                    if eps[h] != e:
                        good = False
                        break
                else:
                    eps[h] = e
                    nw.append(h)
            if not good:
                break
        fr = nw
    if good and len(eps) == len(grp):
        chars.append(eps)
check("|G| = %d and G has %d sign characters" % (len(grp), len(chars)), len(grp) == 1536 and len(chars) == 4)

# (3) the logical statement, with the verified inputs
print("(3) K ∩ Q(J[l]) = Q for l = 3 and l = 23: for l = 23 the solvable quotients of GL_2(F_23) are quotients of F_23^* via det, whose quadratic quotient is Q(sqrt(-23)), not in K (Addendum 9);")
print("    K ∩ Q(J[23]) is Galois over Q with group a common quotient of G (solvable) and GL_2(F_23); SL_2(F_23) is perfect so the quotient is a quotient of det (cyclic, order | 22) and abelian, hence of order | gcd(4, 22) = 2; order 2 would give Q(sqrt -23) in K.  For l = 3 a nontrivial common quotient would be a quotient of GL_2(F_3) and of G;")
print("    every non-trivial quotient of GL_2(F_3) (Z/2, S_3, S_4, GL_2(F_3)) has sign character det <-> Q(sqrt -3), not in K.  PROOF GIVEN conditional on G and on the mod-l images above.")
check("(3) -3 and -23 (squarefree) are not among the squarefree classes -6, 69, -46 of the quadratic subfields of K, and G^ab has order 4 (so a common abelian quotient with Z/22 has order <= 2)", {-3, -23}.isdisjoint({-6, 69, -46}) and len(chars) == 4)

# ---------- (4) conditional Frobenius statistics
def fixed(g):
    return sum(1 for i in range(1, 13) if g[i - 1] == i)


# mapping of characters to quadratic fields from Addendum 9: d = -6 -> char 3, d = 69 -> char 1, d = -46 -> char 2 (indices in this enumeration)
c6, c69, c46 = chars[3], chars[1], chars[2]
check("(4) the product of the characters for -6 and 69 equals the character for -46 (as -6 * 69 = -46 * 9)", all(c6[g] * c69[g] == c46[g] for g in grp))
pred = defaultdict(lambda: [0, 0])
for g in grp:
    k = (c6[g], c69[g])
    pred[k][0] += 1
    pred[k][1] += fixed(g)
primes = [p for p in v.primes_upto(300000) if p >= 7 and p != 23]
lo_idx = next(i for i, p in enumerate(primes) if p >= 30000)
emp = defaultdict(lambda: [0, 0, 0.0, 0.0])
blocks = 10
bl = defaultdict(lambda: [[0.0, 0.0] for _ in range(blocks)])
for idx, p in enumerate(primes):
    allp, elig = sm.points(p)
    k = (leg(-6, p), leg(69, p))
    e = emp[k]
    e[0] += 1
    e[1] += len(allp)
    sD = len(elig) / p
    sA = 0.0
    if elig:
        add, neg, mul = sm.group(p)
        P = (1, 1)
        L = math.isqrt(4 * p) + 6
        cur, d, hits, Es = P, None, 0, set(elig)
        for nn in range(1, L + 1):
            if cur is None:
                d = nn
                break
            if cur in Es:
                hits += 1
            cur = add(cur, P)
        if d is None:
            d = sm.order_bsgs(p, P, add, neg, mul)
            hits = sum(1 for z in elig if sm.dlog(P, d, z, add, neg, mul) is not None)
        sA = hits / d
    if p >= 30000:
        e[2] += sA
        e[3] += sD
        b = min(blocks - 1, (idx - lo_idx) * blocks // (len(primes) - lo_idx))
        bl[k][b][0] += sA
        bl[k][b][1] += sD
print("     class (chi_-6(p), chi_69(p)):  predicted mean |D_p| from G   observed mean |D_p|  (#primes)   sum a_p/d_p   sum |D_p^+|/p   ratio (block sd)   [sums over 30000 <= p <= 300000 only]")
tot_ok = True
cls_pred = []
for k in sorted(pred):
    pm = pred[k][1] / pred[k][0]
    e = emp[k]
    om = e[1] / e[0]
    rb = [b[0] / b[1] for b in bl[k] if b[1] > 0]
    mean = sum(rb) / len(rb)
    sd = math.sqrt(sum((r - mean) ** 2 for r in rb) / (len(rb) - 1)) if len(rb) > 1 else float("nan")
    se = 1.5 / math.sqrt(e[0])
    tot_ok = tot_ok and abs(pm - om) < 4 * se + 0.05
    cls_pred.append(pm)
    print("       %-12s %20.4f %24.4f %12d %14.4f %15.4f %10.3f (%.3f)" % (k, pm, om, e[0], e[2], e[3], e[2] / e[3], sd))
check("(4) observed class means of |D_p| agree with the exact prediction from G, which is 1 in every class: the entangled characters do NOT change the first-order mean number of rational points", tot_ok and all(abs(x - 1) < 1e-12 for x in cls_pred))
allr = sum(e[2] for e in emp.values()) / sum(e[3] for e in emp.values())
print("     slope ratio (sum a_p/d_p)/(sum |D_p^+|/p) over 30000 <= p <= 300000: %.3f; per-class values above have block sd about 0.2-0.3, so the experiment cannot see effects of a few percent" % allr)
# (5) eligible points: the w-extension is not in the attested group, so observe |D_p^+| by class
cnt = defaultdict(lambda: [0, 0, 0])
for p in v.primes_upto(1000000):
    if p < 7 or p == 23:
        continue
    allp, elig = sm.points(p)
    k = (leg(-6, p), leg(69, p))
    cnt[k][0] += 1
    cnt[k][1] += len(elig)
    cnt[k][2] += len(elig) ** 2
print("(5) mean |D_p^+| by class (chi_-6(p), chi_69(p)), primes 7 <= p <= 10^6 (expected 0.5 if no coupling; the w-extension is not in the attested group, so no exact prediction):")
means = []
for k in sorted(cnt):
    n_, s1, s2 = cnt[k]
    m = s1 / n_
    se = math.sqrt((s2 / n_ - m * m) / n_)
    means.append((m, se))
    print("       %-10s mean = %.4f +- %.4f  (%d primes)" % (k, m, se, n_))
check("(5) the four class means of |D_p^+| agree with 0.5 and with each other within 3 standard errors: no first-order coupling of the numerator to the entangled characters", all(abs(m - 0.5) < 3 * se for m, se in means))
print("DONE")
sys.exit(0 if ok_all else 1)
