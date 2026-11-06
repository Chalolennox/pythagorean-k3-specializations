exec(open('hilb.py').read().split('bad=0;tot=0')[0])
from fractions import Fraction as Fr
def comps(t):
    u,v=t.numerator,t.denominator
    a,b,c=triple(t)
    ci16=pow(c,-1,16);A16=(a*ci16)%16;B16=(b*ci16)%16
    w2=-1 if (A16,B16) in W2 else 1
    ci9=pow(c,-1,9);A9=(a*ci9)%9;B9=(b*ci9)%9
    w3=-1 if (A9,B9)==(3,8) else 1
    two_c=jac(2,abs(c))
    return w2,w3,two_c
def local(t,p):
    return hilbert(2*t*(1-t*t),Fpoly(t),p)*hilbert(-1,t,p)*hilbert(-6,1-t*t,p)
P=(Fr(1),Fr(1));Q=P;pts={1:P}
for n in range(2,201):
    Q=addq(Q,P);pts[n]=Q
def seqs(transform):
    S2=[];S3=[];E=[]
    for n in range(2,201):
        t=1-pts[n][0]
        if transform: t=(t+1)/(t-1)
        w2,w3,two_c=comps(t)
        Psi2=-w2*two_c*local(t,2)      # all 2-adic data: sign, w2, (2/c), Hilbert symbols at 2
        Psi3= w3*local(t,3)            # all 3-adic data
        Pinf=local(t,0)                # real place
        S2.append(Psi2);S3.append(Psi3);E.append(Psi2*Psi3*Pinf)
    return S2,S3,E
def per(s):
    for p in range(1,40):
        if all(s[i]==s[i+p] for i in range(len(s)-p)): return p
for name,tr in (("nP",False),("nP+T",True)):
    S2,S3,E=seqs(tr)
    print("%s: Psi_2(n) (everything at 2) minimal period %s ; Psi_3(n) (everything at 3) minimal period %s ; product period %s"%(name,per(S2),per(S3),per(E)))
    print("   Psi_2, n=2..13:","".join('+' if x>0 else '-' for x in S2[:12]),"  Psi_3, n=2..13:","".join('+' if x>0 else '-' for x in S3[:12]))
# check product agrees with eps computed from Jacobi symbols
ok=0
for n in range(2,60):
    t=1-pts[n][0]
    f,s,_=pieces(t)
    w2,w3,two_c=comps(t)
    prod=-w2*two_c*local(t,2)*w3*local(t,3)*local(t,0)
    ok+=(prod==f*s)
print("Psi_2*Psi_3*Psi_inf equals eps_n computed from Jacobi symbols for n=2..59:",ok,"/ 58")
