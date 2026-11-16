<!-- Provenance: text supplied by the repository owner on 16 November 2026 (file Fn_discriminant_collision_independent_review.md), reproduced word for word below this line. The Magma computations quoted in it were not reproduced in review; see notes/REVIEW_2026-11-16_F_collision_side_study.md. -->

# Independent Review Dossier: Repeated Values of F(t) and Discriminant Rigidity

**Date:** 16 November 2026  
**Status:** Research summary; conjecture remains open  
**Purpose:** Independent mathematical review of repeated rational values of the discriminant function in a family of elliptic curves.

## 1. Original elliptic-curve family

We study

\[
E_t:\quad Y^2=X^3+4A(t)X-8B(t),\qquad t\in\mathbb Q,
\]

where

\[
A(t)=\frac{1-t^2}{1+t^2},\qquad B(t)=\frac{2t}{1+t^2},\qquad A(t)^2+B(t)^2=1.
\]

Define

\[
F(t)=4A(t)^3+27B(t)^2
=-\frac{4(t^6-30t^4-24t^2-1)}{(1+t^2)^3}.
\]

The discriminant of the displayed Weierstrass model is

\[
\Delta(E_t)=-1024F(t).
\]

Since \(F(-t)=F(t)\), the natural **collision conjecture** is

\[
\boxed{F(t)=F(u),\ t,u\in\mathbb Q\ \Longrightarrow\ u=\pm t.}
\]

Equivalently, the rational function

\[
G(s)=-\frac{4(s^3-30s^2-24s-1)}{(1+s)^3}
\]

is conjectured to be injective when restricted to rational squares \(s\).

Equal values of \(F\) mean equal discriminants of these **specified models**. They do not generally imply equal conductors, ranks, or \(j\)-invariants. The obvious pair \(t,-t\) gives quadratic twists by \(-1\), isomorphic over \(\mathbb Q(i)\).

## 2. Nontrivial collision equation

After clearing denominators and removing the trivial factor \(t^2-u^2\), the nontrivial collision equation obtained in the investigation is

\[
\begin{aligned}
Q(t,u)={}&33t^4u^4+27t^4u^2+2t^4\\
&+27t^2u^4-16t^2u^2-27t^2\\
&+2u^4-27u^2-21=0.
\end{aligned}
\]

With \(x=t^2\) and \(y=u^2\), this is a conic subject to the simultaneous square conditions \(x,y\in\mathbb Q^2\).

A rational parametrization recorded in the investigation is

\[
x=\frac{A_0(m)}{B_0(m)},\qquad y=-\frac{C_0(m)}{D_0(m)},
\]

where

\[
\begin{aligned}
A_0(m)&=m^2-108m+2019,\\
B_0(m)&=m^2-465,\\
C_0(m)&=23m^2-1242m+16143,\\
D_0(m)&=31m^2-1674m+22359.
\end{aligned}
\]

**Review requirement:** independently verify the factorization, parametrization, and exceptional denominator cases. The square conditions are essential: a rational conic point alone does not give a collision.

## 3. Genus-three curve and quotient structure

The product of the square conditions yields the genus-three hyperelliptic curve

\[
H_3:\quad v^2=-A_0(m)B_0(m)C_0(m)D_0(m).
\]

Magma calculations reported:

- The degree-eight polynomial is squarefree and \(H_3\) has genus 3.
- The automorphism group has order 4.
- A nonhyperelliptic involution acts by
  \[
  m\mapsto\frac{31m-897}{m-31},\qquad
  v\mapsto\frac{4096v}{(m-31)^4}.
  \]
- Its elliptic quotient has proven rank 1, with a minimal model
  \[
  E_1:\quad y^2+xy=x^3-8711x+312201.
  \]
- The complementary quotient has genus 2.

The resulting Jacobian decomposition is, up to \(\mathbb Q\)-isogeny,

\[
\operatorname{Jac}(H_3)\sim E_1\times J_2,
\]

so

\[
\operatorname{rank}\operatorname{Jac}(H_3)(\mathbb Q)
=1+\operatorname{rank}J_2(\mathbb Q).
\]

A bounded search for rational \(m\) of height at most 100 found \(m=23\) (trivial rational lifts) and \(m=39\) (no rational square lifts). This is evidence, **not an exhaustive rational-point determination**.

## 4. Genus-two curve and exact 2-descent

The genus-two quotient is

\[
H_2:\quad W^2=-(z-46)(z-78)
(23z^2-3726z+122472)
(31z^2-1674z+11664).
\]

Let \(J_2=\operatorname{Jac}(H_2)\). The defining sextic has factor degrees \([1,1,2,2]\), and the rational 2-torsion subgroup is

