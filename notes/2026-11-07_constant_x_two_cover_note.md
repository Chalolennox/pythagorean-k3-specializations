# Independent Review Request: Finiteness of Simultaneous Constant-\(x\) Specializations

**Status:** Proposed proof with explicit checks requested.  
**Scope:** The *fixed pair of distinct constant-\(x\) covers* of the Pythagorean elliptic-curve family. This note does **not** claim to settle the original rank-\(\ge2\) infinitude problem or exclude arbitrary second sections on a single cover.

## 1. Original family and central problem

Consider
\[
E_t:\quad y^2=x^3+4\frac{1-t^2}{1+t^2}x-\frac{16t}{1+t^2},\qquad t\in\mathbb Q.
\]
Writing
\[
A(t)=\frac{1-t^2}{1+t^2},\qquad B(t)=\frac{2t}{1+t^2},
\]
we have \(A^2+B^2=1\) and \(E_t:y^2=x^3+4Ax-8B\). The overarching question is whether infinitely many rational \(t\) satisfy \(\operatorname{rank}E_t(\mathbb Q)\ge2\).

For a fixed rational \(c\), requiring a point with \(x=c\) leads to
\[
C_c:\quad w^2=(1+t^2)N_c(t),\qquad
N_c(t)=c(c^2-4)t^2-16t+c^3+4c.
\]
Indeed, the corresponding point on \(E_t\) is \((c,w/(1+t^2))\). Each \(C_c\) is a double cover of \(\mathbb P^1_t\).

**Question addressed here.** For distinct *fixed* rational \(a,b\), can the simultaneous conditions \(C_a(\mathbb Q)\) and \(C_b(\mathbb Q)\) above the same rational \(t\) hold for infinitely many \(t\)? The proposed answer is **no**.

## 2. Branch divisors of individual covers

The branch divisor of \(C_c\to\mathbb P^1_t\) is the union of \(t=i,-i\) and the two roots of \(N_c\), interpreted on \(\mathbb P^1\). For \(c=0,\pm2\), \(N_c\) has degree one, and its second root is at infinity.

The relevant exact identities are
\[
\operatorname{disc}_t(N_c)=4(64+16c^2-c^6),
\qquad
\operatorname{Res}_t(N_c,1+t^2)=64(c^2+4).
\]
For rational \(c\), neither expression vanishes:

* \(c^2+4\ne0\) over \(\mathbb Q\).
* If \(c^6-16c^2-64=0\) with \(c\in\mathbb Q\), the rational-root theorem forces \(c\in\mathbb Z\). Odd \(c\) give \(c^6-16c^2-64\equiv1\pmod4\). Even \(c=2k\) give \(64(k^6-k^2-1)\ne0\), since \(k^6-k^2-1\) is odd. Thus there is no rational root.

Consequently, for **every** rational \(c\), the branch divisor has exactly four distinct geometric points, and the smooth projective model of \(C_c\) has genus one by Riemann–Hurwitz.

## 3. Two distinct covers and connectedness

Fix \(a,b\in\mathbb Q\) with \(a\ne b\), and consider the normalization of the fiber product
\[
D_{a,b}:\quad
w_a^2=(1+t^2)N_a(t),\qquad
w_b^2=(1+t^2)N_b(t).
\]
Over \(\overline{\mathbb Q}(t)\), the two quadratic extensions are distinct. Indeed, their square classes could coincide only if their branch divisors coincide, since a square has even valuation everywhere. Both have the fixed points \(\pm i\), so coincidence would require the moving root divisors of \(N_a,N_b\) to coincide.

For finite quadratic \(N_a,N_b\), identical roots imply proportional polynomials; comparing their common \(t\)-coefficient \(-16\) makes them equal. Equality of constant and quadratic coefficients then gives \(8a=8b\), a contradiction. In degree-drop cases \(c\in\{0,\pm2\}\), the moving divisors consist of infinity and the distinct finite points \(0,1,-1\), respectively, and cannot equal a quadratic moving divisor or each other. Hence the branch divisors cannot coincide for \(a\ne b\).

It follows that the compositum has degree four, with geometric Galois group \((\mathbb Z/2\mathbb Z)^2\), and \(D_{a,b}\) is geometrically connected. **Reviewer check requested:** confirm that the above square-class/branch argument covers all degree-drop cases without hidden degeneracies.

## 4. Genus of the normalized fiber product

Let \(m\) be the number of distinct geometric branch points in the union of the two four-point branch divisors. The fixed points \(\pm i\) are shared. The two moving degree-two divisors are distinct, so they share either zero or one geometric point. Thus
\[
m=6\quad\text{or}\quad m=5.
\]
At each branch point, the inertia subgroup in the biquadratic degree-four cover has order two (even when both quadratic subcovers ramify there). The total ramification contribution is \(2\) per branch point. Riemann–Hurwitz gives
\[
2g(D_{a,b})-2=4(-2)+2m=-8+2m,
\]
and therefore
\[
\boxed{g(D_{a,b})=m-3\in\{2,3\}.}
\]
More explicitly:

| Moving branch roots shared | Distinct branch points \(m\) | Genus |
|---|---:|---:|
| None | 6 | 3 |
| Exactly one | 5 | 2 |

There is no genus-zero or genus-one case for distinct rational \(a,b\), provided the branch-divisor and connectedness arguments above are correct.

