#!/usr/bin/env python3
"""Running sums  sum_p |S_{p,j}|/m_p  and  sum_p |N_{p,j}|/m_p  over primes 5 <= p <= LIMIT, j = 0, 1.

Usage:  python3 code/support_density_sum.py LIMIT [OUTFILE]      (stdlib only)
Input:  primes p <= LIMIT.  For each p the orbit nP (n = 1..m_p - 1) is walked once; the branch-1 point is
        nP + T with x(nP + T) = 2/x(nP).  N_{p,j}: H(t) = 0; S_{p,j}: in addition g(t) is a nonzero square
        (definitions in notes/REVIEW_2026-11-22_support_structure_proved.md).
Output: one line per checkpoint (p <= 500, 1000, 2000, 5000, 10000, 15000, 20000, 30000) with the cumulative sums,
        the number of active primes (S non-empty) and the largest |S| seen; recorded in data/support_sum_30000.txt.
Runtime: about 35 seconds for LIMIT = 30000.
The sum of |S|/m is a heuristic quantity (the expected number of indices n in a random residue class that
qualify at p); no theorem is claimed.  Derived with a language model; no human check."""
import sys, math
LIM=int(sys.argv[1])
OUT=sys.argv[2] if len(sys.argv)>2 else 'support_sum_%d.txt'%LIM
def primes(n):
    s=bytearray([1])*(n+1);s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]:
            s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
def Hm(t,p):
    t2=t*t%p
    return (t2*t2%p*t2-30*t2*t2-24*t2-1)%p
def gq(t,p):
    gv=2*t*(1-t*t)%p
    return gv!=0 and pow(gv,(p-1)//2,p)==1
out=open(OUT,'w')
cum=[0.0,0.0]; cumN=[0.0,0.0]; mxS=[0,0]; act=[0,0]
checkpoints=[500,1000,2000,5000,10000,15000,20000,30000]
cp=iter(checkpoints); nxt=next(cp)
for p in primes(LIM):
    if p<5: continue
    # orbit of P=(1,1)
    x,y=1,1; n=1
    S=[[],[]]; N=[0,0]
    while True:
        # point nP=(x,y) affine
        t=(1-x)%p
        if Hm(t,p)==0:
            N[0]+=1
            if gq(t,p): S[0].append(n)
        if x!=0:
            x1=2*pow(x,-1,p)%p; t1=(1-x1)%p
            if Hm(t1,p)==0:
                N[1]+=1
                if gq(t1,p): S[1].append(n)
        # next point: add P
        if x==1:
            if (y+1)%p==0: break          # nP = -P => (n+1)P=O
            lam=(3*x*x-4*x+2)*pow(2*y,-1,p)%p
        else:
            lam=(1-y)*pow(1-x,-1,p)%p
        x3=(lam*lam+2-x-1)%p; y3=(-y+lam*(x-x3))%p
        x,y=x3,y3; n+=1
    m=n+1
    for j in (0,1):
        # each index n in 1..m-1 visited once; n and -n both visited separately
        cum[j]+=len(S[j])/m
        cumN[j]+=N[j]/m
        mxS[j]=max(mxS[j],len(S[j]))
        if S[j]: act[j]+=1
    if p>=nxt:
        out.write('p<=%d cum|S0|/m=%.5f cum|S1|/m=%.5f cum|N0|/m=%.5f cum|N1|/m=%.5f active=%s maxS=%s\n'%(p,cum[0],cum[1],cumN[0],cumN[1],act,mxS)); out.flush()
        try: nxt=next(cp)
        except StopIteration: nxt=10**9
out.write('final %s %s %s %s act=%s maxS=%s\n'%(LIM,cum,cumN,'',act,mxS))
out.close()
