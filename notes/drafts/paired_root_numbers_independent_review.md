<!-- Provenance: uploaded to the chat by the repository owner on 14 November 2026 as paired_root_numbers_independent_review.md. Reviewed in notes/REVIEW_2026-11-14_paired_root_numbers_note.md.
     The text below the line is unmodified. -->

---

# Paired root numbers under a torsion involution: a review draft

**Status:** Working note for independent mathematical review, **not yet a publication-ready theorem**. The algebraic identities and resultant below have been checked symbolically. The local root-number assertions, especially at primes dividing the Pythagorean hypotenuse, require independent proof and computational verification before publication.

## 1. Setup

For a rational parameter \(t\), let
\[
 A(t)=\frac{1-t^2}{1+t^2},\qquad B(t)=\frac{2t}{1+t^2},\qquad
 E_t:\ y^2=x^3+4A(t)x-8B(t).
\]
The involution
\[
 R(t)=-\frac{1+t}{1-t}
\]
acts by \((A,B)\mapsto(-B,-A)\). The point \(t=1\) maps to infinity; projective parameterization is needed there.

Choose a primitive integer Pythagorean triple \((a,b,c)\) with \(c>0\), \(a^2+b^2=c^2\), \(A=a/c\), \(B=b/c\). Put
\[
 F=4a^3+27b^2c,\qquad G=-4b^3+27a^2c.
\]
Directly from the short Weierstrass discriminant,
\[
 \Delta(E_t)=-\frac{4096F}{c^3},\qquad
 \Delta(E_{R(t)})=-\frac{4096G}{c^3}.
\]
The expressions are discriminants of the displayed rational models, not necessarily minimal integral discriminants.

## 2. Multiplicative primes away from the denominator

Let \(p\ge5\) and \(p\nmid c\). If \(p\mid F\), then \(p\nmid ab\) and \(c_4=-192a/c\) is a unit at \(p\); thus \(E_t\) has multiplicative reduction. Its local root number is
\[
 w_p(E_t)=-\left(\frac{ab}{p}\right).
\]
Likewise, if \(p\mid G\), the transformed curve has multiplicative reduction and
\[
 w_p(E_{R(t)})=-\left(\frac{ab}{p}\right).
\]
Here the Legendre symbol is evaluated on the integer \(ab\), nonzero modulo \(p\). These formulas can be proved from the split-multiplicative criterion \((-c_6/p)=1\), using \(a^2+b^2=c^2\) and the respective congruences \(F\equiv0\) or \(G\equiv0\pmod p\). **The reviewer should check this congruence argument explicitly.**

Consequently, for \(p\ge5\), \(p\nmid c\),
\[
 w_p(E_t)w_p(E_{R(t)})=
 \begin{cases}
 -\left(\frac{ab}{p}\right),&p\mid FG\text{ but }p\nmid\gcd(F,G),\\
 +1,&\text{otherwise}.
 \end{cases}
\]
At a common multiplicative bad prime, both signs coincide, so their product is \(+1\).

**Important open verification:** The earlier analysis asserted that the paired local root numbers also cancel for all \(p\ge5\) dividing \(c\). That claim has **not** been independently established here. Such primes generally give additive potentially good reduction in integral models, so the multiplicative argument above does not apply. Until checked, retain their contribution as a separate factor \(C_c(t)\).

## 3. Quotient coordinate and discriminant square class

Define the invariant
\[
 z=t+R(t)=\frac{t^2+1}{t-1}.
\]
Then \(t\) satisfies \(t^2-zt+z+1=0\), whose discriminant is \(z^2-4z-4\).

Set
\[
 P(z)=27z^6-999z^4-2030z^3-1365z^2-312z-32.
\]
An exact symbolic identity is
\[
 \Delta(E_t)\Delta(E_{R(t)})=-\frac{2^{22}}{z^6}P(z).
\]
For \(z\ne0\), the discriminant product has square class \([-P(z)]\) in \(\mathbb Q^\times/\mathbb Q^{\times2}\). Magma reports that \(P\) is irreducible over \(\mathbb Q\) and has discriminant
\[
 56642762775035360714056704\ne0.
\]
Therefore \(y^2=-P(z)\) is a smooth genus-two hyperelliptic curve. By Faltings' theorem it has finitely many rational points. This bounds the rational quotient values \(z\) for which the product of the **displayed model discriminants** is a square. It does **not** by itself constrain the frequency of paired root-number signs.

