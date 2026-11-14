#!/usr/bin/env python3
"""Audit of the proposed smooth proper model over Z_(5) of the twist of S by d(t) = t(t-1)  (other d: set the environment variable TWIST_D, e.g. TWIST_D="t**2-1")
(notes/2026-11-07_integral_resolution_note.md).  Everything is recomputed in sympy, over Q and over F_5; no Magma is used.
  1. global data (equation, degrees, discriminant, fibre types, coprimality over Q and F_5)
  2. the residual cubics of the D4 blowups (this is where the note's z^3 - 128 disagrees with its own equation)
  3. every strict-transform equation of the note, as an exact identity
  4. fibrewise Jacobian smoothness of every chart over q = 0 (resp. s = 0), over Q and F_5, singular locus = declared centre
  5. saturation: in every chart the exceptional coordinate is not a zero divisor (dim V(g,h) = dim V(g) - 1)
  6. the Hessian determinants at the three final A1 centres, and the overlap-ideal equalities for the centres B, C2 and the D4 centre
Needs: python3, sympy.  Takes under a minute.  Exit status 0 = everything expected passes (lines marked FINDING report disagreements with the note)."""
import sys, time, itertools, signal, warnings
warnings.filterwarnings('ignore')
import sympy as sp
from sympy import symbols, Poly, expand, groebner, Matrix, rem, gcd, factor_list, discriminant, cancel
t = symbols('t')
import os
DSTR = os.environ.get('TWIST_D', 't*(t-1)')            # the twist polynomial d(t); default t(t-1); try TWIST_D='t**2-1'
q = t**2 + 1; d = sp.sympify(DSTR, locals={'t': t}); a = 4*(1 - t**2)*d**2; b = 16*t*d**3
DROOTS = sorted(sp.roots(Poly(d, t)).keys(), key=lambda r_: int(r_))      # the two zeros of d, where the I0* fibres sit
PRIMARY = (DSTR == 't*(t-1)')
f6 = t**6 - 30*t**4 - 24*t**2 - 1
ALLOK = True
def check(name, cond, extra=''):
    global ALLOK; ALLOK &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra), flush=True)
def finding(msg): print('FINDING', msg, flush=True)
class TO(Exception): pass
def _h(s, fr): raise TO()
signal.signal(signal.SIGALRM, _h)
def sing_gb(eqs, vs, mod, restr, redp, limit=300):
    """Groebner basis of (eqs, restr, maximal minors of the Jacobian) over Q (mod=None) or F_p. redp = (poly, var) to reduce by, or None."""
    red=(lambda e: rem(expand(e), redp[0], redp[1])) if redp else (lambda e: expand(e))
    r=len(eqs); J=[[red(sp.diff(e,v)) for v in vs] for e in eqs]
    gens=[red(e) for e in eqs]+list(restr)
    for cols in itertools.combinations(range(len(vs)),r):
        m=red(Matrix([[J[i][c] for c in cols] for i in range(r)]).det(method='berkowitz'))
        if m!=0: gens.append(m)
    kw={'modulus':mod} if mod else {'domain':'QQ'}
    signal.alarm(limit)
    try: return groebner(gens,*vs,order='grevlex',**kw)
    except TO: return None
    finally: signal.alarm(0)
