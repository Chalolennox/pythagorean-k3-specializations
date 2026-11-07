# SageMath. Reconstructed genus-three norm-square obstruction.
from sage.all import *
R=PolynomialRing(QQ,'c'); c=R.gen()
H=(c*c+4)*(c**6+36*c**4-1024)
print("H(c) =",H)
print("Factorization =",H.factor())
print("Squarefree =",H.is_squarefree())
if H.is_squarefree(): print("Smooth hyperelliptic genus =", (H.degree()-1)//2)
for a in [QQ(1)/4,QQ(1)/3,QQ(1)/2,QQ(2)/3,QQ(3)/4,
          QQ(1),QQ(5)/4,QQ(4)/3,QQ(3)/2,QQ(5)/2,QQ(3),QQ(4)]:
    v=H(a)
    print("c =",a,"H(c) =",v,"rational square =",v.is_square())
