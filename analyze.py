from sympy import symbols, Poly, Rational, factorint, factor_list, cyclotomic_poly, sqrt, gcd, ZZ, QQ, Integer
from fractions import Fraction as Fr
x=symbols('x')
def sqfree_class(fr):
    fr=Fr(fr); n,d=fr.numerator,fr.denominator
    v=n*d; sgn=-1 if v<0 else 1; v=abs(v); s=1
    for pr,e in factorint(v).items():
        if e%2: s*=pr
    return sgn*s
def newton(Ns):
    P=[None]+[-n for n in Ns]            # power sums p_k = -N_k
    e=[Fr(1)]
    for k in range(1,len(Ns)+1):
        s=Fr(0)
        for i in range(1,k+1): s+=(-1)**(i-1)*e[k-i]*P[i]
        e.append(s/k)
    return e                              # e_0..e_4
def build_R(e,p,eps,e5):
    ee=[None]*11
    for k in range(5): ee[k]=Fr(e[k])
    ee[5]=Fr(e5)
    for k in range(6,11): ee[k]=eps*Fr(p)**(2*(k-5))*ee[10-k]   # e_{10-k}=eps p^{10-2k} e_k  =>  e_j = eps p^{2(j-5)} e_{10-j}
    return ee
def Rval(ee,z):
    return sum((-1)**k*ee[k]*Fr(z)**(10-k) for k in range(11))
def analyze(p,Ns,N5=None,verbose=True):
    e=newton(Ns[:4])
    out=[]
    for eps in (1,-1):
        # determine e5
        if eps==-1:
            cand=[Fr(0)]
        else:
            # R(p)=0 gives e5 ; check R(-p)=0 as consistency
            ee0=build_R(e,p,eps,0)
            Rp=Rval(ee0,p)            # contribution without e5
            e5=Rp/Fr(p)**5            # (-1)^5 e5 p^5 + Rp = 0  => e5 = Rp/p^5
            cand=[e5]
        for e5 in cand:
            ee=build_R(e,p,eps,e5)
            ok_plus=Rval(ee,p)==0; ok_minus=Rval(ee,-p)==0
            out.append((eps,e5,ok_plus,ok_minus,ee))
    return out
def pair_factor(ee,p):
    R=Poly(sum((-1)**k*Integer(ee[k].numerator)*x**(10-k) for k in range(11)),x)
    q,r=R.div(Poly(x**2-p*p,x))
    return R,q,r
def L8_class(ee,p):
    R,q8,r=pair_factor(ee,p)
    assert r.is_zero
    v=Fr(int(q8.eval(p)))*Fr(int(q8.eval(-p)))/Fr(p)**16     # prod (1-alpha^2/p^2) over the 8 remaining roots
    return v,q8
def cyclotomic_pairs(R,p):
    """count eigenvalues of the form p*(root of unity) among the roots of R"""
    cnt=0;details=[]
    for g,m in factor_list(R.as_expr())[1]:
        gp=Poly(g,x);k=gp.degree()
        # g(p y)/p^k should be a cyclotomic polynomial
        coeffs=gp.all_coeffs()
        sc=[Fr(int(c))/Fr(p)**i for i,c in enumerate(reversed(coeffs))]  # coefficient of y^i is c_i p^i / p^k
        sc=list(reversed([Fr(int(c))*Fr(p)**(k-j)/Fr(p)**k*1 for j,c in enumerate(coeffs)]))
        # simpler: build polynomial in y exactly
        y=symbols('y')
        poly_y=Poly(sum(Integer(int(c))*(p*y)**(k-j) for j,c in enumerate(coeffs)),y)
        if all(Fr(int(c)).denominator==1 for c in poly_y.all_coeffs()) :
            # divide by p^k
            from sympy import Rational
            polyn=Poly(poly_y.as_expr()/p**k,y)
            if all(c.q==1 for c in polyn.all_coeffs()):
                for mm in range(1,61):
                    if (Poly(y**mm-1,y).rem(polyn)).is_zero:
                        cnt+=k*m;details.append((k,m,mm));break
    return cnt,details
if __name__=="__main__":
    data={7:[-2,-74,-218,2462],11:[12,-166,-1506,-11826],17:[-12,-382,-810,-270194],19:[-36,-574,5328,-268106]}
    print("VALIDATION on c=2 (paper: classes 2,2,22,1; Lambda_7=512/49, Lambda_11=1152/121, Lambda_17=1408/289, Lambda_19=484/361)")
    for p,Ns in data.items():
        res=analyze(p,Ns)
        good=[r for r in res if r[2] and r[3]]
        for eps,e5,okp,okm,ee in good:
            v,q8=L8_class(ee,p);R,_,_=pair_factor(ee,p)
            nc,det=cyclotomic_pairs(R,p)
            print("  p=%2d  eps=%+d  e5=%s  #eigenvalues of form p*zeta = %d  (rho(F_p-bar)=%d)  Lambda_p=%s  class=%d"%(p,eps,e5,nc,12+nc,v,sqfree_class(v)))
        if not good: print("  p=%d: no consistent epsilon (R(p)=0 and R(-p)=0 fail)"%p, [(r[0],r[2],r[3]) for r in res])
