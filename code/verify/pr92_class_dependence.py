#!/usr/bin/env python3
"""Does the constant C depend on the residue class of p?  (PR #92 sieve dimension.)  Stdlib only.

Written by Claude (a language model), 26 November 2026; no human has checked it.  Observed numerics only; no claim about Problem H.
Motivation: Q(J[8]) contains Q(zeta_8), hence sqrt(2), and the eligibility condition involves chi(2) = (2/p); this could correlate eligibility with the 2-adic structure of J(F_p).
For primes 10007 <= p <= B with an eligible point, compares sum a_p/d_p with the expectation sum |D_p^+|/#J(F_p) under uniformity (the two have the same mean when C = 1), where #J(F_p)
is the unique multiple of d_p in the Hasse interval (primes with an ambiguous order are skipped), split by p mod 4, 8, 16, with bootstrap errors.  Usage: python3 code/verify/pr92_class_dependence.py [B]  (B = 1000000: about 80 s)
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
B = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v
import pr92_sieve_second_moment as sm
rec=[]  # (p, a/d, |D+|/N)
skipped=0
for p in v.primes_upto(B):
    if p<10007 or p==23: continue
    allp,elig=sm.points(p)
    if not elig: 
        continue
    add,neg,mul=sm.group(p); P=(1,1); L=math.isqrt(4*p)+6; cur=P; E=set(elig); hits=0; d=None
    for n in range(1,L+1):
        if cur is None: d=n;break
        if cur in E: hits+=1
        cur=add(cur,P)
    if d is None:
        d=sm.order_bsgs(p,P,add,neg,mul); hits=sum(1 for e in elig if sm.dlog(P,d,e,add,neg,mul) is not None)
    lo=p+1-math.isqrt(4*p)-1; hi=p+1+math.isqrt(4*p)+1
    cands=[m for m in range((lo+d-1)//d*d,hi+1,d)]
    if len(cands)!=1: skipped+=1; continue
    rec.append((p,hits/d,len(elig)/cands[0]))
print("primes used",len(rec),"skipped (ambiguous N)",skipped)
def ratio(rs):
    a=sum(r[1] for r in rs); b=sum(r[2] for r in rs); return a/b if b else float('nan'),a,b
print("overall ratio %.3f (sumA %.4f sumD %.4f)"%ratio(rec))
random.seed(1)
for m in (4,8,16):
    print("mod",m)
    for c in range(1,m,2):
        rs=[r for r in rec if r[0]%m==c]
        R,a,b=ratio(rs)
        # bootstrap error
        bs=[]
        for _ in range(200):
            s=[random.choice(rs) for _ in rs]; bs.append(ratio(s)[0])
        mu=sum(bs)/len(bs); sd=(sum((x-mu)**2 for x in bs)/len(bs))**.5
        print("  p=%d: n=%d ratio %.3f +- %.3f"%(c,len(rs),R,sd))
