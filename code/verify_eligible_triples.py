#!/usr/bin/env python3
"""Finite checks behind the 'eligible-prime triple nonintersection' claim (PR #89 comments 7135709265, 7136747343).  Stdlib only.

Written by Claude (a language model), 24 November 2026; no human has checked it.  It does NOT prove the theorem and does not reproduce the Groebner
computation or the resultant factorization; it checks two consequences independently:

  Setting.  C: y^2 = x^3 - 2x^2 + 2x, t = 1 - x, H(t) = t^6 - 30 t^4 - 24 t^2 - 1, f(x) = H(1-x), g(t) = 2t(1-t^2).
  D = the 12 geometric points (x, y) of C with f(x) = 0.  Claim: D and D+D are disjoint (no d1 + d2 = d3 with d1,d2,d3 in D) over Qbar.

  Check 1 (characteristic 5, replaces 'Groebner basis [1] over GF(5)').  5 is a prime of good reduction (f squarefree mod 5, the cubic
  x(x^2-2x+2) has discriminant -4 != 0 mod 5), so the 12 points of D reduce to 12 distinct points of C(Fbar_5) and the group law commutes with
  reduction.  f mod 5 factors into two cubics, so D lies in C(F_{5^6}).  We build F_{5^6} (15625 elements), list D, and test every pair d1 + d2
  (including doubling and d2 = -d1).  If no sum lies in D, then D cap (D+D) is empty in characteristic 5 and hence, by reduction, in characteristic 0.

  Check 2 (F_p, all primes 7 <= p <= bound, plus given large primes).  A prime p is called ELIGIBLE at a root t of H if g(t) is a nonzero square
  mod p (the reading of 'eligible' used here; the extra condition that Y = x^3-2x^2+2x is a nonzero square is needed for the point to lie on C(F_p)).
  D_p = {(1-t, +-sqrt(Y)) : H(t) = 0, g(t) nonzero square, Y nonzero square}.  We count pairs (d1, d2) in D_p with d1 + d2 in D_p.
  Expected from the comments: the only primes with such a triple are 229, 609613, 1386618529213 (and none below 609613 except 229).
  The weaker reading (Y square only, g ignored) is also reported, because the answer depends on the definition.

Usage: python3 code/verify_eligible_triples.py [--quick | --bound N]    (default bound 700000; --quick = 20000).  Exit 0 iff every check passes.
"""
import random
import sys

random.seed(1)
ok_all = True


def check(name, cond):
    global ok_all
    print(("ok   " if cond else "FAIL ") + name)
    ok_all = ok_all and cond


def Hc(t):
    return t**6 - 30 * t**4 - 24 * t**2 - 1


def gc(t):
    return 2 * t * (1 - t * t)


def Yc(x):
    return x**3 - 2 * x * x + 2 * x


# ----------------------------------------------------------------------------- check 1: characteristic 5 over F_{5^6}
P5, M = 5, 6
Q5 = P5**M


