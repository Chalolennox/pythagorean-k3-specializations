# Local geometry at the two \(I_0^*\) fibers of the constant-\(x\) K3 family

**Research note — 7 November 2026**  
**Status:** algebraic identities and conditional local consequences established; no new global section or rank-jump theorem established.

## 1. Setup and motivation

The original family is

\[
E_t:\quad y^2=x^3+4\frac{1-t^2}{1+t^2}x-16\frac{t}{1+t^2},\qquad t\in\mathbb Q.
\]

Its central arithmetic question is whether infinitely many rational \(t\) have \(\operatorname{rank}E_t(\mathbb Q)\ge2\).

Fixing a rational \(x\)-coordinate \(c\) produces the auxiliary double cover

\[
C_c:\quad w^2=(1+t^2)N_c(t),\qquad
N_c(t)=c(c^2-4)t^2-16t+c(c^2+4).
\]

The associated quadratic-twist elliptic K3 surface (in the polynomial model used in the calculations) is

\[
S_c:\quad Y^2=X^3+4(1-t^4)N_c(t)^2X-16t(1+t^2)^2N_c(t)^3.
\tag{1}
\]

It has the known section

\[
P_c:\quad X_P=c(1+t^2)N_c(t),\qquad Y_P=(1+t^2)N_c(t)^2.
\tag{2}
\]

For generic \(c\), the two roots of \(N_c\) support fibers of type \(I_0^*\). We investigate polynomial sections locally at these fibers, especially those satisfying \(N_c\mid X\).

Throughout the generic analysis, let \(k=\mathbb Q(c)\), \(D=c(c^2-4)\), and \(L=k(\alpha)\), where \(N_c(\alpha)=0\). The polynomial \(N_c\) is irreducible over \(k\), as verified in Magma.

## 2. Valuation and divisibility conditions

Equation (1) has the form

\[
Y^2=X^3+A(t)N_c^2X+B(t)N_c^3,
\quad A(t)=4(1-t^4),\quad B(t)=-16t(1+t^2)^2.
\tag{3}
\]

Reduction modulo \(N_c\) yields

\[
Y^2\equiv X^3\pmod{N_c}.
\tag{4}
\]

If \(N_c\mid X\) for a polynomial section, the right side of (3) is divisible by \(N_c^3\), hence \(N_c^3\mid Y^2\). Since \(N_c\) is irreducible over \(k\), this implies \(N_c^2\mid Y\). Write

\[
X=N_cU,\qquad Y=N_c^2V.
\]

After cancellation,

\[
N_cV^2=U^3+4(1-t^4)U-16t(1+t^2)^2.
\tag{5}
\]

Thus the residue \(u=U(\alpha)\in L\) satisfies

\[
f_\alpha(u)=0,\qquad
f_\alpha(z)=z^3+4(1-\alpha^4)z-16\alpha(1+\alpha^2)^2.
\tag{6}
\]

This argument applies to the stated divisibility pattern; it is **not** a classification of all sections, particularly those with \(N_c\nmid X\) or poles in \(t\).

## 3. The residue cubic and its known root

The known section (2) supplies

\[
r=c(1+\alpha^2),\qquad f_\alpha(r)=0.
\]

Consequently

\[
f_\alpha(z)=(z-r)\,Q_\alpha(z),\qquad
Q_\alpha(z)=z^2+rz+r^2+4(1-\alpha^4).
\tag{7}
\]

The Magma factorization over \(L=\mathbb Q(c,\alpha)\) returned one linear factor and an irreducible quadratic factor. In particular, **generically** the only root of the residue cubic in \(L\) is \(r\).

The discriminant of the quadratic factor is

\[
\delta=r^2-4\bigl(r^2+4(1-\alpha^4)\bigr)
=-3c^2(1+\alpha^2)^2-16(1-\alpha^4).
\tag{8}
\]

The exact generic computation gave \(\delta\notin L^{\times2}\).

## 4. Norm obstruction and a genus-three curve

The computed norm is the exact identity

\[
\boxed{
\operatorname{Norm}_{L/k}(\delta)
=\frac{4096(c^2+4)(c^6+36c^4-1024)}{c^4(c^2-4)^4}.
}
\tag{9}
\]

The numerator factors as \((c^2+4)(c^6+36c^4-1024)\), and the denominator is a square in \(k\). Therefore, for rational \(c\ne0,\pm2\) with \(N_c\) irreducible, splitting of \(Q_\alpha\) over \(\mathbb Q(\alpha)\) **requires**

\[
\boxed{v^2=H(c),\qquad
H(c)=(c^2+4)(c^6+36c^4-1024).}
\tag{10}
\]

