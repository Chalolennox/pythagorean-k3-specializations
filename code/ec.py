from fractions import Fraction as Fr
from math import log
import itertools
class Curve:
    """y^2 = x^3 + a x + b over Q, exact arithmetic."""
    def __init__(s,a,b): s.a=Fr(a); s.b=Fr(b)
    def on(s,P): return P is None or P[1]**2==P[0]**3+s.a*P[0]+s.b
    def neg(s,P): return None if P is None else (P[0],-P[1])
    def add(s,P,Q):
        if P is None: return Q
        if Q is None: return P
        x1,y1=P; x2,y2=Q
        if x1==x2:
            if y1+y2==0: return None
            l=(3*x1*x1+s.a)/(2*y1)
        else: l=(y2-y1)/(x2-x1)
        x3=l*l-x1-x2
        return (x3,l*(x1-x3)-y1)
    def mul(s,n,P):
        if n<0: return s.mul(-n,s.neg(P))
        R=None
        while n:
            if n&1: R=s.add(R,P)
            P=s.add(P,P); n>>=1
        return R
def hnaive(x):
    x=Fr(x); return log(max(abs(x.numerator),abs(x.denominator))) if x!=0 else 0.0
def chat(E,P,n=7):
    """canonical height, normalisation  lim 4^-n h(x(2^n P))  (this is Magma's/Sage's convention; checked against the paper)"""
    Q=P
    for _ in range(n): Q=E.add(Q,Q)
    return hnaive(Q[0])/4**n
def pairing(E,P,Q,n=7): return (chat(E,E.add(P,Q),n)-chat(E,P,n)-chat(E,Q,n))/2
def gram(E,pts,n=7):
    k=len(pts); G=[[0.0]*k for _ in range(k)]
    for i in range(k):
        G[i][i]=chat(E,pts[i],n)
        for j in range(i): G[i][j]=G[j][i]=pairing(E,pts[i],pts[j],n)
    return G
def det3(G): 
    (a,b,c),(d,e,f),(g,h,i)=G
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
