"""Do the data discriminate between the computed image I_k and the FULL preimage of I_{k-1}?  Class densities mod 2^k from both, versus the measured ones (p <= 10^8)."""
import json, sys, math, re
from fractions import Fraction as Fr
from image import generate
from descend import class_densities
data = json.load(open('image_generators_-2_1_1.json'))
I = {l: generate([tuple(g) for g in data[l]['generators']], data[l]['modulus']) for l in ('3', '4')}
def preimage(S, q):
    qp = q//2; LB = [(b0, b1, b2, b3, b4, b5) for b0 in (0, 1) for b1 in (0, 1) for b2 in (0, 1) for b3 in (0, 1) for b4 in (0, 1) for b5 in (0, 1)]
    return {tuple((x + qp*b) % q for x, b in zip(g, lb)) for g in S for lb in LB}
meas16 = {}; n16 = 720000
for l in open('../../data/odd_order_classes_C_P_1e8.txt'):
    m = re.match(r"\s+p = (\d+) mod 16: (\d+) primes, odd-order fraction ([\d.]+)", l)
    if m: meas16[int(m.group(1))] = float(m.group(3))
P16 = preimage(I['3'], 16)
cI = class_densities(I['4'], 4); cP = class_densities(P16, 4)
print("level 16: |I16| = 2^%d  versus  full preimage of I8 = 2^%d" % (len(I['4']).bit_length() - 1, len(P16).bit_length() - 1))
print("%-9s %-9s %-14s %-14s" % ("p mod 16", "measured", "I16 predicts", "full preimage predicts"))
for j in sorted(meas16):
    a, b = float(cI[j][0]), float(cP[j][0])
    sg = math.sqrt(max(a*(1 - a), 1e-12)/n16)
    f = lambda p, s_: ("%+.1fσ" % ((meas16[j] - p)/s_)) if 0 < p < 1 else ("exact" if abs(meas16[j] - p) < 1e-9 else "OFF (predicted %.4f, measured %.4f)" % (p, meas16[j]))
    sgb = math.sqrt(max(b*(1 - b), 1e-12)/n16)
    print("%-9d %-9.5f %-8.5f %-8s %-8.5f %s" % (j, meas16[j], a, f(a, sg), b, f(b, sgb)))
print("densities: I16 -> %s = %.6f,  full preimage of I8 -> %s = %.6f" % (sum(cI[j][0]*cI[j][1] for j in cI), float(sum(cI[j][0]*cI[j][1] for j in cI)), sum(cP[j][0]*cP[j][1] for j in cP), float(sum(cP[j][0]*cP[j][1] for j in cP))))