\[
J_2(\mathbb Q)[2]\cong(\mathbb Z/2\mathbb Z)^2.
\]

Magma explicitly verified that the divisor class represented by the pair of Weierstrass points \((46,0)\) and \((78,0)\) has order dividing 2.

**Latest reproduced Magma V2.30-1 computation:**

```text
2-Selmer dimension = 4
2-torsion dimension = 2
Rank upper bound from Selmer = 2
TwoSelmerGroupData runtime ≈ 8.2–8.4 seconds
Abstract Selmer group = (Z/2)^4
Sdata component lengths = [6, 2, 0]
```

Thus the exact Selmer sequence gives

\[
\boxed{\operatorname{rank}J_2(\mathbb Q)
+\dim_{\mathbb F_2}\Sha(J_2)[2]=2.}
\]

The possibilities are:

| Mordell–Weil rank | Required \(\dim_{\mathbb F_2}\Sha(J_2)[2]\) |
|---:|---:|
| 0 | 2 |
| 1 | 1 |
| 2 | 0 |

The curve has rational Weierstrass points, so the canonical Cassels–Tate pairing is alternating. **Conditional on finiteness of the 2-primary part of \(\Sha\)**, the rank must be even, leaving ranks 0 and 2. Without that assumption, the unconditional bounds remain

\[
\boxed{0\le\operatorname{rank}J_2(\mathbb Q)\le2.}
\]

A nontrivial Cassels–Tate pairing on the relevant Selmer classes would provide an obstruction to rank 2, potentially establishing rank 0 unconditionally. A vanishing pairing would not establish rank 2.

## 5. Computational approaches already tried

| Approach | Finding | Remaining limitation |
|---|---|---|
| Genus-three rational-point search | Only trivial rational lifts in bounded search | Not exhaustive |
| Genus-two rational-point search (PARI/GP) | Points with \(z=46,78\) found at height ≤100 | Does not determine Jacobian rank |
| Magma 2-descent | \(\dim\operatorname{Sel}_2=4\), rank bound 2 | Cannot distinguish rank 0, 1, 2 |
| Richelot 2-isogenies | 15 other genus-two Jacobians, no elliptic products or Weil restrictions | No improved rank bound |
| Genus-two Mordell–Weil computation | Timed out after 300 seconds | No rank determination |
| SageCell direct rank methods | No applicable built-in genus-two Jacobian rank method found | No direct result |
| Fisher–Yan Cassels–Tate code | Source identified and examined | MagmaCell file attachment and input-size restrictions |

For the Richelot splitting into the three displayed quadratic factors, the determinant was computed as \(331776=576^2\ne0\).

**Fisher–Yan reference:** [Computing the Cassels–Tate pairing on the 2-Selmer group of a genus 2 Jacobian](https://arxiv.org/abs/2306.06011).  
**Implementation:** [Tom Fisher's Magma source](https://github.com/TomAFisher/Cassels-Tate-pairing--Genus-2).

## 6. Open questions for independent review

1. **Algebraic audit:** Is the collision polynomial \(Q(t,u)\) exactly correct? Are the conic parametrization and genus-three covering complete, including exceptional and points-at-infinity cases?
2. **Exact Jacobian rank:** Can one rigorously determine \(\operatorname{rank}J_2(\mathbb Q)\in\{0,1,2\}\), preferably by a Cassels–Tate pairing, 4-descent, or another efficient method?
3. **Direct rational-point proof:** Can one classify rational points on \(H_3\) satisfying both square-lift conditions without first determining the full Mordell–Weil group of \(J_2\)?
4. **Finiteness:** Can one rigorously establish that nontrivial rational collisions are finite using the covering geometry and Faltings' theorem, even if their nonexistence remains open?
5. **Rigidity theorem:** Can one prove that equal values of \(F\) force \(u=\pm t\), hence equal model discriminants determine the family parameter up to the \(-1\) quadratic twist?
6. **Implications and limits:** What does any proven discriminant rigidity actually imply for isomorphism classes, conductors, or rank variation? Avoid claiming consequences for infinitely many rank-two specializations without a separate argument.

## 7. Precise request to the reviewer

Please independently verify the algebraic reduction and the genus-three/genus-two quotient geometry; check whether the existing 2-Selmer data permit a practical Cassels–Tate pairing or another rank improvement; and, crucially, look for a direct proof of the absence of nontrivial rational collisions. Clearly distinguish exact computational proofs, bounded numerical searches, conditional parity statements, and unresolved claims.

**Current conclusion:** The collision conjecture is open. The genus-two Jacobian has a proven 2-Selmer dimension of 4, rational 2-torsion dimension of 2, and rank bound \([0,2]\). The key unresolved problem is to turn the geometric reduction into an exhaustive arithmetic argument.
