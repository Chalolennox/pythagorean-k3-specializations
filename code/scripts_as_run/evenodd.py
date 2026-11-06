import sys, time
from fractions import Fraction as Fr
from sympy import primerange
def hval(r,p): return (r**6-6*r**5-15*r**4+100*r**3-189*r**2+162*r-54)%p
def orbit_hits(p):
    """returns (m, set of residues r in [1,m-1] with p | F_r) where m = ord(P mod p); P=(1,1) on y^2=x^3-2x^2+2x"""
    P=(1%p,1%p);Q=P;r=1;hits=[]
    while True:
        if hval(Q[0],p)==0: hits.append(r)
        # Q <- Q+P
        x1,y1=Q;x2,y2=P
        if x1==x2:
            if (y1+y2)%p==0: return r+1,hits          # Q + P = O  => order r+1
            lam=(3*x1*x1-4*x1+2)*pow(2*y1,-1,p)%p
        else: lam=(y2-y1)*pow(x2-x1,-1,p)%p
        x3=(lam*lam+2-x1-x2)%p
        Q=(x3,(lam*(x1-x3)-y1)%p);r+=1
def dens(p):
    m,hits=orbit_hits(p)
    if m%2==1:
        c=Fr(len(hits),m); return m,c,c
    ev=sum(1 for r in hits if r%2==0);od=len(hits)-ev
    return m,Fr(ev,m//2),Fr(od,m//2)
t0=time.time()
SE=SO=Fr(0);rows=[];checkpoints=[100,300,1000,3000,10000]
res={}
for p in primerange(5,10001):
    m,de,do=dens(p)
    SE+=de;SO+=do
    rows.append((p,m,de,do))
    if p in (97,293,997,2999,9973) or p>=9973:
        pass
    for cp in checkpoints:
        if p<=cp: res[cp]=(float(SE),float(SO))
print("time %.0fs"%(time.time()-t0))
for cp in checkpoints:
    e,o=res[cp];print("B=%5d : sum_even=%.5f  sum_odd=%.5f  R = %.6f"%(cp,e,o,e/o))
print("\nR(infinity,10000) = %.11f"%(float(SE/SO)))
pickle_rows=rows
import pickle;pickle.dump(rows,open('evenodd_rows.pkl','wb'))
