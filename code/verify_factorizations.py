#!/usr/bin/env python3
"""Check data/factorizations.json.

For every entry the number N (the part of |F(U_n, V_n)| prime to 6) is recomputed from the group law on
J : y^2 = x^3 - 2x^2 + 2x, P = (1, 1); then the script checks that the listed primes multiply to N, that each
passes the strong probable-prime test of sympy (BPSW; no known counterexample, but not a proof of primality),
and that every listed composite cofactor is composite.  Needs: python3, sympy.   Exit status 0 = all checks pass.
"""
import json, os, sys
from fractions import Fraction as Fr
from sympy import isprime
sys.set_int_max_str_digits(0)

def F(U, V):
    return U**6 - 30*U**4*V**2 - 24*U**2*V**4 - V**6

def add(P, Q):
    x1, y1 = P; x2, y2 = Q
    lam = (3*x1*x1 - 4*x1 + 2) / (2*y1) if x1 == x2 else (y2 - y1) / (x2 - x1)
    x3 = lam*lam + 2 - x1 - x2
    return (x3, lam*(x1 - x3) - y1)

def prime_to_6_part(m):
    m = abs(m)
    while m % 2 == 0: m //= 2
    while m % 3 == 0: m //= 3
    return m

def N_value(orbit, n):
    P = (Fr(1), Fr(1)); Q = P
    for _ in range(n - 1): Q = add(Q, P)
    t = 1 - Q[0]
    if orbit == 'nP+T': t = (t + 1) / (t - 1)
    return prime_to_6_part(F(t.numerator, t.denominator))

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, '..', 'data', 'factorizations.json')))
    ok = True
    for e in data['entries']:
        N = N_value(e['orbit'], e['n'])
        good = (str(N) == e['N'])
        if e['status'] == 'complete':
            primes = [int(p) for p in e['primes']]
            prod = 1
            for p in primes: prod *= p
            good &= (prod == N) and all(isprime(p) for p in primes) and len(set(primes)) == len(primes)
            note = '%d primes, squarefree' % len(primes)
        else:
            known = [int(p) for p in e.get('known_primes', [])]
            comp = int(e['composite_cofactor']); prod = comp
            for p in known: prod *= p
            good &= (prod == N) and not isprime(comp)
            note = 'cofactor of %d digits is composite and unfactored' % len(str(comp))
        ok &= good
        print('%-5s n=%-2d %3d digits  %s  %s' % (e['orbit'], e['n'], e['digits'], 'OK  ' if good else 'FAIL', note))
    print('ALL CHECKS PASS' if ok else 'SOME CHECK FAILED')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
