# SageMath. Symbolic check of the known non-torsion candidate section.
# Checks equation only; non-torsion requires separate height argument.
from sage.all import *
K=FractionField(PolynomialRing(QQ,'c')); c=K.gen()
R=PolynomialRing(K,'t'); t=R.gen()
N=c*(c*c-4)*t*t-16*t+c**3+4*c
X=c*(1+t*t)*N
Y=(1+t*t)*N*N
rhs=X**3+4*(1-t**4)*N**2*X-16*t*(1+t*t)**2*N**3
print("Section identity:",Y**2==rhs)
assert Y**2==rhs
