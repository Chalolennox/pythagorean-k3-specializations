import numpy as np, math
from sympy import primerange
def a_primes_short(a4,a6,M):
    """a_p = -sum_x chi(x^3+a4 x+a6) for all p<=M (valid at good and multiplicative primes of a model minimal at p)."""
    out={}
    for p in primerange(2,M+1):
        x=np.arange(p,dtype=np.int64)
        f=(x*x%p*x+(a4%p)*x+(a6%p))%p
        chi=np.zeros(p,dtype=np.int64)
        sq=(x*x)%p
        if p==2:
            chi[:]=0; chi[sq]=1
            out[p]=-int(np.sum(np.where(f==0,0,1)))*0 + (p - int(np.sum(1+np.where(np.isin(f,sq),1,-1)*(f!=0)+0*(f==0)))) if False else None
            # direct count for p=2
            cnt=sum(1 for xx in range(2) for yy in range(2) if (yy*yy-(xx**3+a4*xx+a6))%2==0)
            out[p]=p-cnt
            continue
        chi[sq]=1; chi=np.where(chi==1,1,-1); chi[0]=0
        out[p]=-int(np.sum(chi[f]))
    return out
def an_list(ap,N_bad,M):
    """a_n for n<=M from a_p; N_bad: dict p->conductor exponent (0 good; >=1 bad: a_p overridden by caller)"""
    a=[0]*(M+1);a[1]=1
    # multiplicative building via smallest prime factor
    spf=list(range(M+1))
    for i in range(2,int(M**0.5)+1):
        if spf[i]==i:
            for j in range(i*i,M+1,i):
                if spf[j]==j: spf[j]=i
    # prime powers first
    for n in range(2,M+1):
        p=spf[n]
        if p==n:
            a[n]=ap[p]
        else:
            m=n;pk=1
            while m%p==0: m//=p;pk*=p
            if m==1:
                # prime power p^k = n
                k=0;t=n
                while t>1:t//=p;k+=1
                chi=0 if N_bad.get(p,0)>0 else 1
                a[n]=ap[p]*a[n//p]-chi*p*(a[n//(p*p)] if k>=2 else 0)
            else:
                a[n]=a[pk]*a[m]
    return a
def sign_test(a,N,y=1.2):
    s=math.sqrt(N)
    g=lambda yy: sum(a[n]*math.exp(-2*math.pi*n*yy/s) for n in range(1,len(a)))
    g1=g(y);g2=g(1/y)
    return y*y*g1/g2 if abs(g2)>1e-14 else float('nan'),g1,g2
# ---------- validation on 11a (w=+1) and 37a (w=-1): general Weierstrass, brute force a_p
def ap_general(a1,a2,a3,a4,a6,M):
    out={}
    for p in primerange(2,M+1):
        cnt=0
        for x in range(p):
            for y in range(p):
                if (y*y+a1*x*y+a3*y-(x**3+a2*x*x+a4*x+a6))%p==0: cnt+=1
        out[p]=p-cnt
    return out
for name,coef,N,bad in (("11a",(0,-1,1,-10,-20),11,{11:1}),("37a",(0,0,1,-1,0),37,{37:1}),("14a",(1,0,1,4,-6),14,{2:1,7:1}),("389a",(0,1,1,-2,0),389,{389:1})):
    M=int(9*math.sqrt(N))+20
    ap=ap_general(*coef,M)
    a=an_list(ap,bad,M)
    for y in (1.2,1.5):
        r,g1,g2=sign_test(a,N,y)
        print(name,"y=%.1f"%y,"y^2 g(y)/g(1/y) =",round(r,6))
