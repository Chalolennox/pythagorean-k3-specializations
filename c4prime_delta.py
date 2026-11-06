import sys, time, signal
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from sympy import factorint, isprime
Fs=lambda U,V: U**6-30*U**4*V**2-24*U**2*V**4-V**6
def addp(P,Q):          # v^2 = w^3 + 8
    x1,y1=P;x2,y2=Q
    if x1==x2: lam=(3*x1*x1)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam-x1-x2
    return (x3,lam*(x1-x3)-y1)
R=(Fr(1),Fr(3));S=R;pts={1:R}
for n in range(2,9):
    S=addp(S,R);pts[n]=S
def N6(m):
    m=abs(m)
    while m%2==0:m//=2
    while m%3==0:m//=3
    return m
class TO(Exception): pass
def h(sig,frm): raise TO()
signal.signal(signal.SIGALRM,h)
res={}
for n in range(1,9):
    w=pts[n][0];t=(w-2)/(w+2)
    N=N6(Fs(t.numerator,t.denominator))
    t0=time.time()
    signal.alarm(70)
    try:
        f=factorint(N,use_ecm=True) if True else None
        ok=all(isprime(p) for p in f)
        om=sum(f.values())
        res[n]=(len(str(N)),f,om)
        print("n=%d t=%s  digits(F'')=%d  ω(with mult)=%d  delta=%+d  exps=%s  [%.0fs]"%(n,t,len(str(N)),om,(-1)**om,sorted(f.values(),reverse=True),time.time()-t0),flush=True)
    except TO:
        print("n=%d t=%s  digits(F'')=%d  : timed out"%(n,t,len(str(N))),flush=True)
    finally:
        signal.alarm(0)
