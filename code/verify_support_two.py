#!/usr/bin/env python3
"""Support-two review (2026-11-19): exact algebra and a scan of S_p, R_p, the isogeny index and the class A/B split.

C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), t(Q) = 1 - x(Q), H(t) = t^6 - 30t^4 - 24t^2 - 1.
R_p = {Q in C(F_p): H(t(Q)) = 0, (2t(1-t^2)/p) = +1}   (a union of +-pairs);
S_p = R_p intersected with <P mod p>.

Checks (all asserted):
  1. Exact (Fractions): disc H = 2^6 3^18 23^2, disc f = 3^9 23 (f = z^3-30z^2-24z-1), N(a(t)) = -2^8 3^6, N(d(t)) = -2^7 3^3, N(1-t) = N(1+t) = -54, N(1+t^2) = 64.
  2. Exact: phi_hat(P') = P for the 2-isogeny phi_hat: C' -> C, C': Y^2 = X^3 + 4X^2 - 4X, P' = (2,-4).
  3. For every prime 5 <= p < LIM: |{Q: delta(Q) trivial}| = N_p/2 (delta = x mod squares, delta(T) = 2),
     P lies in ker delta, hence m_p divides N_p/2 and the index [C(F_p):<P>] is even.
  4. Class B (|R_p| = 2, the root has chi(1-t) = -1) gives S_p = empty.
  5. Class A (|R_p| = 2, chi(1-t) = +1) with j_p = [ker delta : <P>] = 1 gives |S_p| = 2.
  6. p = 7 example: R_7 = {(5, +-1)}, S_7 = empty.
Prints the distributions.  Pure Python, standard library only; full run with LIM = 10000 takes about 6 seconds,
the default (LIM = 3000) about 1 second.   Usage: python3 verify_support_two.py [LIM]
Derived with a language model; no human check; no consequence for Problem H."""
import sys, collections
from fractions import Fraction as Fr

LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

# ---------- 1. exact algebra
def det(M):
    n = len(M); M = [[Fr(x) for x in r] for r in M]; d = Fr(1)
    for i in range(n):
        piv = next((r for r in range(i, n) if M[r][i] != 0), None)
        if piv is None: return Fr(0)
        if piv != i: M[i], M[piv] = M[piv], M[i]; d = -d
        d *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n): M[r][c] -= f * M[i][c]
    return d
def res(a, b):                      # Sylvester resultant, coefficient lists with highest degree first
    m, n = len(a) - 1, len(b) - 1; N = m + n; S = []
    for i in range(n): S.append([0] * i + a + [0] * (N - m - 1 - i))
    for i in range(m): S.append([0] * i + b + [0] * (N - n - 1 - i))
    return det(S)
def factor_small(n):
    n = abs(int(n)); out = {}
    for q in range(2, 100):
        while n % q == 0: out[q] = out.get(q, 0) + 1; n //= q
    assert n == 1, "unexpected large prime factor"
    return out
