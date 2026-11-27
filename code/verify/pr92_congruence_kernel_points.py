#!/usr/bin/env python3
"""Independent check of the rational-point data in notes/TORSION_CONGRUENCE_KERNEL_2026-11-27.md.

Written by Claude (a language model), independent of the PR author's scripts and of the
owner's Magma replay. No human has checked it. Stdlib only, exact integer arithmetic.
Runtime: well under 10 seconds.

CHECKS (J: y^2 = x^3 - 2x^2 + 2x over F_p):
  - p prime, p = 65 mod 128; the quoted points lie on J.
  - at both primes: 32A = T1=(0,0), 2*T1 = O, 64B = O, 32B not in {O, T1}
    (so A, B generate a full Z/64 x Z/64 inside J(F_p)).
  - p=8956097: 2U = A, 64U = T1; quoted #J = 64 * 139904 is consistent with order-64 points.
  - p=2738753: D=(1532999,0) is a 2-torsion point, D != T1 (cheap part of the c=1 witness).
DOES NOT CHECK: the quoted group orders #J by point counting, the F_{p^2} half points / Frobenius
difference U^Frob - U (needs sqrt in F_{p^2}), the Galois-theoretic deduction, or the
hyperplane / squaring argument. It is evidence from Claude, not a human check or a Certified result.
"""
def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True

def make(p):
    def on(P): return P is None or (P[1]*P[1] - (P[0]**3 - 2*P[0]**2 + 2*P[0])) % p == 0
    def add(P, Q):
        if P is None: return Q
        if Q is None: return P
        x1, y1 = P; x2, y2 = Q
        if x1 == x2 and (y1 + y2) % p == 0: return None
        if P == Q:
            l = (3*x1*x1 - 4*x1 + 2) * pow(2*y1, -1, p) % p
        else:
            l = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (l*l + 2 - x1 - x2) % p
        return (x3, (l*(x1 - x3) - y1) % p)
    def mul(n, P):
        R = None
        while n:
            if n & 1: R = add(R, P)
            P = add(P, P); n >>= 1
        return R
    return on, add, mul

T = (0, 0)
data = {
 8956097: dict(A=(8023164,4886572), B=(3491812,6904152), U=(3305919,2881857), n=8953856),
 2738753: dict(A=(2419569,1057284), B=(2701647,1471702), n=2736128),
}
ok = True
def chk(label, c):
    global ok
    print(("PASS " if c else "FAIL ") + label); ok &= bool(c)
for p, d in data.items():
    on, add, mul = make(p)
    print("p =", p)
    chk("prime and p = 65 mod 128", isprime(p) and p % 128 == 65)
    chk("T1 on curve, 2*T1 = O", on(T) and mul(2, T) is None)
    A, B = d['A'], d['B']
    chk("A, B on curve", on(A) and on(B))
    chk("32A = T1", mul(32, A) == T)
    chk("64B = O", mul(64, B) is None)
    chk("32B not in {O, T1}", mul(32, B) not in (None, T))
    chk("64 divides quoted #J", d['n'] % 64 == 0)
    if 'U' in d:
        U = d['U']
        chk("U on curve", on(U))
        chk("2U = A", mul(2, U) == A)
        chk("64U = T1", mul(64, U) == T)
        chk("quoted #J = 64*139904", d['n'] == 64 * 139904)
    else:
        x = 1532999
        chk("D=(1532999,0): on curve, 2-torsion", (x**3 - 2*x*x + 2*x) % p == 0 and (x*x - 2*x + 2) % p == 0)
        chk("D != T1", x % p != 0)
print("ALL PASS" if ok else "SOME FAIL")
