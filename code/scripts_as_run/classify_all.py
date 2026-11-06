import os
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','data')
import numpy as np, json, cmath, math
from fractions import Fraction as Fr
from sympy import symbols, Poly, Integer, factor_list, resultant
exec(open('analyze.py').read().split('if __name__')[0])
xs=symbols('x'); ys=symbols('y')
def Rpoly(ee): return Poly(sum((-1)**k*Integer(ee[k].numerator)*xs**(10-k) for k in range(11)),xs)
def weil(R,p):
    r=np.roots([float(c) for c in R.all_coeffs()]); return np.allclose(np.abs(r),p,atol=3e-4*p)
def cyc_count(R,p):
    tot=0
    for g,mult in factor_list(R.as_expr())[1]:
        gp=Poly(g,xs);k=gp.degree();co=gp.all_coeffs()
        py=Poly(sum(Integer(int(c))*(p*ys)**(k-j) for j,c in enumerate(co)),ys)
        if all(int(c)%(p**k)==0 for c in py.all_coeffs()):
            pn=Poly(py.as_expr()/p**k,ys)
            for mm in range(1,61):
                if (Poly(ys**mm-1,ys).rem(pn)).is_zero: tot+=k*mult;break
    return tot
def candidates(p,Ns):
    e=newton(Ns[:4]); out=[]
    # eps=-1
    ee=build_R(e,p,-1,0); R=Rpoly(ee)
    if weil(R,p): out.append((-1,0,R,ee))
    # eps=+1 : e5 from R(p*zeta)=0 for roots of unity zeta
    seen=set()
    for m in (1,2,3,4,5,6,8,10,12):
        for j in range(m):
            if math.gcd(j,m)!=1: continue
            z=cmath.exp(2j*math.pi*j/m)
            ee0=build_R(e,p,1,0)
            A=sum((-1)**k*complex(ee0[k])*(p*z)**(10-k) for k in range(11))
            e5=A/(-1*(p*z)**5) *(-1)      # solve A + (-1)^5 e5 (pz)^5 = 0  ->  e5 = A/(pz)^5
            e5=A/((p*z)**5)
            if abs(e5.imag)<1e-6*abs(e5.real+1) and abs(e5.real-round(e5.real))<1e-3:
                v=int(round(e5.real))
                if v in seen: continue
                seen.add(v)
                ee=build_R(e,p,1,Fr(v)); R=Rpoly(ee)
                if weil(R,p): out.append((1,v,R,ee))
    return out
rows=[json.loads(l) for l in open(os.path.join(DATA,'point_counts_covers.jsonl'))]
decision={}
for r in rows:
    c,p,Ns=r['c'],r['p'],r['N']
    cands=[]
    for eps,e5,R,ee in candidates(p,Ns):
        nc=cyc_count(R,p)
        if nc>=2 and nc%2==0:
            rho=12+nc
            cls=None
            if rho==14:
                # remove the cyclotomic part and compute Lambda via resultants over the remaining degree-8 factor
                rest=R
                from sympy import factor_list as fl
                rem=1
                for g,mult in fl(R.as_expr())[1]:
                    gp=Poly(g,xs);k=gp.degree();co=gp.all_coeffs()
                    py=Poly(sum(Integer(int(cc))*(p*ys)**(k-j) for j,cc in enumerate(co)),ys)
                    if all(int(cc)%(p**k)==0 for cc in py.all_coeffs()):
                        continue
                    rem*=gp.as_expr()**mult
                rem=Poly(rem,xs)
                if rem.degree()==8:
                    val=Fr(int(resultant(rem.as_expr(),xs**2-p*p,xs)))/Fr(p)**16   # prod (1-alpha^2/p^2)
                    # prod_i (alpha_i^2 - p^2) = Res(rem, x^2-p^2) up to sign; Lambda = prod(1-alpha^2/p^2) = Res/p^16 (even degree)
                    cls=sqfree_class(val)
            cands.append((eps,e5,rho,cls))
    decision[(c,p)]=cands
    print("c=%-6s p=%2d : consistent L-functions (eps, e5, rho(F_p-bar), class): %s"%(c,p,cands if cands else "none"))
import pickle;pickle.dump(decision,open('decision.pkl','wb'))
