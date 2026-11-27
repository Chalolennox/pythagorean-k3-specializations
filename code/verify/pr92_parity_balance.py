#!/usr/bin/env python3
"""Parity balance of the finite coverage count X_B(n) = #{p <= B : n mod d_p in A_p} for n in [1, N].  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Observed numerics only; no claim about Problem H.
Compares the observed fraction of n with X_B(n) even with the independent-Bernoulli prediction (1 + prod_p (1 - 2 c_p)) / 2, and the fraction with X_B(n) = 0 with prod_p (1 - c_p),
where c_p is the exact fraction of n <= N covered by p (see pr92_sieve_second_moment.py for the setting).  The model parity bias prod (1 - 2 c_p) = (log B)^(-C + o(1)) decays only slowly.
Usage: python3 code/verify/pr92_parity_balance.py [B] [N]    (defaults 300000 1000000, about 20 s; '--quick' = 20000 200000)
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
B = int(args[0]) if len(args) > 0 else 300000
N = int(args[1]) if len(args) > 1 else 1000000
if "--quick" in sys.argv:
    B, N = 20000, 200000
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v, pr92_sieve_second_moment as sm
cnt=[0]*(N+1); prod1=1.0; prod2=1.0
rows=[]
marks=sorted({m for m in (10**3,10**4,10**5) if m<B}|{B}); mi=0
def report(cp):
    xs=cnt[1:]
    ev=sum(1 for x in xs if x%2==0)/N
    zero=sum(1 for x in xs if x==0)/N
    print("B=%-8d fraction even %.4f  model (1+prod(1-2c))/2 = %.4f   empty %.4f  model prod(1-c) = %.4f"%(cp,ev,(1+prod2)/2,zero,prod1),flush=True)
for p in v.primes_upto(B):
    if p<7: continue
    allp,elig=sm.points(p)
    if elig:
        add,neg,mul=sm.group(p); P=(1,1); L=math.isqrt(4*p)+6; cur=P; E=set(elig); hits=[]; d=None
        for n in range(1,L+1):
            if cur is None: d=n;break
            if cur in E: hits.append(n)
            cur=add(cur,P)
        if d is None:
            d=sm.order_bsgs(p,P,add,neg,mul); hits=[k for k in (sm.dlog(P,d,e,add,neg,mul) for e in elig) if k is not None]
        else: hits=[n for n in hits if n<d]
        if hits:
            h=0
            for a in set(hits):
                for n in range(a,N+1,d): cnt[n]+=1; h+=1
            c=h/N; prod1*=1-c; prod2*=1-2*c
    while mi<len(marks) and p>=marks[mi]-0: report(marks[mi]); mi+=1
report(B)
