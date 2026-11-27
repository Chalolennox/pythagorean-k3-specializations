"""Exhaustive active-period transpose obstruction for seeds 72*k.
Python 3.10+, standard library only. Owner Magma residues are inputs.
"""
from math import gcd,lcm
rows=[(2131,1031,[388,643]),(5779,2903,[1286,1617]),(6907,1151,[6,1145]),(10321,2589,[639,874,1715,1950]),(12907,6465,[810,5655]),(13763,6959,[240,6719]),(18797,9404,[2600,6804]),(23747,11783,[3037,8746]),(40841,10247,[4507,5740]),(46933,23492,[1344,2872,20620,22148]),(47657,11927,[5069,6858]),(47701,23708,[714,9644,14064,22994]),(52883,26343,[11592,14751]),(54517,27256,[3244,5520,21736,24012]),(72883,36479,[9393,27086]),(77347,38711,[5713,32998])]
def intersect(A,B):
    r,a,b=A; s,c,d=B
    g=gcd(r,s); l=lcm(b,d)
    h=a*(l//b)-c*(l//d)
    t=l*g//gcd(h,g)
    X=a*(t//b); Y=c*(t//d)
    assert (Y-X)%g==0
    R=lcm(r,s)
    return R,(X+r*((Y-X)//g*pow(r//g,-1,s//g)%(s//g)))%R,t
def swap(A):
    r,a,b=A; g=gcd(r,a); R=b*r//g
    return R,(b*pow(a//g,-1,r//g))%R,g
def lattice(e):
    P={}; x=1
    while x not in P:
        P[x]=len(P); x=2*x%e
    assert x==1
    b=1; y=3%e
    while y not in P:
        y=3*y%e; b+=1
    return len(P),P[y],b
def main():
    states={(1,0,1)}
    for p,d,z in rows:
        E=d//gcd(d,72); opts=[]
        for e in range(2,E+1):
            if E%e: continue
            g=d//e
            if not any(v%g==0 and gcd(v//g,e)==1 for v in z): continue
            opts.append(lattice(e))
        states |= {intersect(A,B) for A in states for B in opts}
        print(p,opts,len(states),flush=True)
    assert len(states)==98304
    assert all(swap(swap(A))==A for A in states)
    matches={A for A in states if swap(A) in states}
    assert matches=={(1,0,1)},matches
    print("PASS: 98304 candidate lattices; only trivial transpose match")
if __name__=="__main__":
    main()
