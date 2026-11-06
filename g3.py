import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from sympy import symbols, expand, Poly
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
X,z=symbols('X z')
h=X**6-6*X**5-15*X**4+100*X**3-189*X**2+162*X-54
hT=-54*X**6+324*X**5-756*X**4+800*X**3-240*X**2-192*X+64
print("h_T(X) = X^6 h(2/X):",expand(X**6*h.subs(X,2/X)-hT)==0)
print("identity h_T(1+3z) = -54(729z^6-81z^4+32z^3-9z^2+1):",expand(hT.subs(X,1+3*z)+54*(729*z**6-81*z**4+32*z**3-9*z**2+1))==0)
def v(m,p):
    m=abs(m);k=0
    while m%p==0: m//=p;k+=1
    return k
Fh=lambda a,d: a**6-6*a**5*d-15*a**4*d**2+100*a**3*d**3-189*a**2*d**4+162*a*d**5-54*d**6
Gh=lambda a,d: -54*a**6+324*a**5*d-756*a**4*d**2+800*a**3*d**3-240*a**2*d**4-192*a*d**5+64*d**6
P=(Fr(1),Fr(1));Q=P;pts={1:P}
NM=200
for n in range(2,NM+1):
    Q=add(Q,P);pts[n]=Q
bad=[];tab={}
for n in range(1,NM+1):
    x=pts[n][0];a,d=x.numerator,x.denominator
    F=Fh(a,d);G=Gh(a,d)
    # F_n = d^6 h(a/d) = Fh(a,d); G_n = d^6 h_T(a/d) = Gh(a,d)
    ok=(v(F,2)==0 and v(F,3)==0 and v(G,2)==1 and v(G,3)==(4 if n%9 in (4,5) else 3))
    if not ok: bad.append((n,v(F,2),v(F,3),v(G,2),v(G,3)))
    # residue of x(nP) mod 9
    r=n%9
    xm=("inf" if d%9==0 else (a*pow(d,-1,9))%9) if d%3==0 or True else None
    tab.setdefault(r,set()).add(xm)
print("n=1..%d: v2(F)=v3(F)=0, v2(G)=1, v3(G)=3+[n=4,5 mod 9] hold for all n: %s ; exceptions %s"%(NM,len(bad)==0,bad[:3]))
print("x(nP) mod 9 by n mod 9:",{r:sorted(map(str,s)) for r,s in sorted(tab.items())})
# G_n is the C-value of the translate member: x(nP+T)=2/x(nP) = 2d/a with a a perfect square
from math import isqrt
print("a_n is a perfect square (so x(nP+T)=2d/a has denominator a square):",all(isqrt(pts[n][0].numerator)**2==pts[n][0].numerator for n in range(1,NM+1)))
