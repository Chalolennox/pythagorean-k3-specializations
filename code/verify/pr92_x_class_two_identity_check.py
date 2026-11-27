#!/usr/bin/env python3
"""Check of the exact identity behind  x_j = 2 mod K*^2  (Addendum 19).

Setting: H(t)=t^6-30t^4-24t^2-1, h(x)=H(1-x), roots x_j=1-t_j, t_j^2=w_j, m(w)=w^3-30w^2-24w-1, f(x)=x^3-2x^2+2x=x((x-1)^2+1).
Claim: for each root x of h with partner x'=2-x (t -> -t), and with s(w)=w^2-29w-26,
   2x = -6 * ( t s(w) / (9 y') )^2,   y'^2 = f(x'),
and  (prod_a y_a)^2 = -3456 = -6*24^2, so  -6 = (prod_a y_a/24)^2.  Hence 2x is a square in K.

Part 1 (exact, Fractions):  w s(w)^2 = 27(w^2-1) in Q[w]/(m);  h(0) = -54;  m(-1) = -8;  prod f(x_j) = -3456.
Part 2 (mod p): for every prime p<=BOUND completely split in K (h splits, all f(x_j) squares) test the displayed square-root formula,
   and chi(x_j) = chi(2) for p=1 mod 4 (and any p).
Usage: python3 -I pr92_x_class_two_identity_check.py [BOUND]
"""
import sys, os, random
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pr92_kummer_lattice_scan import h_splits, roots_of, Hc
from pr92_p_divisibility_scan import small_primes

def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def red_m(a):               # reduce mod w^3 = 30w^2+24w+1
    a = a[:]
    while len(a) > 3:
        c = a.pop(); n = len(a)
        a[n - 1] += 30 * c; a[n - 2] += 24 * c; a[n - 3] += c
    return a + [0] * (3 - len(a))
def peval(c, x): return sum(ci * x ** i for i, ci in enumerate(c))

def part1():
    s = [-26, -29, 1]
    lhs = red_m(pmul([0, 1], pmul(s, s)))
    rhs = [F(-27), F(0), F(27)]
    assert lhs == rhs, (lhs, rhs)
    print("OK  w*s(w)^2 = 27(w^2-1) in Q[w]/(w^3-30w^2-24w-1), s=w^2-29w-26  (coefficients", [int(x) for x in lhs], ")")
    h0 = peval(Hc, 0); assert h0 == -54; print("OK  h(0) = -54")
    m = lambda w: w ** 3 - 30 * w * w - 24 * w - 1
    assert m(-1) == -8; print("OK  m(-1) = -8, so prod_k (1+w_k) = 8 and prod over the six roots of (1+t^2) = 64")
    assert -54 * 64 == -3456 == -6 * 24 ** 2; print("OK  prod_j f(x_j) = prod x_j * prod(1+w_j) = -54*64 = -3456 = -6*24^2")

def leg(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
def sqrt_any(a, p):         # Tonelli-Shanks
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

def part2(B):
    sp = small_primes(int(B ** 0.5) + 2)
    seg = bytearray([1]) * (B + 1)
    for q in sp:
        if q * q <= B: seg[q * q::q] = bytearray(len(seg[q * q::q]))
    n = 0; nviol = 0; stats = {}
    for p in range(101, B + 1):
        if not seg[p]: continue
        if not h_splits(p): continue
        xs = roots_of(Hc[:], p, random.Random(p))
        if len(xs) != 6: continue
        fx = lambda x: (x * x * x - 2 * x * x + 2 * x) % p
        if any(fx(x) == 0 or leg(fx(x), p) != 1 for x in xs): continue
        n += 1
        ys = {x: sqrt_any(fx(x), p) for x in xs}
        prod = 1
        for x in xs: prod = prod * ys[x] % p
        r6 = prod * pow(24, -1, p) % p             # r6^2 = -6
        assert r6 * r6 % p == (-6) % p
        for x in xs:
            xp = (2 - x) % p; t = (1 - x) % p; w = t * t % p
            s = (w * w - 29 * w - 26) % p
            root = r6 * t % p * s % p * pow(9 * ys[xp], -1, p) % p
            if root * root % p != 2 * x % p: nviol += 1
            if leg(x, p) != leg(2, p): nviol += 1
        stats[p % 8] = stats.get(p % 8, 0) + 1
    print("OK  checked %d K-split primes 101<=p<=%d (by p mod 8: %s): square-root formula for 2x_j and chi(x_j)=chi(2) at all six x_j: %d violations" % (n, B, stats, nviol))
    return nviol

if __name__ == "__main__":
    part1()
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 3000000
    sys.exit(1 if part2(B) else 0)
