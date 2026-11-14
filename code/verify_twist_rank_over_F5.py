#!/usr/bin/env python3
"""Frobenius characteristic polynomial over F_5 of the three twists E^d, d in {t(t-1), t(t+1), t^2-1}.

E^d : Y^2 = X^3 + 4(1-t^2) d(t)^2 q(t)^3 X - 16 t d(t)^3 q(t)^5,   q = t^2 + 1,   an elliptic surface with chi = 3, fibres 2 I0* + 2 III* + 6 I1.
For q = 5^k, k = 1..6 the program counts N_k = sum over t in P^1(F_q) of a_t (a C program), then
  * checks N_1..N_3 against an independent pure-Python implementation of F_(5^k) and of the point count,
  * forms the power sums p_k = -N_k, the elementary symmetric functions (Newton), and fixes the sign of the functional equation with N_6,
  * checks that the degree-10 polynomial has integer coefficients and all roots of modulus exactly 5 (Weil bound),
  * tests whether any eigenvalue has the form 5*(root of unity).
If none has, Tate's inequality gives rho(S_{F_5-bar}) = 24 = rank of the trivial lattice, hence rank E^d(F_5-bar(t)) = 0; with the smooth model of
code/verify_integral_resolution_note.py (TWIST_D = d) this gives rank E^d(Q-bar(t)) = 0.
Needs: python3, sympy, mpmath, gcc.  Exit status 0 = all checks pass.  Takes under a minute."""
import sys, os, subprocess, tempfile, itertools, warnings
warnings.filterwarnings('ignore')
import sympy as sp, mpmath as mp
from sympy import symbols, Poly, expand, factor_list, cyclotomic_poly, totient
t, x, u = symbols('t x u')
OK = True
def check(name, cond, extra=''):
    global OK; OK &= bool(cond); print('%-4s %s %s' % ('OK' if cond else 'FAIL', name, extra), flush=True)

C_SOURCE = r"""// N_k = sum over t in P^1(F_q), q = 5^k, of a_t for E^d: Y^2 = X^3 + A(t) X + B(t), plus the fibre at infinity (a4,a6) = (-4, 0).
// a_t = -sum_x chi(x^3 + A x + B): valid for good, multiplicative and additive fibres of the Weierstrass model.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int k, q, qm1;
static int *EXP, *LOG, *CHI;
static unsigned char ADD3[125][125];
static int digs_add(int x,int y){ return ADD3[x%125][y%125] + 125*ADD3[x/125][y/125]; }
static inline int ADD(int x,int y){ return ADD3[x%125][y%125] + 125*ADD3[x/125][y/125]; }
static inline int MUL(int x,int y){ if(!x||!y) return 0; int s=LOG[x]+LOG[y]; if(s>=qm1) s-=qm1; return EXP[s]; }
int main(int argc,char**argv){
  k=atoi(argv[1]); int r[8]; for(int i=0;i<k;i++) r[i]=atoi(argv[2+i]);
  int nA=13,nB=18; int Ac[13],Bc[18]; int base=2+k;
  for(int i=0;i<nA;i++) Ac[i]=atoi(argv[base+i]); for(int i=0;i<nB;i++) Bc[i]=atoi(argv[base+nA+i]);
  int a4inf=atoi(argv[base+nA+nB]), a6inf=atoi(argv[base+nA+nB+1]);
  q=1; for(int i=0;i<k;i++) q*=5; qm1=q-1;
  for(int x=0;x<125;x++) for(int y=0;y<125;y++){ int s=0,m=1,xx=x,yy=y; for(int i=0;i<3;i++){ s+=((xx%5+yy%5)%5)*m; m*=5; xx/=5; yy/=5;} ADD3[x][y]=s; }
  EXP=malloc(sizeof(int)*q); LOG=malloc(sizeof(int)*q); CHI=malloc(sizeof(int)*q);
  int dg[8]; memset(dg,0,sizeof dg); dg[0]=1;
  for(int i=0;i<qm1;i++){
    int v=0,m=1; for(int j=0;j<k;j++){ v+=dg[j]*m; m*=5; }
    EXP[i]=v; LOG[v]=i;
    int top=dg[k-1]; int nd[8]; for(int j=k-1;j>=1;j--) nd[j]=dg[j-1]; nd[0]=0;
    for(int j=0;j<k;j++) nd[j]=(nd[j]+top*r[j])%5;
    memcpy(dg,nd,sizeof(int)*8);
  }
  LOG[0]=0; CHI[0]=0; for(int z=1;z<q;z++) CHI[z]=(LOG[z]%2==0)?1:-1;
  int *CUBE=malloc(sizeof(int)*q); for(int x=0;x<q;x++) CUBE[x]=MUL(x,MUL(x,x));
  long N=0;
  for(int t=0;t<q;t++){
    int A=0,B=0; for(int i=nA-1;i>=0;i--) A=ADD(MUL(A,t),Ac[i]); for(int i=nB-1;i>=0;i--) B=ADD(MUL(B,t),Bc[i]);
    long s=0; for(int x=0;x<q;x++){ int f=ADD(ADD(CUBE[x],MUL(A,x)),B); s+=CHI[f]; }
    N+= -s;
  }
  { int A=a4inf%5, B=a6inf%5; long s=0; for(int x=0;x<q;x++){ int f=ADD(ADD(CUBE[x],MUL(A,x)),B); s+=CHI[f]; } N+= -s; }
  printf("%d %ld\n",k,N); return 0; }
"""

