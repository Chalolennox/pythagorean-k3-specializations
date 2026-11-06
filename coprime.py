import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from math import gcd, isqrt
from sympy import symbols, Poly, resultant, factorint, GF, gcd as sgcd, factor_list
X=symbols('X')
h =Poly(X**6-6*X**5-15*X**4+100*X**3-189*X**2+162*X-54,X)
hT=Poly(-54*X**6+324*X**5-756*X**4+800*X**3-240*X**2-192*X+64,X)
R=resultant(h.as_expr(),hT.as_expr(),X)
print("Res(h,h_T) =",R,"=",factorint(abs(R)))
primes=[p for p in factorint(abs(R))]
print("candidate primes:",primes)
def addp(P,Q,p):
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2:
        if (y1+y2)%p==0:return None
        lam=(3*x1*x1-4*x1+2)*pow(2*y1,-1,p)%p
    else: lam=(y2-y1)*pow(x2-x1,-1,p)%p
    x3=(lam*lam+2-x1-x2)%p
    return (x3,(lam*(x1-x3)-y1)%p)
def hv(r,p): return (r**6-6*r**5-15*r**4+100*r**3-189*r**2+162*r-54)%p
def hTv(r,p): return (-54*r**6+324*r**5-756*r**4+800*r**3-240*r**2-192*r+64)%p
for p in primes:
    if p==2: continue
    if p<10**5:
        roots=[r for r in range(p) if hv(r,p)==0 and hTv(r,p)==0]
    else:
        # find roots of gcd mod p via brute force (p~5e5 is fine)
        roots=[r for r in range(p) if hv(r,p)==0 and hTv(r,p)==0]
    print("\np=%d: common roots of h and h_T in F_p: %s"%(p,roots))
    # orbit of P=(1,1) mod p
    P=(1%p,1%p);orb={};Q=P;n=1
    xs=set()
    while Q is not None:
        xs.add(Q[0]);Q=addp(Q,P,p);n+=1
        if n>3*p:break
    print("   order of P mod p =",n,"; x-coordinates of <P> (affine part) number",len(xs))
    for r in roots:
        rhs=(r**3-2*r**2+2*r)%p
        onc=any((y*y-rhs)%p==0 for y in range(p)) if p<2000 else pow(rhs,(p-1)//2,p) in (0,1)
        print("   root %d: on J(F_p): %s ; x(Q)=root is an x-coordinate of <P>: %s"%(r,onc,r in xs))
# brute-force: gcd(F_n,G_n) for n<=150
def add(P,Q):
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2:
        if y1+y2==0:return None
        lam=(3*x1*x1-4*x1+2)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam+2-x1-x2
    return (x3,lam*(x1-x3)-y1)
Fh=lambda a,d: a**6-6*a**5*d-15*a**4*d**2+100*a**3*d**3-189*a**2*d**4+162*a*d**5-54*d**6
Gh=lambda a,d: -54*a**6+324*a**5*d-756*a**4*d**2+800*a**3*d**3-240*a**2*d**4-192*a*d**5+64*d**6
P=(Fr(1),Fr(1));Q=P;bad=[]
for n in range(1,151):
    if n>1:Q=add(Q,P)
    x=Q[0];F=Fh(x.numerator,x.denominator);G=Gh(x.numerator,x.denominator)
    g=gcd(abs(F),abs(G))
    if g!=1: bad.append((n,g))
print("\nbrute force n=1..150: gcd(|F_n|,|G_n|)=1 for all n:",not bad,bad[:5])