H  = [1, 0, -30, 0, -24, 0, -1];  dH = [6, 0, -120, 0, -48, 0]
f3 = [1, -30, -24, -1];           df3 = [3, -60, -24]
discH = (-1) ** (6 * 5 // 2) * res(H, dH)          # monic
discf = (-1) ** (3 * 2 // 2) * res(f3, df3)
assert factor_small(discH) == {2: 6, 3: 18, 23: 2}, factor_small(discH)
assert factor_small(discf) == {3: 9, 23: 1}, factor_small(discf)
# norms of the other radicands of L*: 1-t, 1+t (-> -54 = -2*3^3), 1+t^2 (-> 2^6): all {2,3}-units, so the Kummer layer of L* is unramified outside 2, 3
assert res(H, [-1, 1]) == -54 and res(H, [1, 1]) == -54 and res(H, [1, 0, 1]) == 64
# a(t) = 2t(1-t^2) = -2t^3 + 2t ; d(t) = (1-t)(1+t^2) = -t^3 + t^2 - t + 1   (H monic, so N = Res(H, .))
Na = res(H, [-2, 0, 2, 0]);  Nd = res(H, [-1, 1, -1, 1])
assert Na == -2 ** 8 * 3 ** 6, Na
assert Nd == -2 ** 7 * 3 ** 3, Nd
print("exact: disc H = 2^6 3^18 23^2, disc f = 3^9 23, N(a) = -2^8 3^6, N(d) = -2^7 3^3  =>  L ramified only at 2, 3, 23")

# ---------- 2. the dual 2-isogeny sends P' = (2,-4) to P = (1,1)   (Silverman III.4.5 with a'=4, b'=-4)
X, Y = Fr(2), Fr(-4)
assert Y * Y == X ** 3 + 4 * X * X - 4 * X
xx = Y * Y / (X * X); yy = Y * (-4 - X * X) / (X * X)       # point on y^2 = x^3 - 8x^2 + 32x
assert yy * yy == xx ** 3 - 8 * xx * xx + 32 * xx
x_C, y_C = xx / 4, yy / 8                                   # rescale to C: x = x''/4, y = y''/8
assert (x_C, y_C) == (1, 1)
print("exact: phi_hat(P') = P")

# ---------- scan
def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** .5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

def analyse(p):
    sq = bytearray(p);
    for x in range(1, p): sq[x * x % p] = 1
    chi = lambda v: 0 if v % p == 0 else (1 if sq[v % p] else -1)
    # points of C(F_p): affine points (x,y); count and delta-trivial count
    Np = 1; ker = 1                                          # the point at infinity
    for x in range(p):
        fx = (x * x * x - 2 * x * x + 2 * x) % p
        c = chi(fx); n_pts = 1 if fx == 0 else (2 if c == 1 else 0)
        Np += n_pts
        if x == 0:
            if chi(2) == 1: ker += n_pts                    # delta(T) = 2 mod squares
        elif chi(x) == 1: ker += n_pts
    # orbit of P
    def add(A, B):
        if A is None: return B
        if B is None: return A
        x1, y1 = A; x2, y2 = B
        if x1 == x2 and (y1 + y2) % p == 0: return None
        l = (3 * x1 * x1 - 4 * x1 + 2) * pow(2 * y1, -1, p) % p if A == B else (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (l * l + 2 - x1 - x2) % p
        return (x3, (l * (x1 - x3) - y1) % p)
    P = (1, 1); Q = P; xs = {1}; m = 1
    while True:
        Q = add(Q, P); m += 1
        if Q is None: break
        xs.add(Q[0])
    # roots of H
    roots = [t for t in range(p) if (pow(t, 6, p) - 30 * pow(t, 4, p) - 24 * t * t - 1) % p == 0]
    R = S = 0; info = []
    for t in roots:
        a = 2 * t * (1 - t * t) % p; d = (1 - t) * (1 + t * t) % p
        if a and d and chi(a) == 1 and chi(d) == 1:
            R += 2; inx = (1 - t) % p in xs
            S += 2 if inx else 0
            info.append((t, chi((1 - t) % p), inx))
    return Np, ker, m, R, S, info

cntS = collections.Counter(); cntR = collections.Counter(); jc = collections.Counter()
classB = classB_ok = classA = classA_j1 = classA_j1_ok = classA_in = 0
S2 = []; ex7 = None; minidx = 10 ** 9
for p in primes_upto(LIM):
    if p < 5: continue
    Np, ker, m, R, S, info = analyse(p)
    assert 2 * ker == Np, (p, Np, ker)                      # check 3: |ker delta| = N_p / 2
    assert (Np // 2) % m == 0                               # P in ker delta  =>  m_p | N_p/2
    j = Np // 2 // m; jc[j == 1] += 1; minidx = min(minidx, Np // m)
    cntS[S] += 1; cntR[R] += 1
    if S == 2: S2.append(p)
    if p == 7: ex7 = (R, S, info)
    if R == 2:
        t, c, inx = info[0]
        if c == -1:
            classB += 1; classB_ok += (S == 0); assert S == 0   # check 4
        else:
            classA += 1; classA_in += inx
            if j == 1:
                classA_j1 += 1; classA_j1_ok += (S == 2); assert S == 2   # check 5
assert ex7[0] == 2 and ex7[1] == 0                         # check 6
print("primes 5 <= p < %d: |S_p| distribution %s" % (LIM, sorted(cntS.items())))
print("|R_p| distribution %s" % sorted(cntR.items()))
print("|S_p| = 2 for %d primes: %s ..." % (len(S2), S2[:12]))
print("[C(F_p):<P>] always even (min index %d); j_p = 1 for %d of %d primes" % (minidx, jc[True], jc[True] + jc[False]))
print("class B (|R|=2, chi(1-t)=-1): %d primes, S_p empty for %d" % (classB, classB_ok))
print("class A (|R|=2, chi(1-t)=+1): %d primes, Q_p in <P> for %d; with j_p=1: %d primes, |S_p|=2 for %d" %
      (classA, classA_in, classA_j1, classA_j1_ok))
print("OK")
