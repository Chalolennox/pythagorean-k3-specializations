#!/usr/bin/env python3
"""Cross-check of the closed root-number formula (paper F.28, code/root_number_formula.py) and of the reflection formula against root numbers computed by Magma or PARI/GP.
The reflection formula (to be tested): for t = a/b, u = (t+1)/(t-1) = (a_u/b_u) in lowest terms, J = 2ab(a^2-b^2), R_t, R_u the products of the primes >= 5 dividing
H(a,b), H(a_u,b_u):   W(E_t) W(E_u) = l(t) * (-1)^(w(R_t)+w(R_u)) * ( -J / (R_t R_u) ),   l(t) = C2 * C3,
C2 = -1 iff (A,B) mod 16 in {(0,15),(1,0),(4,9),(7,4),(7,12),(9,4),(12,7),(12,9)},  C3 = -1 iff (A,B) mod 9 in {(1,6),(3,8)},  A = a_P/c, B = b_P/c for the primitive triple of t.
Workflow (the roots numbers must come from Magma or PARI; this sandbox has neither):
  python3 code/root_number_crosscheck.py --gen            writes crosscheck_input.txt, crosscheck.m (Magma) and crosscheck.gp (PARI/GP)
  magma -b crosscheck.m       (or   gp -q crosscheck.gp > crosscheck_out.txt)     -> a file of lines 'a b W'
  python3 code/root_number_crosscheck.py --check crosscheck_out.txt
  python3 code/root_number_crosscheck.py --selftest       tests the parser and the comparison with data generated from the formula (CI-safe; proves nothing about the formula)
Exit 0 = every line agrees; exit 1 otherwise. Options for --gen: --big adds the orbit points t_7, t_8 (large; Magma needs to factor 55- and 70-digit numbers)."""
import sys, os, random
from fractions import Fraction as Fr
from math import gcd
try:
    import sympy  # noqa
except ImportError:                      # small stand-in for factorint / jacobi_symbol
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import root_number_formula as RN

def H(a, b): return a**6-30*a**4*b**2-24*a**2*b**4-b**6
def norm(a, b):
    g = gcd(a, b); a //= g; b //= g
    return (-a, -b) if b < 0 else (a, b)
def refl(a, b):
    return None if a == b else norm(a+b, a-b)
def rad_ge5(n): return sorted(p for p in factorint(abs(n)) if p >= 5)

def make_list(big=False):
    S = set(); rnd = random.Random(1)
    for b in range(1, 11):
        for a in range(-10, 11):
            if gcd(a, b) == 1: S.add((a, b))
    while len(S) < 400:
        a, b = rnd.randint(-60, 60), rnd.randint(1, 60)
        if gcd(a, b) == 1: S.add((a, b))
    n_shared = n_sq = 0
    for b in range(1, 61):
        for a in range(-60, 61):
            if gcd(a, b) != 1 or a in (b, -b): continue
            u = refl(a, b); Rt, Ru = rad_ge5(H(a, b)), rad_ge5(H(*u))
            if set(Rt) & set(Ru) and n_shared < 80: S.add((a, b)); n_shared += 1
            if any(factorint(abs(H(a, b)))[p] > 1 for p in Rt) and n_sq < 40: S.add((a, b)); n_sq += 1
    for t in [(4, 1), (-4, 1), (3, 4), (4, 3), (5, 12), (12, 5), (2, 11), (11, 2), (7, 24), (24, 7), (-3, 1)]: S.add(t)
    # orbit points t_n = 1 - x(nP)
    def add(P, Q):
        if P is None: return Q
        if Q is None: return P
        (x1, y1), (x2, y2) = P, Q
        if x1 == x2:
            if y1+y2 == 0: return None
            l = (3*x1*x1-4*x1+2)/(2*y1)
        else: l = (y2-y1)/(x2-x1)
        x3 = l*l+2-x1-x2; return (x3, l*(x1-x3)-y1)
    P = (Fr(1), Fr(1)); Q = P
    for n in range(1, 9 if big else 7):
        t = 1-Q[0]; S.add(norm(t.numerator, t.denominator)); Q = add(Q, P)
    T = (Fr(0), Fr(0)); Q = P
    for n in range(1, 9 if big else 7):
        t = 1-add(Q, T)[0]; S.add(norm(t.numerator, t.denominator)); Q = add(Q, P)
    for (a, b) in list(S):                       # close under the reflection
        u = refl(a, b)
        if u is not None: S.add(u)
    return sorted(S, key=lambda p: (abs(p[0])+p[1], p))