def in_rad(GB,p,maxpow=4): return any(GB.contains(expand(p**k)) for k in range(1,maxpow+1))
def analyse(name, eqs, vs, centres, restr=None, redp='default', mods=(None,5)):
    restr=[t**2+1] if restr is None else restr
    redp=(t**2+1,t) if redp=='default' else redp
    parts=[]; allok=True
    for mod in mods:
        lab='Q ' if mod is None else 'F5'
        t0=time.time(); GB=sing_gb(eqs,vs,mod,restr,redp)
        if GB is None: parts.append('%s: TIMEOUT'%lab); allok=False; continue
        empty=(list(GB.exprs)==[1])
        if not centres:
            ok=empty; verdict='smooth over the restriction' if ok else 'SINGULAR: %s'%[str(g)[:60] for g in GB.exprs][:4]
        elif empty: ok=False; verdict='NO singular points, but %d centre(s) declared'%len(centres)
        else:
            kw={'modulus':mod} if mod else {'domain':'QQ'}
            cgbs=[groebner(list(restr)+list(c),*vs,order='grevlex',**kw) for c in centres]
            inside=all(all(cg.contains(g) for g in GB.exprs) for cg in cgbs)
            if len(centres)==1: covers=all(in_rad(GB,g) for g in list(centres[0])+list(restr))
            else: covers=all(in_rad(GB,expand(sp.Mul(*p))) for p in itertools.product(*[list(c)+list(restr) for c in centres]))
            ok=inside and covers
            verdict=('singular locus = the %d declared centre(s)'%len(centres)) if ok else 'DIFFERS from declared centres: %s'%[str(g)[:50] for g in GB.exprs][:4]
        allok&=ok; parts.append('%s: %s (%.1fs)'%(lab,verdict,time.time()-t0))
    print('%-4s %-46s %s'%('OK' if allok else 'FAIL',name,' | '.join(parts)),flush=True)
    return allok
def dim_gb(GB, vs):
    if list(GB.exprs)==[1]: return None
    lms=[]
    for g in GB.polys:
        mons=g.monoms(order='grevlex'); lms.append(mons[0])
    best=0
    for k in range(len(vs)+1):
        for S in itertools.combinations(range(len(vs)),k):
            if not any(all(m[i]==0 for i in range(len(vs)) if i not in S) for m in lms): best=max(best,k)
    return best
def sat(name, eqs, vs, h, restr=None, redp='default'):
    """dim V(eqs, h, restr) must equal (#vars - #eqs) - 1 over Q and F5, or V must be empty: then h is not a zero divisor on any component."""
    restr=[t**2+1] if restr is None else restr
    redp=(t**2+1,t) if redp=='default' else redp
    red=(lambda e: rem(expand(e), redp[0], redp[1])) if redp else (lambda e: expand(e))
    want=len(vs)-len(eqs)-1; res=[]; ok=True
    for mod in (None,5):
        kw={'modulus':mod} if mod else {'domain':'QQ'}
        GB=groebner([red(e) for e in eqs]+[red(h)]+list(restr),*vs,order='grevlex',**kw)
        dm=dim_gb(GB,vs); good=(dm is None) or dm==want
        ok&=good; res.append('%s: dim V(g,h) = %s'%('Q ' if mod is None else 'F5','empty' if dm is None else dm))
    print('%-4s %-46s expected %d | %s'%('OK' if ok else 'FAIL',name,want,' | '.join(res)),flush=True); return ok

def run(ok):
    global ALLOK; ALLOK &= bool(ok)

# ------------------------------------------------------------------------------------------------------------------ 1. global data
X, Y, U, V, z = symbols('X Y U V z')
print('=== 1. global data')
check('deg a4 = 12, deg a6 = 17 (chi = 3, so the surface is not a K3)', Poly(expand(a*q**3), t).degree() == 12 and Poly(expand(b*q**5), t).degree() == 17)
Delta = expand(-16*(4*(a*q**3)**3 + 27*(b*q**5)**2))
check('Delta = 4096 d^6 q^9 f, degree 36, so the fibre at infinity is smooth', expand(Delta - 4096*d**6*q**9*f6) == 0 and Poly(Delta, t).degree() == 36)
check('Euler number 2*6 (I0*) + 2*9 (III*) + 6*1 (I1) = 36 = 12 chi', 2*6 + 2*9 + 6 == 36)
for mod in (None, 5):
    kw = {'modulus': mod} if mod else {}
    deg = lambda p1, p2: Poly(gcd(Poly(p1, t, **kw), Poly(p2, t, **kw)), t, **kw).degree()
    lab = 'F5' if mod else 'Q '
    check('%s: gcd(q,q\') = gcd(q,d) = gcd(q,f) = gcd(f,f\') = gcd(d,f) = 1' % lab, all(v_ == 0 for v_ in (deg(q, q.diff(t)), deg(q, d), deg(q, f6), deg(f6, f6.diff(t)), deg(d, f6))))