## 4. Common bad-prime restriction

With
\[
 H(t)=t^6-30t^4-24t^2-1,
\quad J(t)=27t^6-27t^4-32t^3-27t^2+27,
\]
one finds exactly
\[
 \operatorname{Res}_t(H,J)=398539554953136128
 =2^{11}\cdot7\cdot103\cdot519521^2.
\]
The common factors of their reductions modulo the exceptional odd primes are

| \(p\) | \(\gcd(H,J)\) in \(\mathbb F_p[t]\) |
|---|---|
| 7 | \(t+3\) |
| 103 | \(t+37\) |
| 519521 | \(t^2-97448t+97449\) |

This restricts primes at which the **two polynomial reductions** can share a root. Caution: translating this directly to primitive \(F,G\) requires tracking numerator/denominator clearing and primes dividing \(c\).

## 5. Global paired root number: unconditional decomposition

Let \(K(t)=W(E_t)W(E_{R(t)})\). The two archimedean local root numbers multiply to \(+1\). Thus
\[
 K(t)=C_{2,3}(t)\,C_c(t)
 \prod_{\substack{p\ge5,\ p\nmid c\\p\mid FG,\ p\nmid\gcd(F,G)}}
 \left[-\left(\frac{ab}{p}\right)\right],
\]
where
\[
 C_{2,3}(t)=\prod_{p\in\{2,3\}}w_p(E_t)w_p(E_{R(t)}),
\qquad
 C_c(t)=\prod_{\substack{p\ge5\\p\mid c}}w_p(E_t)w_p(E_{R(t)}).
\]
This formulation **does not assume** the unverified claim \(C_c(t)=1\). Establishing or refuting that claim is a priority for review.

The product satisfies the exact symmetry \(K(R(t))=K(t)\), simply because \(R\) is an involution. The discriminant square class \([-P(z)]\) does not determine \(K(t)\): local splitting characters at primes dividing exactly one of \(F,G\) remain necessary.

## 6. Numerical checks on the rational circle orbit

The rational recurrence
\[
 t_{n+1}=\frac{2(t_n-2)}{t_n^2}-t_{n-1},\qquad
 t_1=0,\quad t_2=3/4
\]
generates the same parameters as translation by the chosen point on the auxiliary elliptic curve (where defined). Magma V2.30-1 returned:

| \(n\) | \(W(E_{t_n})\) | \(W(E_{R(t_n)})\) | \(K(t_n)\) |
|---:|---:|---:|---:|
| 1 | +1 | -1 | -1 |
| 2 | -1 | +1 | -1 |
| 3 | -1 | -1 | +1 |
| 4 | -1 | -1 | +1 |
| 5 | -1 | -1 | +1 |
| 6 | +1 | -1 | -1 |
| 7 | +1 | +1 | +1 |
| 8 | -1 | -1 | +1 |

These observations rule out a constant global paired sign on this sample, but establish no distribution theorem.

## 7. Questions for the independent reviewer

1. Prove or disprove the proposed multiplicative splitting-character identity at every \(p\ge5\), \(p\nmid c\), including valuation edge cases.
2. **Most importantly:** determine \(w_p(E_t)w_p(E_{R(t)})\) when \(p\ge5\) divides \(c\). Is it always \(+1\), or does a residual character remain?
3. Verify the quotient polynomial identity and check that the square-class and genus-two deductions account for excluded projective points and singular specializations.
4. Check the precise relationship between the resultant of \(H,J\) and simultaneous divisibility of the primitive integer quantities \(F,G\).
5. Determine whether the quotient square class \([-P(z)]\) has any genuine role in the paired **local root-number** formula, rather than only in the discriminant product.
6. Assess whether the resulting statement is new relative to standard local root-number formulas for elliptic curves and families of twists.

## 8. Scope and publication status

The note provides a potentially useful **structural reduction** for the paired root-number observable under a rational torsion involution. It does **not** prove equidistribution of root numbers, infinitude of any rank stratum, or Problem H. The denominator-prime local factor and literature novelty must be resolved before any theorem is submitted for publication.
