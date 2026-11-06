import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from sympy import symbols, Poly, expand, resultant, factor_list, factorint, discriminant, QQ, sqrt, Rational, cancel, together
from sympy.polys.numberfields.galoisgroups import galois_group
X,U,Z=symbols('X U Z')
h =X**6-6*X**5-15*X**4+100*X**3-189*X**2+162*X-54
hT=-54*X**6+324*X**5-756*X**4+800*X**3-240*X**2-192*X+64
R=-54*U**6+648*U**5-1242*U**4-11404*U**3+62082*U**2-113832*U+73224
print("1. R irreducible over Q:",Poly(R,U).is_irreducible, "| factor_list:",[ (str(f),m) for f,m in factor_list(R)[1]] if not Poly(R,U).is_irreducible else "")
dR=discriminant(Poly(R,U)); dh=discriminant(Poly(h,X))
print("   disc(R) =",dR,"=",factorint(abs(dR))," sign",1 if dR>0 else -1)
print("   disc(h) =",dh,"=",factorint(abs(dh))," sign",1 if dh>0 else -1)
# 2. involution identity  h*hT = X^6 R(X+2/X)
rhs=sum(Poly(R,U).coeff_monomial(U**i)*X**(6-i)*(X**2+2)**i for i in range(7))
print("2. h*hT == X^6 R(X+2/X):",expand(h*hT-rhs)==0)
# 3. norm: Res_Z(Z^2-U Z+2, h(Z)) = R(U)
res=resultant(Z**2-U*Z+2,h.subs(X,Z),Z)
print("3. Res_Z(Z^2-UZ+2,h(Z)) == R(U):",expand(res-R)==0)
# 6. translated sextic
RT=expand(R.subs(U,X+2))
print("6. R(X+2) =",RT,"| irreducible:",Poly(RT,X).is_irreducible)
# 4. quadratic fields: factor degrees of R over Q(sqrt d)
for d in (-1,2,-2,3,-3,5,-5,7,-7,23,-23,69,-69,-3*23,6,-6):
    try:
        fl=factor_list(R,extension=sqrt(d))[1]
        print("   d=%4d factor degrees:"%d,[Poly(f,U).degree() for f,m in fl])
    except Exception as e: print("   d=",d,"err",e)
# Galois groups
Gh=galois_group(Poly(h,X));Gr=galois_group(Poly(R,U))
print("5. Galois group of h:",Gh[0].order(),Gh[1],"; of R:",Gr[0].order(),Gr[1])
