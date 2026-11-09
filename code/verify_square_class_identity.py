#!/usr/bin/env python3
"""The square-class identity behind the index-four obstruction, checked independently of the scan.

Faces.  f(t) = t^6 - 30t^4 - 24t^2 - 1 = g(t^2), g(s) = s^3 - 30s^2 - 24s - 1; roots come in pairs +-tau_j.  A FACE F is a set of three roots of f containing
exactly one root of each pair (8 faces).  Put h_F(t) = prod_{r in F} (t - r) = t^3 + a t^2 + b t + c, so a = -sum(F), b = sum of pairwise products, c = -prod(F).
Since (prod F)^2 = prod s_j = 1, c = +-1: TYPE I (c = +1) or TYPE II (c = -1); F -> -F exchanges the types, 4 faces of each type.
f(t) = -h_F(t) h_F(-t) gives c^2 = 1, 2b - a^2 = -30, b^2 - 2ac = -24, hence b = (a^2 - 30)/2 and a is a root of Q_c(a) = a^4 - 60a^2 - 8c*a + 996.
Identity (eps_F = 1 for type I, 3 for type II):   eps_F (1+i) prod_{r in F}(1-r)(r+i) = w_F^2   with
   w_I  = (i/2)(a^2 - 2i a - 28 - 2i),     w_II = (i/6)(a^3 + a^2 - 32a - 24 - 54i).
This script checks (1) the number field of a, (2) the identity exactly, (3) the identity as an equality of residues at every face of every prime p = 1 (mod 8)
below X for which f splits completely (both square roots of -1), and (4) the resulting character identity.   Needs: python3, sympy, gcc.  Exit 0 = all pass."""
import sys, os, subprocess, tempfile, collections, warnings, itertools
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
import sympy
from sympy import symbols, expand, rem, I, Rational, discriminant, factor_list, factorint, Poly, sqrt, sqrt_mod
OK = True
def check(name, cond, extra=''):
    global OK; OK &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra), flush=True)
a, y, s, t = symbols('a y s t'); i = I
Qp = a**4 - 60*a**2 - 8*a + 996; Qm = a**4 - 60*a**2 + 8*a + 996
# ---- (1) the number field of a ----------------------------------------------------------------------------------------------------
check('Q_+(a) = a^4 - 60a^2 - 8a + 996 is irreducible over Q, and Q_-(a) = Q_+(-a)', len(factor_list(Qp)[1]) == 1 and expand(Qm - Qp.subs(a, -a)) == 0)
d = discriminant(Qp, a); res = y**3 + 60*y**2 - 3984*y - 239104
g = s**3 - 30*s**2 - 24*s - 1
check('disc Q_+ = 2^12 3^9 23, not a square; resolvent cubic y^3 + 60y^2 - 3984y - 239104 is irreducible: Galois group S4 (the S4 of f; quadratic subfield Q(sqrt 69))',
      factorint(d) == {2: 12, 3: 9, 23: 1} and len(factor_list(res)[1]) == 1 and int(sqrt(d))**2 != d)
check('the resolvent cubic has the roots y = 4s - 60 for the roots s of g (so Q(a) is the quartic subfield attached to the cubic field Q(s))', rem(expand(res.subs(y, 4*s - 60)), g, s) == 0)
# ---- (2) the identity, exactly ---------------------------------------------------------------------------------------------------------
b = (a**2 - 30)/2
h = lambda x, c: x**3 + a*x**2 + b*x + c
wI = (i/2)*(a**2 - 2*i*a - 28 - 2*i); wII = (i/6)*(a**3 + a**2 - 32*a - 24 - 54*i)
check('coefficients: -h(t)h(-t) = t^6 + (2b - a^2)t^4 + (b^2 - 2ac)t^2 - c^2', [expand(c_) for c_ in Poly(expand(-(t**3 + a*t**2 + symbols('b')*t + symbols('c'))*((-t)**3 + a*t**2 - symbols('b')*t + symbols('c'))), t).all_coeffs()] == [1, 0, 2*symbols('b') - a**2, 0, symbols('b')**2 - 2*a*symbols('c'), 0, -symbols('c')**2])
check('type I  (c = +1): (1+i) prod_{r in F}(1-r)(r+i) = -(1+i) h(1) h(-i) = w_I^2    modulo Q_+(a)', rem(expand(wI**2 - expand(-(1 + i)*h(1, 1)*h(-i, 1))), Qp, a) == 0)
check('type II (c = -1): 3(1+i) prod_{r in F}(1-r)(r+i) = -3(1+i) h(1) h(-i) = w_II^2  modulo Q_-(a)', rem(expand(wII**2 - expand(-3*(1 + i)*h(1, -1)*h(-i, -1))), Qm, a) == 0)

