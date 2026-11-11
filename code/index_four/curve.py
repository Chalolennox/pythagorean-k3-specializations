import random, math
from sympy import factorint
def inv(a,p): return pow(a,-1,p)
def add(P_,Q_,p):
    if P_ is None: return Q_
    if Q_ is None: return P_
    x1,y1=P_;x2,y2=Q_
    if x1==x2:
        if (y1+y2)%p==0: return None
        l=(3*x1*x1-4*x1+2)*inv(2*y1,p)%p
    else: l=(y2-y1)*inv(x2-x1,p)%p
    x3=(l*l+2-x1-x2)%p; return (x3,(l*(x1-x3)-y1)%p)
def mul(n,P_,p):
    R=None
    while n:
        if n&1: R=add(R,P_,p)
        P_=add(P_,P_,p); n>>=1
    return R
def neg(P_,p): return None if P_ is None else (P_[0],(-P_[1])%p)
def rand_point(p):
    while True:
        x=random.randrange(1,p); y2=x*(x*x-2*x+2)%p
        if pow(y2,(p-1)//2,p)==1:
            # sqrt
            if p%4==3: y=pow(y2,(p+1)//4,p)
            else:
                from sympy import sqrt_mod
                y=sqrt_mod(y2,p)
            return (x,y)
def order_divides(P_,N,p): return mul(N,P_,p) is None
def group_order(p):
    """|C(F_p)| by baby-step giant-step on several random points; N = 0 mod 4 when p = 1 mod 4."""
    lo=p+1-2*math.isqrt(p)-2; hi=p+1+2*math.isqrt(p)+2
    cands=[N for N in range(lo,hi+1) if N%4==0] if p%4==1 else list(range(lo,hi+1))
    pts=[rand_point(p) for _ in range(6)]
    # BSGS on first point to get candidates, verify with the others
    Q=pts[0]; m=math.isqrt(hi-lo)+1
    baby={}; R=None
    for j in range(m+1):
        baby.setdefault(R,[]).append(j); R=add(R,Q,p)
    mQ=mul(m,Q,p); mQ_neg=neg(mQ,p)
    res=set()
    # find N in [lo,hi] with N*Q = O : N = lo + a with (lo*Q) + a*Q = O ; write lo+a = lo + i*m - j  -> (lo + i m) Q = j Q
    base=mul(lo,Q,p); G=base
    for i in range(0,(hi-lo)//m+2):
        for j in baby.get(G,[]):
            N=lo+i*m-j
            if lo<=N<=hi: res.add(N)
        G=add(G,mQ,p)
    good=[N for N in res if all(order_divides(Pt,N,p) for Pt in pts[1:])]
    cand=[N for N in good if (p%4!=1 or N%4==0)]
    return sorted(cand)
def point_order(P_,N,p):
    o=N
    for q in factorint(N):
        while o%q==0 and mul(o//q,P_,p) is None: o//=q
    return o
