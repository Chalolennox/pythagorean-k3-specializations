# SageMath. Verify reported points at t=-46/9 lie on the curve.
# Does NOT by itself prove independence or rank exactly three.
from sage.all import *
t=QQ(-46)/9
A=(1-t*t)/(1+t*t); B=2*t/(1+t*t)
E=EllipticCurve(QQ,[0,0,0,4*A,-8*B])
pts=[(QQ(-18)/13,QQ(396)/169),
     (QQ(-242)/117,QQ(6172)/4563),
     (QQ(-243)/169,QQ(5091)/2197),
     (QQ(358)/117,QQ(20572)/4563)]
print("E =",E)
for x,y in pts:
    print((x,y),"on curve:", y*y==x*x*x+4*A*x-8*B)
print("Rank bounds =",E.rank_bounds())