def mult(poly, fac):
    k = 0; p = Poly(poly, t); g = Poly(fac, t)
    while True:
        quo, r_ = sp.div(p, g)
        if r_.is_zero: k += 1; p = quo
        else: return k
va = lambda p_, tt: mult(p_, tt)
v_q = (va(expand(a*q**3), q), va(expand(b*q**5), q), va(Delta, q))
v_r = [(va(expand(a*q**3), t - r_), va(expand(b*q**5), t - r_), va(Delta, t - r_)) for r_ in DROOTS]
check('valuations (a4, a6, Delta): (3, 5, 9) at q = 0 (III*); at the zeros of d: v(a4) >= 2, v(a6) >= 3, v(Delta) = 6 (I0*)',
      v_q == (3, 5, 9) and all(v_[0] >= 2 and v_[1] >= 3 and v_[2] == 6 for v_ in v_r), '(computed %s; %s)' % (v_q, v_r))

# ------------------------------------------------------------------------------------------------------------------ 2. D4 residual cubics
print('=== 2. D4: residual cubics')
sD = symbols('s'); cub = {}
for c in DROOTS:
    tt = c + sD; qq_ = q.subs(t, tt); aa = a.subs(t, tt); bb = b.subs(t, tt)
    C = cancel(aa*qq_**3/sD**2); D = cancel(-bb*qq_**5/sD**3)
    cub[c] = sp.expand((U**3 + C*U + D).subs(sD, 0))
    Fl = Y**2 - X**3 - sD**2*C*X - sD**3*D
    check('c = %d: with X = sU, Y = sV the equation becomes s^2 (V^2 - s(U^3 + C U + D))' % c, expand(Fl.subs({X: sD*U, Y: sD*V}, simultaneous=True) - sD**2*(V**2 - sD*(U**3 + C*U + D))) == 0)
    print('     residual cubic at t = %d: %s' % (c, sp.factor(cub[c])))
for c in DROOTS:
    check('t = %d: the residual cubic is squarefree over Q and mod 5' % c, discriminant(cub[c], U) != 0 and discriminant(cub[c], U) % 5 != 0)
if PRIMARY:
    check('t = 0: z^3 + 4z (as in the note)', sp.expand(cub[0] - (U**3 + 4*U)) == 0)
    check('t = 1: the equation of section 2 gives z^3 - 512', sp.expand(cub[1] - (U**3 - 512)) == 0)
    finding('the note says to retain z^3 - 128 at t = 1 (z^3 + 2 mod 5); the equation printed in its section 2 gives z^3 - 512 (z^3 + 3 mod 5). '
            '-128 would come from q^3 in place of q^5 in the constant term (-16 t^4 q^3 = -128 at t = 1), which is a different surface. '
            'The cubics are not isomorphic over Q (512/128 = 4 is not a cube); squarefreeness, hence the argument, is unaffected.')

# ------------------------------------------------------------------------------------------------------------------ 3. strict-transform identities
print('=== 3. strict-transform equations (exact identities; a, b, q are free symbols here)')
A_, B_, Q_ = symbols('a b q')
e, Q, R, S, E, T, sig, lam, eps, kap, ell, rho, Vv, ep, Qp, Hh, uu, vv, qq, xp, yp, tau, sp_, xx = symbols('e Q R S E T sigma lambda epsilon kappa ell rho Vv ep Qp H u v qq xp yp tau sp x')
def ident(name, F, mp, h, m, Fp):
    check('%-52s' % name, expand(F.subs(mp, simultaneous=True) - h**m*Fp) == 0)
