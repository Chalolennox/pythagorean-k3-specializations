# Multiplication block 1110: third witness (25 November 2026)

For J: y²=x³−2x²+2x, take x(Q)=1/3 on the quadratic twist 39y²=x³−2x²+2x (y=1/9). This is not a rational point of J itself. The twist class is 39 and the 2-isogeny descent class [39x] is 13.

Set t_k=1−x(kQ)=u/v in lowest terms, H(u,v)=u^6−30u^4v²−24u²v^4−v^6. The qualifying primes are p≥5 dividing H with Legendre symbol (2uv(v²−u²)/p)=+1. Count distinct qualifying primes.

| k | t_k | prime factors of the part of abs(H) prime to 6, with Legendre signs | count |
|---|---|---|---|
| 1 | 2/3 | 7 (+), 1823 (−) | 1 |
| 2 | −133/156 | 1699 (−), 2999 (−), 95921323 (+) | 1 |
| 3 | −250102/168507 | 7547143 (−), 572594053502898006171745007 (+) | 1 |
| 6 | 11631640620053859093467/25660687322701771922556 | 23 (−), 1156207384315456631316581 (+), 615890274633941872316574131861303 (+), 125318956991164066595458062549358158645607085882569104845849693382743479293307 (−) | 2 |

All listed exponents are one. The owner supplied the factorization of the 134-digit cofactor at k=6; its product was independently checked. The full discriminant numerator has the additional factor 23, independently checked to be nonqualifying. Thus the full prime-to-6 part has 16 divisors, whereas the supplied cofactor has 8. SymPy isprime returned True for every listed factor (probable-prime tests for large integers, not formal primality certificates). Exact rational multiplication and Legendre symbols were independently computed.

The parity matrix, with doubling horizontal and tripling vertical, is [[1,1],[1,0]] (binary code 14). Thus 39 belongs to D_1110, subject to primality of the large factors. This is not an all-odd witness, and no claim about realization on the original orbit or Problem H follows.

Reproduction (Python 3 + SymPy):

```python
from fractions import Fraction as F
from math import prod
from sympy import isprime, legendre_symbol
x = F(1,3)
f = lambda x: x*(x*x-2*x+2)
D = lambda x: (x*x-2)**2/(4*f(x))
z = D(x)
m = (3*x*x-4*x+2)/(2*f(x))
w = ((-2+m*(x-z))/(z-x))**2*f(x)+2-x-z
factors = [
 [7,1823],
 [1699,2999,95921323],
 [7547143,572594053502898006171745007],
 [23,1156207384315456631316581,615890274633941872316574131861303,125318956991164066595458062549358158645607085882569104845849693382743479293307]
]
for k,X,ps in zip([1,2,3,6],[x,z,w,D(w)],factors):
    t=1-X
    u,v=t.numerator,t.denominator
    N=abs(u**6-30*u**4*v**2-24*u*u*v**4-v**6)
    for p in [2,3]:
        while N%p==0: N//=p
    assert prod(ps)==N
    assert all(isprime(p) for p in ps)
    signs=[legendre_symbol(2*u*v*(v*v-u*u),p) for p in ps]
    print(k,t,list(zip(ps,signs)),sum(s==1 for s in signs))
```
