import sys, math, itertools, time
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from math import gcd
from sympy import factorint
src=open('t4.py').read().split("for (U,V) in ((-4,1),(4,1)):")[0]
exec(src)
cands=[]
for V in (1,2,3,4,5,8,9,16):
    for U in range(-14,15):
        if U==0 or gcd(abs(U),V)!=1 or abs(U)==V: continue
        c0=U*U+V*V
        if c0%2==0 or c0%3==0: continue
        F=U**6-30*U**4*V**2-24*U**2*V**4-V**6
        fa=factorint(abs(F));rest=1
        for p in fa:
            if p>=5: rest*=p
        for p in factorint(c0):
            if p>=5: rest*=p**2
        if rest<=12000: cands.append((rest,U,V,fa))
cands.sort()
print("candidate t:",[(U,V) for r,U,V,fa in cands],flush=True)
agree=tot=0
import io,contextlib
for rest,U,V,fa in cands[:10]:
    t0=time.time()
    try: f,fa2,ex,naive=formula(U,V)
    except Exception as e:
        print("t=%d/%d: formula n/a (%s)"%(U,V,e),flush=True);continue
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        best=analysis(U,V)
    signs=sorted(set(round(r) for N,e,r,r2 in best))
    tot+=1
    ok=(len(signs)==1 and signs[0]==ex)
    agree+=ok
    print("t=%d/%d  F''=%s  formula W=%+d (naive %+d)  analytic: conductors %s signs %s  -> %s  [%.0fs]"%(U,V,dict(fa2),ex,naive,[N for N,e,r,r2 in best],signs,"AGREE" if ok else "DISAGREE/none",time.time()-t0),flush=True)
print("summary: %d of %d agree"%(agree,tot),flush=True)
