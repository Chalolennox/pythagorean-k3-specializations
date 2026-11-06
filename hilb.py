exec(open('eps.py').read().split('if __name__')[0])
from fractions import Fraction as Fr
def sqfree_int(q):
    # rational q != 0 -> integer with same square class
    q=Fr(q); return q.numerator*q.denominator
def val(n,p):
    k=0
    while n%p==0: n//=p;k+=1
    return k,n
def leg(u,p):
    u%=p
    r=pow(u,(p-1)//2,p)
    return 1 if r==1 else -1
def hilbert(a,b,p):
    a=sqfree_int(a);b=sqfree_int(b)
    if p==0:   # infinity
        return -1 if (a<0 and b<0) else 1
    al,u=val(a,p);be,v=val(b,p)
    if p==2:
        e=lambda x:((x-1)//2)%2; w=lambda x:((x*x-1)//8)%2
        ex=(e(u)*e(v)+al*w(v)+be*w(u))%2
        return -1 if ex else 1
    s=(-1)**(al*be*((p-1)//2))
    return s*(leg(u,p)**be if be else 1)*(leg(v,p)**al if al else 1)
def Fpoly(t): return t**6-30*t**4-24*t**2-1
bad=0;tot=0;detail=[]
for D in range(1,8):
    V=D*D
    for U in range(-120,3*V+40):
        if gcd(abs(U),V)!=1 or U==0: continue
        t=Fr(U,V)
        if t in (1,-1): continue
        try: f,s,_=pieces(t)
        except Exception: continue
        eps=f*s
        prod=1
        for p in (2,3,0):
            prod*=hilbert(2*t*(1-t*t),Fpoly(t),p)*hilbert(-1,t,p)*hilbert(-6,1-t*t,p)
        tot+=1
        if eps!=f*prod: bad+=1;detail.append((U,V,eps,f*prod))
print("eps(t)=f(t)*prod_{v in {2,3,inf}} (2t(1-t^2),F)_v (-1,t)_v (-6,1-t^2)_v : %d / %d agree (t=U/V, V=D^2, D<=7, all real positions of t)"%(tot-bad,tot))
print(detail[:5])
