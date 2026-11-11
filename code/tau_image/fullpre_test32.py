"""Level 32: class densities mod 32 from I32 (computed) and from the FULL preimage of I16, versus the measured ones (p <= 10^8)."""
import json, re, math
from fractions import Fraction as Fr
from image import generate
from descend import class_densities
data = json.load(open('image_generators_-2_1_1.json'))
I16 = generate([tuple(g) for g in data['4']['generators']], 16)
qp, q = 16, 32
LB = [(b0, b1, b2, b3, b4, b5) for b0 in (0, 1) for b1 in (0, 1) for b2 in (0, 1) for b3 in (0, 1) for b4 in (0, 1) for b5 in (0, 1)]
P = {tuple((x + qp*b) % q for x, b in zip(g, lb)) for g in I16 for lb in LB}
cP = class_densities(P, 5)
pred = {}
for l in open('results_levels_-2_1_1.log'):
    m = re.match(r"\s+p =\s*(\d+) mod 32 \(prob [^)]*\): predicted fraction (\S+) = ([\d.]+)", l)
    if m: pred[int(m.group(1))] = float(m.group(3))
meas = {}
for l in open('../../data/odd_order_classes_C_P_1e8.txt'):
    m = re.match(r"\s+p = (\d+) mod 32: (\d+) primes, odd-order fraction ([\d.]+)", l)
    if m: meas[int(m.group(1))] = (float(m.group(3)), int(m.group(2)))
print("level 32: |I32| = 2^18 versus full preimage of I16 = 2^%d" % (len(P).bit_length() - 1))
print("%-9s %-9s %-16s %-16s" % ("p mod 32", "measured", "I32 predicts", "full preimage predicts"))
for j in sorted(pred):
    x, n = meas[j]; a = pred[j]; b = float(cP[j][0]); sg = lambda p: math.sqrt(max(p*(1 - p), 1e-12)/n)
    f = lambda p: ("%+.1fσ" % ((x - p)/sg(p))) if 0 < p < 1 else ("exact" if abs(x - p) < 1e-9 else "OFF")
    print("%-9d %-9.5f %-8.5f %-7s %-8.5f %s" % (j, x, a, f(a), b, f(b)))
