import random, sys
from math import gcd
from sympy import factorint, symbols, expand
# Delta = 2^12 c0^9 F ?  c4 prime to p | F ?  split iff (-c6/p) = (ab/p) ?
U_,V_=symbols('U V')
F=U_**6-30*U_**4*V_**2-24*U_**2*V_**4-V_**6
Delta=-16*(4*(4*(V_**2-U_**2)*(U_**2+V_**2)**3)**3+27*(16*U_*V_*(U_**2+V_**2)**5)**2)
print("Delta == 2^12 (U^2+V^2)^9 F(U,V):",expand(Delta-2**12*(U_**2+V_**2)**9*F)==0)
def leg(a,p):
    a%=p
    return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)
random.seed(5);tot=bad4=badsplit=0
for _ in range(400):
    V=random.choice([1,4,9,25]);U=random.randint(-60,60)
    if U==0 or gcd(abs(U),V)!=1 or abs(U)==V: continue
    Fv=U**6-30*U**4*V**2-24*U**2*V**4-V**6
    c0=U*U+V*V;a4=4*(V*V-U*U)*c0**3;a6=-16*U*V*c0**5;c4=-48*a4;c6=-864*a6
    a=V*V-U*U;b=2*U*V;d=gcd(gcd(abs(a),abs(b)),c0);a//=d;b//=d
    for p,e in factorint(abs(Fv)).items():
        if p<5: continue
        tot+=1
        if c4%p==0: bad4+=1
        if leg(-c6,p)!=leg(a*b,p): badsplit+=1
print("primes p>=5 dividing F in %d cases: p | c4 in %d; (-c6/p) != (ab/p) in %d"%(tot,bad4,badsplit))
