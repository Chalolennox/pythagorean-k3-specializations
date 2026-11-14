#!/usr/bin/env python3
"""Appendix B / F.53: finite exact verification of the period laws along the ORIGINAL sequences t_n = 1 - x(nP) and t'_n = 1 - x(nP+T) on C : y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), for ALL n >= 2:
      eps(t_n) = +1  iff  n = 0, 1, 5 (mod 6);      eps(t'_n) = +1  iff  3 | n;        (eps = f(t) (ab/N), F.24)
together with  f(t_n) = +1  and  f(t'_n) of exact period 18  (n >= 2).
Same method as F.52 (Lemma R = the reciprocity function G of verify_mirror_collapse.py; Lemma L = local periodicity of the data along the orbit of P), with three differences:
  (i)   t = 1 - x(nP) = U/V with U = B^2 - A, V = B^2;   t' = 1 - 2/x(nP) = U/V with U = A - 2B^2, V = A (V = A is a perfect square, P' = B^2 is a perfect square, d = 2); x_n = A/B^2;
  (ii)  the real signs are NOT constant: for n >= 2 the point x_n lies in one of the intervals (0,1), (1,2), (2,oo) cut at the algebraic number 1 + t_0 (resp. 2/(1+t_0)); this gives four real-sign classes
        (sg, sF) in {((+,+,+,+),-), ((-,+,+,+),-), ((-,+,+,-),-), ((-,+,+,-),+)}, with sg = signs of (U, V, P', Q') and sF = sign F_s; all four occur and G is evaluated on all four;
  (iii) the factor that vanishes at x = 1 (U along t_n, Q' along t'_n) or at x = 2 (Q along t_n, U along t'_n) can have unbounded valuation at 2 AND at 3; each such factor is replaced by 'high' when its valuation is >= 6 and
        G is required to be independent of its (valuation parity, odd part mod 8) at 2 and of its (valuation parity, leading digit) at 3.
Usage: python3 code/verify_orbit_laws.py [--quick]   (full run a few minutes; --quick compares with the direct Jacobi computation on n <= 40 and uses shorter cycles; exit 0 = all checks pass).  Needs sympy and code/mirror_projection_eps.py.
"""
import sys, os, itertools, time
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_mirror_collapse as M
from verify_mirror_collapse import make, v_unit, G, L_of, A9B9, minperiod, Fs_int, sign

SQ = {'S0': ('V',), 'S0p': ('P',)}
LAW = {'S0': lambda n: 1 if n % 6 in (0, 1, 5) else -1, 'S0p': lambda n: 1 if n % 3 == 0 else -1}
CLASSES = [((1, 1, 1, 1), -1), ((-1, 1, 1, 1), -1), ((-1, 1, 1, -1), -1), ((-1, 1, 1, -1), 1)]
K0 = 6
def UV(Wf, n, mod, which):
    psi = Wf(n); psi2 = (psi*psi) % mod; phi = (psi2 - Wf(n + 1)*Wf(n - 1)) % mod
    return ((psi2 - phi) % mod, psi2) if which == 'S0' else ((phi - 2*psi2) % mod, phi)
