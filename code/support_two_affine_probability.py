#!/usr/bin/env python3
"""Local probability beta_l that l divides j_p = [E(F_p) : <P', T'>] in the maximal affine model
Gal(K_l/Q) = F_l^2 x| GL_2(F_l)  (l odd; K_l = Q(E[l], P'/l); the l-division of T' lies in Q(E[l])).

Criterion (Kummer theory, notes/REVIEW_2026-11-19_support_two.md, section 'Second round'): for g = (A, v),
    l does not divide j_p  <=>  the class of v spans the coinvariants V / (A - I)V          (kappa_T = 0 for l odd).
This script counts all (A, v) in GL_2(F_l) x F_l^2 for l = 3, 5, 7 by brute force and asserts
    beta_l = (l^3 - l - 1) / (l^2 (l-1)^2 (l+1)),
with the derivation: P(dim ker(A-I) = 1) = (l^2-l-1)/(l (l-1)^2) fails with probability 1/l, and P(A = I) = 1/(l (l-1)^2 (l+1)) always fails.
(The formula (l^2-2)/(l^2 (l^2-1)) stated in an earlier brief is not correct: e.g. l = 3 gives 23/144, not 7/72.)
Standard library only, about 3 seconds.  Derived with a language model; no human check; no consequence for Problem H."""
import itertools
from fractions import Fraction as Fr

def beta(l):
    V = [(a, b) for a in range(l) for b in range(l)]
    tot = bad = 0
    for a, b, c, d in itertools.product(range(l), repeat=4):
        if (a * d - b * c) % l == 0: continue
        M = ((a - 1) % l, b, c, (d - 1) % l)
        im = {((M[0] * x + M[1] * y) % l, (M[2] * x + M[3] * y) % l) for x, y in V}
        for v in V:
            tot += 1
            span = {((i[0] + k * v[0]) % l, (i[1] + k * v[1]) % l) for i in im for k in range(l)}
            if len(span) != l * l: bad += 1
    return Fr(bad, tot)

for l in (3, 5, 7):
    b = beta(l)
    P1 = Fr(l * l - l - 1, l * (l - 1) ** 2); P0 = Fr(1, l * (l - 1) ** 2 * (l + 1))
    assert b == P1 / l + P0 == Fr(l ** 3 - l - 1, l ** 2 * (l - 1) ** 2 * (l + 1)), (l, b)
    assert b != Fr(l * l - 2, l * l * (l * l - 1))
    print("l = %d: beta_l = %s = %.5f" % (l, b, float(b)))
print("OK")
