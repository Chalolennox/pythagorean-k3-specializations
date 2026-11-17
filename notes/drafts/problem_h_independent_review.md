<!-- Provenance: uploaded to the chat by the repository owner on 17 November 2026 as problem_h_independent_review.md. Reviewed in notes/REVIEW_2026-11-17_problem_h_dossier.md; the companion Magma script is problem_h_independent_review.m in this directory.
     The text below the line is unmodified. -->

---

# Problem H: Independent review dossier

**Scope:** (A) disjoint qualifying-prime sets at consecutive orbit indices; (B) Chebotarev density of primes with no qualifying roots.  
**Status:** The resultant identity in (A) is an exact algebraic calculation, subject to independent reproduction. The global disjointness assertion still requires exceptional-prime and denominator checks. The numerical density in (B) is a **computational candidate**, not yet a certified theorem.

## Setup

Consider

\[
C:\ y^2=x^3-2x^2+2x,\qquad P=(1,1),\quad T=(0,0),\quad t(Q)=1-x(Q),
\]

and

\[
H(t)=t^6-30t^4-24t^2-1.
\]

For a prime \(p\ge5\), outside finitely many exceptional cases, call \(a\in\mathbb F_p\) **qualifying** if

\[
H(a)=0,\qquad q(a)=\frac{2a(1-a^2)}{(1+a^2)^2}\in(\mathbb F_p^\times)^2,
\qquad r(a)=(1-a)(1+a^2)\in(\mathbb F_p^\times)^2,
\]

and, when \((2/p)=+1\), additionally \(x(a)=1-a\) is a square. Let \(\mathcal Q_p\) denote the set of qualifying roots. The *orbit-contributing* condition is stronger: a qualifying root must be attained by \(t(nP)\) or \(t(nP+T)\) modulo \(p\).

## A. Consecutive qualifying-prime sets

### Algebraic elimination

For consecutive points \(Q,Q+P\), write \(t=t(Q)\) and \(u=t(Q+P)\). The addition law gives the necessary polynomial relation

\[
\Phi(t,u)=(t^2u-t+2)^2-4(1-t)(1+t^2)=0.
\]

If a prime \(p\ge5\) divides both discriminant sextic values at two consecutive **finite, integral** orbit parameters, then, provided the reduction and denominator conditions apply, the three equations

\[
H(t)=H(u)=\Phi(t,u)=0\pmod p
\]

have a common solution. Consequently \(p\) divides the integer iterated resultant

\[
D=\operatorname{Res}_t\bigl(H(t),\operatorname{Res}_u(\Phi(t,u),H(u))\bigr).
\]

The reported exact factorization is

\[
\boxed{|D|=2^{18}3^{30}\cdot7\cdot103\cdot113^3\cdot13085561^2.}
\]

Thus the **only candidate common primes \(p\ge5\)** arising from the affine elimination are

\[
\boxed{7,\ 103,\ 113,\ 13085561.}
\]

The resultant establishes a necessary condition for common **bad primes**, not automatically for common **qualifying primes**. Previous computations reportedly found that \(7,103,113\) yield no qualifying consecutive pair and that \(13085561\) is nonqualifying. These exceptional-prime claims require independent verification, including projective/denominator configurations, before the statement that consecutive qualifying-prime sets are disjoint for **all** orbit indices can be called proved.

**Independent checks requested:** Recompute \(D\), verify its factorization and \(\gcd(H,\operatorname{Res}_u(\Phi,H(u)))=1\) over \(\mathbb Q[t]\), and check every exceptional prime with the actual qualifying tests and orbit branches. Explicitly handle points reducing to infinity or to poles of the rational parameterization.

## B. Density of primes with an empty qualifying-root set

### Resolvents and finite Galois conditions

Let \(a_1,\dots,a_6\) be the roots of \(H\) in an algebraic closure. Define the two resolvents by their generic roots:

\[
R_-(z):\quad \pm\sqrt{q(a_i)}\pm\sqrt{r(a_i)}\quad (24\text{ roots}),
\]

\[
R_+(z):\quad \pm\sqrt{q(a_i)}\pm\sqrt{r(a_i)}\pm\sqrt{1-a_i}\quad (48\text{ roots}).
\]

These are obtained by elimination from \(H\), with denominators cleared and primitive parts taken. The reported calculations find both polynomials irreducible and squarefree, with a common splitting field \(L\) of degree

\[
|\operatorname{Gal}(L/\mathbb Q)|=24576.
\]

For unramified primes away from a finite exceptional set, the existence of a qualifying root is expressible as a Frobenius fixed-point condition on the relevant radical configurations. Since this is a conjugacy-invariant condition in a finite Galois group, **Chebotarev proves the existence and rationality of the corresponding natural density**. The precise rational value depends on correctly identifying the permutation actions and counting the relevant Frobenius elements.

