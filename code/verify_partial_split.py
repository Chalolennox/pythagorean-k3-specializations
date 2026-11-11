#!/usr/bin/env python3
"""Specialization of the face identity to every Frobenius class (partially split f), and local character relations at rational roots.

For a prime p = 1 (mod 4) (so i in F_p) let h be a monic cubic over F_p with f(t) = -h(t) h(-t) ("Frobenius-stable face": h is the product of (t - r) over a set F of
three roots of f containing one root of each pair +-r, stable under Frobenius).  Then c = h(0) = +-1.  With u = h(1), v = h(-1), w = h(i), x = h(-i):
  type I  (c = +1):  W = ((1+i)u + (1-i)v)/2 = (1+a) + i(1+b);     W^2 = -(1+i) u x    [uses only  w x = -f(i) = 8]
  type II (c = -1):  W' = (1-a) + i(1+b);     -3(1+i) u x = (36(1+i)/W')^2             [uses  u v = -f(1) = 54  and  w x = 8]
Character form (p = 1 mod 4, chi(-1) = 1):   chi(h(1) h(-i)) = chi(1+i) * chi(eps),   eps = 1 (type I) or 3 (type II).
Checks: Frobenius classes of f mod p and their stable faces; the identities as residues at every stable cubic factor; and, at rational roots,
  R1.  if (1-t)(1+t^2) is a nonzero square then chi(1+t) = chi(-3)                                          (any p >= 5)
  R2.  if +-tau are both roots, p = 1 (mod 4):  u(tau) u(-tau) = chi(3), where u(r) = chi(1-r) chi(r+i)         (from f = 0 alone)
  R3.  type B (one rational pair +-tau, quadratic factors q(t), q(-t)):  u(r0) = chi(1+i) chi(eps) chi(q(1) q(-i)) for r0 = +-tau, with the face (t - r0) q(t).
Needs python3, sympy.   Usage: python3 code/verify_partial_split.py [X]  (default 150000).   Exit 0 = all pass."""
import sys, itertools, collections, warnings
warnings.filterwarnings('ignore')
from sympy import symbols, Poly, primerange, sqrt_mod, GF
OK = True
def check(name, cond, extra=''):
    global OK; OK &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra), flush=True)
