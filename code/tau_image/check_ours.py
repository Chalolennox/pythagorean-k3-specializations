"""Regression check for our curve C : y^2 = x^3 - 2x^2 + 2x, P = (1,1) ([a,c,k] = [-2,1,1]): rebuild the images mod 8, 16, 32 from the stored generators
(image_generators_-2_1_1.json, produced by levels.py), check their orders and compatibility, and recompute the densities.  Takes about 2 minutes."""
import json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from image import generate
from density import density
data = json.load(open(os.path.join(HERE, 'image_generators_-2_1_1.json'))); I = {}
for lvl in ('3', '4', '5'):
    q = data[lvl]['modulus']; I[lvl] = generate([tuple(g) for g in data[lvl]['generators']], q)
    assert len(I[lvl]).bit_length() - 1 == data[lvl]['order_log2']; print("level 2^%s: |I| = 2^%d" % (lvl, data[lvl]['order_log2']), flush=True)
red = lambda S, q: {tuple(x % q for x in g) for g in S}
assert red(I['4'], 8) == I['3'] and red(I['5'], 16) == I['4']; print("reductions are compatible: I32 -> I16 -> I8")
for lvl, expected in (('3', Fr(95, 224)), ('4', Fr(1521, 3584)), ('5', Fr(48673, 114688))):
    d = density(I[lvl], int(lvl)); print("density at level 2^%s (assuming the full preimage above it): %s = %.6f  %s" % (lvl, d, float(d), "OK" if d == expected else "MISMATCH")); assert d == expected
print("OK")
