#!/usr/bin/env python3
"""Validation of the tau-image pipeline against Liang-Rouse (arXiv 1810.10583), Table 1.
 (1) the density formula on rows 1-17 (subgroups defined explicitly in the paper)              -> test_density.py
 (2) the whole pipeline (numerical coset test + descent + density) on four of their curves:
        [a,c,k]   = [3,3,1] [-3,1,3] [2,3,1] [2,-5,1]    with Table 1 densities 5/21, 10/21, 83/336, 1/7.
Needs python3, mpmath, sympy not required.  Takes about 2-3 minutes.  Exit status 0 = all match."""
import subprocess, sys, os
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
r = subprocess.run([sys.executable, os.path.join(HERE, 'test_density.py')], capture_output=True, text=True, cwd=HERE)
print(r.stdout.strip().split('\n')[-1]); ok = 'ALL ROWS 1-17 MATCH' in r.stdout
from descend import run
for (a, c, kk), expected in (((3, 3, 1), Fr(5, 21)), ((-3, 1, 3), Fr(10, 21)), ((2, 3, 1), Fr(83, 336)), ((2, -5, 1), Fr(1, 7))):
    H, chain, dens = run(a, c, kk, 3, verbose=False)
    good = (dens == expected); ok &= good
    print("[a,c,k] = [%d,%d,%d]: |im tau mod 8| = 2^%d, density %s, Table 1: %s  %s" % (a, c, kk, len(H).bit_length() - 1, dens, expected, "OK" if good else "MISMATCH"), flush=True)
print("ALL VALIDATIONS PASS" if ok else "VALIDATION FAILED"); sys.exit(0 if ok else 1)
