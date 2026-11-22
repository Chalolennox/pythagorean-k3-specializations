#!/usr/bin/env python3
"""Square-class ranks of the qualifying-root character field and the parity characters a_j + i.

Checks the statements of notes/REVIEW_2026-11-22_kummer_compositum.md:
  1  the resolvent R12(z) = H(z-i) H(z+i) = z^12 - 54 z^10 + 687 z^8 + 5130 z^6 + 8121 z^4 + 3348 z^2 + 64
  2  the exact identity s(a)^2 = 3 (a^4 - 1) mod H(a), s(a) = a (26 + 29 a^2 - a^4)/3, and prod (1 - s_j) = U(1) = -54
  3  finite-field character matrices over the primes p = 1 mod 4 that split H completely (48 compatible
     embeddings each: 6 orderings of the roots of U, 4 sign choices with a1 a2 a3 = 1, 2 choices of i):
       11 reduced generators of the old field F = L*:  rank 9, kernel masks 993, 1433, 1656
       with the three new classes [a_j + i]:             rank 12
       the 9 classes q_j, r_j^+, r_j^- (criterion without x): rank 9, still 9 after adding [2], 12 with [a_j + i]
  4  the 12-row certificate data/kummer_rank_certificate.txt (ranks 12 and 9)
  5  locus: odd weight of the six bits chi(a_j +- i) <=> p = 5 mod 8; primes completely split in the
     criterion field are 1 mod 8
  7  K5: at p = 1 mod 8 the characters chi(a_j + i) bound the support, |S_{p,j}| <= 4 (3 - w_j), on the 106 search cases
  6  single-root independence: over the degree-one primes of Q(a, i), the characters of
     g(a), 1 - a, 1 + a, 1 + a^2, 2 are independent and chi(a + i) is not a product of them

Generators (bit k of a mask), old field:  0: 2, 1: a1, 2: a2, 3: 1-a1, 4: 1+a1, 5: 1-a2, 6: 1+a2, 7: 1-a3,
8: 1+a3, 9: 1+a1^2, 10: 1+a2^2 (a1 a2 a3 = 1; bit = 1 iff the Legendre symbol is -1).

The rank of a finite-field matrix is a rigorous lower bound for the rank of the square-class group in M
(a relation over M would hold at every embedding); the upper bounds come from the exact identities.

Usage: python3 code/verify_kummer_compositum.py [--quick]     (stdlib only; --quick about 5 s, default about 30 s)
Derived with a language model; no human check."""
import sys, itertools, random
from fractions import Fraction as Fr

QUICK = "--quick" in sys.argv
LIM = 2000 if QUICK else 300000      # split primes used for the rank matrices (certificate primes are < 2000)
LIM6 = 5000 if QUICK else 20000
fails = []
def check(name, cond, info=""):
    print(("ok   " if cond else "FAIL ") + name + (("  " + info) if info else ""))
    if not cond: fails.append(name)

