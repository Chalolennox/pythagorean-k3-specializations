#!/usr/bin/env python3
"""Independent checks of the data in the reviewer's context files of 7 November 2026 (MASTER_CONTEXT.md and the two reports).
Needs: python3, sympy, numpy.  Uses code/ec.py (exact curve arithmetic, canonical heights) and code/scripts_as_run/eps.py
(the exact root-number pieces of F.28).  Takes about a minute.  Exit status 0 = the checks that are expected to pass pass
(lines marked FINDING report a disagreement with the reviewer's text; they do not change the exit status)."""
import sys, os, warnings, itertools, signal
warnings.filterwarnings('ignore')
from fractions import Fraction as Fr
from math import gcd
import numpy as np
import sympy
from sympy import symbols, Poly, expand, factorint, resultant
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, 'scripts_as_run')]
from ec import Curve, gram, det3, chat
from eps import pieces, triple, Fs, jac
ok = True
def check(name, cond, extra=''):
    global ok; ok &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra))
def finding(name, extra=''): print('FINDING %s %s' % (name, extra))

def W(t):
    t = Fr(t); f, s, Fv = pieces(t); a, b, c = triple(t); w = f
    for p in factorint(Fv): w *= -jac(a*b, p)
    return w
def AB(t): t = Fr(t); D = 1 + t*t; return (1 - t*t)/D, 2*t/D
def jinv(a4, a6): a4, a6 = Fr(a4), Fr(a6); return 1728*4*a4**3/(4*a4**3 + 27*a6**2)
def disc(a4, a6): return -16*(4*Fr(a4)**3 + 27*Fr(a6)**2)

# ---- 1. discriminant formula ---------------------------------------------------------------------------------------
t = Fr(3, 7); A, B = AB(t)
d_right = disc(4*A, -8*B); u, v = t.numerator, t.denominator
check('Delta = -4096A^3 - 27648B^2 = 4096 F(u,v)/(u^2+v^2)^3', d_right == -4096*A**3 - 27648*B**2 == 4096*Fs(u, v)/Fr(u*u + v*v)**3)
finding('MASTER_CONTEXT section 1 writes Delta = -1024A^3 - 27648B^2; the coefficient of A^3 is -4096 (a typo in the context)',
        '(at t = 3/7 the stated expression differs from Delta by %s)' % (-1024*A**3 - 27648*B**2 - d_right))

# ---- 2. j-invariants quoted ------------------------------------------------------------------------------------------
check('j(E_{1/2}) = 576/7 and j(E_{4/3}) = -592704/96857', jinv(4*AB(Fr(1,2))[0], -8*AB(Fr(1,2))[1]) == Fr(576, 7) and jinv(4*AB(Fr(4,3))[0], -8*AB(Fr(4,3))[1]) == Fr(-592704, 96857))

# ---- 3. the four rank-3 curves: models, discriminants, j -------------------------------------------------------------
models = {Fr(-46,9): (-105820, 14552928, -15654925305663488, Fr(-14562534888000, 1739646449)),
          Fr(-12,11): (-1712085500, 2760090253800000, -3290697240551623662620392000000000, Fr(-21024576, 124656553)),
          Fr(-17,31): (1344, 105400, -4954530917376, Fr(9710862336, 179200337)),
          Fr(15,8): (-186116, -160360320, -10696464936824467456, Fr(-7211429568, 108189919))}
rat = {Fr(-46,9): (Fr(-8140,2197), Fr(6624,2197)), Fr(-12,11): (Fr(-92,265), Fr(2112,265)), Fr(-17,31): (Fr(1344,625), Fr(4216,625)), Fr(15,8): (Fr(-644,289), Fr(-1920,289))}
for tt in models:
    A, B = AB(tt); a4, a6 = 4*A, -8*B
    check('t = %s: the rational coefficients quoted equal 4A, -8B' % tt, (a4, a6) == rat[tt])
    I4, I6, Dq, jq = models[tt]
    r4, r6 = Fr(I4)/a4, Fr(I6)/a6
    u2 = r6/r4; uu = sympy.sqrt(sympy.Rational(u2.numerator, u2.denominator)); rational_u = uu.is_Rational
    check('   quoted integral model is E_t scaled by u (u^4 = a4\'/a4, u^6 = a6\'/a6, u = %s)' % (uu if rational_u else '?'), rational_u and Fr(int(uu.p), int(uu.q))**4 == r4)
    check('   quoted discriminant and j-invariant of that model are correct', disc(I4, I6) == Dq and jinv(I4, I6) == jq == jinv(a4, a6))

# ---- 4. three further rank-3 equations -----------------------------------------------------------------------------------
quoted = {Fr(-86,27): (Fr(-26668,8125), Fr(37152,8125)), Fr(55,37): (Fr(-3312,2197), Fr(-16280,2197)), Fr(11,60): (Fr(13916,3721), Fr(-10560,3721))}
check('E_{-86/27}, E_{55/37}, E_{11/60}: quoted coefficients equal 4A(t), -8B(t)', all((4*AB(tt)[0], -8*AB(tt)[1]) == c for tt, c in quoted.items()))