# ---- normalization: the polynomial of the original conjecture is F(t) = -t^6 + 30t^4 + 24t^2 + 1 = -f(t) ---------------------------------------------------------------
Fpoly = -t**6 + 30*t**4 + 24*t**2 + 1; fpoly = t**6 - 30*t**4 - 24*t**2 - 1
b_, c_ = symbols('b'), symbols('c'); hs = t**3 + a*t**2 + b_*t + c_
diffF = Poly(expand(hs*hs.subs(t, -t) - Fpoly), t).all_coeffs()      # coefficients of h(t)h(-t) - F(t): must vanish iff the face relations hold
check('normalization: F = -f; F(1) = 54, F(i) = 8 while f(1) = -54, f(i) = -8; F(t) = h(t)h(-t) holds iff  c^2 = 1,  2b - a^2 = -30,  b^2 - 2ac = -24  (the same relations as f = -h(t)h(-t))',
      expand(Fpoly + fpoly) == 0 and Fpoly.subs(t, 1) == 54 and expand(Fpoly.subs(t, I)) == 8 and fpoly.subs(t, 1) == -54 and expand(fpoly.subs(t, I)) == -8
      and [expand(x_) for x_ in diffF] == [expand(-(2*b_ - a**2) - 30), 0, expand(-(b_**2 - 2*a*c_) - 24), 0, expand(c_**2 - 1)])       # the t^6 coefficient is 0 and is dropped by all_coeffs()
check("the complementary face h'(t) = -h(-t) satisfies h'(t)h'(-t) = h(t)h(-t) (so F, and f = -F, are unchanged), with coefficients (a', b', c') = (-a, b, -c)",
      expand((-hs.subs(t, -t))*(-hs) - hs*hs.subs(t, -t)) == 0 and expand(-hs.subs(t, -t) - (t**3 - a*t**2 + b_*t - c_)) == 0)

# ---- (2b) the elementary derivation (no quartic needed): polynomial identities in a, b, i with a, b FREE ------------------------------------------------
import mpmath as mp
bb = symbols('b'); hh = lambda x, c: x**3 + a*x**2 + bb*x + c
Wt = (1 + a) + i*(1 + bb)
u1, v1, w1, x1 = hh(1, 1), hh(-1, 1), hh(i, 1), hh(-i, 1)
check('type I, c = +1, a and b free:  W := (1+a) + i(1+b) = ((1+i)h(1) + (1-i)h(-1))/2 and  W^2 + (1+i) h(1) h(-i) + i (h(i)h(-i) - 8) = 0',
      expand(Wt - ((1 + i)*u1 + (1 - i)*v1)/2) == 0 and expand(Wt**2 + (1 + i)*u1*x1 + i*(w1*x1 - 8)) == 0)
Wp = (1 - a) + i*(1 + bb); u2, v2, w2, x2 = hh(1, -1), hh(-1, -1), hh(i, -1), hh(-i, -1)
check("type II, c = -1, a and b free (complementary face h'(t) = -h(-t), (a', b', c') = (-a, b, +1)):  W'^2 + (1+i) h(-1) h(i) + i (h(i)h(-i) - 8) = 0, W' = (1-a) + i(1+b)",
      expand(Wp**2 + (1 + i)*v2*w2 + i*(w2*x2 - 8)) == 0)
check('where the factor 3 comes from:  (1+i)^2 * f(1) f(i) = 2i * 54 * 8 = 864 i = 3 (12(1+i))^2  (f(1) = -54, f(i) = f(-i) = -8)', expand(864*i - 3*(12*(1 + i))**2) == 0 and (1 + 0)*(-54) == (1 - 30 - 24 - 1) and (i**6 - 30*i**4 - 24*i**2 - 1) == -8)
ub = (a**2 + 2*a - 26)/2
check('u = h(1) = (a^2 + 2a - 26)/2 satisfies u^4 - 8u^3 + 2916 = 0 modulo Q_+(a)', rem(expand(ub**4 - 8*ub**3 + 2916), Qp, a) == 0)
# the quartic Q_+ is the quartic of the sign combinations -(e1 tau1 + e2 tau2 + e3 tau3), tau1 tau2 tau3 = -1, and its resolvent is the pair-sum relation (a + a')^2 = 4 s
mp.mp.dps = 50
ss = mp.polyroots([1, -30, -24, -1], maxsteps=500, extraprec=200); tau = [mp.sqrt(x_) for x_ in ss]
if mp.re(tau[0]*tau[1]*tau[2]) > 0: tau[0] = -tau[0]
if abs(tau[0]*tau[1]*tau[2] + 1) > mp.mpf(10)**-30: tau[0] = -tau[0]
avals = [-(e1*tau[0] + e2*tau[1] + e3*tau[2]) for e1, e2, e3 in itertools.product((1, -1), repeat=3) if e1*e2*e3 == 1]
Qnum = lambda z_: z_**4 - 60*z_**2 - 8*z_ + 996
check('Q_+ has the four roots a = -(e1 tau1 + e2 tau2 + e3 tau3), e1 e2 e3 = +1, with tau1 tau2 tau3 = -1 (the four type I faces); pair sums a + a\' = -2 e tau_j, so (a + a\')^2 = 4 s_j',
      all(abs(Qnum(z_)) < mp.mpf(10)**-30 for z_ in avals) and sorted(round(float(mp.re((avals[k] + avals[l])**2)), 6) for k in range(4) for l in range(k + 1, 4)) == sorted(round(float(4*ss[j].real), 6) for j in range(3) for _ in range(2)))

