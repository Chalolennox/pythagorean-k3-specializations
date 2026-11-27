#!/usr/bin/env python3
"""Independent check of the four 'final four' odd-saturation certificates, PR #92.

Written by Claude (a language model), independent of the PR author's scripts.
No human has checked it.  Runtime: about 15-20 seconds (stdlib only, exact integers).

CHECKS, for each certificate [l,p,N,xU,yU,xV,yV] in notes/KUMMER_ODD_SATURATION_10000.md:
  * l and p are prime, p > 3;
  * N = #E(F_p) for E: y^2 = x^3 - 2x^2 + 2x, counted directly (Legendre-symbol sum),
    and l divides N;
  * (xU,yU) lies on E, f(yU)=0 mod p and h(xU)=0 mod p (so xU is a root of h and of
    X^3-2X^2+2X-yU^2, as the gcd step claims);
  * V=[N/l]U computed by exact double-and-add equals (xV,yV), V != O, and l*V = O.
  * the count 1228 of odd primes <= 10000 is reproduced.
DOES NOT CHECK: that the gcd of h and the cubic is linear over F_p (only that xU is a
common root), that p does not divide disc(f), anything over the number field F,
the owner's compact scan through p=2,000,000, the torsion/primitivity inputs, the
reduction argument itself, or the height route.  This is evidence from Claude, not a
human check and not a Certified result.
"""
def isprime(n):
    if n<2: return False
    i=2
    while i*i<=n:
        if n%i==0: return False
        i+=1
    return True
H=lambda x:(x**6-6*x**5-15*x**4+100*x**3-189*x**2+162*x-54)
F=lambda y:(y**12-66*y**10-29922*y**8+73214*y**6-62559*y**4+22032*y**2-3456)
C=[[8431,2123831,2124612,1566839,703827,1895189,199072],
[6841,2136527,2134392,1706561,635147,1458897,1616987],
[5167,2302987,2304482,1823048,98124,2285848,162389],
[8627,2487581,2484576,2113923,169161,672642,955731]]
def add(P,Q,p):
    if P is None: return Q
    if Q is None: return P
    x1,y1=P;x2,y2=Q
    if x1==x2 and (y1+y2)%p==0: return None
    if P==Q: m=(3*x1*x1-4*x1+2)*pow(2*y1,-1,p)%p
    else: m=(y2-y1)*pow(x2-x1,-1,p)%p
    x3=(m*m+2-x1-x2)%p   # a2=-2: x3=m^2-a2-x1-x2
    return (x3,(m*(x1-x3)-y1)%p)
def mul(k,P,p):
    R=None
    while k:
        if k&1:R=add(R,P,p)
        P=add(P,P,p);k>>=1
    return R
def count(p):
    n=1
    for x in range(p):
        r=(x**3-2*x*x+2*x)%p
        if r==0:n+=1
        else:n+=1+pow(r,(p-1)//2,p) if pow(r,(p-1)//2,p)==1 else 0
    return n
print("odd primes <=10000:",sum(1 for q in range(3,10001,2) if isprime(q)))
ok=True
for l,p,N,xu,yu,xv,yv in C:
    r=[isprime(l),isprime(p),p>3,N%l==0]
    n=count(p); r.append(n==N)
    r.append((yu*yu-(xu**3-2*xu*xu+2*xu))%p==0)
    r.append(F(yu)%p==0); r.append(H(xu)%p==0)
    V=mul(N//l,(xu,yu),p)
    r+= [V is not None, V==(xv,yv), mul(l,V,p) is None]
    print(l,p,N,"count",n,"checks",r); ok&=all(r)
print("ALL PASS" if ok else "FAIL")
