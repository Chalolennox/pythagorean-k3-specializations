#!/usr/bin/env python3
"""Audit of the 'paired root numbers under a torsion involution' review draft (R(t) = -(1+t)/(1-t), (A,B) -> (-B,-A)).
Everything is exact (Fractions / integers); sympy is used if present, otherwise a small built-in factoriser and Jacobi symbol replace it.
Checks: (1) the discriminant constant, (2) Delta*Delta' = c*P(z)/z^6 and P = the paper's quotient sextic R of F.26, (3) disc(P),
(4) Res(H,J), (5) the recurrence for t_n, (6) the hypotenuse at t and R(t) coincide (so the factors at p | c cancel),
(7) K(t) = W(E_t) W(E_R(t)) equals C_{2,3}(t) * prod over p | F xor p | G of -(ab/p) on all |u|,|v| <= BOUND,
(8) the exceptional primes of gcd(F,G), (9) the table of C_{2,3} by (A,B) mod 144."""
import sys, random
from fractions import Fraction as Fr
from math import gcd
try:
    import sympy  # noqa
except ImportError:                      # stand-in used only when sympy is missing
    import types
    def _isp(n):
        if n < 2: return False
        for p in (2,3,5,7,11,13,17,19,23,29,31,37):
            if n % p == 0: return n == p
        d, s = n-1, 0
        while d % 2 == 0: d //= 2; s += 1
        for a in (2,3,5,7,11,13,17,19,23,29,31,37):
            x = pow(a, d, n)
            if x in (1, n-1): continue
            for _ in range(s-1):
                x = x*x % n
                if x == n-1: break
            else: return False
        return True
    def _rho(n):
        if n % 2 == 0: return 2
        c = 1
        while True:
            x = y = 2; d = 1
            while d == 1:
                x = (x*x+c) % n; y = (y*y+c) % n; y = (y*y+c) % n; d = gcd(abs(x-y), n)
            if d != n: return d
            c += 1
    def factorint(n):
        n = abs(n); f = {}
        for p in range(2, 1000):
            while n % p == 0: f[p] = f.get(p, 0)+1; n //= p
        st = [n] if n > 1 else []
        while st:
            m = st.pop()
            if m == 1: continue
            if _isp(m): f[m] = f.get(m, 0)+1; continue
            d = _rho(m); st += [d, m//d]
        return f
    def jacobi_symbol(a, n):
        a %= n; r = 1
        while a:
            while a % 2 == 0:
                a //= 2
                if n % 8 in (3, 5): r = -r
            a, n = n, a
            if a % 4 == 3 and n % 4 == 3: r = -r
            a %= n
        return r if n == 1 else 0
    m = types.ModuleType('sympy'); m.factorint = factorint; m.jacobi_symbol = jacobi_symbol; sys.modules['sympy'] = m
from sympy import factorint, jacobi_symbol
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import root_number_formula as RN

BOUND = 40
def AB(t): return (1-t*t)/(1+t*t), 2*t/(1+t*t)
def R(t): return -(1+t)/(1-t)
def Fp(t): return t**6-30*t**4-24*t**2-1                      # H
def Delta(t):
    A, B = AB(t); p, q = 4*A, -8*B; return -16*(4*p**3+27*q*q)
def primitive(t):
    u, v = t.numerator, t.denominator
    d = gcd(gcd(v*v-u*u, 2*u*v), v*v+u*u); return (v*v-u*u)//d, (2*u*v)//d, (v*v+u*u)//d
def polymul_eval(co, x): 
    r = 0
    for c in co: r = r*x + c
    return r
def det_frac(M):
    M = [[Fr(x) for x in r] for r in M]; n = len(M); d = Fr(1)
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i] != 0), None)
        if p is None: return Fr(0)
        if p != i: M[i], M[p] = M[p], M[i]; d = -d
        d *= M[i][i]
        for r in range(i+1, n):
            f = M[r][i]/M[i][i]
            for c in range(i, n): M[r][c] -= f*M[i][c]
    return d
def resultant(f, g):                       # coefficient lists, highest degree first
    m, n = len(f)-1, len(g)-1; N = m+n; S = []
    for i in range(n): S.append([0]*i+f+[0]*(N-m-1-i))
    for i in range(m): S.append([0]*i+g+[0]*(N-n-1-i))
    return det_frac(S)
def fmt(n):
    return ' * '.join('%d^%d' % (p, e) if e > 1 else str(p) for p, e in sorted(factorint(abs(n)).items()))
fails = 0
def check(name, ok, extra=''):
    global fails; fails += (not ok); print(('PASS ' if ok else 'FAIL ')+name+(' '+extra if extra else ''))

random.seed(7)
ts = []
while len(ts) < 300:
    u, v = random.randint(-60, 60), random.randint(1, 60)
    if gcd(u, v) == 1 and u != v: ts.append(Fr(u, v))

