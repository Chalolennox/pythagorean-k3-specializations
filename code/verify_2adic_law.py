#!/usr/bin/env python3
"""Exact checks for F.55 (the 2-adic law v2(F_n - F_m) = 1 + v2(n^2 - m^2) and the injectivity of n -> F(t_n)).

C: y^2 = x^3 - 2x^2 + 2x, P = (1,1); psi_n = psi_n(P), U_n = psi_{n-1} psi_{n+1}, V_n = psi_n^2, F_n = Phi(U_n, V_n).
Checks (one line each; exit status 0 if all pass, 1 otherwise).  They test the stated inequalities of the proof on a finite
range; they are not part of the proof.
 1. psi_n from the recurrences; t_n = U_n/V_n = 1 - x(nP) and psi_{2n} = 2 y(nP) psi_n^4 against explicit point addition
 2. 2P = (1/4, -5/8) (infinite order by Lutz-Nagell) and the duplication identity (1) V_2n = 4 V_n (V_n-U_n)(U_n^2+V_n^2)
 3. parity psi_n = n mod 2, v2(psi_n) = v2(n), gcd(psi_n, psi_{n+1}) = 1
 4. f1(s) = (1-s)(1+s^2) and g1(s) = 2s^3 - s^2 + 1 have no common root mod an odd prime p < 300; Res = +-16
 5. the intermediate congruences of the coprimality argument: p | psi_{2m+1}, p not| psi_m psi_{m+1} => t_m = t_{m+1} mod p and p not| psi_{2m} psi_{2m+2}
 6. Ward's identity, and U_{n+h} U_{n-h} = (U_n V_{h-1} - U_{h-1} V_n)(U_n V_{h+1} - U_{h+1} V_n) for all h <= 40, |n| <= 60
 7. the Theorem: v2(F_n - F_m) = 1 + v2(n^2-m^2) for all 1 <= m < n <= NT
 8. section (e): every inequality used in the reduction (both odd, both even, mixed parity)
 9. section (c): Lambda_k exact symmetry, D_j valuation >= 6, v(Lambda_k - Lambda_j) >= 4 + v(k-j) for all integer pairs
10. section (d): the lattice recurrence (2) exactly for h = 2, 4, 8, 16; Step 1 v(Gamma_{2^s}) >= 2s+2; v(Gamma_n - Gamma_m) >= nu+2 for all even pairs;
    Step 4 (r = 2, 3, 4): v >= nu + r for the quadratic-corrected sequence; Step 5: v >= 5 + max(v(k-l), v(k+l)) for n, m = 2 mod 4
11. Lemma L on random integer polynomials
Usage: python3 code/verify_2adic_law.py [--quick]   (full run about 40 s; --quick about 8 s).  Standard library only.
"""
import sys, random
from fractions import Fraction as Fr
from math import gcd
QUICK = "--quick" in sys.argv
NPSI = 200 if QUICK else 400        # range for psi checks
NT   = 70 if QUICK else 160         # pairs of the Theorem
MR   = 60 if QUICK else 90          # pairs of section (e)
KO   = 22 if QUICK else 36          # Lambda_k, |k| <= KO
NE   = 44 if QUICK else 88          # even n <= NE
P    = 160 if QUICK else 200; Q = P + 30; MOD = 1 << Q; MP = 1 << P
results = []
def check(name, ok, extra=""):
    results.append(bool(ok)); print(("PASS " if ok else "FAIL ") + name + (("  " + extra) if extra else ""))
def v2(x):
    x = Fr(x)
    if x == 0: return 10**9
    n, d = x.numerator, x.denominator
    return ((n & -n).bit_length() - 1) - ((d & -d).bit_length() - 1)
LIM = max(NPSI, 2*NT, 2*MR, 2*NE) + 60
W = {0: 0, 1: 1, 2: 2, 3: 3, 4: -20}
for n in range(5, 2*LIM + 8):
    m = n // 2
    W[n] = W[m+2]*W[m]**3 - W[m-1]*W[m+1]**3 if n % 2 else W[m]*(W[m+2]*W[m-1]**2 - W[m-2]*W[m+1]**2)//2
for n in range(1, 2*LIM + 8): W[-n] = -W[n]
U = lambda n: W[n-1]*W[n+1]; V = lambda n: W[n]**2
Phi = lambda a, b: a**6 - 30*a**4*b**2 - 24*a**2*b**4 - b**6
Fn = lambda n: Phi(U(n), V(n))
nu = lambda n, m: v2(n*n - m*m)
# 1
def add(Pt, Qt):
    x1, y1 = Pt; x2, y2 = Qt
    l = (3*x1*x1 - 4*x1 + 2)/(2*y1) if x1 == x2 else (y2 - y1)/(x2 - x1)
    x3 = l*l + 2 - x1 - x2; return (x3, l*(x1 - x3) - y1)
