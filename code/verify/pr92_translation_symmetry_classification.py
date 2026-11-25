#!/usr/bin/env python3
"""Independent check for PR #92 note ARITHMETIC_TRANSLATION_SYMMETRY_CLASSIFICATION.md.
Written by Claude (a language model), independent of the PR author's scripts. No human has checked it.
Stdlib only, exact integer arithmetic. Runtime: about 85 seconds.
Checks, for the 16 (p, d=ord(P), residues) rows copied from code/verify/pr92_walsh_distribution.py:
 for every divisor e of d/gcd(72,d), g=d/e, R_e={z/g mod e : g | z}, H_e=<2,3> mod e,
 the number of hits #{t in H_e : u*t mod e in R_e} for every unit u; reports every (p,e) with |H_e| even
 or with any hit, and checks the note's list (12907: e=5, e=2155; 46933: e=1,7,839,5873) and the hit counts.
Also checks the densities 5028/5873, 845/5873.
Does NOT check: the residue data (owner Magma output), the lattice/CRT argument for K=C4xC2 or C4xC4,
or the proof that the quotient lattice images are as stated."""
from math import gcd
rows=[(2131,1031,[388,643]),(5779,2903,[1286,1617]),(6907,1151,[6,1145]),(10321,2589,[639,874,1715,1950]),(12907,6465,[810,5655]),(13763,6959,[240,6719]),(18797,9404,[2600,6804]),(23747,11783,[3037,8746]),(40841,10247,[4507,5740]),(46933,23492,[1344,2872,20620,22148]),(47657,11927,[5069,6858]),(47701,23708,[714,9644,14064,22994]),(52883,26343,[11592,14751]),(54517,27256,[3244,5520,21736,24012]),(72883,36479,[9393,27086]),(77347,38711,[5713,32998])]
def gen(e):
    S={1%e};fr=[1%e]
    while fr:
        nf=[]
        for x in fr:
            for m in(2,3):
                y=x*m%e
                if y not in S:S.add(y);nf.append(y)
        fr=nf
    return S
for p,d,z in rows:
    D=d//gcd(72,d)
    for e in range(1,D+1):
        if D%e:continue
        g=d//e
        R={v//g%e for v in z if v%g==0}
        H=gen(e)
        evenH=len(H)%2==0
        hits=set()
        if R:
            for u in range(e):
                if gcd(u,e)==1:
                    hits.add(sum(1 for t in H if u*t%e in R))
        if evenH or (hits-{0}):
            print("p",p,"e",e,"|H|",len(H),"R",sorted(R),"hit-count values over units",sorted(hits))
print(5028/5873,845/5873,5028+845==5873)
