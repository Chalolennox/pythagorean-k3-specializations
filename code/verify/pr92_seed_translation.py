"""Standalone Python 3.10+ certificate; no external dependencies.
Uses owner Magma residue data. Run directly from any directory.
"""
from math import gcd
rows=[(2131,1031,[388,643]),(5779,2903,[1286,1617]),(6907,1151,[6,1145]),(10321,2589,[639,874,1715,1950]),(12907,6465,[810,5655]),(13763,6959,[240,6719]),(18797,9404,[2600,6804]),(23747,11783,[3037,8746]),(40841,10247,[4507,5740]),(46933,23492,[1344,2872,20620,22148]),(47657,11927,[5069,6858]),(47701,23708,[714,9644,14064,22994]),(52883,26343,[11592,14751]),(54517,27256,[3244,5520,21736,24012]),(72883,36479,[9393,27086]),(77347,38711,[5713,32998])]
U=57734055708745284484672341832708165195
V=4886099
def orbit(n,d):
    q=[n%d]; seen=set(q)
    for x in q:
        for m in (2,3):
            y=x*m%d
            if y not in seen:
                seen.add(y); q.append(y)
    return seen
def lattice(e):
    powers={1:0}; x=2%e; r=1
    while x!=1:
        powers[x]=r; r+=1; x=x*2%e
    b=1; x=3%e
    while x not in powers:
        b+=1; x=x*3%e
    return r,powers[x],b
def crt(x,r,y,s):
    g=gcd(r,s)
    assert (y-x)%g==0
    return (x+r*((y-x)//g*pow(r//g,-1,s//g)%(s//g)))%(r*s//g)
def intersect(A,B):
    r,a,b,x,y=A; s,c,d,u,v=B
    Y=crt(y,b,v,d); L=b*d//gcd(b,d); g=gcd(r,s)
    X=x-a*((Y-y)//b); Z=u-c*((Y-v)//d)
    h=a*(L//b)-c*(L//d); q=gcd(h,g)
    assert (X-Z)%q==0
    Y+=L*((X-Z)//q*pow(h//q,-1,g//q)%(g//q))
    Bnew=L*g//q
    return (r*s//g,crt(a*(Bnew//b),r,c*(Bnew//d),s),Bnew,
            crt(x-a*((Y-y)//b),r,u-c*((Y-v)//d),s),Y)
def main():
    L=(1,0,1,0,0); active=0
    for p,d,z in rows:
        O=orbit(72,d); R=set(z)
        images=[{m*x%d for x in O} for m in (1,5,7,35)]
        for m,I in zip((1,5,7,35),images):
            assert I==orbit(72*m,d)
        assert {7*x%d for x in images[1]}=={5*x%d for x in images[2]}==images[3]
        print(p,[(len(I),sorted(I&R)) for I in images],flush=True)
        A,B=images[2],images[3]
        e=d//gcd(504,d)
        r,a,b=lattice(e)
        assert len(A)==len(B)==r*b
        t=pow(2,U,d)*pow(3,V,d)%d
        assert all(((5*x%d in R)==(t*x%d in R)) for x in A)
        if not A&R:
            assert not B&R
            continue
        active+=1
        assert len(A&R)==len(B&R)==1
        hits=[]
        for j in range(b):
            for i in range(r):
                x=504*pow(2,i,d)*pow(3,j,d)%d
                if x in R: old=(i,j)
                if 5*x%d in R: new=(i,j)
        X,Y=old[0]-new[0],old[1]-new[1]
        L=intersect(L,(r,a,b,X,Y))
        print("  translation constraint",r,a,b,X,Y,flush=True)
    assert active==14
    r,a,b,x,y=L
    assert (V-y)%b==0 and (U-x+a*((V-y)//b))%r==0
    print("PASS: simultaneous translation",U,V,"solution coset",L)
if __name__=="__main__":
    main()
