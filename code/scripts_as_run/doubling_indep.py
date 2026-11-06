from sympy import symbols, Poly, resultant, factor_list, gcd, expand, QQ, sqf_list, discriminant, factorint
X,al=symbols('X alpha')
h=X**6-6*X**5-15*X**4+100*X**3-189*X**2+162*X-54
hal=h.subs(X,al)
q=(X**2-2)**2-4*al*X*(X**2-2*X+2)
Num=Poly(expand(resultant(hal,q,al)),X)           # = Res_alpha(h(alpha), q_alpha(X,1)),  h(delta(X)) = Num/(4X(X^2-2X+2))^6
print("deg Num =",Num.degree()," leading coeff",Num.LC())
# check h(delta(X)) * (4X(X^2-2X+2))^6 == Num
from sympy import cancel, together
delta=(X**2-2)**2/(4*X*(X**2-2*X+2))
chk=cancel(together(h.subs(X,delta)*(4*X*(X**2-2*X+2))**6-Num.as_expr()))
print("h(delta(X))*(4X(X^2-2X+2))^6 == Num(X):",chk==0)
fl=factor_list(Num.as_expr())
print("factorization of Num over Q: content",fl[0],"; irreducible factors (degree, multiplicity):",[(Poly(f,X).degree(),m) for f,m in fl[1]])
print("gcd(h, Num) =",gcd(Poly(h,X),Num).as_expr())
print("Num squarefree:",gcd(Num,Num.diff(X)).degree()==0)
print("h irreducible:",Poly(h,X).is_irreducible)
# conclusion for the classes modulo constants*squares in Q(X)^*
sqNum=all(m%2==0 for f,m in fl[1])
print("Num is constant*square:",sqNum,"; h is constant*square: False (irreducible) ; h*Num is constant*square:",(gcd(Poly(h,X),Num).degree()==0 and sqNum and False))
print("disc(Num) primes:",factorint(abs(int(discriminant(Num)))) if False else "skipped")
