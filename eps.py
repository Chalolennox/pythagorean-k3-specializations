from fractions import Fraction as Fr
from math import gcd
import sys
sys.setrecursionlimit(10000)
def jac(a,n):
    # Jacobi symbol (a/n), n odd positive, big ints, iterative
    assert n>0 and n%2==1
    a%=n;res=1
    while a:
        while a%2==0:
            a//=2
            if n%8 in (3,5): res=-res
        a,n=n,a
        if a%4==3 and n%4==3: res=-res
        a%=n
    return res if n==1 else 0
def addq(P,Q):
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2:
        if y1+y2==0:return None
        lam=(3*x1*x1-4*x1+2)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam+2-x1-x2
    return (x3,lam*(x1-x3)-y1)
W2=[(0,1),(1,0),(4,9),(8,1),(9,4),(12,9),(15,0),(15,8)]
def triple(t):
    u,v=t.numerator,t.denominator
    d=gcd(gcd(abs(v*v-u*u),abs(2*u*v)),u*u+v*v)
    return (v*v-u*u)//d,2*u*v//d,(u*u+v*v)//d
def Fs(u,v): return u**6-30*u**4*v**2-24*u**2*v**4-v**6
def pieces(t):
    u,v=t.numerator,t.denominator
    a,b,c=triple(t)
    assert c%2==1
    ci16=pow(c,-1,16);A16=(a*ci16)%16;B16=(b*ci16)%16
    w2=-1 if (A16,B16) in W2 else 1
    if c%3==0: raise ValueError("3|c")
    ci9=pow(c,-1,9);A9=(a*ci9)%9;B9=(b*ci9)%9
    w3=-1 if (A9,B9)==(3,8) else 1
    cc=abs(c)
    f=-w2*w3*jac(2,cc)
    Fv=abs(Fs(u,v))
    while Fv%2==0:Fv//=2
    while Fv%3==0:Fv//=3
    s=jac(a*b,Fv)
    return f,s,Fv
if __name__=="__main__":
    P=(Fr(1),Fr(1));pts={1:P};Q=P
    for n in range(2,12): Q=addq(Q,P);pts[n]=Q
    # test against the table: f column and eps = W*lambda
    tab={('2P',2):(-1,2),('3P',3):(-1,2),('4P',4):(-1,2),('5P',5):(-1,3),('6P',6):(1,4),('7P',7):(1,4),('8P',8):(-1,4),('9P',9):(1,5)}
    tabT={2:(1,1),3:(-1,3),4:(-1,2),5:(-1,2),6:(-1,3),7:(1,5),8:(-1,4),9:(1,4)}
    fP={2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1};fT={2:-1,3:-1,4:1,5:-1,6:1,7:1,8:1,9:-1}
    okf=okE=0;tot=0
    for n in range(2,10):
        t=1-pts[n][0]
        for lab,tv,(W,om),fexp in (("nP",t,tab[(str(n)+'P',n)],fP[n]),("nP+T",(t+1)/(t-1),tabT[n],fT[n])):
            f,s,Fv=pieces(tv)
            eps=f*s
            lam=(-1)**om
            tot+=1;okf+=(f==fexp);okE+=(eps==W*lam)
    print("f(t) matches the table column in %d/%d members; eps = f*(ab/F'') equals W*lambda in %d/%d members"%(okf,tot,okE,tot))
