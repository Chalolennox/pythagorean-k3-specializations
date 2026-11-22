#!/usr/bin/env python3
"""Support structure of the qualifying indices: numerical and exact checks of the statements in
notes/REVIEW_2026-11-22_support_structure_proved.md.

Setting.  C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), H(t) = t^6 - 30 t^4 - 24 t^2 - 1 = C3(t^2),
C3(s) = s^3 - 30 s^2 - 24 s - 1, g(t) = 2t(1-t^2), t(Q) = 1 - x(Q).  For a prime p >= 5 and j in {0,1}
    N_{p,j} = { n mod m_p : Q = nP + jT is affine and H(t(Q)) = 0 mod p },
    S_{p,j} = { n in N_{p,j} : g(t(Q)) is a nonzero square mod p },     m_p = ord(P mod p).

Statements checked (numbers refer to the note):
  1  exact identities: C3(1) = -54, C3(-1) = -8, disc C3 = 3^9 * 23, H(1) = -54, H(+-i) = -8;
     the Galois model of order 24 gives fixed-point counts 6, 2, 0 with multiplicities 1, 9, 14
  2  #{t in F_p : H(t) = 0} is 0, 2 or 6 for every prime 5 <= p <= LIMIT (brute force) and <= 60000 (gcd)
  3  N_{p,j} and S_{p,j} are symmetric under n -> -n and have even cardinality
  4  |S_{p,j}| <= 2 (p=3 mod 4, 2 roots), 6 (3 mod 4, 6 roots), 4 (1 mod 4, 2 roots), 12 (1 mod 4, 6 roots)
  5  the necessary congruence p = 1 mod 24 for |S| = 12 (tested on the hypotheses "all six roots qualify")
     and the example p = 5251537 with |S_{p,1}| = 12 (full group law, original definition)
  6  x(nP) is a square mod p for nP not in {O,T};  x(Q+T) = 2/x(Q)
  7  p = 5 mod 8:  m_p is even;  (-1)^n = chi(t+i) for Q = nP and (-1)^n = chi(t+i) chi(-(1+i)) for
     Q = nP + T  (all n, not only qualifying ones);  for p = 1 mod 4 and n even, chi(t+i) = 1
  8  p = 5 mod 8: if both t and -t occur as t(Q) on one branch, the two indices have equal parity
     (branch 0) or opposite parity (branch 1)
  9  the parity obstruction for pairs of primes = 5 mod 8, and the counts of the dossier below 2000
 10  the counterexamples p = 85453 (|S_{p,0}| = 8) and p = 32237 (|S_{p,1}| = 8)

Usage:  python3 code/verify_support_structure.py [--quick]
        --quick: LIMIT = 2000 (about 7 s);  default: LIMIT = 4000 (about 10 s).
Standard library only.  Derived with a language model; no human check."""
import sys, math, itertools
from fractions import Fraction as Fr

QUICK = "--quick" in sys.argv
LIMIT = 2000 if QUICK else 4000


