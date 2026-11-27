#!/usr/bin/env python3
"""Addendum 22: second-level classes z_i = [x(W_i)], 2 W_i = U_b - U_a (partner pairs), over L0 = K(zeta_8).
(1) G (owner's generators, notes/data/pr92_signed_galois_output.txt): |G| = 1536, kernel of the action on the six x-coordinates = all 64 sign flips,
    unique invariant pairing of the x-coordinates (the partner pairing), image on the three pairs = S_3.
(2) x(U_b - U_a) = mu^2, mu = (y + y')/(2t), t = 1 - x (chord formula with x + x' = 2); halves: x(W) = (mu + s2)(mu + s3), s_2^2 = mu^2 - 1 - i, s_3^2 = mu^2 - 1 + i.
(3) At K-split primes p = 1 mod 8 (scan file) with chi(1+i) = +1 (so square classes of L0 mod [1+i] are evaluated without ambiguity) compute
    v = (chi(x_a-1-i) for the three pairs ; chi(x(W_i)) for the three pairs); verify sum c_i = 0, sum n_i = [p = 9 mod 16]  (i.e. z_1 z_2 z_3 = [zeta_8] there),
    and the rank of the span of the S_3-orbits of the v (5 = the dimension of the hyperplane sum c_i = 0).
(4) Level-2 divisibility of the three partner differences U_1-U_2, U_3-U_4, U_5-U_6 by 4, by torsion level m_p (observed triple frequency vs 4^-3 and 2*4^-3).
Usage: python3 -I pr92_z_class_check.py REPO_ROOT [NPRIMES]"""
import sys, os, re, gzip, random, itertools
from collections import defaultdict
root = sys.argv[1]; NP = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
sys.path.insert(0, os.path.join(root, "code/verify"))
from pr92_kummer_lattice_scan import roots_of, Hc
def leg(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
def sqrt_any(a, p):
    a %= p
    if p % 4 == 3: return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0: q //= 2; s += 1
    z = 2
    while leg(z, p) != -1: z += 1
    M, c, t, R = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1: tt = tt * tt % p; i += 1
        b = pow(c, 1 << (M - i - 1), p); M, c, t, R = i, b * b % p, t * b * b % p, R * b % p
    return R

# (1) the group
txt = open(os.path.join(root, "notes/data/pr92_signed_galois_output.txt")).read()
gtxt = txt.split("Generators:")[1].split("}")[0]
def parse(s):
    p = list(range(13))
    for cyc in re.findall(r"\(([^)]*)\)", s):
        c = [int(v) for v in cyc.split(",")]
        for i in range(len(c)): p[c[i]] = c[(i + 1) % len(c)]
    return tuple(p)
gens = [parse(s) for s in re.findall(r"(?:\([^)]*\))+", gtxt)]
mul = lambda a, b: tuple(a[b[i]] for i in range(13))
e = tuple(range(13)); Gs = {e}; fr = [e]
while fr:
    n = []
    for g in fr:
        for s in gens:
            h = mul(s, g)
            if h not in Gs: Gs.add(h); n.append(h)
    fr = n
opp = [(1, 3), (2, 4), (5, 9), (6, 10), (7, 12), (8, 11)]
oi = {a: k for k, pr in enumerate(opp) for a in pr}
act6 = lambda g: tuple(oi[g[opp[k][0]]] for k in range(6))
A6 = {act6(g) for g in Gs}
ker = [g for g in Gs if act6(g) == tuple(range(6))]
def pairings(items):
    if not items: yield []; return
    a = items[0]
    for b in items[1:]:
        for r in pairings([x for x in items if x not in (a, b)]): yield [(a, b)] + r
inv = [pr for pr in pairings(list(range(6))) if all({frozenset(g[i] for i in b) for b in pr} == {frozenset(b) for b in pr} for g in A6)]
idx = {i: k for k, b in enumerate(inv[0]) for i in b}
blocks = {tuple(idx[g[b[0]]] for b in inv[0]) for g in A6}
print("(1) |G| = %d; image on the 6 x-coordinates %d; kernel (sign flips) %d; invariant pairings %d; image on the 3 pairs %d" % (len(Gs), len(A6), len(ker), len(inv), len(blocks)))

# (3) evaluation vectors
vecs = []; viol = 0; seen = set()
for line in gzip.open(os.path.join(root, "notes/data/pr92_kummer_lattice_scan.tsv.gz"), "rt"):
    if line.startswith("#"): continue
    p = int(line.split("\t")[0])
    if p in seen: continue
    seen.add(p)
    if len(seen) > NP: break
    i = sqrt_any(p - 1, p)
    if leg(1 + i, p) != 1: continue
    xs = sorted(roots_of(Hc[:], p, random.Random(p))); done = set(); cs = []; ns = []
    for x in xs:
        if x in done: continue
        xp = (2 - x) % p; done |= {x, xp}
        t = (1 - x) % p; w = t * t % p
        y = sqrt_any(x * (w + 1), p); yp = sqrt_any(xp * (w + 1), p)
        mu = (y + yp) * pow(2 * t, -1, p) % p
        s2 = sqrt_any(mu * mu - 1 - i, p); s3 = sqrt_any(mu * mu - 1 + i, p)
        assert s2 * s2 % p == (mu * mu - 1 - i) % p
        xw = (mu + s2) * (mu + s3) % p
        ns.append(0 if leg(xw, p) == 1 else 1); cs.append(0 if leg(x - 1 - i, p) == 1 else 1)
    if sum(cs) % 2 != 0 or sum(ns) % 2 != (1 if p % 16 == 9 else 0): viol += 1
    vecs.append(cs + ns)
def rank(vs):
    basis = []
    for v in vs:
        x = int("".join(map(str, v)), 2)
        for b in basis: x = min(x, x ^ b)
        if x: basis.append(x)
    return len(basis)
orb = [[v[:3][k] for k in pm] + [v[3:][k] for k in pm] for v in vecs for pm in itertools.permutations(range(3))]
print("(3) K-split primes p = 1 mod 8 with chi(1+i) = +1 among the first %d scan primes: %d; violations of {sum c_i = 0, sum n_i = [p = 9 mod 16]}: %d; rank of the S_3-orbit span: %d" % (NP, len(vecs), viol, rank(orb)))

# (4) triple of partner differences at level 2 by torsion level
rows = []
for fn in ("pr92_kummer_lattice_scan.tsv.gz", "pr92_kummer_lattice_scan_deep.tsv.gz"):
    seen = set()
    for line in gzip.open(os.path.join(root, "notes/data", fn), "rt"):
        if line.startswith("#"): continue
        f = line.rstrip("\n").split("\t"); p = int(f[0])
        if p in seen: continue
        seen.add(p); rows.append((int(f[1]), [int(v) for v in f[4].split(",")]))
by = defaultdict(lambda: [0, 0])
for m, pd in rows:
    if m < 2: continue
    b = by[min(m, 4)]; b[0] += 1; b[1] += int(all(pd[i] >= 2 for i in (0, 9, 14)))
print("(4) triple (U1-U2, U3-U4, U5-U6 all in 4J(F_p)); independent prediction 1/64, one extra F_2-coupling 1/32:")
tot = [0, 0]
for m in sorted(by):
    n, t = by[m]; print("    m_p %s: %d primes, triple %d (%.5f); expected indep %.1f, coupled %.1f" % (("%d%s" % (m, "+" if m == 4 else "")), n, t, t / n, n / 64, n / 32))
    if m >= 3: tot[0] += n; tot[1] += t
n, t = tot; print("    m_p >= 3 pooled: %d vs %.1f (indep) / %.1f (coupled); z = %.1f" % (t, n / 64, n / 32, (t - n / 64) / (n / 64 * (1 - 1 / 64)) ** .5))