def primes(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, int(n ** .5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]
def chi(a, p):
    a %= p
    if a == 0: return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1
def rank(rows):
    b = {}
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in b: r ^= b[h]
            else: b[h] = r; break
    return len(b)
def kernel(rows, n):
    return [m for m in range(1, 1 << n) if all(bin(m & r).count("1") % 2 == 0 for r in rows)]

# ------------------------------------------------------------------ 1. R12 exactly (Gaussian integers as pairs)
def cm(x, y): return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def ca(x, y): return (x[0] + y[0], x[1] + y[1])
def pmulc(a, b):
    r = [(0, 0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] = ca(r[i + j], cm(x, y))
    return r
def Hshift(c):
    zc = [c, (1, 0)]; r = [(0, 0)]; pw = [(1, 0)]
    for co in [-1, 0, -24, 0, -30, 0, 1]:
        n = max(len(r), len(pw))
        r = [ca(r[i] if i < len(r) else (0, 0), (co * pw[i][0], co * pw[i][1]) if i < len(pw) else (0, 0)) for i in range(n)]
        pw = pmulc(pw, zc)
    return r
R = pmulc(Hshift((0, -1)), Hshift((0, 1)))
check("1  R12(z) = H(z-i) H(z+i) has the coefficients of the dossier",
      [c[0] for c in R] == [64, 0, 3348, 0, 8121, 0, 5130, 0, 687, 0, -54, 0, 1] and all(c[1] == 0 for c in R))

# ------------------------------------------------------------------ 2. exact identities
H = [Fr(-1), 0, Fr(-24), 0, Fr(-30), 0, Fr(1)]
def pmul(a, b):
    r = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def pmodH(a):
    a = [Fr(x) for x in a]
    while len(a) >= 7:
        c = a[-1]
        for k in range(7): a[len(a) - 7 + k] -= c * H[k]
        a.pop()
    return a + [Fr(0)] * (6 - len(a))
s_ = [0, Fr(26, 3), 0, Fr(29, 3), 0, Fr(-1, 3)]
check("2  s(a)^2 = 3 (a^4 - 1) modulo H(a)  (so -3(1 - a^4) is a square already in Q(a))", pmodH(pmul(s_, s_)) == pmodH([-3, 0, 0, 0, 3]))
U = lambda s: s ** 3 - 30 * s ** 2 - 24 * s - 1
check("2  prod (1 - s_j) = U(1) = -54 and prod (1 + s_j) = -U(-1) = 8", U(1) == -54 and -U(-1) == 8)

# ------------------------------------------------------------------ root finding mod p (as in code/search_support_twelve.py)
def red(a, p):
    a = a[:]
    for k in range(len(a) - 1, 2, -1):
        c = a[k]
        if c:
            a[k - 3] = (a[k - 3] + c) % p; a[k - 2] = (a[k - 2] + 24 * c) % p; a[k - 1] = (a[k - 1] + 30 * c) % p
        a.pop()
    while len(a) < 3: a.append(0)
    return [x % p for x in a]
def mul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] = (r[i + j] + x * y) % p
    return red(r, p)
def pw(base, e, p):
    r = [1, 0, 0]
    while e:
        if e & 1: r = mul(r, base, p)
        base = mul(base, base, p); e >>= 1
    return r
def trim(a):
    a = a[:]
    while a and a[-1] == 0: a.pop()
    return a
def pmod(a, b, p):
    a = trim(a); b = trim(b); inv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        c = a[-1] * inv % p; sh = len(a) - len(b)
        for i, x in enumerate(b): a[sh + i] = (a[sh + i] - c * x) % p
        a = trim(a)
    return a
def pdiv(a, b, p):
    a = trim(a); b = trim(b); inv = pow(b[-1], -1, p); q = [0] * (len(a) - len(b) + 1)
    while len(a) >= len(b):
        c = a[-1] * inv % p; sh = len(a) - len(b); q[sh] = c
        for i, x in enumerate(b): a[sh + i] = (a[sh + i] - c * x) % p
        a = trim(a)
    return q
def pgcd(a, b, p):
    a = trim(a); b = trim(b)
    while b: a, b = b, pmod(a, b, p)
    inv = pow(a[-1], -1, p); return [x * inv % p for x in a]
def roots_U(p):
    """the three roots of U(s) = s^3 - 30 s^2 - 24 s - 1 mod p if it splits completely, else None."""
    Cp = [(-1) % p, (-24) % p, (-30) % p, 1]
    if pw([0, 1, 0], p, p) != [0, 1, 0]: return None
    rts = []
    def split(f):
        if len(f) == 2: rts.append((-f[0]) % p); return
        while True:
            a = random.randrange(p)
            r = pw([a, 1, 0], (p - 1) // 2, p); r = [(r[0] - 1) % p, r[1], r[2]]
            if not any(r): continue
            g = pgcd(f, r, p)
            if 1 < len(g) < len(f):
                split(g); split(pdiv(f, g, p)); return
    split(Cp)
    return rts
def tonelli(a, p):
    q = p - 1; s = 0
    while q % 2 == 0: q //= 2; s += 1
    z = 2
    while chi(z, p) != -1: z += 1
    m = s; c = pow(z, q, p); t = pow(a, q, p); r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 0; tt = t
        while tt != 1: tt = tt * tt % p; i += 1
        b = pow(c, 1 << (m - i - 1), p); m = i; c = b * b % p; t = t * c % p; r = r * b % p
    return r
def sqrtm1(p):
    z = 2
    while chi(z, p) != -1: z += 1
    return pow(z, (p - 1) // 4, p)

def embeddings(p):
    """the 48 embeddings (a1, a2, a3, i) of M into F_p, for p = 1 mod 4 splitting H completely; else []."""
    if p % 4 != 1 or p < 29: return []
    rts = roots_U(p)
    if not rts or any(chi(x, p) != 1 for x in rts): return []
    i0 = sqrtm1(p); base = [tonelli(x, p) for x in rts]; out = []
    for perm in itertools.permutations(range(3)):
        a = [base[k] for k in perm]
        if a[0] * a[1] % p * a[2] % p != 1: a[2] = (-a[2]) % p
        for sg in ((1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)):
            A = [a[k] * sg[k] % p for k in range(3)]
            for ii in (i0, p - i0): out.append((A, ii))
    return out

def bits_old(p, A):
    gens = [2, A[0], A[1]] + [v for k in range(3) for v in (1 - A[k], 1 + A[k])] + [1 + A[0] ** 2, 1 + A[1] ** 2]
    return [0 if chi(v, p) == 1 else 1 for v in gens]
def bits_new(p, A, ii): return [0 if chi(A[k] + ii, p) == 1 else 1 for k in range(3)]
def mask(b, sh=0): return sum(x << (k + sh) for k, x in enumerate(b))

old = []; comb = []; q9 = []; q9two = []; q9new = []; nsplit = 0; weight = {}; crit_mod8 = {}
for p in primes(LIM):
    E = embeddings(p)
    if not E: continue
    nsplit += 1
    for A, ii in E:
        bo = bits_old(p, A); bn = bits_new(p, A, ii)
        old.append(mask(bo)); comb.append(mask(bo) | mask(bn, 11))
        gens = []
        for x in A: gens += [2 * x * (1 - x) * (1 + x) % p, (1 - x) * (1 + x * x) % p, (1 + x) * (1 + x * x) % p]
        b9 = [0 if chi(v, p) == 1 else 1 for v in gens]
        q9.append(mask(b9)); q9two.append(mask(b9) | (mask([0 if chi(2, p) == 1 else 1]) << 9)); q9new.append(mask(b9) | (mask(bn) << 9))
    A, ii = E[0]
    w = sum(0 if chi(A[k] + s * ii, p) == 1 else 1 for k in range(3) for s in (1, -1)) % 2
    weight.setdefault((w, p % 8), 0); weight[(w, p % 8)] += 1
    # locus: all six roots satisfy q, r squares?
    ok = all(chi(2 * y * (1 - y * y), p) == 1 and chi((1 - y) * (1 + y * y), p) == 1 for x in A for y in (x, (-x) % p))
    if ok: crit_mod8[p % 8] = crit_mod8.get(p % 8, 0) + 1
print("     split primes used: %d (p <= %d), rows %d" % (nsplit, LIM, len(old)))
check("3  old field, 11 reduced generators: rank 9", rank(old) == 9, "rank %d" % rank(old))
check("3  old kernel masks are exactly 993, 1433, 1656 (993 xor 1433 = 1656)", kernel(old, 11) == [993, 1433, 1656] and 993 ^ 1433 == 1656, str(kernel(old, 11)))
check("3  with the three classes [a_j + i]: rank 12", rank(comb) == 12, "rank %d" % rank(comb))
check("3  criterion classes q_j, r_j^+, r_j^- (9 generators): rank 9 (no relation); with [2]: still 9; with [a_j + i]: 12",
      rank(q9) == 9 and rank(q9two) == 9 and rank(q9new) == 12, "%d, %d, %d" % (rank(q9), rank(q9two), rank(q9new)))
check("5  weight parity of the six bits chi(a_j +- i) is odd exactly when p = 5 mod 8 (%s)" % dict(sorted(weight.items())),
      all((w == 1) == (m8 == 5) for (w, m8) in weight))
check("5  primes completely split in M(sqrt q, sqrt r) are 1 mod 8 (consequence of [2] being in the span: %d such primes up to %d; may be 0 at this range)" % (sum(crit_mod8.values()), LIM), set(crit_mod8) <= {1})

# ------------------------------------------------------------------ 4. the certificate file
rows = []; ok = True
try:
    for line in open("data/kummer_rank_certificate.txt"):
        if line.startswith("#") or not line.strip(): continue
        p, a1, a2, a3, i, m = map(int, line.split())
        Hm = lambda t: (pow(t, 6, p) - 30 * pow(t, 4, p) - 24 * t * t - 1) % p
        A = [a1, a2, a3]
        ok &= all(Hm(a) == 0 for a in A) and a1 * a2 * a3 % p == 1 and i * i % p == p - 1
        ok &= (mask(bits_old(p, A)) | mask(bits_new(p, A, i), 11)) == m
        rows.append(m)
    check("4  certificate: %d rows with consistent embeddings, rank %d on all 14 columns, rank %d on the first 11" % (len(rows), rank(rows), rank([r & 0x7FF for r in rows])),
          ok and len(rows) == 12 and rank(rows) == 12 and rank([r & 0x7FF for r in rows]) == 9)
except FileNotFoundError:
    check("4  certificate file present (run from the repository root)", False)

# ------------------------------------------------------------------ 6. single root, degree-one primes of Q(a, i)
Hm_ = lambda t, p: (pow(t, 6, p) - 30 * pow(t, 4, p) - 24 * t * t - 1) % p
rows6 = []
for p in primes(LIM6):
    if p < 5 or p % 4 != 1 or p == 23: continue
    i = sqrtm1(p)
    for t in range(p):
        if Hm_(t, p): continue
        vals = [chi(2 * t * (1 - t * t), p), chi(1 - t, p), chi(1 + t, p), chi(1 + t * t, p), chi(2, p)]
        if 0 in vals: continue
        for ii in (i, p - i):
            c = chi(t + ii, p)
            if c: rows6.append((tuple(0 if v == 1 else 1 for v in vals), 0 if c == 1 else 1))
ind = all(any(sum(r[0][k] for k in range(5) if m >> k & 1) % 2 == 1 for r in rows6) for m in range(1, 32))
notin = all(any((sum(r[0][k] for k in range(5) if m >> k & 1) + r[1]) % 2 == 1 for r in rows6) for m in range(32))
check("6  g(a), 1-a, 1+a, 1+a^2, 2 are independent and chi(a + i) is none of their 32 products (%d degree-one primes of Q(a,i), p <= %d)" % (len(rows6), LIM6), ind and notin)

# ------------------------------------------------------------------ 7. K5: |S| <= 4 (3 - w) on the search survivors
import re
try:
    cases = []
    for line in open("data/support_twelve_search_3e7.txt"):
        m = re.match(r"p=(\d+) .*branch (\d): .*\(\|S\|=(\d+)\)", line)
        if m: cases.append(tuple(map(int, m.groups())))
    bad = eq = 0; twelve = []
    for p, j, sz in cases:
        A, ii = embeddings(p)[0]
        c1 = chi(-(1 + ii), p); target = 1 if j == 0 else c1
        w = sum(1 for a in A if chi(a + ii, p) != target)
        bad += sz > 4 * (3 - w); eq += sz == 4 * (3 - w)
        if sz == 12: twelve.append((p, j, w))
    check("7  K5: |S_{p,j}| <= 4(3 - w_j) on the %d prime-branch cases of data/support_twelve_search_3e7.txt (%d equalities); the |S| = 12 case has w = 0: %s" % (len(cases), eq, twelve),
          len(cases) == 106 and bad == 0 and twelve == [(5251537, 1, 0)])
except FileNotFoundError:
    check("7  data/support_twelve_search_3e7.txt present (run from the repository root)", False)

print()
print("ALL CHECKS PASSED" if not fails else "FAILED: %s" % fails)
sys.exit(1 if fails else 0)