# ---- 5. points at t = -46/9 ---------------------------------------------------------------------------------------------
t0 = Fr(-46, 9); A, B = AB(t0); E = Curve(4*A, -8*B)
P = [(Fr(-18,13), Fr(396,169)), (Fr(-242,117), Fr(6172,4563)), (Fr(-243,169), Fr(5091,2197))]
others = {'(486/13, 38580/169)': (Fr(486,13), Fr(38580,169)), '(358/117, 20572/4563)': (Fr(358,117), Fr(20572,4563)), '(-932/1521, 133372/59319)': (Fr(-932,1521), Fr(133372,59319)),
          'report 1: (-3146/9, 80236/27) on the model y^2=x^3-105820x+14552928': (Fr(-3146,9)/169, Fr(80236,27)/2197),
          'report 1: (-151763/441, 29597651/9261)': (Fr(-151763,441)/169, Fr(29597651,9261)/2197), 'report 1: (6318, 501540)': (Fr(6318)/169, Fr(501540)/2197)}
check('all the points quoted for t = -46/9 (both reports, 9 points) lie on the curve', all(E.on(Q) for Q in P + list(others.values())))
G = np.array(gram(E, P, 6)); n = 6
for nm, Q in others.items():
    rhs = np.array([(chat(E, E.add(Q, Pi), n) - chat(E, Q, n) - chat(E, Pi, n))/2 for Pi in P])
    co = np.linalg.solve(G, rhs); ci = [int(round(x)) for x in co]
    R = None
    for cj, Pj in zip(ci, P): R = E.add(R, E.mul(cj, Pj))
    check('   %s is exactly %s P1 + %s P2 + %s P3 (P1,P2,P3 = first three points of script 09)' % (nm[:44], *ci), R == Q, '(float coefficients %s)' % ['%.3f' % x for x in co])
reg = det3(G.tolist()); G7 = np.array(gram(E, P, 7)); reg7 = det3(G7.tolist()); extra = (4*reg7 - reg)/3
print('     regulator of P1,P2,P3: n=6 -> %.4f, n=7 -> %.4f, Richardson -> %.4f; the reviewer reports 87.59946' % (reg, reg7, extra))
check('regulator agrees with the reported 87.59946 to 0.01', abs(extra - 87.59946) < 0.01)

# ---- 6. Jacobian of the cover c = -11/5 -------------------------------------------------------------------------------------
a2, a4, a6 = Fr(-7144, 3125), Fr(678969, 390625), Fr(-21574186, 48828125)
onJ = lambda x, y: y*y == x**3 + a2*x*x + a4*x + a6
Pj = (Fr(9549, 3125), Fr(271256, 78125)); Qj = (Fr(3029922, 3321125), Fr(12112568, 541343375)); T2 = (Fr(113, 125), Fr(0))
check('J: P, Q and the 2-torsion point (113/125, 0) lie on y^2 = x^3 - (7144/3125)x^2 + (678969/390625)x - 21574186/48828125', onJ(*Pj) and onJ(*Qj) and onJ(*T2))
sh = a2/3; A_ = a4 - a2*a2/3; B_ = a6 - a2*a4/3 + 2*a2**3/27; EJ = Curve(A_, B_)
Ps = (Pj[0] + sh, Pj[1]); Qs = (Qj[0] + sh, Qj[1])
Gj = gram(EJ, [Ps, Qs], 5); regj = Gj[0][0]*Gj[1][1] - Gj[0][1]**2
print('     regulator of P, Q on J (n=5 doublings): %.3f; the reviewer reports 66.2469 and section 6 of the paper 66.25' % regj)
check('J: regulator within 0.2 of 66.2469 (independent canonical heights)', abs(regj - 66.2469) < 0.2)

# ---- 7. the reflection M, G(a,b) and the resultant ---------------------------------------------------------------------------
M = lambda t: (10 - 11*t)/(10*t + 11)
pairs = {Fr(-7): Fr(-87,59), Fr(-201,43): Fr(-2641,1537), Fr(-41491871,26984647): Fr(-3286231,534333), Fr(-510518809,250676113): Fr(-36753249,10623307),
         Fr(-77776328417,27672051631): Fr(-1132260128897,473370716229), Fr(-20933431433,3628611919): Fr(-266553864953,169419583221),
         Fr(-160640731831297210959,22469254219915219837): Fr(-1991740592343421518919,1359245521893904691383)}
