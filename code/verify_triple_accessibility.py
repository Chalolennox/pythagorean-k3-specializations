#!/usr/bin/env python3
"""Accessibility of the eligible triples: which F_p triples d1 + d2 = d3 in D_p^+ lie in the reductions of <P> and <P,T>?  Stdlib only.

Written by Claude (a language model), 24 November 2026; no human has checked it.  Setting and the definition of D_p^+ as in verify_eligible_triples.py
(H(1-x) = 0, g(1-x) a nonzero square mod p, point on C(F_p)).  P = (1,1), T = (0,0).  For a prime p the script finds ord(P) mod p by baby-step giant-step on the
Hasse interval (assuming ord(P) exceeds the interval width, which the discrete logs confirm), decides membership of each eligible point in <P> and in <P,T>
(= <P> union (<P> + T), T having order 2) by discrete logarithm, and counts the ordered triples inside each subgroup.
Expected: p = 229: 6 triples in D_p^+, none inside <P,T> (so 229 is not an exceptional prime of the theorem);
p = 609613: 6 triples, all inside <P>; p = 1386618529213: 6 triples, all inside <P,T>, none inside <P> (only 4 of the 6 eligible points lie in <P>).
Usage: python3 code/verify_triple_accessibility.py [--quick]   (--quick: 229 and 609613, a few seconds; full run adds 1386618529213, about 40 s)
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_eligible_triples as v

def mk(p):
    inv=lambda a:pow(a,-1,p)
    def add(A,B):
        if A is None: return B
        if B is None: return A
        x1,y1=A;x2,y2=B
        if x1==x2:
            if (y1+y2)%p==0: return None
            lam=(3*x1*x1-4*x1+2)*inv(2*y1)%p
        else: lam=(y2-y1)*inv(x2-x1)%p
        x3=(lam*lam+2-x1-x2)%p
        return (x3,(-(lam*(x3-x1)+y1))%p)
    def neg(A): return None if A is None else (A[0],(-A[1])%p)
    def mul(k,A):
        R=None
        while k:
            if k&1: R=add(R,A)
            A=add(A,A); k>>=1
        return R
    return add,neg,mul
def factor(n):
    f={};d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1 if d==2 else 2
    if n>1: f[n]=f.get(n,0)+1
    return f
def order(p,P,add,neg,mul):
    w=math.isqrt(4*p)+2; lo=p+1-w; hi=p+1+w
    s=math.isqrt(hi-lo)+1
    base={}
    A=None
    for j in range(s+1):
        base.setdefault(A,[]).append(j); A=add(A,P)   # jP
    G=mul(s,P)  # giant step
    cands=[]
    cur=mul(lo,P)
    for i in range(s+1):
        # cur = (lo+i*s)P ; want (lo+i*s + j... ) -> m = lo+i*s+j with cur + jP = O  => cur = -jP
        nc=neg(cur)
        if nc in base:
            for j in base[nc]: cands.append(lo+i*s+j)
        cur=add(cur,G)
    g=0
    for m in cands: g=math.gcd(g,m) if g else m
    n=g
    for q in factor(g):
        while n%q==0 and mul(n//q,P) is None: n//=q
    return n
def dlog(p,Pt,n,X,add,neg,mul):
    s=math.isqrt(n)+1
    baby={}; A=None
    for j in range(s):
        baby.setdefault(A,j); A=add(A,Pt)
    G=neg(mul(s,Pt)); cur=X
    for i in range(s+1):
        if cur in baby: return (i*s+baby[cur])%n
        cur=add(cur,G)
    return None
def analyse(p):
    add,neg,mul=mk(p)
    P=(1,1);T=(0,0)
    n=order(p,P,add,neg,mul)
    # eligible set
    D=[]
    for x in v.roots_mod_p(p):
        t=(1-x)%p; gg=v.gc(t)%p
        if gg==0 or pow(gg,(p-1)//2,p)!=1: continue
        y=v.sqrt_mod(v.Yc(x),p)
        if y in (None,0): continue
        D+=[(x,y),(x,(-y)%p)]
    inP={};inPT={}
    for d in D:
        a=dlog(p,P,n,d,add,neg,mul)
        if a is not None: inP[d]=a
        b=dlog(p,P,n,add(d,T),add,neg,mul)  # d+T = -? (T 2-torsion so d = aP + T iff d+T=aP)
        if a is not None or b is not None: inPT[d]=(a,b)
    S=set(D)
    trip=[(a,b,add(a,b)) for a in D for b in D if add(a,b) in S]
    tPT=[t for t in trip if all(z in inPT for z in t)]
    tP=[t for t in trip if all(z in inP for z in t)]
    print("     p=%d: ord(P)=%d, |D+|=%d, in <P>: %d, in <P,T>: %d, triples in D+: %d, inside <P,T>: %d, inside <P>: %d" % (p, n, len(D), len(inP), len(inPT), len(trip), len(tPT), len(tP)))
    return len(D), len(inP), len(inPT), len(trip), len(tPT), len(tP)

EXPECTED = {229: (4, 0, 0, 6, 0, 0), 609613: (4, 4, 4, 6, 6, 6), 1386618529213: (6, 4, 6, 6, 6, 0)}

if __name__ == "__main__":
    ok = True
    for p in ([229, 609613] if "--quick" in sys.argv else [229, 609613, 1386618529213]):
        got = analyse(p)
        good = got == EXPECTED[p]
        ok = ok and good
        print(("ok   " if good else "FAIL ") + "p=%d: (|D+|, in<P>, in<P,T>, triples, in<P,T>, in<P>) = %s, expected %s" % (p, got, EXPECTED[p]))
    print("ALL CHECKS PASSED" if ok else "SOME CHECK FAILED")
    sys.exit(0 if ok else 1)