R = (Fr(1), Fr(1)); bad = 0; pts = {1: R}
for n in range(2, 121):
    R = add(R, (Fr(1), Fr(1))); pts[n] = R
    if 1 - R[0] != Fr(U(n), V(n)) or R[1] != Fr(W[2*n], 2*V(n)**2): bad += 1
check("1 t_n = 1 - x(nP) and psi_2n = 2 y(nP) psi_n^4 for 2 <= n <= 120", bad == 0, "failures %d" % bad)
# 2
bad = sum(1 for n in range(1, NPSI+1) if V(2*n) != 4*V(n)*(V(n) - U(n))*(U(n)**2 + V(n)**2))
check("2 2P = (1/4,-5/8) on C; duplication (1) for n <= %d" % NPSI,
      pts[2] == (Fr(1, 4), Fr(-5, 8)) and Fr(-5, 8)**2 == Fr(1, 4)**3 - 2*Fr(1, 4)**2 + 2*Fr(1, 4) and bad == 0, "failures %d" % bad)
# 3
bp = sum(1 for n in range(1, NPSI+1) if W[n] % 2 != n % 2 or v2(W[n]) != v2(n) or gcd(W[n], W[n+1]) != 1)
check("3 parity, v2(psi_n) = v2(n), gcd(psi_n,psi_{n+1}) = 1 for n <= %d" % NPSI, bp == 0, "failures %d" % bp)
# 4
primes = [q for q in range(3, 300) if all(q % r for r in range(2, int(q**.5) + 1))]
common = [(p, s) for p in primes for s in range(p) if (1 - s)*(1 + s*s) % p == 0 and (2*s**3 - s*s + 1) % p == 0]
res = (2*(2 - 2j)*(2 + 2j))
check("4 f1, g1 have no common root mod odd p < 300; g1(1) g1(i) g1(-i) = 16", not common and abs(res - 16) < 1e-9, "common roots %s" % common)
# 5
cnt = viol = badpair = 0
for p in [q for q in primes if q < 400] if False else [q for q in range(3, 400) if all(q % r for r in range(2, int(q**.5) + 1))]:
    for m in range(2, NPSI//2 - 1):
        if W[2*m+1] % p or W[m] % p == 0 or W[m+1] % p == 0: continue
        cnt += 1
        if (U(m)*pow(V(m), -1, p) - U(m+1)*pow(V(m+1), -1, p)) % p: viol += 1
        if W[2*m] % p == 0 or W[2*m+2] % p == 0: badpair += 1
check("5 coprimality chain: t_m = t_{m+1} (mod p) and p not| psi_2m psi_2m+2, %d cases with p | psi_{2m+1}" % cnt, viol == 0 and badpair == 0 and cnt > 0,
      "violations %d, %d" % (viol, badpair))
# 6
bw = sum(1 for n in range(-60, 61) for m in range(-60, 61) if U(n)*V(m) - U(m)*V(n) != W[n+m]*W[n-m])
bl = sum(1 for h in range(1, 41) for n in range(-60, 61)
         if U(n+h)*U(n-h) != (U(n)*V(h-1) - U(h-1)*V(n))*(U(n)*V(h+1) - U(h+1)*V(n)))
check("6 Ward's identity (|n|,|m| <= 60) and the product identity of (d) (h <= 40, |n| <= 60)", bw == 0 and bl == 0, "failures %d, %d" % (bw, bl))
# 7
bad = [(n, m) for n in range(2, NT+1) for m in range(1, n) if v2(Fn(n) - Fn(m)) != 1 + nu(n, m)]
check("7 Theorem: v2(F_n - F_m) = 1 + v2(n^2 - m^2) for all 1 <= m < n <= %d" % NT, not bad, "violations %d" % len(bad))
# 8
X = lambda n: U(n)**2; Y = lambda n: V(n)**2
b8 = 0; c8 = 0
for n in range(2, MR+1):
    for m in range(1, n):
        d = nu(n, m); c8 += 1
        if n % 2 and m % 2:
            ok = (v2(U(n) - U(m)) >= d and v2(X(n) - X(m)) >= d + 3 and v2(Y(n) - Y(m)) == d + 1
                  and v2(24*(X(n)*Y(n)**2 - X(m)*Y(m)**2)) >= d + 4 and v2(30*(X(n)**2*Y(n) - X(m)**2*Y(m))) >= d + 4
                  and v2(X(n)**3 - X(m)**3) >= d + 4 and v2(Y(n)**3 - Y(m)**3) == d + 1)
        elif n % 2 == 0 and m % 2 == 0:
            sg = [s for s in (1, -1) if v2(U(n) - s*U(m)) == d]
            ok = (v2(X(n) - X(m)) == d + 1 and len(sg) == 1 and v2(V(n) - sg[0]*V(m)) >= d and v2(Y(n) - Y(m)) >= d + 1
                  and v2(30*(X(n)**2*Y(n) - X(m)**2*Y(m))) >= d + 2 and v2(24*(X(n)*Y(n)**2 - X(m)*Y(m)**2)) >= d + 4
                  and v2(Y(n)**3 - Y(m)**3) >= d + 4 and v2(X(n)**3 - X(m)**3) == d + 1)
        else:
            ok = (Fn(n) - Fn(m)) % 8 in (2, 6) and (Fn(n) % 8, Fn(m) % 8) in ((7, 1), (1, 7))
        if not ok: b8 += 1
check("8 section (e): all inequalities, %d pairs, three parity cases" % c8, b8 == 0, "failures %d" % b8)
# 2-adic log
def padlog(x):
    y = (x - 1) % MOD; tot = 0; yj = 1
    for j in range(1, Q):
        yj = yj*y % MOD
        if yj == 0: break
        vj = (j & -j).bit_length() - 1; o = j >> vj
        term = (yj >> vj)*pow(o, -1, MOD) % MOD
        tot = (tot + (term if j % 2 else -term)) % MOD
    return tot % MP
L9 = padlog(9); T = lambda k: k*(k + 1)//2
Lam = {k: (padlog(V(2*k+1) % MOD) - T(k)*L9) % MP for k in range(-KO, KO+1)}
sym = all(Lam[-1-k] == Lam[k] for k in range(0, KO)) and Lam[0] == 0
Dj = {j: (Lam[j] - Lam[j-1]) % MP for j in range(-KO+1, KO+1)}
dv = min(v2(x) for x in Dj.values() if x)
lip = min(v2(Lam[k] - Lam[j]) - (4 + v2(k - j)) for k in Lam for j in Lam if k > j)
check("9 section (c): Lambda symmetric, Lambda_0 = 0, min v(D_j) = %d >= 6, min slack of Lipschitz-4 over all integer pairs = %d >= 0" % (dv, lip),
      sym and dv >= 6 and lip >= 0)
# 10
inv = lambda a: pow(a % MP, -1, MP)
Gam = {0: 0}
for n in range(2, 2*KO + 1, 2): Gam[n] = (Lam[n//2] + Lam[n//2 - 1]) % MP
Gf = lambda n: Gam[abs(n)]
tj = lambda j: U(j)*inv(V(j)) % MP
qn = lambda n: V(n)*inv(U(n)) % MP
xi = lambda h, n: (padlog((1 - tj(h+1)*qn(n)) % MOD) + padlog((1 - tj(h-1)*qn(n)) % MOD)) % MP
bad = 0
for h in (2, 4, 8, 16):
    for n in range(0, 2*KO - h, 2):
        if (Gf(n+h) - 2*Gf(n) + Gf(n-h) - 2*Gf(h) - 2*xi(h, n)) % MP: bad += 1
check("10a lattice recurrence (2) exact for h = 2, 4, 8, 16", bad == 0, "failures %d" % bad)
steps = [(s, v2(Gf(2**s))) for s in range(2, 6) if 2**s <= 2*KO]
check("10b Step 1: v(Gamma_{2^s}) >= 2s+2 %s" % steps, all(v >= 2*s + 2 for s, v in steps) and len(steps) >= 2)
ev = list(range(0, 2*KO + 1, 2))
full = sum(1 for n in ev for m in ev if n > m and v2(Gf(n) - Gf(m)) < nu(n, m) + 2)
check("10c all even pairs: v(Gamma_n - Gamma_m) >= nu + 2 (d1)", full == 0, "violations %d" % full)
worst = 10**9
for r in (2, 3, 4):
    h = 2**(r+1); ns = [2**r*(2*j + 1) for j in range(1, 40) if 2**r*(2*j + 1) <= 2*KO]
    for n in ns:
        for m in ns:
            if n > m:
                diff = (Gf(n) - Gf(m)) - Fr(Gf(h), h*h)*(n*n - m*m)
                worst = min(worst, v2(diff) - (nu(n, m) + r))
check("10d Step 4: min slack of v(Gamma~_n - Gamma~_m) over nu + r (r = 2,3,4) = %d" % worst, worst >= 0)
w5 = min(v2(Gf(n) - Gf(m)) - (5 + max(v2(n//2 - m//2), v2(n//2 + m//2))) for n in ev for m in ev if n > m and n % 4 == 2 and m % 4 == 2)
check("10e Step 5: min slack of v(H_k - H_l) over 5 + max(v(k-l), v(k+l)) = %d" % w5, w5 >= 0)
# 11
random.seed(7); worst = 10**9
for _ in range(300):
    N = random.randint(1, 200); cs = [random.getrandbits(30) for _ in range(5)]
    S = sum((N - a)*sum(c*a**i for i, c in enumerate(cs)) for a in range(N)); worst = min(worst, v2(S) - v2(N) + 1)
check("11 Lemma L on 300 random integer polynomials: min of v(sum) - (v(N) - 1) = %d" % worst, worst >= 0)
sys.exit(0 if all(results) else 1)
