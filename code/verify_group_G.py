#!/usr/bin/env python3
"""Group G = Gal(L*/Q) (order 24576) as a permutation group on the 48 roots of Rp, built from the
three relations among the radicals; the character chi2 (action on sqrt2); fixed-point-free counts.
Needs numpy only.  Derived with a language model; no human check."""
import itertools, numpy as np
from fractions import Fraction as Fr
# ---- exact check of the s-identity: s(a)=a*w(a^2), w(z)=(26+29z-z^2)/3, s^2=3(a^4-1) mod g(z)=z^3-30z^2-24z-1
def pmul(p,q):
    r=[Fr(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): r[i+j]+=x*y
    return r
def pmod(p,m):  # m monic
    p=p[:]
    while len(p)>=len(m):
        c=p[-1]
        for k in range(len(m)): p[len(p)-len(m)+k]-=c*m[k]
        p.pop()
    return p+[Fr(0)]*(len(m)-1-len(p))
g=[Fr(-1),Fr(-24),Fr(-30),Fr(1)]
w=[Fr(26,3),Fr(29,3),Fr(-1,3)]
lhs=pmod(pmul([Fr(0),Fr(1)],pmul(w,w)),g)          # z*w(z)^2
rhs=pmod([Fr(-3),Fr(0),Fr(3)],g)                    # 3(z^2-1)
assert lhs==rhs; print("exact: z*w(z)^2 = 3(z^2-1) mod g")
# ---- numerics
z=np.sort(np.roots([1,-30,-24,-1]).astype(complex)); a=[np.sqrt(x) for x in z]
if abs(a[0]*a[1]*a[2]-1)>1e-9: a[2]=-a[2]
R=[a[0],a[1],a[2],-a[0],-a[1],-a[2]]
al=[np.sqrt(1-r) for r in R]; ga=[np.sqrt(1+a[i]**2) for i in range(3)]
gp=[np.sqrt(2*a[i]*(1-a[i]**2)) for i in range(3)]; gs=gp+[1j*x for x in gp]
sf=lambda b: b*(26+29*b*b-b**4)/3
S=[]
for pi in itertools.permutations(range(3)):
    for sg in itertools.product([1,-1],repeat=3):
        if sg[0]*sg[1]*sg[2]==1:
            m=[None]*6
            for i in range(3): m[i]=pi[i]+(0 if sg[i]==1 else 3); m[i+3]=(m[i]+3)%6
            S.append(m)
def act(m,e):
    A=[e[k]*al[m[k]] for k in range(6)]; C=[e[9+i]*ga[m[i]%3] for i in range(3)]
    Gs=[e[6+i]*gs[m[i]] for i in range(3)]; Gs+= [e[12]*e[6+i]*1j*gs[m[i]] for i in range(3)]
    return A,C,Gs
def rel(A,C,Gs):
    T=lambda k: A[k]*A[k+3]*C[k]
    return T(0)/T(1),T(1)/T(2),C[0]*C[1]*C[2]*Gs[0]*Gs[1]*Gs[2]*A[0]*A[3]*A[1]*A[4]*A[2]*A[5]
b=rel(al,ga,gs); k12=round((b[0]/(sf(R[0])/sf(R[1]))).real); k23=round((b[1]/(sf(R[1])/sf(R[2]))).real); nD=round(b[2].real)
assert abs(nD)==432; print("kappa12, kappa23, nD =",k12,k23,nD)
Gam=[]
for si,m in enumerate(S):
    t12=k12*sf(R[m[0]])/sf(R[m[1]]); t23=k23*sf(R[m[1]])/sf(R[m[2]])
    for e in itertools.product([1,-1],repeat=13):
        r=rel(*act(m,e))
        if abs(r[0]-t12)<1e-6 and abs(r[1]-t23)<1e-6 and abs(r[2]-nD)<1e-4: Gam.append((si,e))
assert len(Gam)==24576; print("|Gamma| =",len(Gam),"(= |G| by F.5, so Gamma = G)")
pts=[];lab=[]
for k in range(6):
    sq=gs[k]/(1+R[k]**2); sr=al[k]*ga[k%3]
    for e in itertools.product([1,-1],repeat=3): pts.append(e[0]*sq+e[1]*sr+e[2]*al[k]); lab.append((k,)+e)
pts=np.array(pts); assert min(abs(pts[i]-pts[j]) for i in range(48) for j in range(i))>1e-3
def p48(si,e):
    m=S[si]; A,C,Gs=act(m,e); out=[]
    for k in range(6):
        sq=Gs[k]/(1+R[m[k]]**2); sr=A[k]*C[k%3]
        for ee in itertools.product([1,-1],repeat=3):
            v=ee[0]*sq+ee[1]*sr+ee[2]*A[k]; d=abs(pts-v); j=int(np.argmin(d)); assert d[j]<1e-6; out.append(j)
    return tuple(out)
P=[p48(si,e) for si,e in Gam]; assert len(set(P))==24576
blocks={}; 
for i,(k,e1,e2,e3) in enumerate(lab): blocks.setdefault((k,e1,e2),[]).append(i)
bl=sorted(blocks); bidx={bk:n for n,bk in enumerate(bl)}; blk=lambda i: bidx[lab[i][:3]]
def p24(p):
    q=[None]*24
    for i in range(48):
        j=blk(i)
        if q[j] is None: q[j]=blk(p[i])
        assert q[j]==blk(p[i])
    return tuple(q)
P24=[p24(p) for p in P]
def orbit(perms,pt):
    o={pt}
    for p in perms: o.add(p[pt])
    return o
assert len(orbit(P,0))==48 and len(orbit(P24,0))==24   # transitive (a stabiliser-free orbit count: every image of point 0 is hit)
print("G is transitive on the 48 roots of Rp and on the 24 roots of Rm")
psi=[e[9]*e[10]*e[11] for si,e in Gam]     # chi2 = product of signs on sqrt(1+a_i^2)
assert abs(ga[0]*ga[1]*ga[2]-2*np.sqrt(2))<1e-9
ff=lambda p: all(i!=x for i,x in enumerate(p))
n48=sum(map(ff,P)); n24=sum(map(ff,P24))
Hff48=sum(1 for p,c in zip(P,psi) if c==1 and ff(p)); Hff24=sum(1 for p,c in zip(P24,psi) if c==1 and ff(p))
Cff24=sum(1 for p,c in zip(P24,psi) if c==-1 and ff(p)); Cff48=sum(1 for p,c in zip(P,psi) if c==-1 and ff(p))
print("|H| =",sum(1 for c in psi if c==1))
print("fixed-point-free: deg48 total",n48," deg24 total",n24)
print("H (chi2=+1): deg48",Hff48," deg24",Hff24,"   coset chi2=-1: deg24",Cff24," deg48",Cff48)
assert (n48,n24,Hff48,Cff24)==(22035,19709,11013,9854)
print("density of primes with no qualifying root =",Fr(Hff48+Cff24,24576),"=",(Hff48+Cff24)/24576)