F0 = Y**2 - X**3 - A_*Q_**3*X + B_*Q_**5
ident('stage 1 q-chart (X=qu, Y=qv)', F0, {X: Q_*uu, Y: Q_*vv}, Q_, 2, vv**2 - Q_*uu**3 - A_*Q_**2*uu + B_*Q_**3)
ident('stage 1 X-chart (Y=X y, q=X qq)', F0, {Y: X*yp, Q_: X*qq}, X, 2, yp**2 - X - A_*X**2*qq**3 + B_*X**3*qq**5)
ident('stage 1 Y-chart (X=Y x, q=Y qq)', F0, {X: Y*xp, Q_: Y*qq}, Y, 2, 1 - Y*xp**3 - A_*Y**2*qq**3*xp + B_*Y**3*qq**5)
F1 = vv**2 - Q_*uu**3 - A_*Q_**2*uu + B_*Q_**3
ident('stage 2 q-chart (u=qU, v=qV)', F1, {uu: Q_*U, vv: Q_*V}, Q_, 2, V**2 - Q_**2*U**3 - A_*Q_*U + B_*Q_)
ident('stage 2 u-chart (q=eQ, u=e, v=eV)', F1, {Q_: e*Q, uu: e, vv: e*V}, e, 2, V**2 - e**2*Q - A_*e*Q**2 + B_*e*Q**3)
ident('stage 2 v-chart (q=vQ, u=vU, v=V)', F1, {Q_: Vv*Q, uu: Vv*U, vv: Vv}, Vv, 2, 1 - Vv**2*Q*U**3 - A_*Vv*Q**2*U + B_*Vv*Q**3)
G2 = V**2 - Q_**2*U**3 - Q_*Hh
ident('stage 3a (i)   (V=qS, H=qT)', G2, {V: Q_*S, Hh: Q_*T}, Q_, 2, S**2 - U**3 - T)
ident('stage 3a (ii)  (q=HQ, V=HS)', G2, {Q_: Hh*Q, V: Hh*S}, Hh, 2, S**2 - Q**2*U**3 - Q)
ident('stage 3a (iii) (q=VQ, H=VT)', G2, {Q_: V*Q, Hh: V*T}, V, 2, 1 - Q**2*U**3 - Q*T)
check('H = aU - b makes G = V^2 - q^2U^3 - aqU + bq equal V^2 - q^2 U^3 - qH', expand(V**2 - Q_**2*U**3 - A_*Q_*U + B_*Q_ - (V**2 - Q_**2*U**3 - Q_*(A_*U - B_))) == 0)
G3 = V**2 - e*Q*(e + A_*Q - B_*Q**2)
check('u-chart equation V^2 - e^2 Q - a e Q^2 + b e Q^3 = V^2 - eQ(e + aQ - bQ^2)', expand(V**2 - e**2*Q - A_*e*Q**2 + B_*e*Q**3 - G3) == 0)
ident('stage 3b e-chart (Q=eR, V=eS)', G3, {Q: e*R, V: e*S}, e, 2, S**2 - e*R*(1 + A_*R - B_*e*R**2))
ident('stage 3b Q-chart (e=QE, V=QS)', G3, {e: Q*E, V: Q*S}, Q, 2, S**2 - Q*E*(E + A_ - B_*Q))
ident('stage 3b V-chart (e=V e\', Q=V Q\')', G3, {e: V*ep, Q: V*Qp}, V, 2, 1 - V*ep*Qp*(ep + A_*Qp - B_*V*Qp**2))
Le = 1 + A_*R - B_*e*R**2; Ge = S**2 - e*R*Le
ident('stage 4 A, e-chart (S=e sigma, R=e rho)', Ge, {S: e*sig, R: e*rho}, e, 2, sig**2 - rho*(1 + A_*e*rho - B_*e**3*rho**2))
ident('stage 4 A, S-chart (e=S eps, R=S rho)', Ge, {e: S*eps, R: S*rho}, S, 2, 1 - eps*rho*(1 + A_*S*rho - B_*S**3*eps*rho**2))
ident('stage 4 A, R-chart (e=R eps, S=R sigma)', Ge, {e: R*eps, S: R*sig}, R, 2, sig**2 - eps*(1 + A_*R - B_*R**3*eps))
ident('stage 4 B, e-chart (S=e sigma, L=e lambda)', S**2 - e*R*ell, {S: e*sig, ell: e*lam}, e, 2, sig**2 - R*lam)
ident('stage 4 B, S-chart (e=S eps, L=S lambda)', S**2 - e*R*ell, {e: S*eps, ell: S*lam}, S, 2, 1 - eps*R*lam)
ident('stage 4 B, L-chart (e=L eps, S=L sigma)', S**2 - e*R*ell, {e: ell*eps, S: ell*sig}, ell, 2, sig**2 - eps*R)
Gq = S**2 - Q*E*(E + A_ - B_*Q)
ident('stage 4 C, Q-chart (S=Q sigma, E=Q eps)', Gq, {S: Q*sig, E: Q*eps}, Q, 2, sig**2 - eps*(Q*eps + A_ - B_*Q))
ident('stage 4 C, S-chart (Q=S kappa, E=S eps)', Gq, {Q: S*kap, E: S*eps}, S, 2, 1 - kap*eps*(S*eps + A_ - B_*S*kap))
ident('stage 4 C, E-chart (Q=E kappa, S=E sigma)', Gq, {Q: E*kap, S: E*sig}, E, 2, sig**2 - kap*(E + A_ - B_*E*kap))

