"""Confirms that the computed images belong to EXACTLY  C : y^2 = x^3 - 2x^2 + 2x,  P = (1,1)  and are independent of the arbitrary choices in the construction.
 1. parameter map [a,c,k] = [-2,1,1]  ->  E : y^2 = x^3 + a x^2 + b x, alpha = (c, c k), b = c k^2 - a c - c^2
 2. the numerical objects: curve equation of alpha, of the torsion basis and of the whole chain beta_j, 2^k beta_k = alpha, orders of A_k and B_k, T = (0,0)
 3. the data side: independent recomputation of the odd-order fraction by naive point counting (no BSGS, no shared code) against the C program
 4. frame independence: the image orders at levels 8 and 16 for other branch choices when halving (TAU_CHOICE)"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf
from fractions import Fraction as Fr
a, c, kk = -2, 1, 1; b = c*kk*kk - a*c - c*c
print("1. [a,c,k] = [%d,%d,%d] -> b = %d: E : y^2 = x^3 + (%d) x^2 + %d x = x^3 - 2x^2 + 2x : %s ;  alpha = (%d, %d) = (1,1) : %s" %
      (a, c, kk, b, a, b, (a, b) == (-2, 2), c, c*kk, (c, c*kk) == (1, 1)))
assert (a, b, c, c*kk) == (-2, 2, 1, 1) and c**3 + a*c**2 + b*c == (c*kk)**2        # alpha lies on E:  1 - 2 + 2 = 1
from image import Curve
C = Curve(a, c, kk, 4)
on = lambda P: abs(P[1]**2 - (P[0]**3 + C.a*P[0]**2 + C.b*P[0])) < mpf(10)**(-80)
assert C.a == -2 and C.b == 2
alpha = (mp.mpc(1), mp.mpc(1)); assert on(alpha) and C.same(C.beta[0], alpha)
assert all(on(B) for B in C.beta) and on((C.A[0], C.A[1])) and on((C.B[0], C.B[1]))
assert C.same(C.mul(2**4, C.beta[4]), alpha) and all(C.same(C.add(C.beta[j], C.beta[j]), C.beta[j-1]) for j in range(1, 5))
T = (mp.mpc(0), mp.mpc(0)); T1 = ((2 + mp.sqrt(-4))/2, mp.mpc(0))
print("2. numerical objects at level 16: curve a = %s, b = %s; alpha = (1,1) on E; all beta_j (j <= 4) on E with 2 beta_j = beta_{j-1} and 2^4 beta_4 = alpha;" % (C.a, C.b))
print("   2^3 B_4 = (0,0) = T : %s ; 2^3 A_4 = (1+i, 0) : %s ; A_4, B_4 on E" % (C.same(C.mul(8, C.B), T), C.same(C.mul(8, C.A), T1)))
# 3. independent naive recomputation of the odd-order fraction up to 20000 (brute-force group order; order of P by trial division of that order)
def naive(pmax):
    odd = tot = 0
    for p in range(3, pmax):
        if any(p % q == 0 for q in range(2, int(p**0.5) + 1)): continue
        n = 1                                                                 # point count by Legendre symbols
        for x in range(p):
            v = (x**3 - 2*x*x + 2*x) % p; n += 1 if v == 0 else (2 if pow(v, (p - 1)//2, p) == 1 else 0)
        def add(P, Q):
            if P is None: return Q
            if Q is None: return P
            if P[0] == Q[0]:
                if (P[1] + Q[1]) % p == 0: return None
                l = (3*P[0]**2 - 4*P[0] + 2)*pow(2*P[1], -1, p) % p
            else: l = (Q[1] - P[1])*pow(Q[0] - P[0], -1, p) % p
            x3 = (l*l + 2 - P[0] - Q[0]) % p; return (x3, (l*(P[0] - x3) - P[1]) % p)
        def mul(k, P):
            R = None
            while k:
                if k & 1: R = add(R, P)
                P = add(P, P); k >>= 1
            return R
        m = n
        while m % 2 == 0: m //= 2                                             # P has odd order iff (odd part of |C(F_p)|) * P = O
        tot += 1; odd += (mul(m, (1, 1)) is None)
    return odd, tot
odd, tot = naive(20000)
here = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(here, '..', 'odd_order_density.c'); exe = '/tmp/_ood'
subprocess.run(['gcc', '-O2', '-o', exe, src, '-lm'], check=True)
out = subprocess.run([exe, '-2', '1', '1', '20000'], capture_output=True, text=True).stdout.split('\n')[0]
import re; m = re.search(r'FINAL p <= \d+: (\d+) primes .*odd order (\d+) =', out); cprimes, codd = int(m.group(1)), int(m.group(2))
print("3. naive Python (own point count, own group law, hard-coded C and P): %d of %d primes in [3, 20000) with odd order;  C program with args -2 1 1: %d of %d  ->  %s" % (odd, tot, codd, cprimes, "identical" if (odd, tot) == (codd, cprimes) else "DIFFERENT"))
assert (odd, tot) == (codd, cprimes)
# 4. frame independence
print("4. frame independence (orders of the images at level 8 and 16 for other branch choices of the halving):")
for ch in ("0,0,0", "1,0,0", "0,1,0", "0,0,2", "3,2,1"):
    env = dict(os.environ, TAU_CHOICE=ch)
    r = subprocess.run([sys.executable, os.path.join(here, 'levels.py'), '-2', '1', '1', '4'], capture_output=True, text=True, env=env, cwd=here)
    lv = re.findall(r"level (\d) \(mod (\d+)\): \|I\| = 2\^(\d+)", r.stdout)
    print("   TAU_CHOICE=%s : %s" % (ch, ", ".join("mod %s: 2^%s" % (m_, o) for _, m_, o in lv) if lv else "FAILED: " + r.stderr[-200:]), flush=True)
print("DONE")
