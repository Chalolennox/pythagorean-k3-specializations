# SageMath. Reconstructed exact constant-x cover genus and branch checks.
from sage.all import *
R=PolynomialRing(QQ,'c'); c=R.gen()
S=PolynomialRing(R,'t'); t=S.gen()
N=c*(c*c-4)*t*t-16*t+c**3+4*c
D=N.discriminant()
Res=N.resultant(t*t+1)
print("N =",N)
print("Discriminant in t =",D)
print("Resultant with t^2+1 =",Res)
print("Discriminant factorization =",D.factor())
print("Resultant factorization =",Res.factor())
for cc in [QQ(0),QQ(1),QQ(2),QQ(4),QQ(-3)]:
    U=PolynomialRing(QQ,'u'); u=U.gen()
    F=(u*u+1)*(cc*(cc*cc-4)*u*u-16*u+cc**3+4*cc)
    print("c =",cc,"degree =",F.degree(),"squarefree =",F.is_squarefree())