# ------------------------------------------------------------------------------------------------------------------ 4 and 5. smoothness and saturation chart by chart
print('=== 4. fibrewise smoothness over q = 0 (s = 0 for D4), Q and F5;  5. saturation: dim V(g,h) = dim V(g) - 1')
Hs = a*U - b
CH = []     # (name, eqs, vars, centres, h, restr, redp)
def add(name, eqs, vs, centres, h, restr=None, redp='default'): CH.append((name, eqs, vs, centres, h, restr, redp))
add('E7 stage 0: original surface', [Y**2 - X**3 - a*q**3*X + b*q**5], [t, X, Y], [[X, Y]], None)
add('E7 stage 1, q-chart', [vv**2 - q*uu**3 - a*q**2*uu + b*q**3], [t, uu, vv], [[uu, vv]], q)
add('E7 stage 1, X-chart', [t**2 + 1 - X*qq, yp**2 - X - a*X**2*qq**3 + b*X**3*qq**5], [t, X, yp, qq], [], X)
add('E7 stage 1, Y-chart', [t**2 + 1 - Y*qq, 1 - Y*xp**3 - a*Y**2*qq**3*xp + b*Y**3*qq**5], [t, Y, xp, qq], [], Y)
add('E7 stage 2, q-chart', [V**2 - q**2*U**3 - a*q*U + b*q], [t, U, V], [[V, Hs]], q)
add('E7 stage 2, u-chart', [t**2 + 1 - e*Q, V**2 - e**2*Q - a*e*Q**2 + b*e*Q**3], [t, e, Q, V], [[e, Q, V], [e, V, b*Q - a]], e)
add('E7 stage 2, v-chart', [t**2 + 1 - Vv*Q, 1 - Vv**2*Q*U**3 - a*Vv*Q**2*U + b*Vv*Q**3], [t, Vv, Q, U], [], Vv)
add('E7 stage 3a (i)', [V - q*S, a*U - b - q*T, S**2 - U**3 - T], [t, U, V, S, T], [], q)
add('E7 stage 3a (ii)', [t**2 + 1 - Hs*Q, V - Hs*S, S**2 - Q**2*U**3 - Q], [t, U, V, Q, S], [], Hs)
add('E7 stage 3a (iii)', [t**2 + 1 - V*Q, a*U - b - V*T, 1 - Q**2*U**3 - Q*T], [t, U, V, Q, T], [], V)
L = 1 + a*R - b*e*R**2
add('E7 stage 3b, e-chart', [t**2 + 1 - e**2*R, S**2 - e*R*L], [t, e, R, S], [[e, S, R], [e, S, L]], e)
add('E7 stage 3b, Q-chart', [t**2 + 1 - Q**2*E, S**2 - Q*E*(E + a - b*Q)], [t, Q, E, S], [[Q, S, E], [Q, S, E + a - b*Q], [E, S, a - b*Q]], Q)
add('E7 stage 3b, V-chart', [t**2 + 1 - Vv**2*ep*Qp, 1 - Vv*ep*Qp*(ep + a*Qp - b*Vv*Qp**2)], [t, Vv, ep, Qp], [], Vv)
add('E7 stage 4, A blown up: e-chart', [t**2 + 1 - e**3*rho, sig**2 - rho*(1 + a*e*rho - b*e**3*rho**2)], [t, e, rho, sig], [], e)
add('E7 stage 4, A blown up: S-chart', [t**2 + 1 - S**3*eps**2*rho, 1 - eps*rho*(1 + a*S*rho - b*S**3*eps*rho**2)], [t, S, eps, rho], [], S)
add('E7 stage 4, A blown up: R-chart (B remains)', [t**2 + 1 - R**3*eps**2, sig**2 - eps*(1 + a*R - b*R**3*eps)], [t, R, eps, sig], [[eps, sig, 1 + a*R - b*R**3*eps]], R)
add('E7 stage 4, B blown up: e-chart', [t**2 + 1 - e**2*R, S - e*sig, L - e*lam, sig**2 - R*lam], [t, e, R, S, sig, lam], [], e)
add('E7 stage 4, B blown up: S-chart', [t**2 + 1 - e**2*R, e - S*eps, L - S*lam, 1 - eps*R*lam], [t, e, R, S, eps, lam], [], S)
add('E7 stage 4, B blown up: L-chart (A remains)', [t**2 + 1 - e**2*R, ell - L, e - ell*eps, S - ell*sig, sig**2 - eps*R], [t, e, R, S, ell, eps, sig], [[e, S, R, eps, sig, ell - 1]], ell)
add('E7 stage 4, C blown up: Q-chart (C2 remains)', [t**2 + 1 - Q**3*eps, sig**2 - eps*(Q*eps + a - b*Q)], [t, Q, eps, sig], [[eps, sig, Q*eps + a - b*Q]], Q)
add('E7 stage 4, C blown up: S-chart', [t**2 + 1 - S**3*kap**2*eps, 1 - kap*eps*(S*eps + a - b*S*kap)], [t, S, kap, eps], [], S)
add('E7 stage 4, C blown up: E-chart (B remains)', [t**2 + 1 - E**3*kap**2, sig**2 - kap*(E + a - b*E*kap)], [t, E, kap, sig], [[kap, sig, E + a - b*E*kap]], E)
for c in DROOTS:
    s = sD; tt = c + s; qq_ = q.subs(t, tt); aa = a.subs(t, tt); bb = b.subs(t, tt)
    C = cancel(aa*qq_**3/s**2); D = cancel(-bb*qq_**5/s**3); Hf = U**3 + C*U + D; H0 = sp.expand(Hf.subs(s, 0)); K = cancel((Hf - H0)/s)
    Yv = symbols('Yv')
    add('D4 t=%d stage 1, s-chart' % c, [V**2 - s*Hf], [s, U, V], [[s, V, H0]], s, [s], None)
    add('D4 t=%d stage 1, X-chart' % c, [yp**2 - X*(1 + sp_**2*C.subs(s, X*sp_) + sp_**3*D.subs(s, X*sp_))], [X, yp, sp_], [[X, yp, 1 + sp_**2*C.subs(s, 0) + sp_**3*D.subs(s, 0)]], X, [X*sp_], None)
    add('D4 t=%d stage 1, Y-chart' % c, [1 - Yv*(xx**3 + sp_**2*C.subs(s, Yv*sp_)*xx + sp_**3*D.subs(s, Yv*sp_))], [Yv, xx, sp_], [], Yv, [Yv*sp_], None)
    add('D4 t=%d stage 2, s-chart' % c, [H0 - s*tau, sig**2 - tau - K], [s, U, sig, tau], [], s, [s], None)
    add('D4 t=%d stage 2, V-chart' % c, [H0 - Vv*tau, 1 - sp_*tau - sp_**2*K.subs(s, Vv*sp_)], [Vv, sp_, U, tau], [], Vv, [Vv*sp_], None)
    add('D4 t=%d stage 2, H0-chart' % c, [s - H0*sp_, V - H0*sig, sig**2 - sp_*(1 + sp_*K)], [s, U, V, sp_, sig], [], H0, [s], None)
