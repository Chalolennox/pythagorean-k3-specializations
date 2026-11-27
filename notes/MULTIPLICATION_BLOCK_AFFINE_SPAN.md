# Multiplication blocks: full affine span (25 November 2026)

Let a_n and b_n be the parity of the number of distinct qualifying primes on nP and nP+T, respectively (not the global root-number parity on the mirror branch). Put A_n=(a_n,a_{2n},a_{3n},a_{6n}) and B_n=(b_n,a_{2n},b_{3n},a_{6n}), in row-major order. The shared entries follow from 2T=0.

## Reused arithmetic data

The exact eligible-prime rectangle output of 24 November (through n=9) gives:
- a_1,...,a_9 = 0,1,1,1,1,0,0,1,0.
- b_1,...,b_9 = 0,1,0,1,0,1,0,1,1.

The canonical paper, F.38, records the complete probable-prime factorization at 12P, with s=3, f=+1, W=-1. Thus a_12=1. The listed factors are 23, 83, 18397, 7851197, 172604961553, 3022285517285783321, and 63444875642234219830688037601870240082732857828883494817671516344727361247789078750329402859044190800003740275757566803. No new factorization or primality certification is claimed.

## Full affine span without the quadratic-twist witness

Write z=a_18, which need not be known. The five rows, augmented by a leading 1, are:

    A_1  1 0 1 1 0
    B_1  1 0 1 0 0
    A_2  1 1 1 0 1
    A_3  1 1 0 0 z
    B_3  1 0 0 1 z

Exact Gaussian elimination over F_2 gives the identity matrix for both z=0 and z=1. Thus the affine span of the combined original and mirror blocks is all of F_2^4, on the recorded arithmetic data. Conditional on the recorded arithmetic data, every nonzero affine coefficient vector is excluded. This strengthens the earlier calculation using x=1/3: no twist witness is needed, and its factorization is not relied upon.

## Scope and stopping criterion

Conditional on the recorded arithmetic inputs, close the search for a universal affine parity identity on the union of these two branches. This does not exclude branch-specific identities, nonlinear restrictions, eventual identities, or establish recurrence of any configuration. It does not prove Problem H or exclude the all-odd block. The original branch alone remains a separate affine-span question. The arithmetic input from F.38 uses probable primes, as explicitly stated in the paper.

## Review correction: exact dependence on the arithmetic input

Proof given (ChatGPT, AI-authored; human review pending). In the displayed augmented matrix replace the last entry of A_2 by w=a_12. Add B_1 to each of the other rows, then add the resulting A_1 row to the resulting B_3 row. The four rows with leading zero, after dropping that coordinate, are (0,0,1,0), (1,0,0,w), (1,1,0,z), (0,1,0,z). Adding the last two gives (1,0,0,0); adding this to the second gives (0,0,0,w). Thus the augmented rank is 5 if w=1 and 4 if w=0, independently of z. Exact elimination independently executed by ChatGPT on all four (w,z) combinations: ranks 4,4,5,5 in lexicographic order. This confirms Claude comment 7167339349. The full-span conclusion is conditional on the recorded a_n,b_n and in particular on the probable-prime factorization in F.38; if w=0 these five rows alone do not establish full span. The original 24 November raw rectangle log has not been recovered in this review; its listed bits remain inputs, not independently verified here.

## Arithmetic corroboration (25 November 2026)

ChatGPT, AI-authored; human review pending. Historical rectangle counts reported in the preceding ChatGPT conversation (shared reference https://chatgpt.com/s/t_6b07283c7770819199e2ffe2b6a08ba2; original raw log not independently retrieved):

| n | original count | mirror count |
|---|---:|---:|
|1|0|0|
|2|1|1|
|3|1|0|
|4|1|1|
|5|1|2|
|6|2|1|
|7|2|2|
|8|1|1|
|9|0|3|

These reproduce the recorded bits, but are historical reported data, not a fresh factorization of the rectangle.

Fresh exact verification executed with Python Fraction and SymPy 1.14.0: compute 12P by twelve additions of P=(1,1), put t=1-x(12P)=u/v in lowest terms, compute abs(u^6-30u^4v^2-24u^2v^4-v^6), and remove all factors 2 and 3. The product of the seven F.38 factors listed above equals the resulting integer exactly. SymPy isprime returned True for all seven; Legendre symbols of 2uv(v^2-u^2), in the listed order, were -1,+1,+1,-1,-1,+1,-1. Thus the qualifying factors are 83, 18397, 3022285517285783321 and a_12=1 under the probable-prime input. No rigorous primality certificate for the large factor is claimed.

Reproduction code (Python 3, SymPy 1.14.0):

```python
from fractions import Fraction as F
import sympy as s
P = (F(1), F(1))
def add(A, B):
    if A is None: return B
    if B is None: return A
    x,y = A; u,v = B
    if x == u and y == -v: return None
    l = (3*x*x-4*x+2)/(2*y) if A == B else (v-y)/(u-x)
    z = l*l+2-x-u
    return z,l*(x-z)-y
Q = None
for n in range(12): Q = add(Q,P)
t = 1-Q[0]; u,v = t.numerator,t.denominator
N = abs(u**6-30*u**4*v**2-24*u*u*v**4-v**6)
for p in (2,3):
    while N%p == 0: N //= p
ps = [23,83,18397,7851197,172604961553,3022285517285783321,63444875642234219830688037601870240082732857828883494817671516344727361247789078750329402859044190800003740275757566803]
assert N == s.prod(ps)
assert all(s.isprime(p) for p in ps)
signs = [s.legendre_symbol(2*u*v*(v*v-u*u),p) for p in ps]
assert signs == [-1,1,1,-1,-1,1,-1]
print('qualifying factors:', [p for p,e in zip(ps,signs) if e==1])
```

## Owner rigorous primality verification (25 November 2026)

The owner executed the following standalone Magma script with proof enabled for the 119-digit factor. This supersedes the large-factor probable-prime qualification above. Owner-reported execution, not independently rerun by ChatGPT; human review of the full affine-span argument remains pending.

```magma
clear;
p := 63444875642234219830688037601870240082732857828883494817671516344727361247789078750329402859044190800003740275757566803;
print "Number of digits:", #IntegerToString(p);
print "Starting rigorous primality verification";
time result := IsPrime(p : Proof := true);
print "Proven prime:", result;
assert result;
print "PRIMALITY VERIFICATION: PASS";
```

Verbatim owner-pasted output:

```text
Number of digits: 119
Starting rigorous primality verification
Time: 0.330
Proven prime: true
PRIMALITY VERIFICATION: PASS

# 802ms · Magma V2.30-1 | 0.41s | 32.09MB | seed 1778788593
```

The large factor is therefore supported by a proof-enabled Magma run, not merely a probable-prime test. The other six factors are below 2^64 and covered by the deterministic range of SymPy isprime. The recorded factorization and eligibility computation support a_12=1. The historical rectangle counts remain a separate provenance dependency; the raw rectangle log has not been recovered. No claim of a new Problem H result. Record added by ChatGPT (AI-authored).
