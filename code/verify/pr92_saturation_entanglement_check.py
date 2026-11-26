#!/usr/bin/env python3
"""Saturation witnesses at 3 and 23, and the quadratic subfields of K = Q(D) (PR #92).  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Does NOT re-run Magma.  Checks, independently of the archived output:
(1) the split-prime and saturation witnesses of notes/KUMMER_ODD_SATURATION.md (point counts, completely split primes up to 229469, the stated multiples [N/l]P, [N/l]U);
(2) which quadratic fields Q(sqrt d), d squarefree with prime factors in {-1, 2, 3, 23}, can lie in K, using the archived generators of the Galois group G (|G| = 1536, |G^ab| = 4)
    and the factorization patterns of R mod p: if sqrt d were in K then (d/p) = eps(Frob_p) for a sign character eps of G, so eps must take the value (d/p) on some element of the cycle
    type of Frob_p, for every prime p.  If no sign character passes, sqrt d is NOT in K (rigorous given G).  A character that passes is only a necessary condition.
Usage: python3 code/verify/pr92_saturation_entanglement_check.py   (about 40 s)
"""
import itertools
import math
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v
import pr92_sieve_second_moment as sm

ok_all = True


def check(name, cond):
    global ok_all
    print(("ok   " if cond else "FAIL ") + name)
    ok_all = ok_all and cond


def cyc(*cycles):
    p = list(range(13))
    for c in cycles:
        for i in range(len(c)):
            p[c[i]] = c[(i + 1) % len(c)]
    return tuple(p[1:])  # image of 1..12


GENS = [
    cyc((1, 8, 5, 3, 11, 9), (2, 12, 10), (4, 7, 6)),
    cyc((1, 11, 10), (2, 12, 9, 4, 7, 5), (3, 8, 6)),
    cyc((8, 11)), cyc((5, 9)), cyc((7, 12)), cyc((2, 4)),
    cyc((1, 9), (2, 10), (3, 5), (4, 6), (7, 12)),
    cyc((1, 3)),
    cyc((1, 6, 3, 10), (2, 9, 4, 5), (7, 12)),
    cyc((6, 10)),
]
PAIRS = [(1, 3), (2, 4), (5, 9), (6, 10), (7, 12), (8, 11)]


def compose(a, b):  # apply a then b (images of points 1..12 stored 0-based)
    return tuple(b[a[i] - 1] for i in range(12))


identity = tuple(range(1, 13))
grp = {identity}
frontier = [identity]
while frontier:
    new = []
    for g in frontier:
        for s in GENS:
            h = compose(g, s)
            if h not in grp:
                grp.add(h)
                new.append(h)
    frontier = new

def cycle_type(g):
    seen, ct = set(), []
    for i in range(1, 13):
        if i in seen:
            continue
        n, j = 0, i
        while j not in seen:
            seen.add(j)
            j = g[j - 1]
            n += 1
        ct.append(n)
    return tuple(sorted(ct))



R = {12: 1, 10: -66, 8: -29922, 6: 73214, 4: -62559, 2: 22032, 0: -3456}
Rc = [R.get(i, 0) for i in range(13)]


