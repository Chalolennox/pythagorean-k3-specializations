#!/usr/bin/env python3
"""Geometric (algebraic-closure) check of the claim 'D and D+D are disjoint in characteristic p' for small primes.  Stdlib only.

Written by Claude (a language model), 24 November 2026; no human has checked it.  It does NOT verify the Magma resultant computation of PR #89; it tests
its conclusion independently at small primes: for each prime p it builds F_{p^M} (M = splitting degree of f(x) = H(1-x), so every root of f lies in the field),
and decides whether some d1 + d2 = d3 exists among the 12 geometric points D = {(x, +-y): f(x) = 0} of C: y^2 = x^3 - 2x^2 + 2x.  Only x-coordinates are used,
so points with y outside the field are covered:
  * x1 != x2: with Delta = x2 - x1, A' = Y1 + Y2 + (2 - x1 - x2) Delta^2, a root x3 of f is the x-coordinate of d1 +- d2 iff (A' - x3 Delta^2)^2 = 4 Y1 Y2
    (the two signs of y1 y2 give the two values; both +-y3 lie in D, so only x3 matters);
  * x1 = x2 (doubling, Y != 0): 4 Y (x3 - 2 + 2 x1) = (3 x1^2 - 4 x1 + 2)^2.
Expected (from the PR #89 comments: candidate primes 7, 19, 23, 31, 71, 83, 229, ...): among the primes tested, geometric triples occur exactly at 7, 19, 31, 71, 83;
p = 23 (bad reduction, repeated root) is a candidate by discriminant but shows none here; every other tested prime shows none.
Usage: python3 code/verify_geometric_small_primes.py [--quick]   (--quick: fields up to 12769 elements; full run adds q up to 1.2 million, a few minutes)
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_eligible_triples as v

random.seed(7)
def lcm_deg(p):
    f=v.pnorm([c%p for c in v.FC]); L=1
    # brute-force the splitting degree: smallest M with all roots in F_{p^M}  (via x^(p^M) = x mod f' where f' squarefree part)
    # squarefree part
    def deriv(a): return v.pnorm([(i*a[i])%p for i in range(1,len(a))])
    g=v.pgcd(f,deriv(f),p) if deriv(f) else [1]
    sf=f
    if len(g)>1:
        # divide f by g
        q=[0]*(len(f)-len(g)+1); r=f[:]; ig=pow(g[-1],-1,p)
        for i in range(len(q)-1,-1,-1):
            c=r[i+len(g)-1]*ig%p; q[i]=c
            for j in range(len(g)): r[i+j]=(r[i+j]-c*g[j])%p
        sf=v.pnorm(q)
    cur=[0,1]
    for M in range(1,13):
        cur=v.ppowx_shift(cur,p,sf,p)
        if cur==[0,1]: return M
    return None
def build(p,M):
    q=p**M
    while True:
        co=[random.randrange(p) for _ in range(M)]; co[0]=co[0] or 1   # z^M = sum co[i] z^i
        exp=[0]*(q-1); cur=[1]+[0]*(M-1); seen=set(); good=True
        for k in range(q-1):
            code=sum(c*p**i for i,c in enumerate(cur))
            if k>0 and code==1: good=False;break
            exp[k]=code
            top=cur[-1]; cur=[0]+cur[:-1]
            if top: cur=[(cur[i]+top*co[i])%p for i in range(M)]
        if good and sum(c*p**i for i,c in enumerate(cur))==1: return exp
def analyse(p):
    M=lcm_deg(p); q=p**M
    exp=build(p,M); log={c:i for i,c in enumerate(exp)}; N=q-1
    def dig(a): return [(a//p**i)%p for i in range(M)]
    def undig(d): return sum(c*p**i for i,c in enumerate(d))
    def add(a,b): return undig([(x+y)%p for x,y in zip(dig(a),dig(b))])
    def neg(a): return undig([(-x)%p for x in dig(a)])
    def sub(a,b): return add(a,neg(b))
    def mul(a,b): return 0 if a==0 or b==0 else exp[(log[a]+log[b])%N]
    def inv(a): return exp[(-log[a])%N]
    def c(n): return n%p
    def sc(n,a): return mul(c(n),a)
    def pw(a,k):
        r=1
        for _ in range(k): r=mul(r,a)
        return r
    def fx(x):
        t=sub(1,x); t2=mul(t,t); t4=mul(t2,t2); t6=mul(t4,t2)
        return add(add(add(t6,sc(-30,t4)),sc(-24,t2)),c(-1))
    def Y(x): x2=mul(x,x); return add(add(mul(x2,x),sc(-2,x2)),sc(2,x))
    roots=sorted(x for x in range(q) if fx(x)==0)
    R=set(roots); hits=0; dbl=0
    for x1 in roots:
        for x2 in roots:
            if x1==x2:
                Yx=Y(x1)
                if Yx==0: continue
                lamn=add(add(sc(3,mul(x1,x1)),sc(-4,x1)),c(2))
                for x3 in roots:
                    # 4Y(x3-2+2x)=lamn^2
                    if mul(sc(4,Yx),add(sub(x3,c(2)),sc(2,x1)))==mul(lamn,lamn): dbl+=1
            else:
                D=sub(x2,x1); D2=mul(D,D)
                Ap=add(add(Y(x1),Y(x2)),mul(sub(sub(c(2),x1),x2),D2))
                rhs=sc(4,mul(Y(x1),Y(x2)))
                for x3 in roots:
                    L=sub(Ap,mul(x3,D2))
                    if mul(L,L)==rhs: hits+=1
    return M,q,len(roots),hits,dbl

CAND = {7, 19, 23, 31, 71, 83, 229, 797, 5087, 7351, 12113, 363773, 609613, 9624457993, 1386618529213, 49635479695149757}
EXPECT_TRIPLE = {7, 19, 31, 71, 83}
QUICK = [7, 11, 13, 17, 19, 23, 31, 47, 71, 83, 103, 113]
FULL = QUICK + [29, 53, 73, 89, 107]

if __name__ == "__main__":
    ok = True
    for p in (QUICK if "--quick" in sys.argv else FULL):
        M, q, nr, h, d = analyse(p)
        has = (h + d) > 0
        good = (has == (p in EXPECT_TRIPLE)) and (not has or p in CAND)
        ok = ok and good
        print(("ok   " if good else "FAIL ") + "p=%d M=%d q=%d distinct roots=%d triples(x1!=x2)=%d doubling=%d in candidate list: %s" % (p, M, q, nr, h, d, p in CAND), flush=True)
    print("ALL CHECKS PASSED" if ok else "SOME CHECK FAILED")
    sys.exit(0 if ok else 1)
