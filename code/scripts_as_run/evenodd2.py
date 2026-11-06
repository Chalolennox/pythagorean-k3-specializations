import pickle, time, sys
from fractions import Fraction as Fr
from sympy import primerange
exec(open('evenodd.py').read().split("t0=time.time()")[0])
rows=pickle.load(open('evenodd_rows.pkl','rb'))
t0=time.time()
for p in primerange(10001,40001):
    m,de,do=dens(p); rows.append((p,m,de,do))
print("extended to 40000 in %.0fs"%(time.time()-t0),flush=True)
pickle.dump(rows,open('evenodd_rows40k.pkl','wb'))
SE=SO=0.0;cps=[100,300,1000,3000,10000,20000,40000];out={}
for p,m,de,do in rows:
    SE+=float(de);SO+=float(do)
    for cp in cps:
        if p<=cp: out[cp]=(SE,SO)
print("   B      sum_even  sum_odd   difference  ratio R")
for cp in cps:
    e,o=out[cp];print("%6d   %.4f   %.4f   %.4f    %.4f"%(cp,e,o,e-o,e/o))
# who contributes to the difference?
big=sorted(rows,key=lambda r:-abs(float(r[2]-r[3])))[:10]
print("\nlargest per-prime contributions to (even - odd):")
for p,m,de,do in big: print("   p=%5d  ord(P)=%5d  de=%.4f  do=%.4f  diff=%.4f"%(p,m,float(de),float(do),float(de-do)))
# contribution to the difference from primes in dyadic ranges
import math
print("\ndifference summed over prime ranges:")
for lo,hi in ((5,100),(100,300),(300,1000),(1000,3000),(3000,10000),(10000,20000),(20000,40000)):
    d=sum(float(de-do) for p,m,de,do in rows if lo<=p<hi);s=sum(float(de+do) for p,m,de,do in rows if lo<=p<hi)
    print("   p in [%5d,%5d): sum(even-odd) = %+.4f   sum(even+odd) = %.4f"%(lo,hi,d,s))
# parity of ord(P): how many primes have even order, and average of (de-do) for them
ev=[r for r in rows if r[1]%2==0];print("\nfraction of primes with even ord(P): %.3f"%(len(ev)/len(rows)))
