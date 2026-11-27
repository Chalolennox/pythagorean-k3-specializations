#!/usr/bin/env python3
"""Characters of the 16 quarter points of P at primes p = 1 mod 8 with J[2^m] rational.

For S with 4S = P (x-coordinate x) the owner's classes are d1 = x, d2 = x-1-i, d3 = d1*d2
(KUMMER_TWO_ADIC_EIGHTH_INTERSECTION.md).  Per prime we compute the Legendre characters
(chi(d1), chi(d2), chi(d3)) at all 16 quarter x-coordinates for both choices of i, and tabulate the sets of
vectors against d_p (the 2-adic divisibility depth of P).
Usage: pr92_quarter_characters.py primes_file MINM [--check]
"""
import sys, gzip, collections
sys.path.insert(0, __import__("os").path.dirname(__file__))
from pr92_p_divisibility_scan import make_ctx, halves

def chars(p, ctx, x, i):
    def ch(a):
        a %= p
        return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
    c1, c2 = ch(x), ch(x - 1 - i)
    return (c1, c2, c1 * c2)

if __name__ == "__main__":
    fn = sys.argv[1]; minm = int(sys.argv[2]) if sys.argv[2].isdigit() else 0
    if len(sys.argv) > 3 and sys.argv[3] == "--check":
        # replicate the owner's p = 557057 data
        p, i = 557057, 33793
        ctx = make_ctx(p)
        xs = sorted(x2 for x1 in halves(1, ctx) for x2 in halves(x1, ctx))
        owner = sorted([428778,165073,322336,436026,414355,94366,303611,249989,465492,28594,240403,431434,183370,480057,538146,231499])
        print("p=557057: my 16 quarter x-coordinates equal the owner's list:", xs == owner)
        print("characters at i=33793:", set(chars(p, ctx, x, i) for x in xs), " at -i:", set(chars(p, ctx, x, p - i) for x in xs))
        sys.exit(0)
    tab = collections.defaultdict(collections.Counter)
    n = 0
    for line in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        if line.startswith("#"): continue
        p, m, d = map(int, line.split())
        if m < minm: continue
        ctx = make_ctx(p); i = ctx[2]
        xs = [x2 for x1 in halves(1, ctx) for x2 in halves(x1, ctx)]
        assert len(xs) == 16
        s_plus = frozenset(chars(p, ctx, x, i) for x in xs)
        s_minus = frozenset(chars(p, ctx, x, p - i) for x in xs)
        key = (m >= 6, min(d, 3) if d >= 2 else d)
        tab[key][(tuple(sorted(s_plus)), tuple(sorted(s_minus)))] += 1
        n += 1
    print("primes with m_p >= %d: %d" % (minm, n))
    for key in sorted(tab):
        print("\n[m_p>=6: %s, depth d_p (3 means >=3): %d]  (%d primes)" % (key[0], key[1], sum(tab[key].values())))
        for (a, b), c in tab[key].most_common():
            print("   %5d primes: char sets for i: %s ; for -i: %s" % (c, list(a), list(b)))
