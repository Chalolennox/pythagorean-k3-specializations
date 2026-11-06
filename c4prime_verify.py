import sys, time, signal
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from sympy import factorint, isprime
exec(open('c4prime_delta.py').read().split("class TO")[0])
for n in range(1,8):
    w=pts[n][0];t=(w-2)/(w+2)
    N=N6(Fs(t.numerator,t.denominator))
    f=factorint(N,use_ecm=True)
    prod=1
    for p,e in f.items(): prod*=p**e
    print("n=%d: product ok=%s  all prime=%s"%(n,prod==N,all(isprime(p) for p in f)))
    print("     factors:",{p:e for p,e in sorted(f.items())} if n<=6 else {(str(p)[:12]+"...(%d digits)"%len(str(p)) if len(str(p))>14 else p):e for p,e in sorted(f.items())})