## 5. Finiteness theorem for a fixed pair

**Proposed theorem.** For any fixed distinct rational numbers \(a,b\), there are only finitely many rational \(t\) for which \(E_t\) simultaneously contains rational points with \(x=a\) and \(x=b\).

**Proof.** Such a \(t\) lifts to a rational point on the affine fiber product \(D_{a,b}\), away from finitely many special coordinates. Its smooth projective normalization is a geometrically connected curve over \(\mathbb Q\) of genus two or three by Sections 3–4. Faltings' theorem implies that this curve has finitely many rational points. Their images in \(\mathbb P^1_t(\mathbb Q)\) are therefore finite. \(\square\)

**Interpretation.** The proof rules out producing infinitely many rank-two specializations by **holding two distinct rational \(x\)-coordinates fixed** and requiring both corresponding points to exist. It does not require those two points to be independent; even simultaneous existence happens at only finitely many parameters.

## 6. The exceptional resultant equation

Earlier algebraic elimination yielded the resultant
\[
\operatorname{Res}_t(N_a,N_b)
=64(a-b)^2\left[a^2b^2(a+b)^2+4\big((a^2+ab+b^2)^2-16\big)\right].
\]
For \(a\ne b\), a shared moving root is therefore governed by
\[
\boxed{F(a,b)=a^2b^2(a+b)^2+4((a^2+ab+b^2)^2-16)=0.}
\]
This exceptional equation does **not** produce a genus-one fiber product. A single common moving root lowers the genus from three to **two**, still covered by Faltings.

### Relation to full rational 2-torsion

Set
\[
A=-\frac{a^2+ab+b^2}{4},\qquad
B=-\frac{ab(a+b)}8.
\]
Then \(F(a,b)=0\) is equivalent to \(A^2+B^2=1\), and
\[
x^3+4Ax-8B=(x-a)(x-b)(x+a+b).
\]
Thus solutions correspond to rational circle points whose associated cubic splits over \(\mathbb Q\). If \(a=b\) or \(a=-2b\) or \(b=-2a\), roots repeat; such cases must be checked separately when claiming **full** rational 2-torsion. The equation \(F=0\) alone does not guarantee three distinct roots.

For finite rational \(t\), the elliptic-curve discriminant is
\[
\Delta(t)=\frac{4096(t^6-30t^4-24t^2-1)}{(1+t^2)^3}.
\]
Three distinct rational roots imply a rational-square discriminant, and hence the necessary condition
\[
\boxed{z^2=(1+t^2)(t^6-30t^4-24t^2-1).}
\]
The right-hand polynomial is squarefree of degree eight (e.g. its gcd with its derivative over \(\mathbb Q[t]\) is 1), so the smooth projective curve has genus three. Faltings shows that only finitely many finite rational \(t\) can satisfy this **necessary** condition. The circle point \((A,B)=(-1,0)\) corresponds to \(t=\infty\) and has cubic roots \(-2,0,2\).

**Important qualification for review:** The genus-three square-discriminant condition proves finiteness only for the **distinct-root/full-2-torsion** subcase. It does not by itself classify repeated-root solutions of \(F(a,b)=0\). For the original elliptic-curve family over rational circle points, the discriminant sextic has no rational zeros, so repeated roots do not occur at rational nonsingular parameters; nevertheless, this inference should be checked explicitly. The fixed-pair genus argument of Sections 2–5 does not depend on classifying the rational solutions of \(F(a,b)=0\).

## 7. What is proved, and what is not

**Claimed/proved conditional on the elementary branch checks:**

1. Every rational constant-\(x\) cover \(C_c\) has four distinct branch points and genus one.
2. For any distinct rational \(a,b\), the normalized fiber product \(D_{a,b}\) is geometrically connected and has genus two or three.
3. For each fixed pair \((a,b)\), only finitely many rational specializations support both constant-\(x\) points.
4. The resultant equation \(F(a,b)=0\) identifies the possible genus-two cases, not a loophole to genus one.

**Not established:**

- An explicit classification of all rational solutions of \(F(a,b)=0\).
- A uniform bound on the number of simultaneous specializations as \((a,b)\) varies.
- Finiteness of rank-\(\ge2\) specializations in the original family.
- Nonexistence of a second independent section on a *single* genus-one cover \(C_c\).
- Elimination of constructions with rational \(x\)-coordinates varying with \(t\).

## 8. Specific questions for an independent referee

1. Verify the identities for \(\operatorname{disc}_t N_c\), \(\operatorname{Res}_t(N_c,1+t^2)\), and \(\operatorname{Res}_t(N_a,N_b)\).
2. Check smoothness and the four-point branch description for **all** rational \(c\), especially \(c=0,\pm2\).
3. Check geometric connectedness of the compositum and that distinct moving branch divisors cannot coincide.
4. Confirm inertia order two at a common moving branch point, giving genus **two**, not one.
5. Check whether the exceptional resultant equation has rational solutions beyond the obvious \(t=\infty\) cases, while distinguishing distinct and repeated cubic roots.
6. Verify the exact scope of the finiteness theorem and that no claim about arbitrary rank-two specializations follows.

**Bottom line:** Subject to the explicitly identified elementary checks, the fixed-two-constant-\(x\)-cover strategy is eliminated by a uniform genus-\(\ge2\) argument and Faltings' theorem. The original rank-\(\ge2\) infinitude problem remains open.