check('M(t) = (10-11t)/(10t+11): M(M(t)) = t, and the 7 quoted pairs are exact', all(M(M(t)) == t for t in pairs) and all(M(t) == m for t, m in pairs.items()))
a_, b_ = symbols('a b'); Fab = a_**6 - 30*a_**4*b_**2 - 24*a_**2*b_**4 - b_**6
Gab = expand(Fab.subs({a_: 10*b_ - 11*a_, b_: 10*a_ + 11*b_}, simultaneous=True))
quoted_coeffs = [-72191439, -28149660, 81738270, -84019760, 57400236, 26985420, -72209961]
check('G(a,b) = F(10b-11a, 10a+11b) has the quoted expansion', [Gab.coeff(a_, 6-k).coeff(b_, k) for k in range(7)] == quoted_coeffs)
tt = symbols('t'); Ft = Fab.subs({a_: tt, b_: 1}); Gt = Gab.subs({a_: tt, b_: 1})
res = resultant(Ft, Gt, tt); fac = factorint(abs(res))
check('Res(F(t,1), G(t,1)) = 2^20 5^6 7 239^2 6133^2 20873^2 3532913 585807239^2', fac == {2: 20, 5: 6, 7: 1, 239: 2, 6133: 2, 20873: 2, 3532913: 1, 585807239: 2}, '(sign %s)' % ('+' if res > 0 else '-'))
check('G(t,1) = 5(t+5)^6 mod 13 and 13(t+13)^6 mod 17; F = G mod 2 and mod 5',
      Poly(Gt - 5*(tt + 5)**6, tt, modulus=13).is_zero and Poly(Gt - 13*(tt + 13)**6, tt, modulus=17).is_zero and Poly(Ft - Gt, tt, modulus=2).is_zero and Poly(Ft - Gt, tt, modulus=5).is_zero)

# ---- 8. root numbers: the reviewer's 14 pairs, the powers (3+4i)^n --------------------------------------------------------------
class TO(Exception): pass
def alarm(s, f): raise TO()
signal.signal(signal.SIGALRM, alarm)
def Wt(t, sec=90):
    signal.alarm(sec)
    try: return W(t)
    except TO: return None
    finally: signal.alarm(0)
rows = [(-7,+1,-1),(-4,+1,+1),(-3,-1,-1),(-2,+1,-1),(-1,-1,+1),(Fr(-1,2),-1,+1),(0,+1,-1),(Fr(1,2),+1,-1),(1,+1,-1),(2,-1,-1),(3,-1,+1),(4,-1,+1),(5,+1,+1),(Fr(-201,43),-1,-1)]
good = all((Wt(Fr(t)), Wt(M(Fr(t)))) == (w1, w2) for t, w1, w2 in rows)
check('the 28 global root numbers of the reviewer\'s 14-pair table equal the exact formula of F.28', good)
a, b = 1, 0; sg = {1: 1, 2: 1, 3: 1, 4: 1, 5: -1, 6: 1}; good = True
for n in range(1, 7):
    a, b = 3*a - 4*b, 4*a + 3*b; good &= (Wt(Fr(b, 5**n + a), 120) == sg[n])
check('W(E_n) for t_n of the powers (3+4i)^n, n = 1..6: +,+,+,+,-,+ as in the reviewer\'s table', good)

# ---- 9. rank lists: parity against W ------------------------------------------------------------------------------------------
claims = {'-7':2,'-4':2,'8':2,'-4/3':2,'-1/3':2,'4/3':2,'-7/4':2,'2/5':2,'-5/7':2,'1/9':2,'-3':1,'-1':1,'3':1,'-3/2':1,'3/2':1,'-7/5':1,'7/8':1,'1/5':1,'-1/5':1,'1/7':1,'-1/7':1,
          '0':0,'1':0,'1/2':0,'-2':0,'2/3':0,'-2/3':0,'5/2':0,'5':0}
wrong = [k for k, r in claims.items() if (-1)**r != W(Fr(k))]
check('exactly two of the reviewer\'s 29 listed ranks have the wrong parity for W: t = -3/2 (listed rank 1, W = +1) and t = 2/3 (listed rank 0, W = -1)', sorted(wrong) == ['-3/2', '2/3'], '(found %s)' % wrong)
finding('section 5 of the paper has t = -3/2 with rank 0 (dim Sha[2] = 2) and t = 2/3 with rank 1, both consistent with W; t = -7/4, 2/5 (rank 2, W = +1) and 5/2 (rank 0, W = +1) are not in section 5 and are parity-consistent only')

# ---- 10. local sign at multiplicative primes: -(−c6/p) versus the paper's (ab/p) -----------------------------------------------------
agree = total = 0
for u in range(-12, 13):
    for v in range(1, 14):
        if gcd(abs(u), v) != 1: continue
        t = Fr(u, v); a, b, c = triple(t); F = abs(Fs(u, v))
        for p in factorint(F):
            if p < 5 or (u*v*(u*u + v*v)) % p == 0: continue
            lhs = sympy.legendre_symbol((-6*u*v*(u*u + v*v)) % p, p)     # (-c6/p), c6 = 13824 uv/(u^2+v^2), 13824 = 6*48^2
            rhs = sympy.legendre_symbol((a*b) % p, p)
            total += 1; agree += (lhs == rhs)
check('(-6uv(u^2+v^2)/p) = (ab/p) at every multiplicative prime tested (%d pairs t, p)' % total, agree == total)
print('ALL EXPECTED CHECKS PASS' if ok else 'SOME CHECK FAILED'); sys.exit(0 if ok else 1)
