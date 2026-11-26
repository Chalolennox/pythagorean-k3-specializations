#!/usr/bin/env python3
"""Independent check for PR #92, notes/DE_BRUIJN_SYMBOLIC_CLOSURE.md.

Written by Claude (a language model), independent of the PR author's scripts.
No human has checked it. Standard library only, exact integer arithmetic.
Runtime: well under 1 second.

Checks (exactly):
 1. The index maps X (i->i+1 mod 4), Y (j->j+1 mod 4), S (swap i,j, toggle e) on
    n = 32k+16e+4j+i, for n in -64..95: X^4=Y^4=S^2=1, XY=YX, SXS=Y, and the
    orbit of 0 has size 32.
 2. The stated translation amounts: X = +P or -3P, Y = +4P or -12P,
    S = (16(1-2e)+3(i-j))P, as index shifts n -> n + shift.
 3. The balance count: over the 32 valid binary 4x4 de Bruijn arrays (from
    notes/DE_BRUIJN_TRANSFORMATION_GROUP.md, recomputed here by brute force over
    all 65536 arrays), every grid position has exactly 16 ones.
Does NOT check: any parity data, any action on the actual blocks B_n, the
elliptic-curve / Mordell-Lang statements, or anything about Problem H.
"""
import itertools

def split(n):
    k, r = divmod(n, 32)
    e, r = divmod(r, 16)
    j, i = divmod(r, 4)
    return k, e, j, i

def join(k, e, j, i): return 32*k + 16*e + 4*j + i
def X(n): k,e,j,i = split(n); return join(k,e,j,(i+1)%4)
def Y(n): k,e,j,i = split(n); return join(k,e,(j+1)%4,i)
def S(n): k,e,j,i = split(n); return join(k,1-e,i,j)

def pw(f, m, n):
    for _ in range(m): n = f(n)
    return n

R = range(-64, 96)
assert all(pw(X,4,n)==n and pw(Y,4,n)==n and S(S(n))==n for n in R)
assert all(X(Y(n))==Y(X(n)) for n in R)
assert all(S(X(S(n)))==Y(n) for n in R)
orb = {0}; fr = [0]
while fr:
    n = fr.pop()
    for f in (X,Y,S):
        m = f(n)
        if m not in orb: orb.add(m); fr.append(m)
assert len(orb) == 32 and orb == set(range(32)), len(orb)
for n in R:
    k,e,j,i = split(n)
    assert X(n)-n in (1,-3) and Y(n)-n in (4,-12)
    assert S(n)-n == 16*(1-2*e)+3*(i-j)

def valid(a):
    return len({tuple(a[((i+u)%4)*4+(j+v)%4] for u,v in [(0,0),(0,1),(1,0),(1,1)])
                for i in range(4) for j in range(4)}) == 16
V = [a for a in itertools.product(range(2), repeat=16) if valid(a)]
assert len(V) == 32
assert all(sum(a[p] for a in V) == 16 for p in range(16))
print("PASS: index action relations, orbit size 32, shift formulas on -64..95; "
      "32 valid arrays, 16 ones at each of the 16 positions")