def pattern(p):
    f = v.pnorm([c % p for c in Rc])
    d = v.pnorm([(i * f[i]) % p for i in range(1, len(f))])
    if not d or len(v.pgcd(f, d, p)) > 1:
        return None
    degs, g, cur = [], f[:], [0, 1]
    for k in range(1, 7):
        if len(g) <= 1:
            break
        cur = v.ppowx_shift(cur, p, g, p)
        dd = cur + [0] * (2 - len(cur))
        dd = dd[:]
        dd[1] = (dd[1] - 1) % p
        dd = v.pnorm(dd)
        G = g[:] if not dd else v.pgcd(g, dd, p)
        if len(G) > 1:
            degs += [k] * ((len(G) - 1) // k)
            q = [0] * (len(g) - len(G) + 1)
            r = g[:]
            ig = pow(G[-1], -1, p)
            for i in range(len(q) - 1, -1, -1):
                c = r[i + len(G) - 1] * ig % p
                q[i] = c
                for j in range(len(G)):
                    r[i + j] = (r[i + j] - c * G[j]) % p
            g = v.pnorm(q)
            cur = v.pmod(cur, g, p) if len(g) > 1 else cur
    if len(g) > 1:
        degs += [len(g) - 1]
    return tuple(sorted(degs))




# (1) witnesses
def count_points(p):
    n = 1
    for x in range(p):
        Y = v.Yc(x) % p
        n += 1 if Y == 0 else (2 if pow(Y, (p - 1) // 2, p) == 1 else 0)
    return n


def completely_split(p):
    r = v.roots_mod_p(p)
    return len(r) == 6 and all(pow(v.Yc(x) % p, (p - 1) // 2, p) == 1 for x in r)


N2621 = count_points(2621)
check("(1) p = 2621 is completely split with #J = %d = 2^3 * 5 * 67, so J(K) has no 3- or 23-primary torsion" % N2621, completely_split(2621) and N2621 == 2680)
split = [p for p in v.primes_upto(229469) if p >= 7 and p != 23 and completely_split(p)]
check("(1) %d completely split primes up to 229469 (owner list has 17; expected about %.1f)" % (len(split), len(v.primes_upto(229469)) / 1536), len(split) == 17 and split[0] == 2621 and split[-1] == 229469)
for p, pt, l, expect in [(113819, (1, 1), 3, (101754, 42501)), (49253, (3857, 14240), 3, (26339, 2137)), (229469, (1, 1), 23, (202137, 196012)), (229469, (5468, 173790), 23, (215498, 199718))]:
    add, neg, mul = sm.group(p)
    N = count_points(p)
    Q = mul(N // l, pt)
    check("(1) p = %d, #J = %d, [N/%d]%s = %s (stated %s), nonzero, p completely split: %s" % (p, N, l, pt, Q, expect, completely_split(p)), N % l == 0 and Q == expect and completely_split(p))

# (2) quadratic subfields
grp = {tuple(range(1, 13))}
frontier = list(grp)
while frontier:
    new = []
    for g in frontier:
        for s in GENS:
            h = compose(g, s)
            if h not in grp:
                grp.add(h)
                new.append(h)
    frontier = new
identity = tuple(range(1, 13))
chars = []
for signs in itertools.product((1, -1), repeat=len(GENS)):
    eps = {identity: 1}
    fr = [identity]
    good = True
    while fr and good:
        new = []
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
                    new.append(h)
            if not good:
                break
        fr = new
    if good and len(eps) == len(grp):
        chars.append(eps)
AT = []
for c in chars:
    A = defaultdict(set)
    for g, e in c.items():
        A[cycle_type(g)].add(e)
    AT.append(A)
check("(2) |G| = %d and G has %d sign characters (so G^ab/2G^ab has order %d)" % (len(grp), len(chars), len(chars)), len(grp) == 1536 and len(chars) == 4)
data = []
for p in v.primes_upto(60000):
    if p < 5 or p == 23:
        continue
    pt = pattern(p)
    if pt is not None:
        data.append((p, pt))


def kron(d, p):
    return 1 if pow(d % p, (p - 1) // 2, p) == 1 else -1


passing = {}
for mask in range(1, 16):
    d = 1
    for bit, q in enumerate((-1, 2, 3, 23)):
        if mask >> bit & 1:
            d *= q
    okc = [i for i, A in enumerate(AT) if all(kron(d, p) in A[pt] for p, pt in data)]
    passing[d] = okc
print("     %d primes tested; quadratic d with prime factors in {-1,2,3,23} for which some sign character of G is consistent:" % len(data))
for d, okc in sorted(passing.items()):
    print("        d = %5d: %s" % (d, "characters %s" % okc if okc else "none  -> sqrt(d) is not in K"))
cons = sorted(d for d, okc in passing.items() if okc)
check("(2) exactly three such d pass, namely %s (the three quadratic subfields of a biquadratic field; each is a necessary-condition match with a distinct sign character)" % cons, len(cons) == 3 and all(passing[d] for d in cons) and len({passing[d][0] for d in cons}) == 3)
check("(2) sqrt(-1), sqrt(2), sqrt(-2), sqrt(-3) and sqrt(-23) are NOT in K (so Q(i), Q(zeta_8)'s sqrt 2, Q(zeta_3), and the quadratic subfield Q(sqrt(-23)) of Q(zeta_23) do not lie in K)", all(not passing[d] for d in (-1, 2, -2, -3, -23)))
sys.exit(0 if ok_all else 1)
