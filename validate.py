#!/usr/bin/env python3
"""Reproduce the validation table of Appendix G.

Usage:  python3 code/validate.py          (fast: small primes, about a minute)
        python3 code/validate.py --full   (adds c = 2 at p = 17 and p = 19; several minutes)

Step 1 compiles fibrecount.c and compares the point counts N_k with the stored values.
Step 2 feeds the stored counts to lfunc.py and compares the sign, rho and the discriminant class.
Exit status 0 means that everything agrees.
"""
import subprocess, sys, os, tempfile, warnings
warnings.filterwarnings('ignore')
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lfunc

# (c, p, [N1..N4], N5 or None, expected sign, expected set of classes, counts feasible in fast mode)
TABLE = [
    (Fr(2),     7, [-2, -74, -218, 2462],       38,      -1, {2},      True),
    (Fr(2),    11, [12, -166, -1506, -11826],   None,    -1, {2},      True),
    (Fr(2),    17, [-12, -382, -810, -270194],  None,    -1, {22},     False),
    (Fr(2),    19, [-36, -574, 5328, -268106],  4354984, +1, {11},     False),
    (Fr(13, 9), 19, [-26, -714, 2602, -32554],  None,    +1, {15, 69}, True),
    (Fr(13, 9), 41, [-40, -3896, 10046, -3727844], None, -1, {47},     False),  # the count at p = 41 takes about 6 minutes
    (Fr(1),    13, [-10, -256, -1312, -17540],  None,    +1, {1},      True),
]

def coefficients(c, p):
    cc = (c.numerator * pow(c.denominator, -1, p)) % p
    return [str((cc**3 - 4*cc) % p), str((-16) % p), str((cc**3 + 4*cc) % p)]

def compile_counter():
    out = os.path.join(tempfile.mkdtemp(prefix='k3_'), 'fibrecount')     # built outside the repository
    subprocess.run(['gcc', '-O2', '-o', out, os.path.join(HERE, 'fibrecount.c')], check=True)
    return out

def count(binary, c, p, k):
    r = subprocess.run([binary, str(p), str(k)] + coefficients(c, p), capture_output=True, text=True, check=True)
    return int(r.stdout.split()[2])

def main():
    full = '--full' in sys.argv
    ok = True
    binary = compile_counter()
    print('Step 1: point counts')
    for c, p, Ns, N5, sign, classes, fast in TABLE:
        if not (fast or full):
            continue
        got = [count(binary, c, p, k) for k in (1, 2, 3, 4)]
        if N5 is not None and p <= 7:
            got.append(count(binary, c, p, 5))
        want = Ns + ([N5] if len(got) == 5 else [])
        good = got == want
        ok &= good
        print('  c=%-5s p=%2d  %s  counts %s' % (c, p, 'OK ' if good else 'FAIL', got))
    print('Step 2: L-function analysis from the stored counts')
    for c, p, Ns, N5, sign, classes, fast in TABLE:
        eps, res = lfunc.analyse(c, p, Ns)
        got_classes = {cl for (_, rho, cl) in res if rho == 14}
        good = (eps == sign) and got_classes == classes
        ok &= good
        print('  c=%-5s p=%2d  %s  sign %+d, classes %s' % (c, p, 'OK ' if good else 'FAIL', eps, sorted(got_classes)))
    print('ALL AGREE' if ok else 'MISMATCH')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
