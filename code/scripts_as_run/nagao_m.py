import numpy as np, math, pickle
from fractions import Fraction as Fr
from sympy import primerange, factorint
exec(open('nagao.py').read().split("for c,name in")[0].replace("out.append((p,S/W))","out.append((p,S/W)); AP[(c,p)]=Ap").replace("def estimate(c, P_MAX=700, skip=(2,3,7,23)):","AP={}\ndef estimate(c, P_MAX=700, skip=(2,3,7,23)):"))
def leg(m,p):
    m%=p
    return 0 if m==0 else (1 if pow(m,(p-1)//2,p)==1 else -1)
def sqf(m):
    return all(e==1 for e in factorint(abs(m)).values()) if abs(m)>1 else True
ms=[m for m in range(-30,31) if m not in (0,1) and sqf(m)]
res={}
for c in (Fr(2),Fr(13,9)):
    estimate(c)
    ps=sorted(p for (cc,p) in AP if cc==c)
    for m in ms:
        S=W=0.0
        for p in ps:
            if m%p==0: continue
            S+= (-leg(m,p)*AP[(c,p)]/p)*math.log(p); W+=math.log(p)
        res[(c,m)]=S/W
for c in (Fr(2),Fr(13,9)):
    vals=sorted(((res[(c,m)],m) for m in ms),reverse=True)
    print("c =",c," twist-by-m Nagao estimate (rank of E^{d m} over Q(t)); largest 6:",[(m,round(v,2)) for v,m in vals[:6]]," ; median %.2f , min %.2f"%(np.median([v for v,m in vals]),vals[-1][0]))
print("m scanned:",ms)
