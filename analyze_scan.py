import os
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','data')
import json, sys
from fractions import Fraction as Fr
exec(open('classify_all.py').read().split("rows=[json.loads")[0])
exec(open('eps_pred.py').read().split('if __name__')[0].replace("from fractions import Fraction as Fr",""))
def lam_class(R,p):
    rem=1
    for g,mult in factor_list(R.as_expr())[1]:
        gp=Poly(g,xs);k=gp.degree();co=gp.all_coeffs()
        py=Poly(sum(Integer(int(cc))*(p*ys)**(k-j) for j,cc in enumerate(co)),ys)
        if all(int(cc)%(p**k)==0 for cc in py.all_coeffs()): continue
        rem*=gp.as_expr()**mult
    rem=Poly(rem,xs)
    if rem.degree()!=8: return None
    val=Fr(int(resultant(rem.as_expr(),xs**2-p*p,xs)))/Fr(p)**16
    return sqfree_class(val)
rows=[json.loads(l) for l in open(os.path.join(DATA,'point_counts_scan.jsonl'))]
summary=[]
for r in rows:
    c=Fr(r['c']); info={}
    for p,Ns in r['N'].items():
        p=int(p); ep=eps_pred(c,p)[0]; classes=set(); rho_set=set()
        for eps,e5,R,ee in candidates(p,Ns):
            if eps!=ep: continue
            nc=cyc_count(R,p)
            if nc>=2 and nc%2==0:
                rho=12+nc; rho_set.add(rho)
                if rho==14:
                    classes.add(lam_class(R,p))
        if rho_set=={14} and classes and None not in classes: info[p]=classes
        else: info[p]=("rho16/unclear",sorted(rho_set))
    inf=[(p,v) for p,v in info.items() if isinstance(v,set)]
    verdict="insufficient"
    if len(inf)>=2:
        # rho=13 proven if some two informative primes have disjoint class sets
        proven=any(inf[i][1].isdisjoint(inf[j][1]) for i in range(len(inf)) for j in range(i+1,len(inf)))
        if proven: verdict="rho=13 proved"
        else: verdict="*** FLAG: all informative classes overlap -> candidate for rho=14 ***"
    summary.append((str(c),verdict,{p:(sorted(v) if isinstance(v,set) else v) for p,v in info.items()}))
    print("c=%-6s %-34s %s"%(c,verdict,{p:(sorted(v) if isinstance(v,set) else '16') for p,v in info.items()}))
from collections import Counter
print(Counter(s[1] for s in summary))