def build_field():
    # elements are integers 0..5^6-1 (base-5 digits = coefficients); find z-multiplication by an irreducible g whose root z is primitive
    for tail in range(1, Q5):
        coeffs = [(tail // P5**i) % P5 for i in range(M)]  # z^6 = -(c0 + c1 z + ... + c5 z^5)... use z^6 = sum coeffs*z^i
        if coeffs[0] == 0:
            continue
        exp = [1]
        e = [1] + [0] * (M - 1)
        seen_one = False
        cur = e
        for _ in range(Q5 - 2):
            top = cur[-1]
            cur = [0] + cur[:-1]
            if top:
                cur = [(cur[i] + top * coeffs[i]) % P5 for i in range(M)]
            val = sum(cur[i] * P5**i for i in range(M))
            if val == 1:
                seen_one = True
                break
            exp.append(val)
        if not seen_one and len(exp) == Q5 - 1:
            # check next step returns to 1
            top = cur[-1]
            cur = [0] + cur[:-1]
            if top:
                cur = [(cur[i] + top * coeffs[i]) % P5 for i in range(M)]
            if sum(cur[i] * P5**i for i in range(M)) == 1:
                return exp
    raise RuntimeError("no primitive polynomial found")


def digits_add(a, b):
    r = 0
    m = 1
    for _ in range(M):
        r += ((a % P5 + b % P5) % P5) * m
        a //= P5
        b //= P5
        m *= P5
    return r


def digits_neg(a):
    r = 0
    m = 1
    for _ in range(M):
        r += ((-(a % P5)) % P5) * m
        a //= P5
        m *= P5
    return r


def check_char5():
    exp = build_field()
    log = {v: i for i, v in enumerate(exp)}
    N = Q5 - 1

    def mul(a, b):
        return 0 if a == 0 or b == 0 else exp[(log[a] + log[b]) % N]

    def inv(a):
        return exp[(-log[a]) % N]

    def add(a, b):
        return digits_add(a, b)

    def neg(a):
        return digits_neg(a)

    def sub(a, b):
        return add(a, neg(b))

    def const(n):
        return n % P5

    def powe(a, k):
        r = 1
        for _ in range(k):
            r = mul(r, a)
        return r

    def f_at(x):  # f(x) = H(1-x) in F_{5^6}
        t = sub(const(1), x)
        t2 = mul(t, t)
        t4 = mul(t2, t2)
        t6 = mul(t4, t2)
        # H = t^6 - 30 t^4 - 24 t^2 - 1 with 30 = 0, -24 = 1 mod 5
        return add(add(t6, mul(const(-24), t2)), const(-1))

    def Y_at(x):
        x2 = mul(x, x)
        return add(add(mul(x2, x), mul(const(-2), x2)), mul(const(2), x))

    roots = [x for x in range(Q5) if f_at(x) == 0]
    check("char 5: f has 6 distinct roots in F_{5^6}", len(roots) == 6)
    sqrt = {}
    for y in range(1, Q5):
        sqrt.setdefault(mul(y, y), []).append(y)
    D = []
    for x in roots:
        Y = Y_at(x)
        if Y == 0:
            continue
        for y in sqrt.get(Y, []):
            D.append((x, y))
    check("char 5: D has 12 distinct points in C(F_{5^6})", len(set(D)) == 12)
    Dset = set(D)
    two = const(2)

    def addpt(P, Q):
        (x1, y1), (x2, y2) = P, Q
        if x1 == x2:
            if add(y1, y2) == 0:
                return None
            lam = mul(add(add(mul(const(3), mul(x1, x1)), mul(const(-4), x1)), const(2)), inv(mul(two, y1)))
        else:
            lam = mul(sub(y2, y1), inv(sub(x2, x1)))
        x3 = sub(sub(add(mul(lam, lam), const(2)), x1), x2)
        y3 = neg(add(mul(lam, sub(x3, x1)), y1))
        return (x3, y3)

    # sanity: the group law keeps points on the curve
    sample = [addpt(a, b) for a in D for b in D]
    on = all(s is None or mul(s[1], s[1]) == Y_at(s[0]) for s in sample)
    check("char 5: group-law outputs lie on C", on)
    hits = [(a, b) for a in D for b in D if (s := addpt(a, b)) is not None and s in Dset]
    check("char 5: no d1 + d2 = d3 with d1, d2, d3 in D  (D cap (D+D) empty mod 5)", len(hits) == 0)
    inf = sum(1 for a in D for b in D if addpt(a, b) is None)
    print("     (pairs with d1 + d2 = O: %d of 144; these are the pairs d2 = -d1)" % inf)


# ----------------------------------------------------------------------------- check 2: F_p
def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i :: i] = bytearray(len(s[i * i :: i]))
    return [i for i in range(n + 1) if s[i]]


def pnorm(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def pmod(a, b, p):
    a = a[:]
    ib = pow(b[-1], -1, p)
    while len(a) >= len(b):
        c = a[-1] * ib % p
        sh = len(a) - len(b)
        for i in range(len(b)):
            a[sh + i] = (a[sh + i] - c * b[i]) % p
        a.pop()
        pnorm(a)
        if not a:
            break
    return a


def pmulmod(a, b, m, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return pmod(pnorm([c % p for c in r]), m, p)


def ppowx_shift(base, e, m, p):
    r = [1]
    b = base
    while e:
        if e & 1:
            r = pmulmod(r, b, m, p)
        b = pmulmod(b, b, m, p)
        e >>= 1
    return r


def pgcd(a, b, p):
    while b:
        a, b = b, pmod(a, b, p)
    ia = pow(a[-1], -1, p)
    return [c * ia % p for c in a]


def f_coeffs():
    # coefficients of f(x) = H(1-x), integer list low to high
    H = [-1, 0, -24, 0, -30, 0, 1]
    res = [0] * 7
    pw = [1]
    for c in H:
        for i, v in enumerate(pw):
            res[i] += c * v
        npw = [0] * (len(pw) + 1)
        for i, v in enumerate(pw):
            npw[i] += v
            npw[i + 1] -= v
        pw = npw
    return res


FC = f_coeffs()


def roots_mod_p(p):
    """Distinct roots in F_p of f (via gcd with x^p - x, then equal-degree splitting)."""
    f = pnorm([c % p for c in FC])
    if len(f) < 2:
        return []
    xp = ppowx_shift([0, 1], p, f, p)
    d = xp + [0] * (2 - len(xp))
    d[1] = (d[1] - 1) % p
    d = pnorm(d)
    G = f[:] if not d else pgcd(f, d, p)
    out = []

    def split(G):
        if len(G) == 1:
            return
        if len(G) == 2:
            out.append((-G[0]) * pow(G[1], -1, p) % p)
            return
        while True:
            a = random.randrange(p)
            h = ppowx_shift([a, 1], (p - 1) // 2, G, p)
            h = h + [0] * (1 - len(h))
            h[0] = (h[0] - 1) % p
            h = pnorm(h)
            if not h:
                continue
            A = pgcd(G, h, p)
            if 1 < len(A) < len(G):
                break
        # quotient G / A
        q = []
        r = G[:]
        ia = pow(A[-1], -1, p)
        q = [0] * (len(G) - len(A) + 1)
        for k in range(len(q) - 1, -1, -1):
            c = r[k + len(A) - 1] * ia % p
            q[k] = c
            for i in range(len(A)):
                r[k + i] = (r[k + i] - c * A[i]) % p
        pnorm(q)
        split(A)
        split(q)

    split(G)
    return sorted(set(out))


def sqrt_mod(a, p):
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def triples(p, require_g):
    """(|D_p|, number of ordered pairs (d1,d2) in D_p with d1 + d2 in D_p)."""
    D = []
    for x in roots_mod_p(p):
        t = (1 - x) % p
        if require_g and (gc(t) % p == 0 or pow(gc(t) % p, (p - 1) // 2, p) != 1):
            continue
        y = sqrt_mod(Yc(x), p)
        if y is None or y == 0:
            continue
        D += [(x, y), (x, (-y) % p)]
    S = set(D)
    cnt = 0
    for a in D:
        for b in D:
            (x1, y1), (x2, y2) = a, b
            if x1 == x2:
                if (y1 + y2) % p == 0:
                    continue
                lam = (3 * x1 * x1 - 4 * x1 + 2) * pow(2 * y1, -1, p) % p
            else:
                lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
            x3 = (lam * lam + 2 - x1 - x2) % p
            y3 = (-(lam * (x3 - x1) + y1)) % p
            if (x3, y3) in S:
                cnt += 1
    return len(D), cnt


def check_Fp(bound):
    hits_g, hits_Y = [], []
    for p in primes_upto(bound):
        if p < 7:
            continue
        n, c = triples(p, True)
        if c:
            hits_g.append((p, n, c))
        n, c = triples(p, False)
        if c:
            hits_Y.append((p, n, c))
    print("     eligible reading (g square, Y square): primes <= %d with a triple: %s" % (bound, hits_g))
    print("     weaker reading (Y square only):        primes <= %d with a triple: %s" % (bound, hits_Y))
    expected = [229] + ([609613] if bound >= 609613 else [])
    check("F_p: eligible triples occur exactly at %s up to %d" % (expected, bound), [h[0] for h in hits_g] == expected)
    for big in (609613, 1386618529213):
        n, c = triples(big, True)
        check("F_p: p = %d has eligible triples (|D_p| = %d, ordered pairs = %d)" % (big, n, c), c > 0)


if __name__ == "__main__":
    bound = 700000
    if "--quick" in sys.argv:
        bound = 20000
    if "--bound" in sys.argv:
        bound = int(sys.argv[sys.argv.index("--bound") + 1])
    check_char5()
    check_Fp(bound)
    print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
    sys.exit(0 if ok_all else 1)
