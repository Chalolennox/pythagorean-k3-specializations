import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from math import gcd
from sympy import symbols, Poly, resultant, factorint, expand, sqrt, discriminant
X,U=symbols('X U')
h =X**6-6*X**5-15*X**4+100*X**3-189*X**2+162*X-54
Rs=-54*U**6+648*U**5-1242*U**4-11404*U**3+62082*U**2-113832*U+73224
# (a) fixed points of the involution: Res(h, X^2-2)
r=resultant(h,X**2-2,X);print("Res(h,X^2-2) =",r,"=",factorint(abs(r)))
print("disc(R)/disc(h) =",discriminant(Poly(Rs,U))//discriminant(Poly(h,X)),"=",factorint(discriminant(Poly(Rs,U))//discriminant(Poly(h,X))))
# (b) the pair of common roots mod 519521 is swapped by x -> 2/x
p=519521
print("37492*384583 mod 519521 =",37492*384583%p,"(=2 means the two roots are swapped by x->2/x)")
# roots of h mod p: all six? and their pairing
roots=[r for r in range(p) if (r**6-6*r**5-15*r**4+100*r**3-189*r**2+162*r-54)%p==0]
print("roots of h mod 519521:",roots)
# (c) F_n G_n = R_h(p_n,q_n), p_n=A^2+2B^4, q_n=A B^2, orbit of phi(P) on J'
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
def addp(P,Q): # J': Y^2=X^3+4X^2-4X
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2:
        if y1+y2==0:return None
        lam=(3*x1*x1+8*x1-4)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam-4-x1-x2
    return (x3,lam*(x1-x3)-y1)
Fh=lambda a,d: a**6-6*a**5*d-15*a**4*d**2+100*a**3*d**3-189*a**2*d**4+162*a*d**5-54*d**6
Gh=lambda a,d: -54*a**6+324*a**5*d-756*a**4*d**2+800*a**3*d**3-240*a**2*d**4-192*a*d**5+64*d**6
c=[-54,648,-1242,-11404,62082,-113832,73224]  # coefficients of R in U^6..U^0 order: R=sum c[i]U^(6-i)?? set below
Rc={6:-54,5:648,4:-1242,3:-11404,2:62082,1:-113832,0:73224}
Rh=lambda pp,qq: sum(Rc[i]*pp**i*qq**(6-i) for i in range(7))
P=(Fr(1),Fr(1));Pp=(Fr(1),Fr(-1));Q=P;Qp=Pp;ok=0;okiso=0;okgcd=0;N=40
assert Pp[1]**2==Pp[0]**3+4*Pp[0]**2-4*Pp[0]
for n in range(1,N+1):
    if n>1:Q=add(Q,P);Qp=addp(Qp,Pp)
    x=Q[0];A,d=x.numerator,x.denominator
    pp=A*A+2*d*d; qq=A*d
    ok+=(Fh(A,d)*Gh(A,d)==Rh(pp,qq)); okgcd+=(gcd(abs(pp),abs(qq))==1)
    okiso+=(Qp[0]==x+2/x-2)
print("n<=%d: F_n G_n = R_h(A^2+2B^4, A B^2): %d ; gcd(p_n,q_n)=1: %d ; x'(nP'')=x(nP)+2/x(nP)-2 on J' with P''=phi(P)=(1,-1): %d"%(N,ok,okgcd,okiso))
