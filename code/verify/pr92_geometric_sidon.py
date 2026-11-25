#!/usr/bin/env python3
"""Independent check for PR #92 (geometric Sidon certificate).

Written by Claude (a language model), independent of the PR author's Magma
script. No human has checked it. Stdlib only, exact integer arithmetic mod p.
Runtime: well under 1 second.

CHECKS (p = 2621, curve y^2 = x^3 - 2x^2 + 2x, h = x^6-6x^5-15x^4+100x^3-189x^2+162x-54):
  * p prime; curve discriminant -256 is a unit mod p (good reduction);
  * h has six distinct roots in F_p, h(x) coprime to Y(x)=x^3-2x^2+2x there;
  * the twelve points (a, +-sqrt(Y(a))) lie in E(F_p) and are distinct;
  * the set is closed under negation;
  * over all 78 unordered pairs (repetition allowed): exactly 6 zero sums,
    72 nonzero sums, all 72 distinct, no nonzero sum is 2-torsion;
  * the translation multiplicity table: for each R != O the number of ordered
    (Q,S) in D x D with Q-S=R is <= 2 (12 translations with mult. 1,
    60 with mult. 2, identity 12; total 144).
DOES NOT CHECK: that the char-0 argument (reduction is injective on D and
respects addition) is valid; the exceptional-prime classification; any link
to Problem H. It is evidence from Claude, not a human check or a Certified result.
"""
from itertools import combinations_with_replacement as cwr
from collections import Counter
p = 2621
assert all(p % q for q in range(2, int(p**0.5) + 1))
A2, A4 = -2, 2
assert 16 * A4**2 * (A2**2 - 4 * A4) == -256 and (-256) % p != 0
h = lambda x: (x**6 - 6*x**5 - 15*x**4 + 100*x**3 - 189*x**2 + 162*x - 54) % p
Y = lambda x: (x**3 + A2*x**2 + A4*x) % p
roots = [a for a in range(p) if h(a) == 0]
assert len(roots) == 6, roots
# simple roots: h'(a) != 0
dh = lambda x: (6*x**5 - 30*x**4 - 60*x**3 + 300*x**2 - 378*x + 162) % p
assert all(dh(a) for a in roots) and all(Y(a) for a in roots)
O = None
def neg(P): return P if P is O else (P[0], (-P[1]) % p)
def add(P, Q):
    if P is O: return Q
    if Q is O: return P
    if P[0] == Q[0]:
        if (P[1] + Q[1]) % p == 0: return O
        l = (3*P[0]**2 + 2*A2*P[0] + A4) * pow(2*P[1], -1, p) % p
    else:
        l = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p
    x = (l*l - A2 - P[0] - Q[0]) % p
    return (x, (l*(P[0] - x) - P[1]) % p)
D = []
for a in roots:
    ys = [y for y in range(p) if y*y % p == Y(a)]
    assert len(ys) == 2
    D += [(a, y) for y in ys]
assert len(D) == 12 == len(set(D))
assert all(y*y % p == Y(x) for x, y in D)
assert set(neg(Q) for Q in D) == set(D)
zero, sums = 0, []
for Q, S in cwr(D, 2):
    T = add(Q, S)
    if T is O: zero += 1
    else: sums.append(T)
assert zero == 6 and len(sums) == 72 and len(set(sums)) == 72
assert all(add(T, T) is not O for T in sums)
mult = Counter()
for Q in D:
    for S in D:
        R = add(Q, neg(S))
        if R is not O: mult[R] += 1
assert max(mult.values()) == 2
dist = Counter(mult.values())
assert dist == {1: 12, 2: 60}, dist
print("roots of h mod", p, ":", roots)
print("points:", len(D), "zero sums:", zero, "distinct nonzero sums:", len(set(sums)))
print("translation multiplicities (R != O):", dict(dist), "; identity: 12")
print("sum check:", 12*1 + 60*2 + 12, "== 144")
print("ALL CHECKS PASSED")