X = int(sys.argv[1]) if len(sys.argv) > 1 else 150000
t = symbols('t')
def chi(v, p):
    v %= p; return 0 if v == 0 else (1 if pow(v, (p - 1)//2, p) == 1 else -1)
classes = collections.Counter(); stable_by_class = collections.defaultdict(collections.Counter); rat_stats = collections.defaultdict(collections.Counter)
cnt_faces = 0; lit_ok = True; chiform_ok = True; r1_ok = True; r2_ok = True; r3_ok = True; r3_cases = 0; r1_cases = 0; r2_cases = 0
for p in primerange(29, X):
    if p % 4 != 1: continue
    i0 = sqrt_mod(p - 1, p); eta = chi(1 + i0, p); inv2 = pow(2, -1, p)
    f = Poly(t**6 - 30*t**4 - 24*t**2 - 1, t, modulus=p)
    fac = [(Poly(g, t, modulus=p), e) for g, e in f.factor_list()[1]]
    if any(e > 1 for g, e in fac): continue                                   # p | disc: skipped (p = 23 only)
    degs = tuple(sorted(g.degree() for g, e in fac)); g_pol = Poly(t**3 - 30*t**2 - 24*t - 1, t, modulus=p)
    n_g = len(g_pol.ground_roots())
    cls = degs if degs != (1, 1, 2, 2) else ((1, 1, 2, 2, 'A') if n_g == 3 else (1, 1, 2, 2, 'B'))
    classes[cls] += 1
    # all monic cubic divisors h of f with f = -h(t)h(-t)
    stable = []
    for r in range(1, len(fac) + 1):
        for comb in itertools.combinations([g for g, e in fac], r):
            if sum(g.degree() for g in comb) != 3: continue
            h = Poly(1, t, modulus=p)
            for g in comb: h = h*g
            if (-(h*h.compose(Poly(-t, t, modulus=p)))) == f: stable.append(h)
    stable_by_class[cls][len(stable)] += 1
    for h in stable:
        co = [int(c_) % p for c_ in h.all_coeffs()]; a_, b_, c_ = co[1], co[2], co[3]
        assert c_ in (1, p - 1)
        u = h.eval(1) % p; v = h.eval(-1) % p; x = h.eval((-i0) % p) % p; w = h.eval(i0) % p
        if c_ == 1:
            W = ((1 + i0)*u + (1 - i0)*v) % p*inv2 % p; lhs = (-(1 + i0)*u*x) % p; ok = (lhs == W*W % p) and (W == (1 + a_ + i0*(1 + b_)) % p); eps = 1
        else:
            Wp = ((1 - a_) + i0*(1 + b_)) % p
            if Wp == 0: continue
            lhs = (-3*(1 + i0)*u*x) % p; rhs = (36*(1 + i0)*pow(Wp, -1, p)) % p; ok = (lhs == rhs*rhs % p); eps = 3
        lit_ok &= ok; cnt_faces += 1
        chiform_ok &= (chi(u*x, p) == eta*(1 if eps == 1 else chi(3, p)))
    # R1 and R2 and R3 at rational roots
    rts = [int(r) % p for r in f.ground_roots().keys()]
    for r in rts:
        if r in (0, 1, p - 1): continue
        if chi((1 - r)*(1 + r*r), p) == 1:
            r1_cases += 1; r1_ok &= (chi(1 + r, p) == chi(-3, p))
    if p % 8 == 1 and cls in ((1, 1, 2, 2, 'A'), (1, 1, 2, 2, 'B'), (1,)*6):          # how many rational candidates lie in 2C(F_p)?
        n2c = 0
        for r in rts:
            x_ = (1 - r) % p; y2 = x_*(x_*x_ - 2*x_ + 2) % p
            if x_ != 0 and chi(y2, p) in (0, 1) and chi(x_, p) == 1 and chi(r + i0, p) == 1: n2c += 1
        rat_stats[(cls, p % 3)][n2c] += 1
    pairs = [r for r in rts if (-r) % p in rts and r < (-r) % p]
    for r in pairs:
        U = lambda s_: chi(1 - s_, p)*chi(s_ + i0, p)
        r2_cases += 1; r2_ok &= (U(r)*U((-r) % p) == chi(3, p))
    if cls == (1, 1, 2, 2, 'B'):
        q = [g for g, e in fac if g.degree() == 2][0]
        for r0 in rts:
            h = Poly(t - r0, t, modulus=p)*q
            if not (-(h*h.compose(Poly(-t, t, modulus=p)))) == f: h = Poly(t - r0, t, modulus=p)*[g for g, e in fac if g.degree() == 2][1]
            assert (-(h*h.compose(Poly(-t, t, modulus=p)))) == f
            c_ = int(h.all_coeffs()[3]) % p; eps = 1 if c_ == 1 else 3
            qq = h.quo(Poly(t - r0, t, modulus=p)); q1 = qq.eval(1) % p; qmi = qq.eval((-i0) % p) % p
            u_r0 = chi(1 - r0, p)*chi(r0 + i0, p)
            r3_cases += 1; r3_ok &= (u_r0 == eta*(1 if eps == 1 else chi(3, p))*chi(q1*qmi, p))
tot = sum(classes.values())
print('     primes p = 1 (mod 4), 29 <= p < %d: %d' % (X, tot))
dens = {(1,)*6: 1/24, (1, 1, 2, 2, 'A'): 3/24, (1, 1, 2, 2, 'B'): 6/24, (3, 3): 8/24, (2, 4): 6/24}
for k in sorted(classes, key=lambda k: -classes[k]):
    print('     class %-18s %5d primes (%.3f; Chebotarev %.3f); Frobenius-stable faces per prime: %s' % (k, classes[k], classes[k]/tot, dens.get(k, float('nan')), dict(stable_by_class[k])))
expected = {(1,)*6: 8, (1, 1, 2, 2, 'A'): 0, (1, 1, 2, 2, 'B'): 4, (3, 3): 2, (2, 4): 0}
check('number of Frobenius-stable faces is 8, 0, 4, 2, 0 for the classes 1^6, (1,1,2,2)A, (1,1,2,2)B, (3,3), (2,4)', all(set(stable_by_class[k]) == {expected[k]} for k in classes if k in expected))
check('identity at every stable cubic factor as an equality of residues (%d faces)' % cnt_faces, lit_ok)
check('character form  chi(h(1) h(-i)) = chi(1+i) chi(eps)  at every stable cubic factor', chiform_ok)
check('R1: chi(1+t) = chi(-3) at every root t with (1-t)(1+t^2) a nonzero square (%d cases)' % r1_cases, r1_ok)
check('R2: u(tau) u(-tau) = chi(3) at every rational pair +-tau (%d cases)' % r2_cases, r2_ok)
check('R3: type B:  u(r0) = chi(1+i) chi(eps) chi(q(1) q(-i)) at both rational roots (%d cases)' % r3_cases, r3_ok)
print('     number of rational roots t (x = 1 - t on C and in 2C(F_p)), primes p = 1 (mod 8), by class and p mod 3 (R2: at p = 2 mod 3 the rational pair never has both in 2C):')
for k in sorted(rat_stats, key=str): print('        ', k, dict(sorted(rat_stats[k].items())))
check('R2 consequence: for the classes (1,1,2,2)A and (1,1,2,2)B with p = 2 (mod 3), p = 1 (mod 8), at most one of the two rational roots lies in 2C', all(max(v) <= 1 for (c_, m3), v in rat_stats.items() if c_ in ((1, 1, 2, 2, 'A'), (1, 1, 2, 2, 'B')) and m3 == 2))
print('ALL CHECKS PASS' if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
