import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from sympy import symbols, Poly, expand, factor_list, gcd, resultant, discriminant, QQ, rootof, groebner, simplify
u,v,al=symbols('u v alpha')
a2,b2=-2,2   # J: y^2 = x^3 + a2 x^2 + b2 x
# addition formulas for y^2=x(x^2+a x+b):  x+ x- = (uv-b)^2/(u-v)^2 ; x+ + x- = 2[(u+v)(uv+b)+2a uv]/(u-v)^2
S=(u+v)*(u*v+b2)+2*a2*u*v
Nal=(u*v-b2)**2-2*al*S+al**2*(u-v)**2          # (u-v)^2 (x_+ - al)(x_- - al)
# check against actual points
def add(P,Q):
    x1,y1=P;x2,y2=Q
    if x1==x2: lam=(3*x1*x1+2*a2*x1+b2)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam-a2-x1-x2
    return (x3,lam*(x1-x3)-y1)
P=(Fr(1),Fr(1));P2=add(P,P);P3=add(P2,P);P5=add(P3,P2)
for (m,n) in ((P3,P),(P5,P2)):
    xp=add(m,n)[0]; xm=add(m,(n[0],-n[1]))[0]
    uu,vv=m[0],n[0]; al0=Fr(3,7)
    lhs=(uu-vv)**2*(xp-al0)*(xm-al0)
    rhs=(uu*vv-b2)**2-2*al0*((uu+vv)*(uu*vv+b2)+2*a2*uu*vv)+al0**2*(uu-vv)**2
    print("identity N = (u-v)^2 (x+ - alpha)(x- - alpha) on real points:",lhs==rhs)
print("N irreducible over Q(alpha) as polynomial in (u,v,alpha):",len(factor_list(Nal)[1])==1, "; degrees in u,v:",Poly(Nal,u).degree(),Poly(Nal,v).degree())
rho=lambda x: x*(x**2-2*x+2)
# the four possible obstructions to N*(units) being a square: N must be squarefree and coprime to (u-al)(v-al)rho(u)rho(v)(u-v)
sqf=gcd(Poly(Nal,u),Poly(Nal.diff(u),u)).degree()
print("gcd(N, dN/du) has degree (0 means squarefree in u, generic alpha):",sqf)
for name,expr in (("u-alpha",u-al),("v-alpha",v-al),("rho(u)",rho(u)),("rho(v)",rho(v)),("u-v",u-v)):
    r=resultant(Nal,expr,u) if name in("u-alpha","rho(u)","u-v") else resultant(Nal,expr,v)
    print("   Res(N, %s) nonzero:"%name,r!=0)
# specialize at the six roots of h: N must stay nonconstant, squarefree, coprime -> test via resultants modulo h(alpha)
h=al**6-6*al**5-15*al**4+100*al**3-189*al**2+162*al-54
# discriminant of N in u (as a polynomial in v, alpha) and check it does not vanish identically modulo h
D=discriminant(Poly(Nal,u),u)
Dp=Poly(D,v)
nz=[c for c in Dp.all_coeffs() if gcd(Poly(c,al),Poly(h,al)).degree()==0 or Poly(c,al).rem(Poly(h,al))!=0]
print("disc_u(N) is not identically 0 modulo h(alpha) (so N is squarefree for each root alpha of h):",len(nz)>0)
