import random
from fractions import Fraction as Fr
from math import gcd
exec(open('split23.py').read().split("P=(Fr(1),Fr(1));Q=P;pts={1:P}")[0])
psi2=lambda t:(lambda w:(-w[0]*w[2]*local(t,2)))(comps(t))
psi3=lambda t:(lambda w:(w[1]*local(t,3)))(comps(t))
random.seed(7)
ms=[k for k in range(1,60,2) if k%3]
def pts_in(cls,mod,N):
    out=[]
    while len(out)<N:
        m=random.choice(ms);v=m*m;k=random.randint(-40,40)
        u=cls*v+mod*k           # t=u/v = cls + mod*k/v : same class since v is a 2- and 3-adic unit
        t=Fr(u,v)
        if gcd(abs(u),v)!=1 or t in (0,1,-1) or t>=1: continue
        out.append(t)
    return out
print("Psi_2 on rational points u/m^2 (m odd, 3∤m):")
for name,cls,mod in (("t=-1 mod 16 (n odd)",-1,16),("t=-7 mod 64 (n=2 mod 4)",-7,64),("t=1 mod 32 (n=0 mod 4)",1,32)):
    print("  ",name,sorted(set(psi2(t) for t in pts_in(cls,mod,300))))
print("Psi_3 on rational points u/m^2:")
for name,cls,mod in (("t=1 mod 9 (3|n)",1,9),("t=2 mod 9",2,9),("t=5 mod 9",5,9),("t=8 mod 9",8,9)):
    print("  ",name,sorted(set(psi3(t) for t in pts_in(cls,mod,300))))