# (1) discriminant constant: -1024 F/c^3 (the draft says -4096 F/c^3)
ratios = set()
for t in ts:
    a, b, c = primitive(t); ratios.add(Delta(t)/Fr(4*a**3+27*b*b*c, c**3))
check('Delta(E_t) = -1024 F/c^3 on 300 t (the draft states -4096 F/c^3: off by the factor 4)', ratios == {Fr(-1024)}, 'ratios=%s' % sorted(ratios))
check('Delta(E_t) = 4096 H(t)/(1+t^2)^3', all(Delta(t) == 4096*Fp(t)/(1+t*t)**3 for t in ts))

# (2) quotient coordinate z = t + R(t) = 2 - u, u = x + 2/x;  Delta*Delta' = k * P(z)/z^6
Pz = [27, 0, -999, -2030, -1365, -312, -32]
Rq = [-54, 648, -1242, -11404, 62082, -113832, 73224]    # paper F.26, R(U)
ks = set(); ok_zu = True; ok_RP = True
for t in ts:
    z = t+R(t); ok_zu &= (z == (t*t+1)/(t-1))
    x = 1-t; u = x+2/x; ok_zu &= (z == 2-u)
    ok_RP &= (polymul_eval(Rq, u) == -2*polymul_eval(Pz, z))
    if z != 0: ks.add(Delta(t)*Delta(R(t))*z**6/polymul_eval(Pz, z))