### Exact inclusion \(\sqrt2\in L\)

Write \(u_i=a_i^2\), choosing one representative from each pair \(\{a_i,-a_i\}\). The three \(u_i\) are roots of

\[
U^3-30U^2-24U-1=0.
\]

For each representative \(a_i\),

\[
\frac{r(a_i)}{1-a_i}=1+a_i^2=1+u_i.
\]

The radical splitting field contains square roots of both numerator and denominator, hence \(\sqrt{1+u_i}\in L\). Evaluating the cubic at \(-1\) gives

\[
\prod_{i=1}^{3}(1+u_i)=8.
\]

Therefore

\[
\prod_{i=1}^{3}\sqrt{1+u_i}=\pm\sqrt8=\pm2\sqrt2\in L,
\]

so **\(\boxed{\sqrt2\in L}\)**. This is an algebraic argument, independent of the numerical Galois-group enumeration.

### Reported Galois counts and candidate density

The previous Magma calculations reported:

| Computation | Reported value |
|---|---:|
| Galois-group order | 24,576 |
| Fixed-point-free elements in degree-24 action | 19,709 |
| Fixed-point-free elements in degree-48 action | 22,035 |
| \(\chi_2=+1\) subgroup, degree-48 fixed-point-free | 11,013 |
| \(\chi_2=-1\) coset, degree-24 fixed-point-free | 9,854 |

Here \(\chi_2\) is the quadratic character corresponding to \(\mathbb Q(\sqrt2)\). The last count was obtained using invariant pairings of the 48-root action. Two pairings reproduced the independently computed degree-24 total and gave the same coset-conditioned count; **agreement of totals alone does not identify the actual arithmetic degree-24 resolvent action**.

If these permutation-action identifications and the Galois-group computation are certified, Chebotarev gives

\[
\boxed{\delta_{\varnothing}=\frac{11013+9854}{24576}
=\frac{20867}{24576}\approx0.849080403646},
\]

and hence

\[
\boxed{\delta_{\mathrm{nonempty}}=\frac{3709}{24576}
\approx0.150919596354}.
\]

**Proof status:** These rational numbers are **conditional computational candidates**. A fully proved numerical density requires (i) arithmetic identification of the degree-24 action in the 48-root Galois action and (ii) a certified Galois-group computation, for example using an appropriate Magma `GaloisProof` workflow. The existence of some rational density follows from Chebotarev without those numerical certifications.

### Independent finite-prime evidence

A reported scan through \(p\le100000\) found 9,590 primes \(p\ge5\), with 8 excluded exceptional primes; among 9,582 good primes, 8,116 had an empty qualifying set and 1,466 had a nonempty one. The empirical empty proportion was approximately 0.8470, consistent with—but not a proof of—the candidate 0.84908.

A separate orbit-membership experiment through \(p\le20000\) gave:

| Statistic | Count | Fraction of 2,260 primes |
|---|---:|---:|
| Primes tested \(p\ge5\) | 2,260 | 100% |
| Primes with qualifying roots | 348 | 15.3982% |
| Primes with qualifying roots in the reduced orbit | 263 | 11.6372% |
| Qualifying primes excluded by orbit membership | 85 | 3.7611% |

Among the 348 qualifying primes, 85 (24.43%) were excluded by the orbit restriction. These are exact finite-sample observations, **not** a theorem about limiting orbit-contributing density. Conditional on certification of the numerical Chebotarev density, the orbit-contributing set has upper density at most \(3709/24576\). Whether its own natural density exists, and its exact value, remain open here.

## C. Questions for the independent reviewer

1. Verify the consecutive-point relation \(\Phi(t,u)=0\) and the resultant factorization independently.
2. Check the exceptional primes \(7,103,113,13085561\) against the full qualifying conditions, including finite/projective reduction and denominator exceptions. Determine whether global consecutive-set disjointness follows.
3. Verify the degree-24 and degree-48 resolvent constructions, irreducibility, squarefreeness, and common splitting field.
4. Check the elementary proof that \(\sqrt2\in L\).
5. Arithmetically identify the actual degree-24 action within the degree-48 permutation action, rather than relying on matching fixed-point-free totals.
6. Certify the Galois group and coset-conditioned fixed-point-free counts; only then promote \(20867/24576\) from candidate to theorem.
7. Keep separate the density of primes with a qualifying root and the stronger condition that such a root occurs in the reduced orbit.

---

*This document summarizes reported calculations and proof arguments for independent review. It is not a claim that the outstanding checks have been completed.*
