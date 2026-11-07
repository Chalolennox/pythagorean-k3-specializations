#!/usr/bin/env python3
"""Independent symbolic check of the identities in notes/2026-11-07_local_i0star_geometry.md, and of the
'next step' proposed there (substitute X = X_P + lambda N^2).  Needs: python3, sympy.  Exit status 0 = all checks pass.
Takes a few minutes at most (the Groebner bases dominate)."""
import sys
from math import gcd, isqrt
from sympy import symbols, Poly, expand, factor, simplify, cancel, resultant, discriminant, groebner, real_roots
import sympy
t, c, z, a, lam, p0, p1, p2, s, x = symbols('t c z alpha lambda p0 p1 p2 s x')
ok = True
def check(name, cond):
    global ok
    ok &= bool(cond); print('%-4s %s' % ('OK' if cond else 'FAIL', name))

N = c*(c**2-4)*t**2 - 16*t + c*(c**2+4)
A = 4*(1-t**4); B = -16*t*(1+t**2)**2
check('(2) P_c = (c(1+t^2)N, (1+t^2)N^2) lies on Y^2 = X^3 + A N^2 X + B N^3',
      expand(((1+t**2)*N**2)**2 - ((c*(1+t**2)*N)**3 + A*N**2*(c*(1+t**2)*N) + B*N**3)) == 0)
fz = z**3 + 4*(1-a**4)*z - 16*a*(1+a**2)**2; r = c*(1+a**2); Na = N.subs(t, a)
Qz = z**2 + r*z + r**2 + 4*(1-a**4)
check('(6)-(7) f(z) - (z - r)Q(z) = (1+alpha^2)^2 N(alpha), which is 0 in L = k[alpha]/N', expand(fz - (z-r)*Qz - (1+a**2)**2*Na) == 0)
delta = -3*c**2*(1+a**2)**2 - 16*(1-a**4)
check('(8) discriminant of Q equals -3c^2(1+alpha^2)^2 - 16(1-alpha^4)', expand(r**2 - 4*(r**2 + 4*(1-a**4)) - delta) == 0)
norm = cancel(resultant(N, delta.subs(a, t), t)/(c*(c**2-4))**4)
check('(9) Norm_{L/k}(delta) = 4096(c^2+4)(c^6+36c^4-1024)/(c^4(c^2-4)^4)', simplify(norm - 4096*(c**2+4)*(c**6+36*c**4-1024)/(c**4*(c**2-4)**4)) == 0)
H = expand((c**2+4)*(c**6+36*c**4-1024))
check('(10) H squarefree of degree 8 (genus 3)', sympy.gcd(H, H.diff(c)) == 1 and Poly(H, c).degree() == 8)
check('(12) disc_t N_c = 4(-c^6+16c^2+64)', expand(discriminant(N, t) - 4*(-c**6+16*c**2+64)) == 0)
S6 = -c**6 + 16*c**2 + 64
check('(13) -c^6+16c^2+64 squarefree of degree 6 (genus 2)', sympy.gcd(S6, S6.diff(c)) == 1)
q11 = expand((x+4)*(x**3+36*x**2-1024))
check('(11) quartic squarefree (genus one)', sympy.gcd(q11, q11.diff(x)) == 1 and Poly(q11, x).degree() == 4)
# next step of the note: X = X_P + lambda N^2
X = c*(1+t**2)*N + lam*N**2
RHS = expand(X**3 + A*N**2*X + B*N**3)
V2 = expand((1+t**2)**2 + lam*(3*c**2*(1+t**2)**2 + 4*(1-t**4)) + 3*c*(1+t**2)*lam**2*N + lam**3*N**2)
check('X = X_P + lambda N^2 gives RHS = N^4 V2 with V2 = (1+t^2)^2 + lam f\'(r) + 3c(1+t^2)lam^2 N + lam^3 N^2', expand(V2*N**4 - RHS) == 0)
sq = Poly(expand((p2*t**2 + p1*t + p0)**2), t)
eqs = [expand(u - v) for u, v in zip(Poly(V2, t).all_coeffs(), sq.all_coeffs())] + [s*lam*c*(c**2-4) - 1]
G = groebner(eqs, s, p2, p1, p0, lam, c, order='lex')
elim = factor(G.exprs[-1])
check('V2 is a square only if c^6 + 16c^4 + 432c^2 + 1472 = 0 (with lambda != 0, c(c^2-4) != 0)', expand(elim - (c**6 + 16*c**4 + 432*c**2 + 1472)) == 0)
rr = [float(v) for v in real_roots(Poly(x**3 + 16*x**2 + 432*x + 1472, x))]
check('x^3+16x^2+432x+1472 has no positive real root (so no real c, in particular no rational c)', all(v < 0 for v in rr))

