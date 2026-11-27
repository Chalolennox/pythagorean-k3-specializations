"""Independent stdlib-only spot check for PR #92 (birational inverse claim).

Written by Claude (a language model), independent of the PR author's scripts
(it does not use SymPy and does not use code/verify/pr92_birational_inverse.py).
No human has checked it.  Runtime: well under 1 minute.

What it checks (exact rational arithmetic, fractions.Fraction):
  h(x)=x^6-6x^5-15x^4+100x^3-189x^2+162x-54, N=(x^2-2)^2, D=4(x^3-2x^2+2x),
  B=D^6, A=D^6*h(N/D)  (as in the note).  For many specific rational x0, the
  polynomials in Z   h(Z)-h(x0)   and   A(Z)B(x0)-A(x0)B(Z)   have gcd exactly
  Z-x0 (degree 1).  By specialization this is consistent with the claim that
  the generic gcd is Z-X, i.e. Q(h, A/B)=Q(x).
What it does NOT check: the subresultant polynomials L, M, their term counts,
the identity L(h,A/B)=x*M(h,A/B), or the degree-200 denominator.  A finite set
of specializations is evidence only, not a proof; not a Certified result.
"""
from fractions import Fraction as F

def padd(a, b):
    n = max(len(a), len(b)); r = [F(0)] * n
    for i, c in enumerate(a): r[i] += c
    for i, c in enumerate(b): r[i] += c
    return trim(r)
def trim(a):
    while a and a[-1] == 0: a.pop()
    return a
def pmul(a, b):
    if not a or not b: return []
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return trim(r)
def pscale(a, k): return trim([c * k for c in a])
def ppow(a, n):
    r = [F(1)]
    for _ in range(n): r = pmul(r, a)
    return r
def pcompose_rat(coeffs, Np, Dp, d):
    # D^d * h(N/D) = sum c_i N^i D^(d-i)
    r = []
    for i, c in enumerate(coeffs):
        r = padd(r, pscale(pmul(ppow(Np, i), ppow(Dp, d - i)), c))
    return r
def pmod(a, b):
    a = a[:]
    while len(a) >= len(b) and a:
        k = a[-1] / b[-1]; s = len(a) - len(b)
        for i, c in enumerate(b): a[s + i] -= k * c
        trim(a)
    return a
def pgcd(a, b):
    while b: a, b = b, pmod(a, b)
    return pscale(a, 1 / a[-1])
def ev(a, x):
    r = F(0)
    for c in reversed(a): r = r * x + c
    return r

h = [F(c) for c in (-54, 162, -189, 100, -15, -6, 1)]
Np = ppow([F(-2), F(0), F(1)], 2)
Dp = pscale([F(0), F(2), F(-2), F(1)], 4)
B = ppow(Dp, 6)
A = pcompose_rat(h, Np, Dp, 6)
bad = 0; n = 0
for x0 in [F(p, q) for p in range(-9, 10) for q in (1, 2, 3, 5) if p != 0]:
    if ev(Dp, x0) == 0: continue
    f = padd(h, [-ev(h, x0)])
    g = padd(pscale(A, ev(B, x0)), pscale(B, -ev(A, x0)))
    gd = pgcd(f, g); n += 1
    if gd != [-x0, F(1)]:
        bad += 1; print("gcd differs at", x0, gd)
print("specializations tested", n, "mismatches", bad)
print("PASS" if bad == 0 else "FAIL")
