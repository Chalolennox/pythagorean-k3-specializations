"""Exact birational inverse certificate; requires SymPy."""
import sympy as s
x,u,v=s.symbols("x u v")
h=x**6-6*x**5-15*x**4+100*x**3-189*x**2+162*x-54
N=(x*x-2)**2
D=4*(x**3-2*x*x+2*x)
A=s.Poly(sum(c*N**i*D**(6-i) for (i,),c in s.Poly(h,x).terms()),x).as_expr()
B=D**6
gcd=s.gcd(h-h.subs(x,1),A*B.subs(x,1)-A.subs(x,1)*B)
assert gcd==x-1
print("gcd",gcd)
f=h-u
g=s.rem(A-v*B,f,x)
print("remainder degree",s.degree(g,x))
ss=s.subresultants(f,g,x)
degrees=[s.degree(t,x) for t in ss]
assert degrees==[6,5,4,3,2,1,0]
print("degrees",degrees)
r=ss[-2]
M=s.Poly(r,x).coeff_monomial(x)
L=-s.Poly(r,x).coeff_monomial(1)
print("terms",len(s.Poly(L,u,v).terms()),len(s.Poly(M,u,v).terms()))
B=s.Poly(B,x)
A=s.Poly(A,x)
H=s.Poly(h,x)
def ev(p):
    p=s.Poly(p,u,v)
    hp=[H**i for i in range(20)]
    ap=[A**i for i in range(6)]
    bp=[B**i for i in range(6)]
    return sum((c*hp[i]*ap[j]*bp[5-j] for (i,j),c in p.terms()),s.Poly(0,x))
l,m=ev(L),ev(M)
assert not m.is_zero
assert l==s.Poly(x,x)*m
print("exact inverse PASS",m.degree())
# Optional expanded inverse:
if __name__=="__main__":
    import sys
    if "--expand" in sys.argv:
        print("L =",L)
        print("M =",M)