check('z = t+R(t) = (t^2+1)/(t-1) = 2-u with u = x+2/x', ok_zu)
check("the draft's P(z) equals -R(2-z)/2 with R the quotient sextic of paper F.26", ok_RP)
check('Delta*Delta\' * z^6 / P(z) is a constant', len(ks) == 1, 'constant = %s = %s' % (ks, [int(k) for k in ks]))
# (3) discriminant of P
dP = resultant(Pz, [27*6, 0, -999*4, -2030*3, -1365*2, -312])   # Res(P, P')
n = 6; discP = Fr((-1)**(n*(n-1)//2))*dP/27
check('disc(P) = 56642762775035360714056704 (as stated in the draft)', discP == 56642762775035360714056704, '= %s' % fmt(int(discP)))
check('disc(P) = 2^10 3^18 23^2 519521^2 = 2^-10 disc(R) from F.26 (a perfect square)', int(discP) == 2**10*3**18*23**2*519521**2)
# (4) resultant of H and J
H = [1, 0, -30, 0, -24, 0, -1]; J = [27, 0, -27, -32, -27, 0, 27]
J = [27, 0, -27, -32, -27, 0, 27]   # 27 t^6 - 27 t^4 - 32 t^3 - 27 t^2 + 27 : coefficients t^6..t^0
J = [27, 0, -27, -32, -27, 0, 27]
resHJ = resultant(H, J)
check('Res(H,J) = 2^11 7 103 519521^2 = 398539554953136128', int(resHJ) == 398539554953136128 == 2**11*7*103*519521**2, '= %s' % fmt(int(resHJ)))
# H(R(t)) (1-t)^6 = -2 J(t)
ok = all(((1+t)**6-30*(1+t)**4*(1-t)**2-24*(1+t)**2*(1-t)**4-(1-t)**6) == -2*polymul_eval(J, t) for t in ts)
check('(1-t)^6 H(R(t)) = -2 J(t) (so primes of G are the primes of H at R(t))', ok)
p = 519521
check('gcd(H,J) mod 519521 is t^2 - 97448 t + 97449, with roots 1-37492 and 1-384583 (the paper F.25 roots x = 37492, 384583)',
      all((t*t-97448*t+97449) % p == 0 for t in (1-37492, 1-384583)) and ((1-37492)+(1-384583)-97448) % p == 0)
check('gcd(H,J) mod 7 has root t = -3 (x = 4) and mod 103 root t = -37 (x = 38)', polymul_eval(H, -3) % 7 == 0 and polymul_eval(J, -3) % 7 == 0 and polymul_eval(H, -37) % 103 == 0 and polymul_eval(J, -37) % 103 == 0)
# (5) recurrence for t_n
def add(P, Q):
    if P is None: return Q
    if Q is None: return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2:
        if y1+y2 == 0: return None
        l = (3*x1*x1-4*x1+2)/(2*y1)
    else: l = (y2-y1)/(x2-x1)
    x3 = l*l+2-x1-x2; return (x3, l*(x1-x3)-y1)
Pt = (Fr(1), Fr(1)); Q = Pt; tn = []; 
for _ in range(12): tn.append(1-Q[0]); Q = add(Q, Pt)
ok = tn[0] == 0 and tn[1] == Fr(3, 4) and all(tn[i+1] == 2*(tn[i]-2)/tn[i]**2-tn[i-1] for i in range(2, 11)) and tn[2] == 2*(tn[1]-2)/tn[1]**2-tn[0]
check('t_{n+1} = 2(t_n-2)/t_n^2 - t_{n-1} for t_n = 1 - x(nP), n = 2..11 (t_1 = 0, t_2 = 3/4; the step n=1 is undefined since t_1 = 0)', ok)
T = (Fr(0), Fr(0)); QQ = Pt; ok = True
for n in range(1, 12):
    S = add(QQ, T); ok &= (1-S[0] == R(1-QQ[0])); QQ = add(QQ, Pt)
check('t(nP+T) = R(t(nP)) for n = 1..11', ok)

# (6),(7),(8) on all coprime (u, v), |u|,|v| <= BOUND
c_equal = abp = fG = 0; Kbad = 0; tot = 0; exc = set(); kc = {}; cases_pc = 0
for v in range(1, BOUND+1):
    for u in range(-BOUND, BOUND+1):
        if gcd(u, v) != 1 or u == v: continue
        t = Fr(u, v); a, b, c = primitive(t); t2 = R(t); a2, b2, c2 = primitive(t2)
        tot += 1
        c_equal += (c2 == c); abp += (a2 == -b and b2 == -a)
        P1 = RN.parts(u, v); P2 = RN.parts(t2.numerator, t2.denominator)
        F1 = {p for p in P1['fac']}; F2 = {p for p in P2['fac']}
        cp = set(factorint(c)) - {2, 3}
        if cp: cases_pc += 1
        assert not (F1 & cp) and not (F2 & cp)
        # F and G from the draft, primitive
        Fv = 4*a**3+27*b*b*c; Gv = -4*b**3+27*a*a*c
        assert Fv == -4*P1['Fs']//P1['d']**3
        fG += (Gv == -4*P2['Fs']//P2['d']**3)
        g = gcd(abs(Fv), abs(Gv)); common = {p for p in factorint(g) if p >= 5}; exc |= common
        Kl = P1['W']*P2['W']
        C23 = P1['w2']*P1['w3']*P2['w2']*P2['w3']
        prod = 1
        for p in F1 ^ F2: prod *= -jacobi_symbol(a*b % p, p)
        Kbad += (Kl != C23*prod)
        kc[(C23)] = kc.get(C23, 0)+1
check('hypotenuse c(R(t)) = c(t) for all %d coprime (u,v), |u|,|v| <= %d, so v_p(c) agrees and the local factors at p | c cancel' % (tot, BOUND), c_equal == tot)
check('primitive triple of R(t) is (-b, -a, c), so a\'b\' = ab', abp == tot)
check('F(R t) := 4a\'^3+27b\'^2c equals G = -4b^3+27a^2c', fG == tot)
check('K(t) = C_{2,3}(t) * prod_{p>=5, p | F xor p | G} [-(ab/p)] (no residual factor at p | c; %d of the %d t have a prime >= 5 dividing c)' % (cases_pc, tot), Kbad == 0)
check('primes >= 5 dividing gcd(F,G) occur only in {7, 103, 519521}', exc <= {7, 103, 519521}, 'seen: %s' % sorted(exc))
print('C_{2,3} values over the sample:', kc)

# (9) C_{2,3} as a function of (A,B) mod 16 and mod 9 on the classes realised by Pythagorean triples
S2 = RN.S2
def w2f(A, B): return -1 if (A % 16, B % 16) in S2 else 1
def w3f(A, B): return -1 if (A % 9, B % 9) == (3, 8) else 1
c2 = {}; c3 = {}
for v in range(1, 120):
    for u in range(-120, 121):
        if gcd(u, v) != 1 or u == v: continue
        t = Fr(u, v); a, b, c = primitive(t)
        A16, B16 = (a*pow(c, -1, 16)) % 16, (b*pow(c, -1, 16)) % 16
        A9, B9 = (a*pow(c, -1, 9)) % 9, (b*pow(c, -1, 9)) % 9
        # the mirror (A,B) -> (-B,-A)
        k2 = (w2f(A16, B16)*w2f(-B16, -A16)); k3 = (w3f(A9, B9)*w3f(-B9, -A9))
        c2.setdefault((A16, B16), set()).add(k2); c3.setdefault((A9, B9), set()).add(k3)
check('w_2(E_t)w_2(E_R(t)) depends only on (A,B) mod 16', all(len(s) == 1 for s in c2.values()))
print('  classes (A,B) mod 16 realised: %d;  with product -1: %s' % (len(c2), sorted(k for k, s in c2.items() if -1 in s)))
print('  classes (A,B) mod 9 realised: %d;  with product -1: %s' % (len(c3), sorted(k for k, s in c3.items() if -1 in s)))
print('FAILURES: %d' % fails); raise SystemExit(1 if fails else 0)