for name, eqs, vs, centres, h, restr, redp in CH:
    rp = 'default' if redp == 'default' else redp
    run(analyse(name, eqs, vs, centres, restr=restr, redp=rp))
for name, eqs, vs, centres, h, restr, redp in CH:
    if h is None: continue
    rp = 'default' if redp == 'default' else redp
    run(sat('saturation: ' + name, eqs, vs, h, restr=restr, redp=rp))

# ------------------------------------------------------------------------------------------------------------------ 6. Hessians and overlaps
print('=== 6. Hessians and overlap-ideal equalities')
a0 = rem(expand(a), t**2 + 1, t)                              # a modulo q (a = 16 t for d = t(t-1))
check('a is a unit modulo q and 5 (a mod (q) = %s)' % a0, sp.simplify(sp.resultant(a0, t**2 + 1, t)) % 5 != 0)
Rr, ee, SS, EE, QQ_ = symbols('R e S E Q')
def hess_det(F, vs): return Matrix([[sp.diff(F, u1, u2) for u2 in vs] for u1 in vs]).det()
HA = hess_det(SS**2 - ee*Rr, [ee, Rr, SS])                    # quadratic part at A:  S^2 - e R
r0 = -1/a0                                                    # R at B
HB2 = sp.simplify((-2*a0**2*r0**2).subs(t, sp.I))             # determinant at B:  -2 a^2 r0^2 = -2
HC = sp.simplify(hess_det(SS**2 - a0*QQ_*EE, [QQ_, EE, SS]).subs(t, sp.I))     # determinant at C: -2 a^2
vals = [HA, HB2, HC]
if PRIMARY: check('Hessian determinants at A, B, C over Q: -2, -2, 512 (as in the note)', tuple(vals) == (-2, -2, 512), '(computed %s)' % vals)
else: check('Hessian determinants at A, B, C over Q: -2, -2, nonzero (computed %s)' % vals, vals[0] == -2 and vals[1] == -2 and vals[2] != 0)
check('the three Hessian determinants are nonzero mod 5: %s' % [int(v_) % 5 for v_ in vals], all(int(v_) % 5 != 0 for v_ in vals))
check('center C2 glues: (q, V_q, aU - b) = (e, V_u, a - bQ) on the overlap of the q- and u-charts (U = 1/Q, V_q = V_u/Q, q = eQ)',
      all(sp.simplify(g1 - g2) == 0 for g1, g2 in [(Q*e, e*Q), (V/Q*Q, V), ((A_/Q - B_)*Q, A_ - B_*Q)]),
      '(generators agree up to the unit Q)')
RR = symbols('R')
check('center B glues: with Q = eR, E = 1/R, S\' = S/R one has E + a - bQ = (1 + aR - beR^2)/R and e = QE',
      sp.simplify((1/RR + A_ - B_*(e*RR)) - (1 + A_*RR - B_*e*RR**2)/RR) == 0 and sp.simplify(e*RR*(1/RR) - e) == 0)
check('D4 center glues: with U = 1/s\', V = y/s\', s = X s\' one has H0(1/s\') = s\'^-3 (1 + s\'^2 C0 + s\'^3 D0)',
      all(sp.simplify(cub[c].subs(U, 1/sp_) - sp_**-3*(1 + sp_**2*sp.expand(cub[c]).coeff(U, 1) + sp_**3*sp.expand(cub[c]).coeff(U, 0))) == 0 for c in DROOTS))
print('ALL EXPECTED CHECKS PASS' if ALLOK else 'SOME CHECK FAILED'); sys.exit(0 if ALLOK else 1)
