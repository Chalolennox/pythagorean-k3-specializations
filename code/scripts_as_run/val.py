import sys, random
sys.set_int_max_str_digits(0)
from fractions import Fraction as Fr
from math import isqrt
def add(P,Q):
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2:
        if y1+y2==0:return None
        lam=(3*x1*x1-4*x1+2)/(2*y1)
    else: lam=(y2-y1)/(x2-x1)
    x3=lam*lam+2-x1-x2
    return (x3,lam*(x1-x3)-y1)
def vp(n,p):
    k=0
    while n%p==0:n//=p;k+=1
    return k
P=(Fr(1),Fr(1));Q=P;pts={1:P}
N=300
for n in range(2,N+1):
    Q=add(Q,P);pts[n]=Q
ok2=ok3=okz=okp=0
for n in range(1,N+1):
    x,y=pts[n];d=x.denominator;D=isqrt(d);assert D*D==d
    ok2+=(vp(D,2)==vp(n,2));ok3+=(vp(D,3)==vp(n,3))
    # depth of nP in the formal group at 2 (n even): z=-x/y, v2(z)=v2(n)
    if n%2==0:
        z=-x/y; zn,zd=z.numerator,z.denominator
        okz+=((vp(abs(zn),2)-vp(zd,2))==vp(n,2))
    else: okz+=1
print("n<=%d: v2(D_n)=v2(n): %d  v3(D_n)=v3(n): %d  formal-group depth v2(z(nP))=v2(n) (n even): %d"%(N,ok2,ok3,okz))
# doubling lemma: Q with v2(x)=-2r (r>=1): v2(x(2Q)) = v2(x)-2 exactly, from x(2Q)=(x^2-2)^2/(4x(x^2-2x+2))
bad=0;tests=0
for n in range(2,120,2):
    x=pts[n][0]
    x2=(x*x-2)**2/(4*x*(x*x-2*x+2))
    assert x2==pts[2*n][0] if 2*n<=N else True
    def v(q):
        a,b=q.numerator,q.denominator
        return vp(abs(a),2)-vp(b,2)
    tests+=1;bad+=(v(x2)!=v(x)-2)
print("doubling raises 2-adic depth by exactly 1 (x-valuation drops by 2): %d / %d"%(tests-bad,tests))
# 3-adic: v3(z(3P))=1, z=-x/y
x,y=pts[3];z=-x/y;print("z(3P)=",z,"v3=",vp(z.numerator,3)-vp(z.denominator,3))
x,y=pts[2];z=-x/y;print("z(2P)=",z,"v2=",vp(z.numerator,2)-vp(z.denominator,2))
# the elementary identity lambda(N)=chi4(N)(-1)^Omega1 on the known factorizations
def chi4(N):return 1 if N%4==1 else -1
facts={2:[23,4241],3:[307,7743563],4:[4372373,146767982243],5:[2851,12281],7:None}
for n in (2,3,4):
    ps=facts[n];Nn=1
    for p in ps:Nn*=p
    om=len(ps);om1=sum(p%4==1 for p in ps)
    print("n=%d: lambda=%d, chi4(N)*(-1)^Omega1=%d"%(n,(-1)**om,chi4(Nn)*(-1)**om1))
