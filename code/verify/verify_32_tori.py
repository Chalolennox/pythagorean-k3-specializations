from math import gcd
from functools import lru_cache
rows=[(2131,1031,[388,643]),(5779,2903,[1286,1617]),(6907,1151,[6,1145]),(10321,2589,[639,874,1715,1950]),(12907,6465,[810,5655]),(13763,6959,[240,6719]),(18797,9404,[2600,6804]),(23747,11783,[3037,8746]),(40841,10247,[4507,5740]),(46933,23492,[1344,2872,20620,22148]),(47657,11927,[5069,6858]),(47701,23708,[714,9644,14064,22994]),(52883,26343,[11592,14751]),(54517,27256,[3244,5520,21736,24012]),(72883,36479,[9393,27086]),(77347,38711,[5713,32998])]
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

@lru_cache(None)
def grid(e):
    r,a,b=lattice(e)
    D={pow(2,i,e)*pow(3,j,e)%e:(i,j) for j in range(b) for i in range(r)}
    return r,a,b,D

def lattice(e):
    powers={1:0}; x=2%e; r=1
    while x!=1:
        powers[x]=r; r+=1; x=x*2%e
    b=1; x=3%e
    while x not in powers:
        b+=1; x=x*3%e
    return r,powers[x],b

def data(n):
    out=[]
    for p,d,R in rows:
        g=gcd(n,d); e=d//g
        if e==1:
            assert 0 not in R
            out.append(None); continue
        r,a,b,D=grid(e)
        inv=pow(n//g,-1,e)
        hits=[D[z//g*inv%e] for z in R if z%g==0 and z//g*inv%e in D]
        out.append((e,r,a,b,hits) if hits else None)
    return out

base=data(504); seen=set(); count=0
for m in range(1,3000,2):
    if m%3==0: continue
    n=504*m; B=data(n); L=(1,0,1,0,0)
    try:
        for A,C in zip(base,B):
            if A is None or C is None:
                assert A==C; continue
            assert A[:4]==C[:4] and len(A[4])==len(C[4])==1
            e,r,a,b=A[:4]; x,y=A[4][0]; u,v=C[4][0]
            L=intersect(L,(r,a,b,x-u,y-v))
    except AssertionError:
        continue
    r,a,b,u,v=L; v0=v%b; u=(u+a*((v-v0)//b))%r; v=v0
    if (u,v) in seen: continue
    for (p,d,R),A,C in zip(rows,base,B):
        if A is None: continue
        e,rr,aa,bb=A[:4]; x,y=A[4][0]; xx,yy=C[4][0]
        assert (yy+v-y)%bb==0 and (xx+u-x+aa*((yy+v-y)//bb))%rr==0
        t=pow(2,u,d)*pow(3,v,d)%d
        assert all((n*z%d in R)==(504*t*z%d in R) for z in grid(e)[3])
    seen.add((u,v)); count+=1
    print(count,m,n,u,v,flush=True)
    if count==32:
        print('lattice',r,a,b); break
assert count==32
