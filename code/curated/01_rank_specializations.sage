# SageMath / SageCell. Reconstructed from reported successful rank calculations.
# Complete standalone script. Rank bounds, not assumed exact ranks.
from sage.all import *
values = [QQ(-46)/9, QQ(-12)/11, QQ(-17)/31, QQ(15)/8,
          QQ(-7), QQ(-4), QQ(8), QQ(-4)/3, QQ(-1)/3,
          QQ(4)/3, QQ(-7)/4, QQ(2)/5, QQ(-5)/7,
          QQ(1)/9, QQ(1)/2, QQ(1)]
for t in values:
    print("\nPARAMETER", t)
    A=(1-t*t)/(1+t*t)
    B=2*t/(1+t*t)
    E=EllipticCurve(QQ,[0,0,0,4*A,-8*B])
    print("A,B =", A,B)
    print("curve =",E)
    try:
        print("rank bounds =", E.rank_bounds())
    except Exception as err:
        print("rank bounds failed:",err)
    try:
        print("conductor =",E.conductor())
    except Exception as err:
        print("conductor failed:",err)
