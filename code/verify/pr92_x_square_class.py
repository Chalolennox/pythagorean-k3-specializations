#!/usr/bin/env python3
"""Square class of the six roots x_j of h modulo squares of K (primes completely split in K, p <= 3e6).  Stdlib only.
Written by Claude (a language model), 26 November 2026; no human has checked it.  Observation, not a proof; no claim about Problem H.
Expected: x_j is a square mod p iff p = 1, 7 mod 8, for all six j at once, i.e. x_j = 2 mod K*^2 (numerically); no prime with a mixed pattern.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.argv = [sys.argv[0]]
import verify_eligible_triples as v
def leg(a,p): return pow(a%p,(p-1)//2,p)
from collections import defaultdict
res=defaultdict(lambda:[0,0,0])  # p mod 8 -> [n, all squares, all nonsquares]
mixed=0
for p in v.primes_upto(3000000):
    if p<11 or p==23: continue
    r=v.roots_mod_p(p)
    if len(r)!=6 or any(leg(v.Yc(x),p)!=1 for x in r): continue
    s=[leg(x,p)==1 for x in r]
    k=res[p%8]; k[0]+=1
    if all(s): k[1]+=1
    elif not any(s): k[2]+=1
    else: mixed+=1
print(dict(res),"mixed",mixed)
