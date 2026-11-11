"""Stability test above level 32.  Assume the image at level 64 is the FULL preimage P_64 of I_32 (i.e. no new constraint at level 64).  Then the Liang-Rouse weights at level 64
predict the odd-order density in every class mod 64.  Compare with the measured fractions for p <= 10^8 (data/odd_order_classes_C_P_1e8.txt).
If the true image mod 64 were a proper subgroup of P_64 (a new constraint), the prediction would deviate, as the full-preimage predictions did at levels 16 and 32 (26 sigma and 213 sigma).
Usage: python3 stability_mod64.py [r1,r2,...]  (residues mod 32 to treat, default 1,31; 'all' for all 16 odd classes, about 5 minutes per 2 classes)."""
import json, os, sys, re, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from image import generate
from density import mu, agl_size
data = json.load(open(os.path.join(HERE, 'image_generators_-2_1_1.json')))
I5 = generate([tuple(g) for g in data['5']['generators']], 32); m = agl_size(5)//len(I5)         # index of the full preimage in AGL_2 (same at level 64)
arg = sys.argv[1] if len(sys.argv) > 1 else '1,31'
res = [r for r in range(1, 32, 2)] if arg == 'all' else [int(x) for x in arg.split(',')]
meas = {}
for line in open(os.path.join(HERE, '..', '..', 'data', 'odd_order_classes_C_P_1e8.txt')):
    mm = re.match(r'\s*p = (\d+) mod 64: (\d+) primes, odd-order fraction ([0-9.]+)', line)
    if mm: meas[int(mm.group(1))] = (int(mm.group(2)), float(mm.group(3)))
t0 = time.time(); out = {}
for r in res:
    num = {r: Fr(0), r + 32: Fr(0)}; cnt = {r: 0, r + 32: 0}
    for g in I5:
        if (g[2]*g[5] - g[3]*g[4]) % 32 != r: continue
        for lift in range(64):
            s = [(lift >> i) & 1 for i in range(6)]; e, f, a, b, c, d = (g[i] + 32*s[i] for i in range(6))
            j = (a*d - b*c) % 64; cnt[j] += 1; num[j] += mu(6, (e, f), ((a, b), (c, d)), m)
    for j in (r, r + 32):
        pred = num[j]*len(I5)*64/cnt[j]                      # class density = (sum of weights over the class) / (measure of the class)
        n, fr = meas[j]; se = (fr*(1 - fr)/n)**0.5
        out[j] = (float(pred), fr, (fr - float(pred))/se)
        print("p = %2d mod 64: predicted (stable above level 32) %.5f   measured %.5f (%d primes, se %.5f)   difference %+.1f sigma" % (j, float(pred), fr, n, se, (fr - float(pred))/se), flush=True)
print("[%.0fs]" % (time.time() - t0))