# ---- (3) literal specialization -------------------------------------------------------------------------------------------------------------------
X = int(sys.argv[1]) if len(sys.argv) > 1 else 3000000
tmp = tempfile.mkdtemp(prefix='sq_'); exe = os.path.join(tmp, 'scan')
subprocess.run(['gcc', '-O2', '-o', exe, os.path.join(HERE, 'index_four', 'scan.c')], check=True)
primes = [int(l.split()[0]) for l in subprocess.run([exe, str(X)], capture_output=True, text=True).stdout.split('\n') if l.strip()]
Xs = symbols('x')
def chi(v, p):
    v %= p; return 0 if v == 0 else (1 if pow(v, (p - 1)//2, p) == 1 else -1)
faces_tested = 0; lit_ok = True; chi_ok = True; roots_ok = True; typecount = collections.Counter(); p_mod3 = collections.Counter(); chi3_cases = 0
for p in primes:
    f = Poly(Xs**6 - 30*Xs**4 - 24*Xs**2 - 1, Xs, modulus=p); rts = sorted(int(z) % p for z in f.ground_roots().keys())
    if len(rts) != 6: roots_ok = False; continue
    pairs = []; seen = set()
    for r in rts:
        if r in seen: continue
        seen.add(r); seen.add((-r) % p); pairs.append((r, (-r) % p))
    i0 = sqrt_mod(p - 1, p); eta = chi(1 + i0, p); p_mod3[p % 3] += 1
    for face in __import__('itertools').product(*pairs):
        c = (-face[0]*face[1]*face[2]) % p; cF = 1 if c == 1 else (-1 if c == p - 1 else None)
        if cF is None: roots_ok = False; continue
        aF = (-sum(face)) % p; bF = (aF*aF - 30)*pow(2, -1, p) % p
        Qc = (pow(aF, 4, p) - 60*aF*aF - 8*cF*aF + 996) % p
        hF = [1, aF, bF, c]; direct = [1, (-sum(face)) % p, (face[0]*face[1] + face[0]*face[2] + face[1]*face[2]) % p, (-face[0]*face[1]*face[2]) % p]
        roots_ok &= (Qc == 0 and hF == direct)
        for ii in (i0, (-i0) % p):                               # either square root of -1 works
            if cF == 1: w = ii*pow(2, -1, p) % p * ((aF*aF - 2*ii*aF - 28 - 2*ii) % p) % p; eps = 1
            else: w = ii*pow(6, -1, p) % p * ((aF**3 + aF*aF - 32*aF - 24 - 54*ii) % p) % p; eps = 3
            prod = 1
            for r in face: prod = prod*(1 - r)*(r + ii) % p
            lit_ok &= ((eps*(1 + ii)*prod) % p == (w*w) % p)
        # character form: prod chi(r + i) = eta * chi(eps) * prod chi(1 - r)
        psi = 1
        for r in face: psi *= chi(r + i0, p)
        rhs = eta*(1 if cF == 1 else chi(3, p))
        for r in face: rhs *= chi(1 - r, p)
        chi_ok &= (psi == rhs); faces_tested += 1; typecount[cF] += 1
        if cF == -1 and chi(3, p) == -1: chi3_cases += 1
print('     primes p = 1 (mod 8), p < %d, f split completely: %d (p mod 3: %s); faces tested: %d (type I: %d, type II: %d)' % (X, len(primes), dict(p_mod3), faces_tested, typecount[1], typecount[-1]))
check('every face has c = +-1, a is a root of Q_c mod p, and h_F(t) = t^3 + a t^2 + b t + c with b = (a^2 - 30)/2 (the coefficient identities hold mod p)', roots_ok)
check('the identity holds as an equality of residues mod p at every face, for both square roots of -1', lit_ok)
check('character form  prod_{r in F} chi(r+i) = chi(1+i) * chi(eps_F) * prod_{r in F} chi(1-r)  at every face (no qualifying hypothesis)  [type II faces with chi(3) = -1 tested: %d]' % chi3_cases, chi_ok)
print('ALL CHECKS PASS' if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
