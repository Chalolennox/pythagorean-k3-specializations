#!/usr/bin/env python3
"""F.51 (b): finite exact verification that, along the mirror sequences t = 1 + x(nP) and t = 1 + 2/x(nP) on C : y^2 = x^3 - 2x^2 + 2x, P = (1,1),
        eps(1 + x_n) = h(n) * s_n   and   eps(1 + 2/x_n) = -h(n) * s'_n   for ALL n >= 1,     h(n) = +1 iff 3 | n,  s_n, s'_n = sign F_s,
where eps = f(t) (ab/N) is the periodic-part factor of F.24.  Steps (the numbering of F.51 (b)):
  (1) an exact reciprocity formula eps = G(local data) is validated against the direct Jacobi computation for 596 values (n = 2..150, all four sequences 1 -+ x(nP), 1 -+ 2/x(nP));
  (2) the division-polynomial values psi_n(P) are computed modulo 2^80 and 3^14 and checked against the exact orbit (n <= 60);
  (3) the remaining 2-adic and 3-adic data are periodic (periods 8 and 729, checked over many periods; joint period 5832); one factor has unbounded 3-adic valuation and is shown not to matter;
  (4) over a full period, G = h(n) * sign F_s for both signs.
Usage: python3 code/verify_mirror_collapse.py [--quick]   (full run about 2 minutes; --quick compares the formula on n <= 40 only and uses shorter period checks, about 20 s; exit 0 = all checks pass).   Needs sympy and code/mirror_projection_eps.py (direct Jacobi computation).
"""
import sys, os, itertools, time
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
"""[section 1] Division-polynomial values psi_n(P) of C : y^2 = x^3 - 2x^2 + 2x at P = (1,1), computed modulo m (psi_2 = 2 division handled by working modulo 2^L and tracking precision),
with x(nP) = phi_n / psi_n^2,  phi_n = psi_n^2 - psi_{n+1} psi_{n-1}.  Doubling formulas only (division by psi_2 = 2)."""
import sys
sys.setrecursionlimit(10000)
W0 = {0: 0, 1: 1, 2: 2, 3: 3, 4: -20, -1: -1, -2: -2, -3: -3, -4: 20}     # psi_n(P) for small |n|; psi_{-n} = -psi_n
def make(mod, twoadic):
    """returns W(n) mod `mod`.  If twoadic, mod is 2^L and the division by psi_2 = 2 is the exact integer division of an even residue (precision drops one bit per level);
    otherwise mod is coprime to 2 and the division is multiplication by 2^-1."""
    cache = {k: v % mod for k, v in W0.items()}
    inv2 = None if twoadic else pow(2, -1, mod)
    def half(x):
        if twoadic:
            assert x % 2 == 0, "numerator odd: impossible for an integer identity"
            return (x // 2) % mod
        return (x * inv2) % mod
    def W(n):
        if n in cache: return cache[n]
        if n < 0: r = (-W(-n)) % mod
        elif n % 2 == 1:
            j = (n - 1)//2                     # W_{2j+1} = W_{j+2} W_j^3 - W_{j-1} W_{j+1}^3
            r = (W(j + 2)*W(j)**3 - W(j - 1)*W(j + 1)**3) % mod
        else:
            j = n//2                           # W_{2j} = (W_j / W_2)(W_{j+2} W_{j-1}^2 - W_{j-2} W_{j+1}^2)
            r = half(W(j)*(W(j + 2)*W(j - 1)**2 - W(j - 2)*W(j + 1)**2))
        cache[n] = r; return r
    return W

"""[section 2] Exact reciprocity reduction of  eps(t) = L * (ab/N)  for t = U/V (reduced, V > 0):  d = 2 iff U, V both odd;  P' = (V-U)/d, Q' = (V+U)/d;  a = d P'Q', b = 2UV/d, c = (U^2+V^2)/d;  ab = 2 U V P' Q';
F_s = U^6 - 30U^4V^2 - 24U^2V^4 - V^6 = s_F |F_s|,  e2 = v2(F_s), e3 = v3(F_s),  N = |F_s| / (2^e2 3^e3),  L = -w2 w3 (2/c).
(ab/N) = (2/N) prod_{X in {U,V,P',Q'}} (X/N);  X = sigma 2^r 3^k Y (Y > 0 prime to 6):  (X/N) = (sigma/N)(2/N)^r (3/N)^k (Y/N),  (Y/N) = (N/Y) (-1)^{((Y-1)/2)((N-1)/2)},
(N/Y) = (s_F/Y) (g_X/Y) (2/Y)^e2 (3/Y)^e3  with  F_s = f_X mod Y,  g_U = -1 (f_U = -V^6),  g_V = 1 (f_V = U^6),  g_P' = g_Q' = -6 (f = -54 U^6).
Every symbol is a character of Y or N modulo 24, so the result depends only on 2-adic data (valuations and odd parts mod 8) and 3-adic data (valuations and parts mod 3), the signs of U, V, P', Q', and s_F.
Pure functions of those data: data2, data3, G."""
S2 = {(0, 1), (1, 0), (4, 9), (8, 1), (9, 4), (12, 9), (15, 0), (15, 8)}
def v_unit(x, p, e):
    """valuation and unit part (mod p^(e - v)) of an integer known modulo p^e; raises if x = 0 mod p^e"""
    m = p**e; x %= m
    if x == 0: raise ValueError("insufficient precision")
    v = 0
    while x % p == 0: x //= p; v += 1
    return v, x
def data2(U, V, a, skip=()):
    """2-adic data from U, V modulo 2^a (integers or residues).  Units are reported modulo 8 (for X: the unit part of X itself, signed)."""
    m = 2**a; U %= m; V %= m; d = 2 if (U % 2 == 1 and V % 2 == 1) else 1
    P, Q = (V - U) % m, (V + U) % m                       # P' = P/d, Q' = Q/d known modulo 2^(a-1) when d = 2
    ea = a - (1 if d == 2 else 0)
    out = {'d': d}
    for name, X, e in (('U', U, a), ('V', V, a), ('P', P//d if False else None, ea), ('Q', None, ea)):
        pass
    def dv(X, e):
        v, u = v_unit(X, 2, e); assert e - v >= 3, "need 3 more bits"; return v, u % 8
    Pp = (P // 2) % (m // 2) if d == 2 else P; Qp = (Q // 2) % (m // 2) if d == 2 else Q
    assert (P % 2 == 0) == (d == 2)
    for name, X, e in (('U', U, a), ('V', V, a), ('P', Pp, ea), ('Q', Qp, ea)):
        if name not in skip: out[name] = dv(X, e)
    # F_s mod 2^a
    Fs = (U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6) % m; out['F'] = dv(Fs, a)
    # c, a, b mod 16 (need them modulo 2^4 after division by d): a_ = (V^2-U^2)/d, b_ = 2UV/d, c_ = (U^2+V^2)/d  -> computed modulo 2^(a-1)
    mm = m // 2 if d == 2 else m
    a_ = (((V*V - U*U) % m)//d) % mm; b_ = (((2*U*V) % m)//d) % mm; c_ = (((U*U + V*V) % m)//d) % mm
    assert mm % 16 == 0 and c_ % 2 == 1
    ic = pow(c_, -1, 16); out['A16'], out['B16'] = (a_*ic) % 16, (b_*ic) % 16; out['c8'] = c_ % 8
    return out
def data3(U, V, b, skip=()):
    m = 3**b; U %= m; V %= m; P, Q = (V - U) % m, (V + U) % m
    d2 = 2 if None else None
    def dv(X):
        v, u = v_unit(X, 3, b); assert b - v >= 2; return v, u % 3
    out = {nm: dv(X) for nm, X in (('U', U), ('V', V), ('P', P), ('Q', Q)) if nm not in skip}   # division by d (a unit mod 3) changes P, Q by a unit: handled in G through d
    Fs = (U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6) % m; out['F'] = dv(Fs)
    return out
def G(d2, d3, sg, sF, squares=()):
    """sg = signs (sigma_U, sigma_V, sigma_P', sigma_Q') of U, V, P', Q';  sF = sign of F_s.  d2['d'] is d (the 3-adic units of P', Q' are those of P, Q divided by d: 2^-1 = 2 mod 3)."""
    d = d2['d']; inv_d3 = 1 if d == 1 else 2                                  # 2^-1 mod 3
    e2, f2 = d2['F']; e3, f3 = d3['F']
    # N = |F_s| / (2^e2 3^e3)  modulo 8 and modulo 3
    inv3k = lambda k: pow(3, k, 8)                                              # 3^-k = 3^k mod 8 (3^2 = 1)
    N8 = (sF * f2 * inv3k(e3)) % 8 if True else None                           # |F_s| = sF * F_s
    N3 = (sF * f3 * pow(2, e2, 3)) % 3                                          # 2^-e2 = 2^e2 mod 3
    jm1 = lambda Y8: 1 if Y8 % 4 == 1 else -1
    j2 = lambda Y8: 1 if Y8 % 8 in (1, 7) else -1
    j3 = lambda Y8, Y3: (1 if Y3 == 1 else -1) * jm1(Y8)
    JN2 = j2(N8); JN3 = (1 if N3 == 1 else -1) * jm1(N8); JNm1 = jm1(N8)
    res = JN2                                                                   # the factor 2 of ab = 2 U V P' Q'
    gtab = {'U': 'm1', 'V': 'one', 'P': 'm6', 'Q': 'm6'}
    for (name, sig) in zip(('U', 'V', 'P', 'Q'), sg):
        if name in squares:                                                     # |X| is a perfect square prime to N: (X/N) = (sigma/N)
            res *= (JNm1 if sig == -1 else 1); continue
        r, u2 = d2[name]; k, u3 = d3[name]
        if name in ('P', 'Q') and d == 2: u3 = (u3 * inv_d3) % 3
        # |X| = sig * X: odd part mod 8 and unit part mod 3 of |X|
        o8 = (sig * u2) % 8; o3 = (sig * u3) % 3
        Y8 = (o8 * inv3k(k)) % 8; Y3 = (o3 * pow(2, r, 3)) % 3                  # Y = |X| / (2^r 3^k) modulo 8 and modulo 3
        f = (JNm1 if sig == -1 else 1) * (j2(N8) ** r) * (JN3 ** k)             # (sigma/N)(2/N)^r (3/N)^k
        # (N/Y) = (sF/Y)(g/Y)(2/Y)^e2 (3/Y)^e3
        nY = (jm1(Y8) if sF == -1 else 1)
        g = gtab[name]
        if g == 'm1': nY *= jm1(Y8)
        elif g == 'm6': nY *= jm1(Y8) * j2(Y8) * j3(Y8, Y3)
        nY *= (j2(Y8) ** e2) * (j3(Y8, Y3) ** e3)
        rec = -1 if (Y8 % 4 == 3 and N8 % 4 == 3) else 1                        # (-1)^{((Y-1)/2)((N-1)/2)}
        res *= f * nY * rec
    # L = -w2 w3 (2/c)
    A16, B16, c8 = d2['A16'], d2['B16'], d2['c8']
    return res, A16, B16, c8
def L_of(d2, A9B9):
    w2 = -1 if (d2['A16'], d2['B16']) in S2 else 1; w3 = -1 if A9B9 == (3, 8) else 1
    two_c = 1 if d2['c8'] in (1, 7) else -1
    return -w2*w3*two_c
def A9B9(U, V, d):
    m = 9; U %= m; V %= m; a_ = ((V*V - U*U) * pow(d, -1, 9)) % 9; b_ = ((2*U*V) * pow(d, -1, 9)) % 9; c_ = ((U*U + V*V) * pow(d, -1, 9)) % 9
    ic = pow(c_, -1, 9); return (a_*ic) % 9, (b_*ic) % 9
def eps_from_residues(U, V, sg, sF, a=12, b=10, squares=()):
    """eps(t) from the residues of U, V modulo 2^a and 3^b, the signs sg of (U, V, P', Q') and sF = sign F_s"""
    d2 = data2(U, V, a, squares); d3 = data3(U, V, b, squares); res, A16, B16, c8 = G(d2, d3, sg, sF, squares)
    return L_of(d2, A9B9(U, V, d2['d'])) * res

"""[section 3] Finite verification of  eps^+_n = h(n) * s_n  for ALL n >= 1 (see F.50 / the Proposition):  eps = G(2-adic data, 3-adic data, signs, s_F) exactly (eps_formula.py).
Along S1 (t = 1 + x(nP)) U = B^2 + A, V = B^2 (a square), P = V - U = -A, Q = V + U = 2B^2 + A;  along S2 (t = 1 + 2/x(nP)) V = A, U = A + 2B^2, P = -2B^2 (P' = -B^2, a square), Q' = A + B^2.
Squares drop out ((V/N) = 1, (P'/N) = (-1/N)).  One factor has UNBOUNDED 3-adic valuation (Q along S1, U along S2: it vanishes at x = -2, a point of E(Z_3) in the closure of <P>): its valuation k and leading digit o3 are treated as FREE variables.
Claims verified: (1) G does not depend on (k mod 2, o3) of the free factor, for every value of the remaining data that occurs;  (2) the remaining 2-adic and 3-adic data are periodic in n (periods found, checked over >= 3 periods);
(3) over one full joint period, G(n, s_F) = h(n) s_F for both signs s_F = +-1."""
SQ = {'S1': ('V',), 'S2': ('P',)}; FREE = {'S1': 'Q', 'S2': 'U'}
SIGNS = (1, 1, -1, 1)                              # signs of (U, V, P', Q') along both mirror sequences
def UV(Wf, n, mod, which):
    psi = Wf(n); psi2 = (psi*psi) % mod; phi = (psi2 - Wf(n + 1)*Wf(n - 1)) % mod
    return (((psi2 + phi) % mod, psi2) if which == 'S1' else ((phi + 2*psi2) % mod, phi))
def hfun(which, n): return (1 if n % 3 == 0 else -1) * (1 if which == 'S1' else -1) if which == 'S1' else (-1 if n % 3 == 0 else 1)
def h(which, n):
    return (1 if n % 3 == 0 else -1) if which == 'S1' else (-1 if n % 3 == 0 else 1)
K0 = 6
def build(which, N2, N3, a=14, b=14, L=80):
    """lists of the bounded 2-adic and 3-adic data for n = 1..N (the free factor's (k, o3) removed)"""
    W2 = make(2**L, True); W3 = make(3**b, False); free = FREE[which]; T2 = []; T3 = []; kmax = 0; kdata = []
    for n in range(1, N2 + 1):
        U, V = UV(W2, n, 2**L, which); d2 = data2(U % 2**a, V % 2**a, a, SQ[which]); T2.append(d2)
    for n in range(1, N3 + 1):
        U, V = UV(W3, n, 3**b, which)
        # d (2^-1 handled in G via d2['d']); here only the 3-adic residues
        P, Q = (V - U) % 3**b, (V + U) % 3**b; d3 = {}
        for nm, X in (('U', U), ('V', V), ('P', P), ('Q', Q)):
            if nm in SQ[which]: continue
            try: v, u = v_unit(X, 3, b)
            except ValueError: v, u = 99, 0
            if nm == free:
                kdata.append(v if v < b - 2 else None); d3[nm] = (v, u % 3) if v < K0 else ('high', None)
            else:
                assert v < b - 2, "non-free factor with large valuation"; d3[nm] = (v, u % 3)
        Fs = (U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6) % 3**b; v, u = v_unit(Fs, 3, b); assert v < b - 2; d3['F'] = (v, u % 3)
        d3['A9B9'] = None; T3.append((d3, U % 9, V % 9))
    return T2, T3, kdata
def key2(d): return tuple(sorted((k, v) for k, v in d.items()))
def key3(t): d3, U9, V9 = t; return (tuple(sorted((k, v) for k, v in d3.items() if k != 'A9B9')), U9, V9)
def minperiod(keys, start=0):
    N = len(keys)
    for p in range(1, N//3 + 1):
        if all(keys[i] == keys[i + p] for i in range(start, N - p)): return p
    return None

# ---------------------------------------------------------------- driver
def sign(x): return 1 if x > 0 else -1
def Fs_int(U, V): return U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6
def check(name, cond):
    global OK; OK = OK and bool(cond); print('%-4s %s' % ('OK' if cond else 'FAIL', name), flush=True)
OK = True
QUICK = '--quick' in sys.argv
if __name__ == '__main__':
    t0 = time.time()
    from mirror_projection_eps import eps as eps_direct, orbit
    # (2) engine against the exact orbit
    NV = 40 if QUICK else 150; xs = orbit(max(NV, 60)); bad = 0
    for mod, two, modv in ((3**8, False, 3**8), (2**80, True, 2**40)):
        Wf = make(mod, two)
        for n in range(1, 61):
            psi = Wf(n); phi = (psi*psi - Wf(n + 1)*Wf(n - 1)) % mod; x = xs[n - 1]
            bad += ((psi*psi - x.denominator) % modv != 0) or ((phi - x.numerator) % modv != 0)
    check('division-polynomial engine reproduces psi_n^2 = denominator and phi_n = numerator of x(nP), n <= 60, modulo 3^8 and 2^40', bad == 0)
    # (1) the reciprocity formula against the direct Jacobi computation
    seqs = {'1 - x(nP)': (lambda x: 1 - x, ('V',)), '1 - x(nP+T)': (lambda x: 1 - 2/x, ('P',)), '1 + x(nP)': (lambda x: 1 + x, ('V',)), '1 + x(nP+T)': (lambda x: 1 + 2/x, ('P',))}
    tot = bad = 0; M = 2**40*3**30
    for name, (f, sq) in seqs.items():
        for n in range(2, NV + 1):
            t = f(xs[n - 1]); U, V = t.numerator, t.denominator
            if U == 0 or abs(U) == V: continue
            d = 2 if (U % 2 and V % 2) else 1; sg = (sign(U), sign(V), sign((V - U)//d), sign((V + U)//d))
            tot += 1; bad += (eps_from_residues(U % M, V % M, sg, sign(Fs_int(U, V)), 40, 30, sq) != eps_direct(t))
    check('reciprocity formula = direct Jacobi computation for %d values (n = 2..%d, four sequences)' % (tot, NV), bad == 0 and tot == (596 if not QUICK else 4*(NV - 1)))
    # (3), (4) periods, free factor, law over a full period
    for which in ('S1', 'S2'):
        N3 = (3*729 + 40) if QUICK else 3**8*3 + 40; T2, T3, kdata = build(which, 200 if QUICK else 4000, N3)
        p2 = minperiod([key2(d) for d in T2]); p3 = minperiod([key3(t) for t in T3]); Lp = p2*p3//gcd(p2, p3)
        free = FREE[which]; bad_indep = bad_law = nhigh = 0
        for n in range(1, Lp + 1):
            d2 = T2[(n - 1) % p2]; d3b, U9, V9 = T3[(n - 1) % p3]; A9B9v = A9B9(U9, V9, d2['d']); high = (d3b[free][0] == 'high'); nhigh += high
            for sF in (1, -1):
                outs = set(); combos = list(itertools.product((0, 1), (1, 2))) if high else [None]
                for c in combos:
                    d3 = dict(d3b)
                    if high: d3[free] = (K0 + c[0], c[1])
                    res, A16, B16, c8 = G(d2, d3, SIGNS, sF, SQ[which]); outs.add(L_of(d2, A9B9v)*res)
                bad_indep += (len(outs) != 1); bad_law += (len(outs) != 1 or next(iter(outs)) != h(which, n)*sF)
        check('%s: 2-adic period %d, 3-adic period %d, joint period %d; free-factor valuation >= %d in %d residue classes; G independent of its (valuation parity, leading digit): %d violations; G = h(n) sign F_s for n = 1..%d, both signs: %d failures'
              % (which, p2, p3, Lp, K0, nhigh, bad_indep, Lp, bad_law), (p2, p3, Lp, nhigh, bad_indep, bad_law) == (8, 729, 5832, 16, 0, 0))
    print('ALL CHECKS PASS (%.0f s)' % (time.time() - t0) if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
