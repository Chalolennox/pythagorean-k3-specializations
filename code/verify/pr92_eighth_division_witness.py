#!/usr/bin/env python3
from math import isqrt
p=557057
i=33793
assert all(p%d for d in range(2,isqrt(p)+1))
assert i*i%p==p-1
def sq(a):
    return pow(a%p,(p-1)//2,p)
def check_half(x,z):
    assert all(sq(a) in (0,1) for a in (x,x-1-i,x-1+i))
    assert ((z*z-2)**2-4*x*z*(z*z-2*z+2))%p==0
    assert sq(z*(z*z-2*z+2))==1
for path in ([0,430743,308029,34137,522809,553857],
             [33794,205976,111554,384197,97345,52490]):
    for x,z in zip(path,path[1:]):
        check_half(x,z)
    print("32-fold division of independent 2-torsion: PASS",path)
# Enumerate all quarter x-coordinates via duplication.
xs=[428778,165073,322336,436026,414355,94366,303611,249989,
    465492,28594,240403,431434,183370,480057,538146,231499]
def dx(z):
    return (z*z-2)**2*pow(4*z*(z*z-2*z+2)%p,-1,p)%p
assert len(set(xs))==16
for x in xs:
    assert sq(x*(x*x-2*x+2))==1
    assert dx(dx(x))==1
    assert [sq(x),sq(x-1-i),sq(x*(x-1-i))]==[1,p-1,p-1]
    print(x,1,-1,-1)
print("All 16 quarter-point x coordinates: PASS")
print("Classes 2 and 3 excluded from T64; class 1 containment unresolved")
