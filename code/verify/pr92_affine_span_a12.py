#!/usr/bin/env python3
"""Independent check of the a_12 factorization and affine-span rank in
notes/MULTIPLICATION_BLOCK_AFFINE_SPAN.md and the factor facts in notes/COMPLETE_PROPAGATION_GRID_CLOSURE.md (PR #92).

Written by Claude (a language model), independent of the PR author's scripts.
No human has checked it.  Stdlib only, exact integer/Fraction arithmetic.  Runtime: under 5 seconds.

CHECKS
 (1) 12P on y^2=x^3-2x^2+2x, P=(1,1): t=1-x(12P)=u/v, N=|u^6-30u^4v^2-24u^2v^4-v^6| with all 2s,3s removed
     equals the product of the seven listed factors; the Legendre symbols of 2uv(v^2-u^2) mod each factor
     (Euler criterion) are -1,+1,+1,-1,-1,+1,-1, so qualifying factors are 83, 18397, the 19-digit one => a_12=1.
 (2) Deterministic Miller-Rabin for the six factors < 2^64.  The 119-digit factor gets only strong-probable-prime
     tests (12 bases): NOT a proof (the owner's Magma proof run is not reproduced here).
 (3) Rank over F_2 of the 5x5 augmented matrix built from a_1..a_9, b_1..b_9 (as recorded in the note) and a_12=w, a_18=z,
     for all four (w,z): expected ranks 4,4,5,5 for (w,z)=(0,0),(0,1),(1,0),(1,1).
 (4) For L=336737496728799825909507413201: L-1 equals the stated factorisation, each factor is prime (MR),
     and 15 is a Lucas/Pocklington witness (15^(L-1)=1 mod L, gcd(15^((L-1)/q)-1,L)=1 for every prime q|L-1).
DOES NOT CHECK: the recorded a_1..a_9, b_1..b_9 themselves (their raw log is not in the repository), a_18,
primality of the 119-digit factor, any Magma output, resultants or the Legendre table of the grid-closure note.
"""
from fractions import Fraction as F
from math import gcd

def add(A, B):
    if A is None: return B
    if B is None: return A
    x, y = A; u, v = B
    if x == u and y == -v: return None
    l = (3*x*x-4*x+2)/(2*y) if A == B else (v-y)/(u-x)
    z = l*l+2-x-u
    return z, l*(x-z)-y

def mr(n, bases=(2,3,5,7,11,13,17,19,23,29,31,37)):
    if n < 2: return False
    for p in bases:
        if n % p == 0: return n == p
    d, s = n-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def rank2(rows):
    rows = [r[:] for r in rows]; rk = 0; ncol = len(rows[0])
    for c in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][c]:
                rows[i] = [x ^ y for x, y in zip(rows[i], rows[rk])]
        rk += 1
    return rk

P = (F(1), F(1)); Q = None
for _ in range(12): Q = add(Q, P)
t = 1 - Q[0]; u, v = t.numerator, t.denominator
N = abs(u**6 - 30*u**4*v**2 - 24*u**2*v**4 - v**6)
for p in (2, 3):
    while N % p == 0: N //= p
ps = [23, 83, 18397, 7851197, 172604961553, 3022285517285783321,
      63444875642234219830688037601870240082732857828883494817671516344727361247789078750329402859044190800003740275757566803]
prod = 1
for p in ps: prod *= p
print("(1) product of 7 listed factors == N:", prod == N)
w = 2*u*v*(v*v-u*u)
sg = [(1 if pow(w % p, (p-1)//2, p) == 1 else -1) for p in ps]
print("    Legendre signs:", sg, "match:", sg == [-1,1,1,-1,-1,1,-1])
print("    qualifying:", [p for p, s in zip(ps, sg) if s == 1], "=> a_12 =", len([1 for s in sg if s==1]) % 2)
print("(2) MR deterministic-range (<2^64) factors prime:", [mr(p) for p in ps[:6]], "all<2^64:", all(p < 2**64 for p in ps[:6]))
print("    119-digit factor strong-probable-prime (NOT a proof):", mr(ps[6]), "digits:", len(str(ps[6])))
a = [0,1,1,1,1,0,0,1,0]; b = [0,0+1,0,1,0,1,0,1,1]
a = dict(zip(range(1,10), a)); b = dict(zip(range(1,10), [0,1,0,1,0,1,0,1,1]))
for wv in (0, 1):
    for z in (0, 1):
        A = dict(a); A[12] = wv; A[18] = z
        rows = [[1, A[1], A[2], A[3], A[6]], [1, b[1], A[2], b[3], A[6]],
                [1, A[2], A[4], A[6], A[12]], [1, A[3], A[6], A[9], A[18]],
                [1, b[3], A[6], b[9], A[18]]]
        print("(3) (a12,a18)=(%d,%d) rank F2 = %d" % (wv, z, rank2(rows)))
L = 336737496728799825909507413201
fs = [2,2,2,2,5,5,11,19,179,761,8573,3449170715522251]
m = 1
for f in fs: m *= f
print("(4) L-1 factorisation product ok:", m == L-1, " factors prime:", all(mr(f) for f in set(fs)), " L prime(MR):", mr(L))
print("    15^(L-1)==1:", pow(15, L-1, L) == 1, " gcd conditions:", all(gcd(pow(15, (L-1)//q, L)-1, L) == 1 for q in set(fs)))
