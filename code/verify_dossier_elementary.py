#!/usr/bin/env python3
"""Cross-check of code/coq/Dossier_crt_two_adic.v, Dossier_sextic_F26.v and Dossier_Fs_g_hom.v by exact integer arithmetic (stdlib only; about 1 s).

Written by Claude (a language model), 23 November 2026; no human has checked it.  It does NOT replace the Coq compilation (CI job `coq`); it
reads the Definitions and the statement of sextic_cleared_identity out of the .v files themselves, evaluates them in Python integers, and checks every
polynomial identity the file proves at many integer points, plus brute-force checks of the CRT and 2-adic statements on small ranges.  A typo in a
transcribed coefficient therefore fails here even before Coq is run.  Exit status 0 iff every check passes.
"""
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "\n".join(open(os.path.join(HERE, "coq", f)).read() for f in ("Dossier_crt_two_adic.v", "Dossier_sextic_F26.v", "Dossier_Fs_g_hom.v"))
ok_all = True


def check(name, cond):
    global ok_all
    print(("ok   " if cond else "FAIL ") + name)
    ok_all = ok_all and cond


def definition_body(name):
    m = re.search(r"Definition\s+" + re.escape(name) + r"\s*\(([^)]*)\)\s*:\s*Z\s*:=\s*(.*?)\.\s*\n", SRC, re.S)
    assert m, name
    args = m.group(1).split(":")[0].split()
    return args, m.group(2)


def pyfun(name):
    args, body = definition_body(name)
    expr = " ".join(body.split()).replace("^", "**")
    code = compile(expr, name, "eval")
    return lambda *a: eval(code, {}, dict(zip(args, a)))


hZ, hT, RZ, Rcof, Fs, Fs_cof, g_hom = (pyfun(n) for n in ["hZ", "hT", "RZ", "Rcof", "Fs", "Fs_cofactor", "g_hom"])

# the right-hand side of sextic_cleared_identity, read from the file
m = re.search(r"sextic_cleared_identity :\s*forall X : Z,\s*hZ X \* hT X =\s*(.*?)\.\s*Proof", SRC, re.S)
assert m
rhs_src = " ".join(m.group(1).split()).replace("^", "**")
rhs = lambda X: eval(rhs_src, {}, {"X": X})

random.seed(23112026)
pts = [random.randint(-60, 60) for _ in range(200)]

check("hZ(x) = H(1-x), H(t) = t^6 - 30 t^4 - 24 t^2 - 1 (Fs(t,1))",
      all(hZ(x) == Fs(1 - x, 1) for x in pts))
check("sextic_cleared_identity: h(X) hT(X) = sum r_k (X^2+2)^k X^(6-k), 200 points",
      all(hZ(X) * hT(X) == rhs(X) for X in pts))
# the same identity from the definition of R as a polynomial: X^6 R(X + 2/X) with exact fractions
from fractions import Fraction
check("hZ(X) hT(X) = X^6 R(X + 2/X) with exact fractions, X != 0",
      all(Fraction(hZ(X) * hT(X)) == Fraction(X) ** 6 * RZ(Fraction(X) + Fraction(2, X)) for X in pts if X != 0))
check("hT(X) = X^6 h(2/X) with exact fractions",
      all(Fraction(hT(X)) == Fraction(X) ** 6 * hZ(Fraction(2, X)) for X in pts if X != 0))
check("sextic_norm_cofactor: R(z1+z2) - h(z1)h(z2) = (z1 z2 - 2) Rcof, 400 pairs",
      all(RZ(a + b) - hZ(a) * hZ(b) == (a * b - 2) * Rcof(a, b) for a, b in ((random.randint(-30, 30), random.randint(-30, 30)) for _ in range(400))))
# norm identity at honest rational points: z1 z2 = 2 with z1 = p/q, z2 = 2q/p
rat = [Fraction(p, q) for p in range(-9, 10) if p for q in range(1, 8)]
check("sextic_norm_identity at rational pairs (z, 2/z)",
      all(RZ(z + Fraction(2) / z) == hZ(z) * hZ(Fraction(2) / z) for z in rat))

# F_s congruences
UV = [(random.randint(-40, 40), random.randint(-40, 40)) for _ in range(500)]
check("Fs_mod_U: U | Fs + V^6", all((Fs(U, V) + V ** 6) % U == 0 for U, V in UV if U))
check("Fs_mod_V: V | Fs - U^6", all((Fs(U, V) - U ** 6) % V == 0 for U, V in UV if V))
check("Fs_factorization: Fs + 54 U^6 = (V-U)(V+U) K", all(Fs(U, V) + 54 * U ** 6 == (V - U) * ((V + U) * Fs_cof(U, V)) for U, V in UV))
check("Fs(U, +-U) = -54 U^6", all(Fs(U, U) == -54 * U ** 6 == Fs(U, -U) for U in range(-20, 21)))

# g
check("g_hom_tau: g_hom(-(a+b), b-a) = 4 g_hom(a,b)", all(g_hom(-(a + b), b - a) == 4 * g_hom(a, b) for a, b in UV))
# and the rational statement it encodes: g(tau(t)) = 4 g(t)/(1-t)^4 with tau(t) = 1 - 2/(1-t)
g = lambda t: 2 * t * (1 - t * t)
tau = lambda t: 1 - Fraction(2) / (1 - t)
check("g(tau(t)) = 4 g(t)/(1-t)^4 with exact fractions",
      all(g(tau(t)) == 4 * g(t) / (1 - t) ** 4 for t in rat if t != 1))

# CRT
def crt_ok(m_, l_, a, b):
    exists = any((n - a) % m_ == 0 and (n - b) % l_ == 0 for n in range(0, m_ * l_ + 1))
    return exists == ((a - b) % math.gcd(m_, l_) == 0)

check("crt_compat brute force: m,l in 1..12, a,b in 0..11",
      all(crt_ok(m_, l_, a, b) for m_ in range(1, 13) for l_ in range(1, 13) for a in range(12) for b in range(12)))

# 2-adic covering: n - 2^j divisible by 2^(j+1) for exactly one j, for every n > 0
def classes(n):
    return [j for j in range(0, n.bit_length() + 2) if (n - 2 ** j) % 2 ** (j + 1) == 0]

check("two_adic_cover: every n in 1..5000 lies in exactly one A_(j+1)", all(len(classes(n)) == 1 for n in range(1, 5001)))
check("the class index is v_2(n)", all(classes(n) == [(n & -n).bit_length() - 1] for n in range(1, 5001)))

print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
sys.exit(0 if ok_all else 1)
