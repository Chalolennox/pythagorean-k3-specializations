from sympy import symbols, Poly, gcd, factor_list, resultant, I, Rational, discriminant, expand
X=symbols('X')
h =X**6-6*X**5-15*X**4+100*X**3-189*X**2+162*X-54
hT=-54*X**6+324*X**5-756*X**4+800*X**3-240*X**2-192*X+64
Hh=Poly(h*hT,X)
print("h*hT squarefree over Q-bar (gcd with derivative = 1):",gcd(Hh,Hh.diff(X)).degree()==0, "| degree",Hh.degree())
c=Poly(X*(X**2-2*X+2),X)
print("roots of x(x^2-2x+2) among roots of h*hT: ",[ (r, Hh.eval(r)) for r in (0,1+I,1-I)])
print("h*hT*x(x^2-2x+2) squarefree-part degree: ",Poly(expand(h*hT*c.as_expr()),X).degree(),"; gcd with derivative degree:",gcd(Poly(expand(h*hT*c.as_expr()),X),Poly(expand(h*hT*c.as_expr()),X).diff(X)).degree())
