import subprocess, json, time, math, sys
from fractions import Fraction as Fr
from sympy import symbols, Poly, resultant, discriminant, factorint
t=symbols('t'); f=t**6-30*t**4-24*t**2-1
def badprimes(c):
    a,b=c.numerator,c.denominator
    Nint=(a**3-4*a*b*b)*t**2-16*b**3*t+(a**3+4*a*b*b); P=Poly(Nint,t)
    bad={2,3,23}
    for expr in (discriminant(P),resultant(1+t**2,Nint,t),resultant(f,Nint,t),a**3-4*a*b*b,b):
        v=abs(int(expr))
        if v>1: bad|=set(factorint(v).keys())
    return bad
def coeffs(c,p):
    cc=(c.numerator*pow(c.denominator,-1,p))%p
    return [str((cc**3-4*cc)%p),str((-16)%p),str((cc**3+4*cc)%p)]
done={Fr(1),Fr(4),Fr(2),Fr(13,9),Fr(11,5),Fr(14,45)}
cs=sorted({Fr(a,b) for a in range(1,14) for b in range(1,5)}-done)
out=open('scan_new.jsonl','a')
for c in cs:
    bad=badprimes(c); primes=[p for p in (11,13,17,19) if p not in bad]
    rec={"c":str(c),"N":{}}
    for p in primes:
        a=coeffs(c,p); Ns=[]
        for k in (1,2,3,4):
            Ns.append(int(subprocess.run(['./fibrecount',str(p),str(k)]+a,capture_output=True,text=True).stdout.split()[2]))
        rec["N"][p]=Ns
    out.write(json.dumps(rec)+"\n");out.flush()
