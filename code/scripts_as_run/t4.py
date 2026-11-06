import math, sys, itertools
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from math import gcd
from sympy import factorint, primerange
exec(open('rootnum.py').read().split("# ---------- validation")[0])
exec(open('eps.py').read().split('if __name__')[0])
def model(U,V):
    c0=U*U+V*V
    a4=4*(V*V-U*U)*c0**3; a6=-16*U*V*c0**5
    # remove 2^k and p^k factors while minimal-reducible
    changed=True
    while changed:
        changed=False
        for p in [2]+[q for q in factorint(c0)]:
            if a4%(p**4)==0 and a6%(p**6)==0: a4//=p**4;a6//=p**6;changed=True
    return a4,a6
def analysis(U,V,M=None):
    a4,a6=model(U,V)
    D=-16*(4*a4**3+27*a6**2); c4=-48*a4; c6=-864*a6
    fa=factorint(abs(D))
    print("t=%d/%d  model y^2=x^3%+d x%+d ; Delta=%s"%(U,V,a4,a6,fa))
    bad=sorted(fa)
    # base exponent guesses
    cand={}
    for p in bad:
        if p>=5:
            cand[p]=[1] if c4%p!=0 else [2]
        elif p==2: cand[p]=list(range(0,9))
        elif p==3: cand[p]=list(range(0,6))
    print("candidate exponents:",cand)
    best=[]
    Nmax=1
    for p,l in cand.items(): Nmax*=p**max(l)
    M=int(6*math.sqrt(min(Nmax,4*10**8)))+50 if M is None else M
    ap=a_primes_short(a4,a6,M)
    keys=list(cand)
    for combo in itertools.product(*[cand[p] for p in keys]):
        e=dict(zip(keys,combo)); N=1
        for p,k in e.items(): N*=p**k
        if N>4*10**8: continue
        apm=dict(ap)
        for p,k in e.items():
            if k>=2: apm[p]=0
        a=an_list(apm,e,M)
        r,g1,g2=sign_test(a,N,1.2)
        r2,_,_=sign_test(a,N,1.35)
        if abs(abs(r)-1)<1e-3 and abs(abs(r2)-1)<1e-3 and abs(r-r2)<1e-3:
            best.append((N,e,round(r,5),round(r2,5)))
    return best
def formula(U,V):
    t=Fr(U,V)
    f,s,Fv=pieces(t)
    a,b,c=triple(t)
    fa=factorint(Fv)
    R=1
    for p in fa: R*=p
    # exact: f * prod_{p|R} ( -(ab/p) )
    ex=f
    for p in fa:
        ex*= -(jac(a*b,p) if p>2 else 1)
    naive=f*jac(a*b,Fv)*(-1)**sum(fa.values())
    return f,fa,ex,naive
for (U,V) in ((-4,1),(4,1)):
    print("="*70)
    f,fa,ex,naive=formula(U,V)
    print("formula data: f=%d, F''=%s -> exact formula W=%+d ; naive (all exponents odd) W=%+d"%(f,fa,ex,naive))
    best=analysis(U,V)
    print("conductors consistent with a functional equation of sign +-1:",best)