def primitive_polys():
    def mulmod(a_, b_, mod, k):
        res = [0]*(2*k - 1)
        for i, ai in enumerate(a_):
            if ai:
                for j, bj in enumerate(b_): res[i + j] = (res[i + j] + ai*bj) % 5
        for deg in range(2*k - 2, k - 1, -1):
            c = res[deg]
            if c:
                res[deg] = 0
                for i in range(k): res[deg - k + i] = (res[deg - k + i] + c*mod[i]) % 5
        return res[:k]
    def full_order(mod, k):
        n = 5**k - 1
        def power(e):
            r = [1] + [0]*(k - 1); base = ([0, 1] + [0]*(k - 2)) if k > 1 else [mod[0] % 5]
            while e:
                if e & 1: r = mulmod(r, base, mod, k)
                base = mulmod(base, base, mod, k); e >>= 1
            return r
        one = [1] + [0]*(k - 1)
        if power(n) != one: return False
        return all(power(n//p_) != one for p_ in sp.primefactors(n))
    prim = {1: [2]}
    for k in range(2, 7):
        for mod in itertools.product(range(5), repeat=k):
            if mod[0] and full_order(list(mod), k): prim[k] = list(mod); break
    return prim

def independent_count(k, prim, Ac, Bc, a4inf):
    """pure-Python F_(5^k) as polynomials mod the primitive polynomial; direct count of y^2 = f(x)"""
    r = prim[k]
    add = lambda u_, v_: tuple((p_ + q_) % 5 for p_, q_ in zip(u_, v_))
    def mul(u_, v_):
        res = [0]*(2*k - 1)
        for i, ui in enumerate(u_):
            for j, vj in enumerate(v_): res[i + j] = (res[i + j] + ui*vj) % 5
        for deg in range(2*k - 2, k - 1, -1):
            c = res[deg]; res[deg] = 0
            if c:
                for i in range(k): res[deg - k + i] = (res[deg - k + i] + c*r[i]) % 5
        return tuple(res[:k])
    elems = list(itertools.product(range(5), repeat=k)); zero = tuple([0]*k)
    emb = lambda c: tuple([c % 5] + [0]*(k - 1))
    sq = {}
    for y in elems:
        s_ = mul(y, y); sq[s_] = sq.get(s_, 0) + 1
    def horner(coefs, tt):
        v_ = zero
        for c in reversed(coefs): v_ = add(mul(v_, tt), emb(c))
        return v_
    tot = 0
    for tt in elems:
        A = horner(Ac, tt); B = horner(Bc, tt)
        cnt = sum(sq.get(add(add(mul(xx, mul(xx, xx)), mul(A, xx)), B), 0) for xx in elems)
        tot += -(cnt - len(elems))
    A = emb(a4inf); cnt = sum(sq.get(add(mul(xx, mul(xx, xx)), mul(A, xx)), 0) for xx in elems)
    return tot - (cnt - len(elems))

def analyse(label, dpoly, prim, binary):
    q_ = t**2 + 1; a = 4*(1 - t**2)*dpoly**2; b = 16*t*dpoly**3
    A = Poly(expand(a*q_**3), t); B = Poly(expand(-b*q_**5), t)
    Ac = [int(c) % 5 for c in A.all_coeffs()[::-1]]; Bc = [int(c) % 5 for c in B.all_coeffs()[::-1]]
    Ac += [0]*(13 - len(Ac)); Bc += [0]*(18 - len(Bc))
    a4inf = int(A.all_coeffs()[0]) % 5; a6inf = int(B.all_coeffs()[0]) % 5 if B.degree() == 18 else 0
    check('%s: deg a4 = 12, deg a6 <= 18 (chi = 3), a6 at infinity = 0' % label, A.degree() == 12 and B.degree() <= 18 and a6inf == 0)
    Ns = []
    for k in range(1, 7):
        out = subprocess.run([binary, str(k)] + [str(v_) for v_ in prim[k]] + [str(v_) for v_ in Ac] + [str(v_) for v_ in Bc] + [str(a4inf), str(a6inf)], capture_output=True, text=True)
        Ns.append(int(out.stdout.split()[1]))
    print('     N_1..N_6 =', Ns)
    check('%s: independent Python count agrees with the C program for k = 1, 2, 3' % label, [independent_count(k, prim, Ac, Bc, a4inf) for k in (1, 2, 3)] == Ns[:3])
    p_ = [-v_ for v_ in Ns]; e = [sp.Integer(1)]
    for j in range(1, 7): e.append(sum((-1)**(i - 1)*e[j - i]*p_[i - 1] for i in range(1, j + 1))/j)
    check('%s: Newton identities give integers e_1..e_6 = %s' % (label, [int(v_) if v_ == int(v_) else v_ for v_ in e[1:]]), all(v_ == int(v_) for v_ in e))
    eps = [s_ for s_ in (1, -1) if 25*s_*e[4] == e[6]]
    check('%s: N_6 fixes the sign of the functional equation (e_6 = 25 eps e_4): eps = %s' % (label, eps), len(eps) == 1)
    E = [None]*11
    for j in range(7): E[j] = e[j]
    for j in range(5): E[10 - j] = eps[0]*5**(10 - 2*j)*E[j]
    chi = sum((-1)**j*E[j]*x**(10 - j) for j in range(11))
    mp.mp.dps = 40
    roots = mp.polyroots([int(c) for c in Poly(chi, x).all_coeffs()], maxsteps=500, extraprec=500)
    check('%s: all ten roots have modulus exactly 5 (Weil bound)' % label, all(abs(abs(r_) - 5) < mp.mpf(10)**-25 for r_ in roots))
    c, fl = factor_list(chi); k5 = 0
    for f_, m in fl:
        deg = sp.degree(f_, x); g = sp.expand(f_.subs(x, 5*u)/5**deg)
        if all(sp.Rational(cf).q == 1 for cf in Poly(g, u).all_coeffs()):
            for n in range(1, 400):
                if totient(n) == sp.degree(g, u) and sp.expand(cyclotomic_poly(n, u) - g) == 0: k5 += deg*m; break
    check('%s: no eigenvalue of the form 5*(root of unity); factors over Q have degrees %s; chi(5) = %s != 0' % (label, [sp.degree(f_, x) for f_, m in fl], chi.subs(x, 5)), k5 == 0 and chi.subs(x, 5) != 0)
    print('     chi(x) =', chi)

def main():
    prim = primitive_polys(); tmp = tempfile.mkdtemp(prefix='twist_'); src = os.path.join(tmp, 'twistcount.c'); binary = os.path.join(tmp, 'twistcount')
    open(src, 'w').write(C_SOURCE); subprocess.run(['gcc', '-O2', '-o', binary, src], check=True)
    for label, dp in (('d = t(t-1)', t*(t - 1)), ('d = t(t+1)', t*(t + 1)), ('d = t^2-1', t**2 - 1)): analyse(label, dp, prim, binary)
    print('     remark: d = t(t+1) is the image of d = t(t-1) under t -> -t followed by a twist by -1, trivial over Q-bar and over F_5; the identical counts above reflect this.')
    print('ALL CHECKS PASS' if OK else 'SOME CHECK FAILED'); sys.exit(0 if OK else 1)
if __name__ == '__main__': main()
