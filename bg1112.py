import sys, time, signal, pickle
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from sympy import isprime
from sympy.ntheory import ecm
Fs=lambda U,V: U**6-30*U**4*V**2-24*U**2*V**4-V**6
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
def N6(m):
    m=abs(m)
    while m%2==0:m//=2
    while m%3==0:m//=3
    return m
P=(Fr(1),Fr(1));Q=P;pts={1:P}
for n in range(2,13):
    Q=add(Q,P);pts[n]=Q
jobs=[]
for n in (11,12):
    t=1-pts[n][0]
    jobs.append(("nP",n,N6(Fs(t.numerator,t.denominator))))
    tp=(t+1)/(t-1)
    jobs.append(("T",n,N6(Fs(tp.numerator,tp.denominator))))
out={}
class TO(Exception):pass
def h(s,f): raise TO()
signal.signal(signal.SIGALRM,h)
for kind,n,N in jobs:
    primes=[];comp=N
    # trial division
    for p in range(5,2*10**6,2):
        if p%3==0: continue
        if comp%p==0:
            primes.append(p)
            while comp%p==0: comp//=p
    t0=time.time()
    for (B1,B2,curves) in ((2000,200000,25),(11000,1100000,90),(50000,5000000,200)):
        if comp==1 or isprime(comp): break
        signal.alarm(240)
        try:
            fs=ecm(comp,B1=B1,B2=B2,max_curve=curves)
            for f in fs:
                if comp%f==0 and f>1:
                    primes.append(f)
                    while comp%f==0: comp//=f
        except TO:
            pass
        except ValueError:
            pass
        finally:
            signal.alarm(0)
    out[(kind,n)]=(len(str(N)),primes,comp)
    print("%s n=%d digits=%d  small primes found=%s ; remaining cofactor %d digits, probable prime: %s  [%.0fs]"%(kind,n,len(str(N)),[ (p if p<10**12 else '%d-digit'%len(str(p))) for p in primes],len(str(comp)),isprime(comp) if comp>1 else None,time.time()-t0),flush=True)
    pickle.dump(out,open('bg1112.pkl','wb'))