def write_files(L):
    open('crosscheck_input.txt', 'w').write(''.join('%d %d\n' % p for p in L))
    with open('crosscheck.m', 'w') as f:
        f.write('// E_t : y^2 = x^3 + 4A x - 8B, A = (b^2-a^2)/(a^2+b^2), B = 2ab/(a^2+b^2); prints "a b W" per line\nL := [' + ', '.join('[%d, %d]' % p for p in L) + '];\n')
        f.write('for p in L do\n  a := p[1]; b := p[2]; D := a^2+b^2;\n  E := EllipticCurve([4*(b^2-a^2)/D, -16*a*b/D]);\n  fprintf("crosscheck_out.txt", "%o %o %o\\n", a, b, RootNumber(E));\nend for;\n')
    with open('crosscheck.gp', 'w') as f:
        f.write('\\\\ prints "a b W" per line: gp -q crosscheck.gp > crosscheck_out.txt\nL = [' + ', '.join('[%d, %d]' % p for p in L) + '];\n')
        f.write('for(i=1, #L, a=L[i][1]; b=L[i][2]; D=a^2+b^2; e=ellinit([0,0,0,4*(b^2-a^2)/D,-16*a*b/D]); print(a," ",b," ",ellrootno(e)));\n')
    print('wrote crosscheck_input.txt (%d curves), crosscheck.m, crosscheck.gp' % len(L))

C2 = {(0,15),(1,0),(4,9),(7,4),(7,12),(9,4),(12,7),(12,9)}; C3 = {(1,6),(3,8)}
def ell(a, b):
    P = RN.parts(a, b); c = P['c']
    A16, B16 = (P['a']*pow(c, -1, 16)) % 16, (P['b']*pow(c, -1, 16)) % 16
    A9, B9 = (P['a']*pow(c, -1, 9)) % 9, (P['b']*pow(c, -1, 9)) % 9
    return (-1 if (A16, B16) in C2 else 1)*(-1 if (A9, B9) in C3 else 1)
def rhs6_full(a, b):
    # l(t) of the note = (w2 w3)(E_t) (w2 w3)(E_u); by the class tables l = C2*C3 evaluated at t (the pair product), see docstring
    u = refl(a, b); Rt, Ru = rad_ge5(H(a, b)), rad_ge5(H(*u)); R1 = R2 = 1
    for p in Rt: R1 *= p
    for p in Ru: R2 *= p
    M = R1*R2; J = 2*a*b*(a*a-b*b)
    sym = jacobi_symbol((-J) % M, M) if M > 1 else 1
    return ell(a, b)*(-1)**(len(Rt)+len(Ru))*sym

def check(path):
    W = {}
    for ln in open(path):
        s = ln.split()
        if len(s) == 3: W[(int(s[0]), int(s[1]))] = int(s[2])
    print('read %d root numbers from %s' % (len(W), path))
    bad = []; cats = dict(shared=0, squareful=0, Dsq=0)
    for (a, b), w in W.items():
        P = RN.parts(a, b)
        if P['W'] != w: bad.append(('W(E_t)', a, b, w, P['W'], {k: P[k] for k in ('w2', 'w3', 'two_c', 'Y', 'J')}))
        if any(e > 1 for p, e in P['fac'].items()): cats['squareful'] += 1
        if any(e > 1 for p, e in factorint(P['c']).items() if p >= 5): cats['Dsq'] += 1
    npairs = 0; bad6 = []
    for (a, b), w in W.items():
        u = refl(a, b)
        if u is None or u not in W or a*b*(a*a-b*b) == 0: continue
        npairs += 1; Rt, Ru = rad_ge5(H(a, b)), rad_ge5(H(*u)); cats['shared'] += bool(set(Rt) & set(Ru))
        if w*W[u] != rhs6_full(a, b): bad6.append((a, b, u, w*W[u], rhs6_full(a, b)))
    print('closed formula (F.28) vs computed root numbers: %d mismatches among %d' % (len(bad), len(W)))
    for x in bad[:10]: print('   MISMATCH', x)
    print('reflection formula (6) vs computed products: %d mismatches among %d pairs (shared prime in %d pairs)' % (len(bad6), npairs, cats['shared']))
    for x in bad6[:10]: print('   MISMATCH', x)
    print('coverage: %d curves with a square prime power in H, %d with p^2 | c (p >= 5)' % (cats['squareful'], cats['Dsq']))
    ok = not bad and not bad6 and len(W) > 0
    print('RESULT:', 'all agree' if ok else 'DISAGREEMENT'); return 0 if ok else 1

if __name__ == '__main__':
    arg = sys.argv[1:]
    if '--gen' in arg: write_files(make_list('--big' in arg)); sys.exit(0)
    if '--check' in arg: sys.exit(check(arg[arg.index('--check')+1]))
    if '--selftest' in arg:
        L = make_list(False); import tempfile
        d = tempfile.mkdtemp(); p = os.path.join(d, 'out.txt')
        open(p, 'w').write(''.join('%d %d %d\n' % (a, b, RN.parts(a, b)['W']) for a, b in L))
        r1 = check(p)
        lines = open(p).read().split('\n'); a, b, w = lines[5].split(); lines[5] = '%s %s %d' % (a, b, -int(w)); open(p, 'w').write('\n'.join(lines))
        print('--- now one sign flipped on purpose; the check must fail:'); r2 = check(p)
        print('SELFTEST:', 'ok' if (r1 == 0 and r2 == 1) else 'FAILED'); sys.exit(0 if (r1 == 0 and r2 == 1) else 1)
    print(__doc__); sys.exit(2)
