# lfunc.py : from the counts N_1..N_4 to the Picard number rho(S_{F_p-bar}) of the twist surface
#            and the square class of |disc NS| (Artin-Tate), for the cover with x = c.
# Needs: python3, sympy, numpy.  Usage: see the table at the end of the file.
import math, cmath
import numpy as np
from fractions import Fraction as Fr
from sympy import symbols, Poly, Integer, factor_list, resultant, factorint

x, y, t = symbols('x y t')
f6 = t**6 - 30*t**4 - 24*t**2 - 1

def chi(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p-1)//2, p) == 1 else -1)

def sign_of_functional_equation(c, p):
    """epsilon = product of local root numbers: only the places over the roots of f contribute
       (-1 if the node is split, i.e. if 3 x0 = 18 t (1+t^2) N(t) / (1-t^2) is a square there)."""
    cc = (c.numerator * pow(c.denominator, -1, p)) % p
    N = ((cc**3 - 4*cc) % p) * t**2 + ((-16) % p) * t + ((cc**3 + 4*cc) % p)
    r = len(factor_list(f6, modulus=p)[1])
    fp = Poly(f6, t, modulus=p)
    num = Poly(18*t*(1 + t**2)*N, t, modulus=p)
    den = Poly(1 - t**2, t, modulus=p)
    pi = int(resultant(fp, num, t)) * pow(int(resultant(fp, den, t)), -1, p) % p
    return (-1)**r * chi(pi, p)

def elementary(Ns):
    """e_1..e_4 of the eigenvalues from the power sums p_k = -N_k (Newton's identities)."""
    P = [None] + [-n for n in Ns]
    e = [Fr(1)]
    for k in range(1, len(Ns) + 1):
        e.append(sum((-1)**(i-1) * e[k-i] * P[i] for i in range(1, k+1)) / k)
    return e

def char_poly(e, p, eps, e5):
    """R(x) = prod (x - alpha_i): functional equation e_j = eps p^(2(j-5)) e_(10-j) for j > 5."""
    ee = [Fr(v) for v in e[:5]] + [Fr(e5)]
    for j in range(6, 11):
        ee.append(eps * Fr(p)**(2*(j-5)) * ee[10-j])
    return ee, Poly(sum((-1)**k * Integer(int(ee[k])) * x**(10-k) for k in range(11)), x)

def on_circle(R, p):
    r = np.roots([float(c) for c in R.all_coeffs()])
    return bool(np.allclose(np.abs(r), p, atol=3e-4*p))

def eigenvalues_p_times_root_of_unity(R, p):
    """number of eigenvalues of the form p*zeta (zeta a root of unity); rho(F_p-bar) = 12 + this number."""
    total = 0
    for g, mult in factor_list(R.as_expr())[1]:
        gp = Poly(g, x); k = gp.degree()
        gy = Poly(sum(Integer(int(c)) * (p*y)**(k-j) for j, c in enumerate(gp.all_coeffs())), y)
        if all(int(c) % p**k == 0 for c in gy.all_coeffs()):
            cy = Poly(gy.as_expr() / p**k, y)
            if any(Poly(y**m - 1, y).rem(cy).is_zero for m in range(1, 61)):
                total += k * mult
    return total

def squarefree_class(fr):
    v = fr.numerator * fr.denominator
    s = -1 if v < 0 else 1
    for pr, e in factorint(abs(v)).items():
        if e % 2: s *= pr
    return s

def discriminant_class(R, p):
    """Lambda_p = prod over the 8 eigenvalues that are not p*zeta of (1 - alpha^2/p^2); returns its squarefree class."""
    rest = 1
    for g, mult in factor_list(R.as_expr())[1]:
        gp = Poly(g, x); k = gp.degree()
        gy = Poly(sum(Integer(int(c)) * (p*y)**(k-j) for j, c in enumerate(gp.all_coeffs())), y)
        if not all(int(c) % p**k == 0 for c in gy.all_coeffs()):
            rest *= gp.as_expr()**mult
    rest = Poly(rest, x)
    return squarefree_class(Fr(int(resultant(rest.as_expr(), x**2 - p*p, x))) / Fr(p)**16) if rest.degree() == 8 else None

def analyse(c, p, Ns):
    """list of (e5, rho, class) for the L-functions that are Weil-valid, have the predicted sign,
       and have an even number >= 2 of eigenvalues p*zeta."""
    eps = sign_of_functional_equation(c, p)
    e = elementary(Ns[:4]); out = []
    if eps == -1: trial = [0]
    else:
        trial = set()
        for m in (1, 2, 3, 4, 5, 6, 8, 10, 12):
            for j in range(m):
                if math.gcd(j, m) != 1: continue
                z = cmath.exp(2j*math.pi*j/m)
                A = sum((-1)**k * complex(char_poly(e, p, 1, 0)[0][k]) * (p*z)**(10-k) for k in range(11))
                v = A / (p*z)**5
                if abs(v.imag) < 1e-6*(abs(v.real) + 1) and abs(v.real - round(v.real)) < 1e-3: trial.add(int(round(v.real)))
    for e5 in sorted(trial):
        ee, R = char_poly(e, p, eps, e5)
        if not on_circle(R, p): continue
        n = eigenvalues_p_times_root_of_unity(R, p)
        if n >= 2 and n % 2 == 0:
            out.append((e5, 12 + n, discriminant_class(R, p) if n == 2 else None))
    return eps, out

if __name__ == '__main__':
    tests = [(Fr(2), 7, [-2, -74, -218, 2462]), (Fr(2), 17, [-12, -382, -810, -270194]), (Fr(2), 19, [-36, -574, 5328, -268106]),
             (Fr(13, 9), 19, [-26, -714, 2602, -32554]), (Fr(13, 9), 41, [-40, -3896, 10046, -3727844]),
             (Fr(1), 13, [-10, -256, -1312, -17540])]
    for c, p, Ns in tests: print('c =', c, ' p =', p, ' (sign, [(e5, rho, class)]) =', analyse(c, p, Ns))