The polynomial \(H\) is squarefree (verified by \(\gcd(H,H')=1\)). Hence the smooth projective model of (10) is a genus-three hyperelliptic curve. By Faltings' theorem it has finitely many rational points. This yields:

> **Proposition (finite splitting parameters, irreducible case).** There are only finitely many rational \(c\ne0,\pm2\) for which \(N_c\) is irreducible over \(\mathbb Q\) and the residual quadratic \(Q_\alpha\) splits over \(\mathbb Q(\alpha)\).

**Proof.** Splitting implies that \(\delta\) is a square in \(\mathbb Q(\alpha)\), so its norm is a rational square. Equation (9) then yields a rational point \((c,v)\) on (10). Faltings' theorem gives finiteness. \(\square\)

The norm-square condition is **necessary, not sufficient**: even if (10) has a rational point, the discriminant \(\delta\) may remain nonsquare in \(\mathbb Q(\alpha)\).

A useful quotient of (10) under \(c\mapsto-c\) is

\[
v^2=(x+4)(x^3+36x^2-1024),\qquad x=c^2.
\tag{11}
\]

This is a genus-one quartic when smooth. Its rational points with square \(x\) are precisely the candidates coming from rational \(c\); the genus-one quotient alone does not solve the genus-three rational-point problem.

## 5. Reducibility of \(N_c\)

The quadratic discriminant is

\[
\operatorname{disc}_t(N_c)=-4c^6+64c^2+256
=4(-c^6+16c^2+64).
\tag{12}
\]

For rational \(c\ne0,\pm2\), reducibility of \(N_c\) over \(\mathbb Q\) requires a rational point on

\[
w^2=-c^6+16c^2+64.
\tag{13}
\]

The sextic on the right is squarefree (\(\gcd(f,f')=1\)); its smooth projective curve has genus two. Faltings' theorem implies that **only finitely many rational \(c\)** make \(N_c\) reducible (outside the degenerate leading-coefficient cases, which are already finite).

Combining (10) and (13), outside a finite set of rational \(c\), the residue cubic (6) has exactly one root in the quadratic field \(\mathbb Q(\alpha)\), namely \(r=c(1+\alpha^2)\).

## 6. Consequence for bounded-degree polynomial sections

Let \(c\in\mathbb Q\) avoid the finite exceptional set above. Suppose a polynomial section of (1) satisfies

\[
\deg X\le4,\qquad N_c\mid X.
\]

As in Section 2, \(N_c^2\mid Y\), and \(U=X/N_c\) must reduce to the unique residue root \(c(1+\alpha^2)\). Thus

\[
\frac{X}{N_c}\equiv c(1+t^2)\pmod{N_c},
\]

and hence

\[
X\equiv X_P\pmod{N_c^2}.
\]

Since \(\deg N_c^2=4\) and \(\deg X,\deg X_P\le4\), there is a constant \(\lambda\in\mathbb Q\) such that

\[
\boxed{X=X_P+\lambda N_c^2.}
\tag{14}
\]

This is a strong **conditional shape restriction** for this class of polynomial sections. It does not show that a nonzero \(\lambda\) produces a section, or that such a section would be independent of \(P_c\).

For the generic function-field calculation, the analogous coefficient belongs to \(\mathbb Q(c)\).

## 7. Computational evidence

The Magma calculations reported:

- \(N_c\) irreducible over \(\mathbb Q(c)\).
- Residue cubic factoring as one linear and one irreducible quadratic factor over \(\mathbb Q(c,\alpha)\).
- Generic quadratic discriminant nonsquare in \(\mathbb Q(c,\alpha)\).
- Norm formula (9), including the factorization of its numerator.
- \(H(c)\) squarefree.
- A test of 24 nondegenerate rational values from the displayed finite list (including signs) found **no norm-square specialization**. This is numerical evidence only, not a proof that the genus-three curve has no rational points.

The algebraic norm and factorization outputs were independently checked symbolically in the Magma runs; a reproducible standalone verification script can be added separately.

## 8. Scope and unresolved questions

This note establishes a finiteness theorem for **exceptional splitting of a local residue quadratic**, not a finiteness theorem for Picard-number jumps or for rank-two fibers of \(E_t\).

In particular:

1. The local restriction applies only to polynomial sections with \(N_c\mid X\); other component patterns and sections with poles remain outside its scope.
2. A splitting residue quadratic does not automatically lift to a global section.
3. A newly constructed global section must be tested for independence from the known section \(P_c\).
4. The existence of finitely many exceptional local residues does **not** imply that finitely many rational \(t\) have \(\operatorname{rank}E_t(\mathbb Q)\ge2\).

A concrete next step is to substitute (14) into (1), test the resulting square condition, and separately analyze the other local component patterns. The original finite-versus-infinite rank-two specialization problem remains open.
