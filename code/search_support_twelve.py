#!/usr/bin/env python3
"""Search for a prime p with |S_{p,j}| = 12 (all six roots of H qualifying, both signs of the index).

Usage:  python3 code/search_support_twelve.py LIMIT          (stdlib only; no numpy)
Input:  primes p <= LIMIT.
Output: one line per prime/branch that passes the necessary filters of
        notes/REVIEW_2026-11-22_support_structure_proved.md (Prop. 4), with the number of the six
        x-values 1-t that actually lie in the orbit <P> (branch 0) or <P>+T (branch 1), and a final
        'FULL 12' list.
Filters (all proved necessary there): p = 1 mod 24 (branch 0) or p = 1, 5 mod 24 (branch 1);
        C(s)=s^3-30s^2-24s-1 splits completely mod p with all three roots squares (so H has 6 roots);
        g(t) is a square, Q=(1-t, .) lies on the curve, and x(nP) is a square, for each of the 6 roots t.
Only the last test (membership of the six x-values in the orbit) needs the orbit itself.
Result recorded in data/support_twelve_search_3e7.txt (LIMIT = 30000000, about 6 minutes; the first 3000000 take 8 seconds).
Derived with a language model; no human check."""
import sys, random
LIM=int(sys.argv[1])
def primes(n):
    s=bytearray([1])*(n+1);s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
def chi(a,p):
    a%=p
    if a==0: return 0
    return 1 if pow(a,(p-1)//2,p)==1 else -1
# polynomials low->high mod p; modulus C(s)=s^3-30s^2-24s-1
def red(a,p):
    a=a[:]
    for k in range(len(a)-1,2,-1):
        c=a[k]
        if c:
            a[k-3]=(a[k-3]+c)%p; a[k-2]=(a[k-2]+24*c)%p; a[k-1]=(a[k-1]+30*c)%p
        a.pop()
    while len(a)<3:a.append(0)
    return [x%p for x in a]
def mul(a,b,p):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): r[i+j]=(r[i+j]+x*y)%p
    return red(r,p)
def pw(base,e,p):
    r=[1,0,0]
    while e:
        if e&1: r=mul(r,base,p)
        base=mul(base,base,p); e>>=1
    return r
def trim(a):
    a=a[:]
    while a and a[-1]==0:a.pop()
    return a
def pmod(a,b,p):
    a=trim(a);b=trim(b);inv=pow(b[-1],-1,p)
    while len(a)>=len(b):
        c=a[-1]*inv%p;sh=len(a)-len(b)
        for i,x in enumerate(b): a[sh+i]=(a[sh+i]-c*x)%p
        a=trim(a)
    return a
def pgcd(a,b,p):
    a=trim(a);b=trim(b)
    while b: a,b=b,pmod(a,b,p)
    inv=pow(a[-1],-1,p); return [x*inv%p for x in a]
def roots_split(p):
    Cp=[(-1)%p,(-24)%p,(-30)%p,1]
    xp=pw([0,1,0],p,p)
    if xp!=[0,1,0]: return None
    rts=[]
    def split(f):
        if len(f)==2: rts.append((-f[0])%p);return
        while True:
            a=random.randrange(p)
            r=pw([a,1,0],(p-1)//2,p)
            r=[(r[0]-1)%p,r[1],r[2]]
            g=pgcd(f,r,p)
            if 1<len(g)<len(f):
                q=pdiv(f,g,p)
                split(g);split(q);return
    split(Cp)
    return rts
def pdiv(a,b,p):
    a=trim(a);b=trim(b);inv=pow(b[-1],-1,p);q=[0]*(len(a)-len(b)+1)
    while len(a)>=len(b):
        c=a[-1]*inv%p;sh=len(a)-len(b);q[sh]=c
        for i,x in enumerate(b): a[sh+i]=(a[sh+i]-c*x)%p
        a=trim(a)
    return q
def tonelli(a,p):
    q=p-1;s=0
    while q%2==0:q//=2;s+=1
    z=2
    while chi(z,p)!=-1:z+=1
    m=s;c=pow(z,q,p);t=pow(a,q,p);r=pow(a,(q+1)//2,p)
    while t!=1:
        i=0;tt=t
        while tt!=1:tt=tt*tt%p;i+=1
        b=pow(c,1<<(m-i-1),p);m=i;c=b*b%p;t=t*c%p;r=r*b%p
    return r
def orbit_xset(p):
    x,y=1,1;S=set()
    while True:
        S.add(x)
        if x==1:
            if (y+1)%p==0: break
            lam=(3*x*x-4*x+2)*pow(2*y,-1,p)%p
        else: lam=(1-y)*pow(1-x,-1,p)%p
        x3=(lam*lam+1-x)%p; y3=(-y+lam*(x-x3))%p
        x,y=x3,y3
    return S
found=[];cand=0
for p in primes(LIM):
    if p<29 or p%24 not in (1,5): continue
    rts=roots_split(p)
    if not rts: continue
    ts=[]
    ok=True
    for s in rts:
        if chi(s,p)!=1: ok=False;break
        t=tonelli(s,p);ts+=[t,(-t)%p]
    if not ok: continue
    for j in (0,1):
        good=True
        for t in ts:
            gv=2*t*(1-t*t)%p
            if chi(gv,p)!=1: good=False;break
            xq=(1-t)%p
            if chi(xq*(xq*xq-2*xq+2),p)!=1: good=False;break       # Q on curve
            xn=xq if j==0 else 2*pow(xq,-1,p)%p                      # x(nP)
            if chi(xn,p)!=1: good=False;break
        if not good: continue
        cand+=1
        X=orbit_xset(p)
        need=[(1-t)%p if j==0 else 2*pow((1-t)%p,-1,p)%p for t in ts]
        inn=sum(1 for xx in need if xx in X)
        print('p=%d (p%%24=%d) branch %d: filters passed; x-values in <P>: %d of 6 (|S|=%d)'%(p,p%24,j,inn,2*inn),flush=True)
        if inn==6: found.append((p,j))
print('done up to',LIM,'filter-survivors',cand,'FULL 12:',found)