def data2h(U, V, a, skip):
    """2-adic data from U, V mod 2^a; a factor of valuation >= K0 is reported as ('high', None)"""
    m = 2**a; U %= m; V %= m; d = 2 if (U % 2 == 1 and V % 2 == 1) else 1
    P, Q = (V - U) % m, (V + U) % m; ea = a - (1 if d == 2 else 0)
    Pp = (P // 2) % (m // 2) if d == 2 else P; Qp = (Q // 2) % (m // 2) if d == 2 else Q
    assert (P % 2 == 0) == (d == 2)
    out = {'d': d}
    for name, X, e in (('U', U, a), ('V', V, a), ('P', Pp, ea), ('Q', Qp, ea)):
        if name in skip: continue
        try: v, u = v_unit(X, 2, e)
        except ValueError: v, u = 99, 0
        if v >= K0: out[name] = ('high', None)
        else: assert e - v >= 3; out[name] = (v, u % 8)
    Fs = (U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6) % m; v, u = v_unit(Fs, 2, a); assert a - v >= 3 and v < K0; out['F'] = (v, u % 8)
    mm = m // 2 if d == 2 else m
    a_ = (((V*V - U*U) % m)//d) % mm; b_ = (((2*U*V) % m)//d) % mm; c_ = (((U*U + V*V) % m)//d) % mm
    assert mm % 16 == 0 and c_ % 2 == 1
    ic = pow(c_, -1, 16); out['A16'], out['B16'] = (a_*ic) % 16, (b_*ic) % 16; out['c8'] = c_ % 8
    return out
def data3h(U, V, b, skip):
    m = 3**b; U %= m; V %= m; P, Q = (V - U) % m, (V + U) % m; out = {}
    for nm, X in (('U', U), ('V', V), ('P', P), ('Q', Q)):
        if nm in skip: continue
        try: v, u = v_unit(X, 3, b)
        except ValueError: v, u = 99, 0
        if v >= K0: out[nm] = ('high', None)
        else: assert b - v >= 2; out[nm] = (v, u % 3)
    Fs = (U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6) % m; v, u = v_unit(Fs, 3, b); assert b - v >= 2 and v < K0; out['F'] = (v, u % 3)
    return out, U % 9, V % 9
def build(which, N2, N3, a=16, b=14, L=80):
    W2 = make(2**L, True); W3 = make(3**b, False); T2 = []; T3 = []
    for n in range(1, N2 + 1):
        U, V = UV(W2, n, 2**L, which); T2.append(data2h(U % 2**a, V % 2**a, a, SQ[which]))
    for n in range(1, N3 + 1):
        U, V = UV(W3, n, 3**b, which); T3.append(data3h(U, V, b, SQ[which]))
    return T2, T3
def key2(d): return tuple(sorted((k, v) for k, v in d.items()))
def key3(t): d3, U9, V9 = t; return (tuple(sorted(d3.items())), U9, V9)
OK = True
def check(name, cond):
    global OK; OK = OK and bool(cond); print('%-4s %s' % ('OK' if cond else 'FAIL', name), flush=True)
QUICK = '--quick' in sys.argv
if __name__ == '__main__':
    t0 = time.time()
    from mirror_projection_eps import eps as eps_direct, orbit
    import sympy as sp
    # (A) direct exact computation: the laws and the real-sign classes for 2 <= n <= NV
    NV = 40 if QUICK else 150; xs = orbit(NV + 1); t0r = max(r for r in sp.Poly(sp.Symbol('t')**6 - 30*sp.Symbol('t')**4 - 24*sp.Symbol('t')**2 - 1).nroots(n=30) if abs(sp.im(r)) < 1e-20)
    t0r = float(sp.re(t0r)); bad_law = bad_cls = 0; seen = {'S0': set(), 'S0p': set()}
    for n in range(2, NV + 1):
        x = xs[n - 1]; assert x not in (1, 2)
        for which, t in (('S0', 1 - x), ('S0p', 1 - 2/x)):
            U, V = t.numerator, t.denominator; d = 2 if (U % 2 and V % 2) else 1; cls = ((sign(U), sign(V), sign((V - U)//d), sign((V + U)//d)), sign(Fs_int(U, V)))
            xf = float(x); pred = ((1, 1, 1, 1), -1) if (xf < 1 and which == 'S0') or (xf > 2 and which == 'S0p') else None
            if which == 'S0': pred = CLASSES[0] if xf < 1 else CLASSES[1] if xf < 2 else CLASSES[2] if xf < 1 + t0r else CLASSES[3]
            else: pred = CLASSES[3] if xf < 2/(1 + t0r) else CLASSES[2] if xf < 1 else CLASSES[1] if xf < 2 else CLASSES[0]
            bad_cls += (cls != pred); seen[which].add(cls); bad_law += (eps_direct(t) != LAW[which](n))
    check('direct exact computation, 2 <= n <= %d: eps(t_n), eps(t\'_n) follow the two laws (%d failures); the real-sign class of every value is the one predicted by the position of x_n relative to 1, 2, 1 + t_0 = %.6f (%d mismatches); classes seen: %d and %d of 4' % (NV, bad_law, 1 + t0r, bad_cls, len(seen['S0']), len(seen['S0p'])), bad_law == 0 and bad_cls == 0)
    # (B) the local data along the orbit of P: bounded valuations, periods, high classes; G on all four real classes
    for which in ('S0', 'S0p'):
        N2 = 4096 if not QUICK else 600; N3 = 3**8*3 + 40 if not QUICK else 3**8*2 + 40
        T2, T3 = build(which, N2, N3)
        p2 = minperiod([key2(d) for d in T2], 1); p3 = minperiod([key3(t) for t in T3], 1); Lp = p2*p3//gcd(p2, p3)
        high2 = {k for d in T2 for k, v in d.items() if isinstance(v, tuple) and v[0] == 'high'}; high3 = {k for t in T3 for k, v in t[0].items() if v[0] == 'high'}
        v2max = max([v[0] for d in T2 for k, v in d.items() if isinstance(v, tuple) and k in 'UVPQF' and k not in high2 and v[0] != 'high'] or [0])
        v3max = max([v[0] for t in T3 for k, v in t[0].items() if k not in high3 and v[0] != 'high'] or [0])
        fcls = {}
        for n, d in enumerate(T2, 1):
            if n >= 2: fcls.setdefault(n % p2, set()).add(key2(d))
        fcls3 = {}
        for n, t in enumerate(T3, 1):
            if n >= 2: fcls3.setdefault(n % p3, set()).add(key3(t))
        bad_f = []; fseq = []; bad_indep = bad_law = n2h = n3h = tested = 0
        for n in range(2, Lp + 2):
            d2 = T2[(n - 1) % p2]; d3b, U9, V9 = T3[(n - 1) % p3]; A9B9v = A9B9(U9, V9, d2['d']); fseq.append(L_of(d2, A9B9v))
            h2 = [k for k, v in d2.items() if isinstance(v, tuple) and v[0] == 'high']; h3 = [k for k, v in d3b.items() if v[0] == 'high']; n2h += bool(h2); n3h += bool(h3)
            c2 = list(itertools.product(*[[(K0 + r, u) for r in (0, 1) for u in (1, 3, 5, 7)]]*len(h2))) if h2 else [()]
            c3 = list(itertools.product(*[[(K0 + r, u) for r in (0, 1) for u in (1, 2)]]*len(h3))) if h3 else [()]
            for sg, sF in CLASSES:
                outs = set()
                for a2 in c2:
                    for a3 in c3:
                        D2 = dict(d2); D3 = dict(d3b)
                        for k, v in zip(h2, a2): D2[k] = v
                        for k, v in zip(h3, a3): D3[k] = v
                        res, A16, B16, c8 = G(D2, D3, sg, sF, SQ[which]); outs.add(L_of(D2, A9B9v)*res)
                tested += 1; bad_indep += (len(outs) != 1); bad_law += (len(outs) != 1 or next(iter(outs)) != LAW[which](n))
        fp = minperiod(fseq + fseq + fseq, 0)
        check('%s: valuations of the factors that never become high and of F_s are <= %d at 2 and <= %d at 3 (factors that become high: at 2 %s, at 3 %s; the others are bounded, the high factor\'s data, valuation < %d or "high", are periodic like everything else); '
              'every data class is a function of n mod %d (2-adic) and n mod %d (3-adic), which divide 2^8 and 3^8 (cycles checked: n <= %d, n <= %d); joint period %d'
              % (which, v2max, v3max, sorted(high2), sorted(high3), K0, p2, p3, N2, N3, Lp),
              2**8 % p2 == 0 and 3**8 % p3 == 0 and v2max <= 1 and v3max <= 4 and all(len(v) == 1 for v in fcls.values()) and all(len(v) == 1 for v in fcls3.values()))
        check('%s: over n = 2..%d (%d classes of n x real signs, %d with a high factor at 2, %d at 3): G independent of the high factors\' (valuation parity, odd part / leading digit): %d violations; G = law for all four real-sign classes: %d failures'
              % (which, Lp + 1, tested, n2h, n3h, bad_indep, bad_law), bad_indep == 0 and bad_law == 0)
        if which == 'S0': check('S0: f(t_n) = +1 for n = 2..%d (all residue classes of the joint period)' % (Lp + 1), all(f == 1 for f in fseq))
        else: check('S0p: f(t\'_n) has exact period %d (n >= 2); values over one period: %s' % (fp, ''.join('+' if f == 1 else '-' for f in fseq[:fp])), fp == 18)
    print('ALL CHECKS PASS (%.0f s)' % (time.time() - t0) if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
