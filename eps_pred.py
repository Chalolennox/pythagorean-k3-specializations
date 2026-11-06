from sympy import symbols, Poly, resultant, factor_list, GF, Integer
from fractions import Fraction as Fr
t=symbols('t')
f=t**6-30*t**4-24*t**2-1
def chi(a,p):
    a%=p
    return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)
def eps_pred(c,p):
    """sign of the functional equation = product of local root numbers; III and I0* places contribute +1,
       each I1 place contributes -1 if the node is split, +1 otherwise."""
    cc=(c.numerator*pow(c.denominator,-1,p))%p
    n2=(cc**3-4*cc)%p; n1=(-16)%p; n0=(cc**3+4*cc)%p
    N=n2*t**2+n1*t+n0
    fac=factor_list(f,modulus=p)[1]
    r=len(fac)                        # number of places over the roots of f
    # product over all roots t0 of f of 3*x0(t0) = 18 t (1+t^2) N /(1-t^2)
    num=Poly(18*t*(1+t**2)*N,t,modulus=p); den=Poly(1-t**2,t,modulus=p)
    fp=Poly(f,t,modulus=p)
    Rn=int(resultant(fp,num,t))%p; Rd=int(resultant(fp,den,t))%p
    Pi=Rn*pow(Rd,-1,p)%p
    return (-1)**r*chi(Pi,p), r
if __name__=="__main__":
    c2=Fr(2)
    print("validation on c=2 (true epsilon = -1 at p=7,11,17,19 from the paper's data):",[(p,eps_pred(c2,p)[0]) for p in (7,11,13,17,19)])
    c139=Fr(13,9)
    print("c=13/9:",[(p,eps_pred(c139,p)[0]) for p in (11,19,37,41)])
