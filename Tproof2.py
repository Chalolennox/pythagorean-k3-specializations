import sys, random, time
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from math import gcd
src=open('split23.py').read().split("P=(Fr(1),Fr(1));Q=P;pts={1:P}")[0]
exec(src)
def psi2(t): w2,w3,tc=comps(t); return -w2*tc*local(t,2)
def psi3(t): w2,w3,tc=comps(t); return w3*local(t,3)
def add(P,Q):
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2:
        if y1+y2==0:return None
        lam=(3*x1*x1-4*x1+2)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam+2-x1-x2
    return (x3,lam*(x1-x3)-y1)
def vp(q,p):
    q=Fr(q)
    if q==0: return 10**9
    n,d=q.numerator,q.denominator;k=0
    while n%p==0:n//=p;k+=1
    while d%p==0:d//=p;k-=1
    return k
P=(Fr(1),Fr(1));pts={1:P};Q=P
for n in range(2,121):
    Q=add(Q,P);pts[n]=Q
ok2=ok3=tot=0
for n in range(2,121):
    tp=1-2/pts[n][0];tot+=1
    ok2+= (vp(tp+1,2)>=4) if n%2 else ((vp(tp+7,2)>=6) if n%4==2 else (vp(tp-1,2)>=5))
    if n%3==0: ok3+= (vp(tp-1,3)==2*vp(Fr(n),3))
    else: ok3+= ((tp.numerator*pow(tp.denominator,-1,9))%9 in (2,5,8))
print("classes of t'_n:  2-adic %d/%d   3-adic %d/%d"%(ok2,tot,ok3,tot),flush=True)
random.seed(1)
ms=[k for k in range(1,40,2) if k%3]
def rnd(cls,mod,K):  # t = u/v, v=m^2 (m odd, prime to 3), t in the class cls mod `mod` (2-adic or 3-adic)
    for _ in range(200):
        m=random.choice(ms);v=m*m
        k=random.randint(-20,20)
        t=Fr(cls+mod*k,1) if False else None
        # choose t with denominator v: t = (c0 + mod*k)/v requires class of t; solve u = t*v
        t0=Fr(cls)
        u=(cls*v + mod*v*k)  # t=u/v = cls+mod*k  (integer representative); keep denominator v only formally
        t=Fr(cls+mod*k)
        if t in (0,1,-1): continue
        return t
t0=time.time()
print("local constancy of Psi_2 (integers t in the 2-adic classes; V=1 is a square):",flush=True)
for name,cls,mod in (("n odd:   t=-1 mod 16",-1,16),("n=2 mod 4: t=-7 mod 64",-7,64),("n=0 mod 4: t=1 mod 32",1,32)):
    vals=[]
    for _ in range(60):
        t=rnd(cls,mod,0)
        if t is None: continue
        vals.append(psi2(t))
    print("   %-26s Psi_2 values %s  (%.0fs)"%(name,sorted(set(vals)),time.time()-t0),flush=True)
print("local constancy of Psi_3:",flush=True)
for name,cls,mod in (("3|n: t=1 mod 9",1,9),("t=2 mod 9",2,9),("t=5 mod 9",5,9),("t=8 mod 9",8,9)):
    vals=[]
    for _ in range(60):
        t=rnd(cls,mod,0)
        if t is None: continue
        vals.append(psi3(t))
    print("   %-26s Psi_3 values %s  (%.0fs)"%(name,sorted(set(vals)),time.time()-t0),flush=True)
print("real factor, t<1:",sorted(set(local(Fr(random.randint(-300,99),random.randint(1,40)),0) for _ in range(200))),flush=True)
