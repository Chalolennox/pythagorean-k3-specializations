import sys, math
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
import numpy as np
def add(P,Q,a2,a4):   # y^2 = x^3 + a2 x^2 + a4 x + a6 (a6 irrelevant for addition)
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2:
        if y1+y2==0:return None
        lam=(3*x1*x1+2*a2*x1+a4)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam-a2-x1-x2
    return (x3,lam*(x1-x3)-y1)
def digits(q): 
    q=Fr(q);return max(len(str(abs(q.numerator))),len(str(q.denominator)))
# C2: y^2=z^3-2z^2+2z, P=(1,1), t=1-z ; C4': v^2=w^3+8, R=(1,3), t=(w-2)/(w+2)
P=(Fr(1),Fr(1));Q=P;R=(Fr(1),Fr(3));S=R
print(" n | digits of t_n on C2 | digits of t_n on C4'")
d2=[];d4=[]
for n in range(1,13):
    if n>1: Q=add(Q,P,-2,2);S=add(S,R,0,0)
    t2=1-Q[0]; t4=(S[0]-2)/(S[0]+2)
    d2.append(digits(t2));d4.append(digits(t4))
    print("%2d | %8d | %8d"%(n,d2[-1],d4[-1]))
# canonical-height proxy: digits/n^2 for large n
print("digits/n^2 at n=12:  C2 %.3f   C4' %.3f  -> ratio of canonical heights ~ %.2f"%(d2[-1]/144,d4[-1]/144,(d4[-1]/144)/(d2[-1]/144)))
# brute-force count of rational points t=u/v with height <= B on the covers (homogeneous quartics w^2=G(u,v))
B=3000
u=np.arange(-B,B+1,dtype=np.int64)[:,None];v=np.arange(1,B+1,dtype=np.int64)[None,:]
from math import gcd
def count(G,name):
    val=G(u,v)
    ok=(val>=0)
    r=np.zeros_like(val)
    r[ok]=np.round(np.sqrt(val[ok].astype(np.float64))).astype(np.int64)
    sq=ok&(r*r==val)
    pts=[]
    us,vs=np.nonzero(sq)
    for i,j in zip(us,vs):
        uu=int(u[i,0]);vv=int(v[0,j])
        if gcd(abs(uu),vv)==1: pts.append((uu,vv))
    # sizes
    Bs=[10,30,100,300,1000,3000]
    cnt=[sum(1 for (a,b) in pts if max(abs(a),b)<=bb) for bb in Bs]
    print("%-34s # {t: H(t)<=B} for B=%s : %s"%(name,Bs,cnt))
    return pts
count(lambda u,v: v*(v-u)*(u*u+v*v),"C2   w^2=(1-t)(1+t^2)")
count(lambda u,v: (v-u)*v*(v*v+3*u*u),"C4'  w^2=(1-t)(1+3t^2)")
count(lambda u,v: (u*u+v*v)*(3*u*u-u*v+5*v*v),"C4 (c=4) w^2=(1+t^2)(3t^2-t+5)")
count(lambda u,v: (u*u+v*v)*(-3*u*u-16*u*v+5*v*v),"C1 (c=1) w^2=(1+t^2)(-3t^2-16t+5)")
