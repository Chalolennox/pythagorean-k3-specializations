#!/usr/bin/env python3
"""Chebotarev densities for the support-two review, read off the explicit model of G = Gal(L*/Q) (|G| = 24576)
built in code/verify_group_G.py: for each element of G, the number k of roots t of H (up to t <-> -t) with a(t), d(t)
both squares equals (fixed points of the 24-point action)/4, and the number of those with 1-t also a square is
(fixed points of the 48-point action)/8.  Needs numpy only.  Derived with a language model; floating-point signs; no human check.
Expected: |R_p| = 2 has density 3798/24576 = 633/4096; split 1926/24576 = 321/4096 (chi(1-t) = -1, class B)
and 1872/24576 = 39/512 (chi(1-t) = +1, class A)."""
import collections, io, contextlib, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_group_G.py")).read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src.split("ff=lambda p")[0])                      # defines P (48-point perms), P24 (24-point perms), psi
fx = lambda p: sum(1 for i, x in enumerate(p) if i == x)
n24 = collections.Counter(); joint = collections.Counter()
for p48, p24 in zip(P, P24):
    a = fx(p24) // 4; b = fx(p48) // 8
    n24[a] += 1; joint[(a, b)] += 1
tot = len(P); assert tot == 24576
print("density of |R_p|/2 = k:")
for k in sorted(n24): print("  k=%d: %d/24576 = %.5f" % (k, n24[k], n24[k] / tot))
A, B = joint[(1, 1)], joint[(1, 0)]
assert (A, B, A + B) == (1872, 1926, 3798)
print("|R_p| = 2: %d/24576 = 633/4096; class A (1-t square) %d/24576 = 39/512; class B (1-t nonsquare) %d/24576 = 321/4096" % (A + B, A, B))
print("OK")
