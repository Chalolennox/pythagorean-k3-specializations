import numpy as np, math, sys
from fractions import Fraction as Fr
from sympy import primerange
def estimate(c, P_MAX=700, skip=(2,3,7,23)):
    num,den=Fr(c).numerator,Fr(c).denominator
    out=[];S=0.0;W=0.0
    for p in primerange(5,P_MAX):
        if p in skip or num%p==0 or den%p==0: continue
        cc=(num*pow(den,-1,p))%p
        t=np.arange(p,dtype=np.int64)
        inv=np.zeros(p,dtype=np.int64)
        den1=(1+t*t)%p
        ok=den1!=0
        inv[ok]=[pow(int(v),-1,p) for v in den1[ok]]
        A=((1-t*t)%p)*inv%p; B=(2*t%p)*inv%p
        Nc=(((cc**3-4*cc)%p)*t*t-16*t+(cc**3+4*cc))%p
        d=(den1*Nc)%p
        good=ok&(d!=0)
        a4=(4*A*d%p)*d%p                    # twist: y^2 = x^3 + 4A d^2 x - 8B d^3
        a6=(-8*B%p)*d%p*d%p*d%p
        x=np.arange(p,dtype=np.int64)
        x3=(x*x%p)*x%p
        sq=np.zeros(p,dtype=np.int64); sq[(x*x)%p]=1
        chi=np.where(sq==1,1,-1); chi[0]=0
        Ap=0
        for ti in np.nonzero(good)[0]:
            f=(x3+a4[ti]*x+a6[ti])%p
            Ap+= -int(chi[f].sum())
        # -A_p/p * log p  (rank estimate); bad fibres and t=infinity contribute O(1), negligible
        S+= (-Ap/p)*math.log(p); W+=math.log(p)
        out.append((p,S/W))
    return out
for c,name in ((Fr(2),"c=2 (proved geometric rank 1)"),(Fr(13,9),"c=13/9"),(Fr(-11,5),"c=-11/5"),(Fr(14,45),"c=14/45"),(Fr(1),"c=1"),(Fr(4),"c=4")):
    r=estimate(c)
    pts=[(p,v) for p,v in r if p in (101,211,307,401,499,601) or p==r[-1][0]]
    print("%-32s running estimate of the Q(t)-rank of the twist (primes up to p):"%name,[ (p,round(v,2)) for p,v in r if p>=100 and (p%100<12)][:7],"... final %.2f at p=%d"%(r[-1][1],r[-1][0]),flush=True)
