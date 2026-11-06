import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from math import gcd
from sympy import isprime, factorint
exec(open('eps.py').read().split('if __name__')[0])   # jac, triple, pieces, W2 ... Fs
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
P=(Fr(1),Fr(1));Q=P;pts={1:P}
for n in range(2,10):
    Q=add(Q,P);pts[n]=Q
# complete factorizations of the part of |F| prime to 6 (from the earlier sessions; each is re-verified below)
known={
 ('nP',2):[23,4241],
 ('nP',3):[307,7743563],
 ('nP',4):[4372373,146767982243],
 ('nP',7):[2479847,6272027,346414885467478394713,1504836637469463028067],
 ('nP',8):[23,541,55102940955616303821050453,1962865819290420917439766320759157138315321],
 ('nP',9):[599,27269502419,941088050120417071,505725298418800171,949422469729513196700385704989772978754361],
 ('T',7):[23,62653,238858259,210834378622780780591,138886167672809043791],
 ('T',8):[181,8456963754372181,1143775645981565351,47753800121867236572402232971235631],
 ('T',9):[83,412824010409,472497673951447,100417459941548449040182946403104515552059185634197047726873909],
}
def partial(n,kind,smalls):
    t=1-pts[n][0]
    if kind=='T': t=(t+1)/(t-1)
    N=Fs(t.numerator,t.denominator);N=abs(N)
    while N%2==0:N//=2
    while N%3==0:N//=3
    for p in smalls:
        assert N%p==0
        N//=p
    return list(smalls)+[N]
known[('nP',5)]=partial(5,'nP',[2851,12281])
known[('nP',6)]=partial(6,'nP',[631,6907,69736487])
def N6(m):
    m=abs(m)
    while m%2==0:m//=2
    while m%3==0:m//=3
    return m
def tval(n,kind):
    t=1-pts[n][0]
    if kind=='T': t=(t+1)/(t-1)
    return t
def leg(a,p):
    a%=p
    return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)
rows=[]
for kind in ('nP','T'):
    for n in range(2,10):
        t=tval(n,kind);N=N6(Fs(t.numerator,t.denominator))
        key=(kind,n)
        if key in known: fac=known[key]
        else:
            fac=sorted(factorint(N))
            e=factorint(N)
            assert all(v==1 for v in e.values())
        prod=1
        for p in fac: prod*=p
        ok=(prod==N) and all(isprime(p) for p in fac)
        a,b,c=triple(t)
        f,s_j,_=pieces(t)
        s=sum(1 for p in fac if leg(a*b,p)==1)       # split primes
        W=f*(-1)**s
        eps=f*jac(a*b,N)                              # exact definition of eps
        delta=(-1)**len(fac)
        pred=(1 if (n%6 in (0,1,5)) else -1) if kind=='nP' else (1 if n%3==0 else -1)
        rows.append((kind,n,len(str(N)),len(fac),ok,f,s,W,eps,pred,delta,eps*delta))
print("Complete factorizations verified (product = F'', all factors probable primes) and the one-bit decomposition W = eps * delta")
print("kind  n digits omega  f   s   W  eps  pred  delta  eps*delta")
for r in rows:
    kind,n,d,om,ok,f,s,W,eps,pred,delta,ed=r
    print(f"{kind:<4} {n:>2} {d:>5} {om:>4}  {f:+d}  {s:d}  {W:+d}  {eps:+d}   {pred:+d}   {delta:+d}   {ed:+d}   fact_ok={ok}  W==eps*delta:{W==ed}  eps==pred:{eps==pred}")
