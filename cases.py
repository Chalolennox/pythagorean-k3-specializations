from math import gcd
from sympy import factorint
Fs=lambda U,V: U**6-30*U**4*V**2-24*U**2*V**4-V**6
cases=[]
for V in (1,4,9,16,25):
    for U in range(-80,81):
        if U==0 or gcd(abs(U),V)!=1: continue
        if abs(U)==V: continue
        F=Fs(U,V)
        if abs(F)>2*10**6: continue
        fa=factorint(abs(F))
        sq=[p for p,e in fa.items() if e>=2 and p>=5]
        c0=U*U+V*V
        if sq: cases.append((abs(F),U,V,c0,fa))
cases.sort()
for c in cases[:14]: print(c)