# --- the full statement of F.47: only lambda != 0 is saturated, then the specialised cases c = 0 and c = +-2 ---
eqsG = [expand(u - v) for u, v in zip(Poly(V2, t).all_coeffs(), sq.all_coeffs())] + [s*lam - 1]
GG = groebner(eqsG, s, p2, p1, p0, lam, c, order='lex')
G_c = c*(c**6 + 16*c**4 + 432*c**2 + 1472)
check('F.47: the elimination polynomial (only lambda != 0 saturated) is G(c) = c(c^6+16c^4+432c^2+1472)', expand(factor(GG.exprs[-1]) - G_c) == 0)
def system_at(cv):
    Nc = cv*(cv**2-4)*t**2 - 16*t + cv*(cv**2+4)
    R = expand((cv*(1+t**2)*Nc + lam*Nc**2)**3 + A*Nc**2*(cv*(1+t**2)*Nc + lam*Nc**2) + B*Nc**3)
    rhs = Poly(expand(Nc**4*(p2*t**2 + p1*t + p0)**2), t); lhs = Poly(R, t)
    d = max(lhs.degree(), rhs.degree()); a_ = lhs.all_coeffs(); b_ = rhs.all_coeffs()
    a_ = [0]*(d+1-len(a_)) + a_; b_ = [0]*(d+1-len(b_)) + b_
    return [expand(u - v) for u, v in zip(a_, b_)] + [s*lam - 1]
for cv in (2, -2):
    check('c = %d: no solution with lambda != 0 even over C (the ideal is the unit ideal)' % cv,
          groebner(system_at(cv), s, p2, p1, p0, lam, order='lex').exprs == [1])
G0 = groebner(system_at(0), s, p2, p1, p0, lam, order='lex')
hpoly = Poly(1024*lam**4 + 16*lam + 1, lam)
check('c = 0: the system reduces to 1024 lambda^4 + 16 lambda + 1 = 0, that is h^4 + 16h^3 + 1024 = 0 for h = 1/lambda',
      any(expand(g - hpoly.as_expr()) == 0 for g in G0.exprs))
hh = symbols('h')
from sympy import divisors
Ph = Poly(hh**4 + 16*hh**3 + 1024, hh)
check('c = 0: h^4+16h^3+1024 has no integer root (monic, so no rational root)', all(Ph.eval(d*sg) != 0 for d in divisors(1024) for sg in (1, -1)))

# bounded search for rational points on the curves (10) and (13)
def issq(n): return n >= 0 and isqrt(n)**2 == n
B_ = 600
h10 = [(m, n) for n in range(1, B_+1) for m in range(-3*B_, 3*B_+1) if gcd(abs(m), n) == 1 and issq((m*m+4*n*n)*(m**6+36*m**4*n*n-1024*n**6))]
h13 = [(m, n) for n in range(1, B_+1) for m in range(-3*B_, 3*B_+1) if gcd(abs(m), n) == 1 and issq(-m**6+16*m*m*n**4+64*n**6)]
print('     rational points of (10), c = m/n with |m| <= %d, n <= %d: %s' % (3*B_, B_, h10))
print('     rational points of (13) in the same range: %s (only the degenerate c = 0, +-2)' % h13)
check('no nondegenerate rational point of (10) or (13) in the searched range', h10 == [] and set(h13) <= {(0, 1), (2, 1), (-2, 1)})
print('ALL CHECKS PASS' if ok else 'SOME CHECK FAILED'); sys.exit(0 if ok else 1)