def primes(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, int(n ** .5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def chi(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def Hm(t, p):
    t2 = t * t % p
    return (t2 * t2 % p * t2 - 30 * t2 * t2 - 24 * t2 - 1) % p


def add_factory(p):
    def add(Q, R):
        if Q is None: return R
        if R is None: return Q
        x1, y1 = Q; x2, y2 = R
        if x1 == x2:
            if (y1 + y2) % p == 0: return None
            lam = (3 * x1 * x1 - 4 * x1 + 2) * pow(2 * y1, -1, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam + 2 - x1 - x2) % p
        return (x3, (-y1 + lam * (x1 - x3)) % p)
    return add


def sqrtm1(p):
    for a in range(2, p):
        r = pow(a, (p - 1) // 4, p)
        if r * r % p == p - 1: return r


def data(p):
    """m_p, the list xs[n] = x(nP) (None for O), the root list of H, and N, S for both branches."""
    add = add_factory(p)
    pts = [None]; Q = None
    while True:
        Q = add(Q, (1, 1))
        if Q is None: break
        pts.append(Q)
    m = len(pts)
    xs = [None if q is None else q[0] for q in pts]
    # x(nP + T): by the group law for n = 0, 1 (spot check), and by 2/x in general (checked in section 6)
    x1 = [0] + [None if xs[n] == 0 else 2 * pow(xs[n], -1, p) % p for n in range(1, m)]
    roots = [t for t in range(p) if Hm(t, p) == 0]
    out = {}
    for j, xl in ((0, xs), (1, x1)):
        N, S = set(), set()
        for n in range(m):
            x = xl[n]
            if x is None: continue
            t = (1 - x) % p
            if Hm(t, p) == 0:
                N.add(n)
                gv = 2 * t * (1 - t * t) % p
                if gv and chi(gv, p) == 1: S.add(n)
        out[j] = (N, S)
    return m, pts, xs, x1, roots, out


fails = []
def check(name, cond, info=""):
    print(("ok   " if cond else "FAIL ") + name + (("  " + info) if info else ""))
    if not cond: fails.append(name)


# ---------------------------------------------------------------- 1. exact identities, Galois model
C3 = lambda s: s ** 3 - 30 * s ** 2 - 24 * s - 1
Hz = lambda t: t ** 6 - 30 * t ** 4 - 24 * t ** 2 - 1
disc = 18 * 1 * (-30) * (-24) * (-1) - 4 * (-30) ** 3 * (-1) + (-30) ** 2 * (-24) ** 2 - 4 * 1 * (-24) ** 3 - 27 * 1 * 1
check("1  C3(1) = -54, C3(-1) = -8, H(1) = -54, H(i) = -8 (i^2=-1)",
      C3(1) == -54 and C3(-1) == -8 and Hz(1) == -54 and Hz(-1) == -54 and Hz(1j) == -8 and Hz(-1j) == -8)
check("1  disc C3 = 3^9 * 23 = %d" % disc, disc == 3 ** 9 * 23)
cnt = {}
for perm in itertools.permutations(range(3)):
    for eps in itertools.product((1, -1), repeat=3):
        if eps[0] * eps[1] * eps[2] != 1: continue
        fixed = 2 * sum(1 for i in range(3) if perm[i] == i and eps[i] == 1)
        cnt[fixed] = cnt.get(fixed, 0) + 1
check("1  group {(sigma, eps): prod eps = 1} of order 24: fixed roots 6/2/0 occur 1/9/14 times", cnt == {6: 1, 2: 9, 0: 14}, str(cnt))

# ---------------------------------------------------------------- main loop over primes
PR = [p for p in primes(LIMIT) if p >= 5]
D = {}
viol = {k: [] for k in ("roots", "sym", "even", "bound", "sq", "T", "par0", "par1", "pm", "even_impl", "m_even")}
tested = {"par": 0, "pm": 0, "bound": 0}
bnd = {(3, 2): 2, (3, 6): 6, (1, 2): 4, (1, 6): 12}
maxS = {}
mixed_cong = {"b0": 0, "b1": 0}
for p in PR:
    m, pts, xs, x1, roots, out = data(p)
    D[p] = (m, out, len(roots))
    r = len(roots)
    if r not in (0, 2, 6): viol["roots"].append((p, r))
    for j in (0, 1):
        N, S = out[j]
        if N != {(-n) % m for n in N} or S != {(-n) % m for n in S}: viol["sym"].append((p, j))
        if len(N) % 2 or len(S) % 2: viol["even"].append((p, j))
        if r == 0:
            if N: viol["bound"].append((p, j, "nonempty"))
        else:
            tested["bound"] += 1
            if len(S) > bnd[(p % 4, r)]: viol["bound"].append((p, j, len(S)))
        k = (p % 4, r)
        maxS[(k, j)] = max(maxS.get((k, j), 0), len(S))
    # 6: x(nP) square, x(Q+T) = 2/x(Q) via the group law for a few n
    for n in range(1, m):
        x = xs[n]
        if x is not None and x != 0 and chi(x, p) != 1: viol["sq"].append((p, n))
    if p < 200:
        add = add_factory(p)
        for n in range(1, m):
            Q = pts[n]; R = add(Q, (0, 0))
            if (R is None) != (xs[n] == 0): viol["T"].append((p, n))
            elif R is not None and R[0] != x1[n]: viol["T"].append((p, n))
    # 7, 8: descent parity
    if p % 4 == 1:
        i = sqrtm1(p)
        c1 = chi(-(1 + i), p)
        for j, xl in ((0, xs), (1, x1)):
            for n in range(m):
                x = xl[n]
                if x is None or x == 0 or x == 1 + i or x == 1 - i: continue
                t = (1 - x) % p
                c = chi(t + i, p) * (c1 if j else 1)
                if n % 2 == 0 and c != 1: viol["even_impl"].append((p, j, n))
                if p % 8 == 5:
                    tested["par"] += 1
                    if (-1) ** n != c: viol["par%d" % j].append((p, n))
        if p % 8 == 5:
            if m % 2: viol["m_even"].append(p)
            for j, xl in ((0, xs), (1, x1)):
                by_t = {}
                for n in range(m):
                    x = xl[n]
                    if x is not None and x not in (0, 1 + i, 1 - i): by_t[(1 - x) % p] = n
                for t, n in by_t.items():
                    if (-t) % p in by_t and t != (-t) % p:
                        tested["pm"] += 1
                        same = (n % 2 == by_t[(-t) % p] % 2)
                        if same != (j == 0): viol["pm"].append((p, j, t))

check("2  root count of H is 0, 2 or 6 for all 5 <= p <= %d (%d primes; includes p = 23)" % (LIMIT, len(PR)), not viol["roots"], str(viol["roots"][:3]))
check("3  N_{p,j}, S_{p,j} symmetric under n -> -n and of even size", not viol["sym"] and not viol["even"], str((viol["sym"] + viol["even"])[:3]))
check("4  |S_{p,j}| <= 2/6/4/12 by (p mod 4, #roots); %d (prime, branch) cases" % tested["bound"], not viol["bound"], str(viol["bound"][:3]))
print("     largest |S| seen below %d, by ((p mod 4, #roots), branch): %s" % (LIMIT, dict(sorted(maxS.items()))))
check("6  x(nP) is a square for every nP not in {O,T}", not viol["sq"], str(viol["sq"][:3]))
check("6  x(Q+T) = 2/x(Q) (group law, p < 200)", not viol["T"], str(viol["T"][:3]))
check("7  p = 5 mod 8: m_p even", not viol["m_even"], str(viol["m_even"][:3]))
check("7  p = 5 mod 8: (-1)^n = chi(t+i) [branch 0], chi(t+i)chi(-(1+i)) [branch 1] for all %d points" % tested["par"],
      not viol["par0"] and not viol["par1"], str((viol["par0"] + viol["par1"])[:3]))
check("7  p = 1 mod 4: n even  =>  chi(t+i) [chi(-(1+i)) on branch 1] = 1", not viol["even_impl"], str(viol["even_impl"][:3]))
check("8  p = 5 mod 8: +-t on one branch have equal (branch 0) / opposite (branch 1) parity; %d pairs" % tested["pm"], not viol["pm"], str(viol["pm"][:3]))

# the converse of 7 fails for p = 1 mod 8 (P is in 2E there): exhibit it
p = 17; m, pts, xs, x1, roots, out = data(p); i = sqrtm1(p)
bad = [n for n in range(1, m) if xs[n] not in (None, 0, 1 + i, 1 - i) and n % 2 == 1 and chi((1 - xs[n]) + i, p) == 1]
check("7  p = 17 (= 1 mod 8): an odd n with chi(t+i) = 1 exists, so parity is not read off from the character", bool(bad), "n = %s" % bad[:3])

# ---------------------------------------------------------------- 2'. root counts up to 60000 (polynomial gcd) and densities
def pmulmod(a, b, p):
    r = [0] * 11
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    for k in range(10, 5, -1):          # reduce with t^6 = 30 t^4 + 24 t^2 + 1
        c = r[k] % p
        if c:
            r[k - 2] += 30 * c; r[k - 4] += 24 * c; r[k - 6] += c
        r[k] = 0
    return [x % p for x in r[:6]]

def nroots_H(p):
    """number of distinct roots of H in F_p = deg gcd(H, t^p - t)."""
    base = [0, 1, 0, 0, 0, 0]; res = [1, 0, 0, 0, 0, 0]; e = p
    while e:
        if e & 1: res = pmulmod(res, base, p)
        base = pmulmod(base, base, p); e >>= 1
    f = res[:]; f[1] = (f[1] - 1) % p           # t^p - t mod H
    a = [(-1) % p, 0, (-24) % p, 0, (-30) % p, 0, 1]   # H, low -> high
    b = f
    def trim(u):
        u = u[:]
        while u and u[-1] == 0: u.pop()
        return u
    a, b = trim(a), trim(b)
    while b:
        inv = pow(b[-1], -1, p); r = a[:]
        while len(r) >= len(b):
            c = r[-1] * inv % p; sh = len(r) - len(b)
            for k, y in enumerate(b): r[sh + k] = (r[sh + k] - c * y) % p
            r = trim(r)
        a, b = b, r
    return len(a) - 1

hist = {}
for p in primes(60000):
    if p < 5: continue
    c = nroots_H(p)
    hist[c] = hist.get(c, 0) + 1
tot = sum(hist.values())
check("2  root counts for the %d primes 5 <= p <= 60000 are only 0, 2, 6 (polynomial gcd); p = 23 gives 2" % tot,
      set(hist) <= {0, 2, 6} and nroots_H(23) == 2, str(dict(sorted(hist.items()))))
print("     frequencies 0/2/6: %.3f / %.3f / %.3f   (order-24 model: 14/24 = 0.583, 9/24 = 0.375, 1/24 = 0.042)"
      % tuple(hist.get(k, 0) / tot for k in (0, 2, 6)))

# ---------------------------------------------------------------- 5. congruence for |S| = 12
def cong_hyp(p):
    """roots of H mod p; hypothesis of Proposition 4 on each branch: all six g(t) are squares and
    1 - t, 1 + t are squares (branch 0) / have the character of 2 (branch 1)."""
    ts = [t for t in range(p) if Hm(t, p) == 0]
    c2 = chi(2, p)
    hg = all(chi(2 * t * (1 - t * t), p) == 1 for t in ts)
    h0 = hg and all(chi(1 - t, p) == 1 and chi(1 + t * t, p) == 1 for t in ts)
    h1 = hg and all(chi(1 - t, p) == c2 and chi(1 + t * t, p) == c2 for t in ts)
    return ts, hg, h0, h1

vieta_bad = []; n6 = 0; bad = []; met = [0, 0]
for p in PR:
    if D[p][2] != 6: continue
    n6 += 1
    ts, hg, h0, h1 = cong_hyp(p)
    ss = sorted({t * t % p for t in ts})
    pm_ = (1 - ss[0]) * (1 - ss[1]) * (1 - ss[2]) % p; pp_ = (1 + ss[0]) * (1 + ss[1]) * (1 + ss[2]) % p
    if pm_ != (-54) % p or pp_ != 8 % p: vieta_bad.append(p)
    if p % 4 == 1:
        met[0] += h0; met[1] += h1
        if (h0 or h1) and p % 24 != 1: bad.append(p)
check("5  prod(1 - s_i) = -54 and prod(1 + s_i) = 8 mod p at the three roots s_i = t^2 (%d primes with 6 roots)" % n6, not vieta_bad, str(vieta_bad[:3]))
check("5  no prime below %d meets the hypothesis of Proposition 4 without p = 1 mod 24 (%d/%d primes met it on branch 0/1)" % (LIMIT, met[0], met[1]), not bad, str(bad))
ts, hg, h0, h1 = cong_hyp(5251537)
check("5  p = 5251537 (= 1 mod 24) meets the hypothesis on branch 1 (and 0): all six g(t) squares, chi(1-t) = chi(1+t^2) = chi(2)", len(ts) == 6 and h1 and 5251537 % 24 == 1, "h0=%s h1=%s" % (h0, h1))

# ---------------------------------------------------------------- 5/10. large examples, original definition
def full_S(p):
    add = add_factory(p); P = (1, 1); T = (0, 0)
    m = 0; Q = None
    while True:
        m += 1; Q = add(Q, P)
        if Q is None: break
    S = [[], []]; N = [0, 0]; Q = None
    for k in range(m):
        for j in (0, 1):
            R = Q if j == 0 else add(Q, T)
            if R is None: continue
            t = (1 - R[0]) % p
            if Hm(t, p) == 0:
                N[j] += 1
                gv = 2 * t * (1 - t * t) % p
                if gv and pow(gv, (p - 1) // 2, p) == 1: S[j].append(k)
        Q = add(Q, P)
    return m, N, S

for p, j0, want in ((85453, 0, 8), (32237, 1, 8), (5251537, 1, 12)):
    m, N, S = full_S(p)
    check("10 p = %d (p mod 24 = %d): |S_{p,%d}| = %d  [m_p = %d, |N| = %s]" % (p, p % 24, j0, len(S[j0]), m, N), len(S[j0]) == want)
    if p == 5251537: print("     the twelve indices (branch 1):", S[1])

# ---------------------------------------------------------------- 9. parity obstruction and the dossier counts
LIM9 = 2000
act = [[], []]; par = {}
for p in PR:
    if p >= LIM9: break
    for j in (0, 1):
        S = D[p][1][j][1]
        if S:
            act[j].append(p)
            par[(p, j)] = {n % 2 for n in S}
anyact = {p for j in (0, 1) for p in act[j]}
counts = {}
obst_bad = 0; obst_cnt = 0
for j in (0, 1):
    pairs = list(itertools.combinations(act[j], 2)); nc = inc = 0
    for p, q in pairs:
        mp, mq = D[p][0], D[q][0]; d = math.gcd(mp, mq)
        if d > 1: nc += 1
        comp = sum(1 for a in D[p][1][j][1] for b in D[q][1][j][1] if (a - b) % d == 0)
        if comp == 0: inc += 1
        if p % 8 == 5 and q % 8 == 5 and len(par[(p, j)]) == 1 and len(par[(q, j)]) == 1 and par[(p, j)] != par[(q, j)]:
            obst_cnt += 1
            if comp != 0: obst_bad += 1
    counts[j] = (len(act[j]), len(pairs), nc, inc)
check("9  dossier counts below 2000: branch 0 (active, pairs, non-coprime, incompatible) = (17, 136, 62, 29); branch 1 = (19, 171, 66, 32); 28 active on some branch",
      counts[0] == (17, 136, 62, 29) and counts[1] == (19, 171, 66, 32) and len(anyact) == 28, str(counts) + " any=%d" % len(anyact))
check("9  pairs p, q = 5 mod 8 whose S-sets have single, different parities are incompatible (%d such pairs below 2000)" % obst_cnt, obst_bad == 0 and obst_cnt >= 1)
print("     149: m = %d, S_{149,0} = %s;   197: m = %d, S_{197,0} = %s" % (D[149][0], sorted(D[149][1][0][1]), D[197][0], sorted(D[197][1][0][1])))
print("     parities: 149 -> %s, 197 -> %s, gcd(m) = %d" % (par[(149, 0)], par[(197, 0)], math.gcd(D[149][0], D[197][0])))

print()
print("ALL CHECKS PASSED" if not fails else "FAILED: %s" % fails)
sys.exit(1 if fails else 0)
