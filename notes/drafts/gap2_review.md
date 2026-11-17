<!-- Provenance: uploaded to the chat by the repository owner on 17 November 2026 as gap2_review (1).md. Reviewed in notes/REVIEW_2026-11-17_gap_two_dossier.md; the checks are in code/verify_gap_two.py.
     The text below the line is unmodified. -->

---

# Gap-two coincidences in the qualifying-prime sets: review dossier

**Status:** 17 November 2026. This note separates exact algebraic results, independently checked finite-field data, and claims requiring further certification. It is intended for independent mathematical review, not as a publication-ready proof of the complete exceptional-prime classification.

## 1. Setting and notation

Let

\[
 C:\ y^2=x^3-2x^2+2x,\qquad P=(1,1),\qquad T=(0,0).
\]

For either branch \(\varepsilon\in\{0,1\}\), put

\[
 Q_{n,\varepsilon}=nP+\varepsilon T,\qquad
 t_{n,\varepsilon}=1-x(Q_{n,\varepsilon}).
\]

The polynomial governing bad reduction at primes \(p\ge5\) is

\[
 H(t)=t^6-30t^4-24t^2-1.
\]

For a root \(t\in\mathbf F_p\) with the relevant denominators nonzero, set

\[
 q(t)=\frac{2t(1-t^2)}{(1+t^2)^2},\qquad
 r(t)=(1-t)(1+t^2),\qquad x=1-t.
\]

The qualifying-root test used in the computations requires \(q(t)\) and \(r(t)\) to be nonzero squares, and also requires \(x\) to be a square if \((2/p)=+1\). For orbit qualification, the parameter must actually arise from the chosen reduced orbit. Let \(\mathcal Q_{n,\varepsilon}\) be the set of primes satisfying these conditions at index \(n\). These definitions are the finite-field implementation used in the previous Magma computations; the identification with split multiplicative primes in the original rational elliptic-curve model is a separate arithmetic interpretation.

**Question:** Can a prime lie in both \(\mathcal Q_{n,\varepsilon}\) and \(\mathcal Q_{n+2,\varepsilon}\)?

## 2. Exact translation by \(2P\)

On \(C\),

\[
 2P=\left(\frac14,-\frac58\right).
\]

For \(Q=(x,y)\), away from \(x=1/4\), the addition law gives

\[
 x(Q+2P)=\left(\frac{y+5/8}{x-1/4}\right)^2+\frac74-x
 =\frac{A(x)+(5/4)y}{D(x)},
\]

where

\[
 D(x)=(x-1/4)^2,\qquad
 A(x)=\frac{4x^2+17x+8}{16}.
\]

Write \(h(x)=H(1-x)\). Simultaneous gap-two roots require

\[
 h(x)=0,\quad y^2=x^3-2x^2+2x,\quad
 D(x)^6 h\!\left(\frac{A(x)+(5/4)y}{D(x)}\right)=0.
\]

Denominators must be cleared carefully, and \(x=1/4\) must be checked separately. The latter is the pole of this addition formula, not automatically a genuine simultaneous qualifying point.

## 3. Why there are only finitely many exceptional primes

The previously executed Magma certificate works over \(\mathbf F_5\). There,

\[
 \bar h=x^6+4x^5+x^2+2x+1,\quad
 \bar D=x^2+2x+1,\quad
 \bar A=4x^2+2x+3.
\]

Because the coefficient \(5/4\) vanishes modulo 5, the translated \(x\)-coordinate becomes \(\bar A/\bar D\). The certificate verifies

\[
 \gcd(\bar h,\bar D)=1,\qquad
 \gcd\!\left(\bar h,\bar D^6\bar h(\bar A/\bar D)\right)=1.
\]

The user executed the Magma script and obtained `ALL ASSERTIONS PASSED`. This proves that the corresponding *geometric* gap-two incidence locus has no solutions in characteristic zero, provided the cleared-denominator equations are used as above. An equivalent direct certificate is a nonzero characteristic-zero resultant (next section). Thus only finitely many primes can admit a gap-two coincidence.

**Important:** this does *not* prove universal disjointness. The resultant can vanish modulo exceptional primes even when it is nonzero over \(\mathbf Q\).

## 4. Exact elimination and candidate exceptional primes

Define

\[
 F(x)=x^3-2x^2+2x,\quad
 B(x,y)=D(x)^6h\!\left(\frac{A(x)+(5/4)y}{D(x)}\right).
\]

The expression \(B\) is polynomial after clearing rational denominators. Form the nested resultant

\[
 R_2=\operatorname{Res}_x\!\left(h(x),\operatorname{Res}_y(B(x,y),y^2-F(x))\right).
\]

An independent SymPy computation in this review session confirmed the **odd-prime factorization** of \(|R_2|\) (after rational denominator clearing):

\[
 \boxed{23^{12}\,47^2\,947^2\,4241^{12}\,18637\,36997^2\,
 2325076196570957^2.}
\]

The complete integer normalization previously reported was

\[
 |R_2|=2^{186}3^{27}23^{12}47^2 947^2 4241^{12}
 18637\,36997^2\,2325076196570957^2.
\]

The powers of 2 and 3 depend on the chosen integral normalization of the cleared equations. For \(p\ge5\), the **candidate** exceptional primes are therefore

\[
 \boxed{23,47,947,4241,18637,36997,2325076196570957.}
\]

A complete classification must additionally examine the denominator locus and test all candidate points against both the quadratic-residue conditions and actual orbit membership.

## 5. A verified genuine counterexample at \(p=18637\)

The following computations were independently checked by direct modular arithmetic in this review session:

\[
 p=18637,\quad x=3765,\quad t=1-x\equiv14873\pmod p.
\]

The point

\[
 Q=(3765,7534)\in C(\mathbf F_{18637})
\]

satisfies the curve equation, and

\[
 H(14873)\equiv0\pmod{18637}.
\]

Moreover,

\[
 q(14873)\equiv2329\pmod{18637},\qquad
 \left(\frac{2329}{18637}\right)=+1,
\]

and \(r(14873)\equiv11491\pmod{18637}\) is also a nonzero square. Since \(18637\equiv5\pmod8\), \((2/18637)=-1\), so the additional \(x\)-square test is not imposed by the adopted definition.

The reduced group computation gives

\[
 \operatorname{ord}_{C(\mathbf F_{18637})}(P)=9368.
\]

On the \(P+T\) branch,

\[
 \boxed{4683P+T=(3765,7534)},
\]

\[
 \boxed{4685P+T=(3765,11103)}.
\]

These points are negatives of one another (\(7534+11103=18637\)), so both have the same \(x\)-coordinate and parameter. Therefore

\[
 \boxed{18637\in\mathcal Q_{4683,1}\cap\mathcal Q_{4685,1}.}
\]

This is a **genuine gap-two counterexample**, not merely a common root of algebraic equations.

## 6. Why the counterexample occurs at exactly these neighboring indices

The midpoint is \(n=4684\). Because

\[
 (4683P+T)+2P=4685P+T=-(4683P+T),
\]

we obtain

\[
 2(4684P+T)=O.
\]

Indeed, the modular computation gives

\[
 4684P=(3767,0),
\]

which is a nonzero 2-torsion point, and \(4684P+T\) is also 2-torsion. Thus the gap-two coincidence is explained by a **reflection about a 2-torsion midpoint**. The qualifying root happens to occur at the two points adjacent to that midpoint.

More generally, on any branch, if

\[
 (n+1)P+\varepsilon T\in C(\mathbf F_p)[2],
\]

then

\[
 x(nP+\varepsilon T)=x((n+2)P+\varepsilon T).
\]

This gives a mechanism for candidate gap-two coincidences; qualification still requires \(H\) and the square tests. The converse for equal \(x\)-coordinates follows when \(P\) is non-torsion modulo \(p\) of order greater than 2: the two endpoints must be negatives, so their midpoint is 2-torsion.

## 7. Exact periodicity and recurrence density

Since \(P\) has order \(m=9368\), every orbit point repeats with period 9368. Therefore, for every integer \(k\ge0\),

\[
 \boxed{18637\in\mathcal Q_{4683+9368k,1}
 \cap\mathcal Q_{4685+9368k,1}.}
\]

Reflection also gives the partner indices \(-4683\equiv4685\pmod{9368}\). Thus the two gap-two occurrences are the same reflection pair, not two independent qualifying roots.

For the particular qualifying parameter \(t=14873\), the two indices \(4683,4685\pmod{9368}\) give an exact occurrence frequency of

\[
 \frac2{9368}=\frac1{4684}
\]

**for that parameter on the branch**. This does not claim that these are the only qualifying indices for the prime, because other qualifying roots could exist.

## 8. Sign of the prime and sign products

The Legendre-symbol test above gives

\[
 \left(\frac{a_nb_n}{18637}\right)=+1
\]

for both occurrences, using the previously established identification of the normalized split-character with \(q(t)\). At a split multiplicative prime, the local root number is

\[
 \boxed{w_{18637}(E_{4683+9368k})=
 w_{18637}(E_{4685+9368k})=-1.}
\]

Consequently, the contribution of this prime to the *product* of the two global root numbers is \((-1)^2=+1\). This says nothing by itself about the complete global root numbers, because other primes can contribute different signs.

## 9. Claimed full classification: review status

A previous analysis reported that among the seven candidate exceptional primes only \(18637\) yields an actual gap-two qualifying orbit recurrence, and hence

\[
 \mathcal Q_{n,\varepsilon}\cap\mathcal Q_{n+2,\varepsilon}
 \subseteq\{18637\}\qquad(p\ge5).
\]

**This stronger classification has not been independently reverified in full in this review session.** In particular, the very large prime \(2325076196570957\) and all possible denominator-locus cases require a reproducible certificate of the root, quadratic-character, and orbit tests. The independently confirmed conclusions are: finite candidate set, exact odd-prime resultant factors, and the genuine periodic counterexample at 18637. The universal classification should be presented as **provisional** until the remaining finite checks are supplied.

## 10. Questions for an independent reviewer

1. Confirm the exact integral normalization of the resultant and its factorization, including powers of 2 and 3.
2. Verify all exceptional-prime exclusions, particularly the large prime and the denominator locus \(x=1/4\).
3. Check the precise equivalence between the finite-field square tests and the split multiplicative condition for the rational specializations, including primes dividing denominators of the rational parameter.
4. Determine whether the 2-torsion midpoint mechanism yields a more conceptual classification of gap-two coincidences, potentially avoiding expensive orbit enumeration.
5. Distinguish a bound on gap-two *prime intersections* from claims about correlations or distributions of complete global root numbers.

**Bottom line:** Gap-two disjointness holds outside a finite, explicitly factored candidate set. Universal disjointness is false: \(p=18637\) genuinely qualifies at indices 4683 and 4685 on the \(P+T\) branch, and this coincidence recurs every 9368 indices. The assertion that 18637 is the *only* exception remains to be fully certified.

---

## 10. Addendum (17 November 2026): the Gaussian 2-torsion explanation

This addendum preserves the subsequent claims **as reported** and explicitly separates identities that have been checked here from computations requiring an independent audit.

Over \(\mathbb Q(i)\), the two additional nonzero 2-torsion points are
\[
 U_\pm=(1\pm i,0).
\]
Using the elliptic-curve addition law with \(P=(1,1)\),
\[
 x(U_\pm+P)=-1\mp i,
 \qquad t(U_\pm+P)=2\pm i.
\]
The exact Gaussian-integer calculation is
\[
 H(2+i)=20-772i,\qquad H(2-i)=20+772i,
\]
so
\[
 \boxed{N_{\mathbb Q(i)/\mathbb Q}(H(2+i))
 =20^2+772^2=596384=2^5\cdot18637.}
\]
**Verification status:** the evaluation, norm, factorization, and addition-law formula were independently rechecked symbolically for this updated dossier. This identifies \(18637\) as the unique odd prime factor of this particular norm, **not** as the unique possible prime for all types of gap-two coincidence. In particular, it explains the *same-parameter, 2-torsion-midpoint* mechanism, not necessarily distinct-root coincidences.

For \(p=18637\), the previously reported midpoint is
\[
 U=4684P+T=(14872,0),
\]
and its neighboring orbit points are
\[
 U-P=(3765,7534),\qquad U+P=(3765,11103).
\]
Because \(U=-U\), the two neighboring points are negatives and have the same \(x\)-coordinate. Their parameter is \(t=14873\), which passes the qualifying tests. The point/period calculations are recorded in Sections 5–7; independent reviewers should reproduce them from the supplied curve and prime.

### A limitation of the midpoint mechanism

Equality of the two endpoint parameters is *sufficient* to reduce the problem to the 2-torsion midpoint, and for \(\operatorname{ord}(P)>2\) it is also necessary. But the general gap-two incidence conditions allow **different** roots of \(H\) at the two endpoints. Those cases are controlled by the full resultant, not by the single Gaussian norm above. The stronger claim that \(18637\) is the sole qualifying exception remains provisional, as explained in Section 9.

## 11. Addendum: local sign and complete-period cancellation

Define \(h_{p,\varepsilon}(n)\) to be \(-1\) when \(p\) qualifies at the reduced orbit parameter \(t_{n,\varepsilon}\), and \(+1\) otherwise. This is the **prime's split-multiplicative sign factor**, not the full global root number.

The preceding calculation gives
\[
 h_{18637,1}(4683+9368k)=h_{18637,1}(4685+9368k)=-1.
\]
Thus the common prime contributes \(+1\) to the product of the two signs. The previously reported *complete local sequence* for \(p=18637\) on the \(P+T\) branch was
\[
 h_{18637,1}(n)=
 \begin{cases}
 -1,&n\equiv4683,4685\pmod{9368},\\
 +1,&\text{otherwise}.
 \end{cases}
\]
**Verification qualification:** the earlier dossier established the two occurrences of the specific root \(14873\), but did not independently exclude additional qualifying roots on that branch. Consequently, the assertion that the two indices are *all* occurrences of this prime requires a full finite-field root/orbit scan and should be audited separately.

**Conditional on that complete-sequence claim**, the exact period statistics are
\[
 \prod_{n=0}^{9367}h_{18637,1}(n)=+1,
 \qquad \sum_{n=0}^{9367}h_{18637,1}(n)=9364,
\]
\[
 \frac1{9368}\sum_{n=0}^{9367}h_{18637,1}(n)
 =\frac{9364}{9368}=\frac{2341}{2342}\approx0.999573.
\]
The occurrence frequency is \(2/9368=1/4684\) under the same condition.

### General complete-period product theorem

For any prime \(p\ge5\) of good reduction where the qualifying condition is a function of \(x(nP+\varepsilon T)\) and excludes \(x=0\), put \(m_p=\operatorname{ord}(P\bmod p)\). Then
\[
 x((-n)P+\varepsilon T)=x(nP+\varepsilon T),
\]
so \(h_{p,\varepsilon}(-n)=h_{p,\varepsilon}(n)\). Any fixed index under \(n\mapsto-n\) would have \(2(nP+\varepsilon T)=O\); it is either the identity or a 2-torsion point. The identity has no finite \(x\)-coordinate, while the sole rational 2-torsion point \(T=(0,0)\) and any other 2-torsion points have \(y=0\), so they fail the adopted nonzero-square \(r(t)\) condition. Therefore qualifying indices have no fixed points under reflection and occur in distinct pairs. Hence
\[
 \boxed{\prod_{n=0}^{m_p-1}h_{p,\varepsilon}(n)=+1.}
\]
For any **finite** set of primes \(S\), if \(M\) is a common multiple of the orders \(m_p\), then
\[
 \boxed{\prod_{n=0}^{M-1}\prod_{p\in S}h_{p,\varepsilon}(n)=+1.}
\]
This exact finite-product cancellation does **not** prove cancellation for the full root-number sequence, since the set of relevant primes is unbounded as \(n\) varies. Interchanging the index and prime products is an additional, currently unjustified step.

## 12. Addendum: reported small-prime contributions at the counterexample indices

The subsequent analysis reported a sieve of qualifying primes **up to 100,000** on the \(P+T\) branch:

| Index | Reported qualifying primes \(p\le100000\) | Count | Truncated sign |
|---|---|---:|---:|
| \(4683\) | \(397,2969,18637\) | 3 | \(-1\) |
| \(4685\) | \(18637,93053\) | 2 | \(+1\) |

On those reported lists,
\[
 \mathcal Q_{4683,1}^{(\le100000)}\cap
 \mathcal Q_{4685,1}^{(\le100000)}=\{18637\},
\]
\[
 h_{\le100000,1}(4683)=-1,\qquad
 h_{\le100000,1}(4685)=+1,
\]
\[
 \boxed{h_{\le100000,1}(4683)h_{\le100000,1}(4685)=-1.}
\]
The shared prime contributes \((-1)^2=+1\) to the pair product; the other reported primes give the remaining negative factor.

**Evidence status:** these lists were asserted in the prior analysis, but no complete reproducible sieve output or independent verification accompanies them in the current dossier. They must be regarded as **reported, not certified**. The cutoff at 100,000 is essential: none of these truncated values is a claim about the full global root number, and the full specializations at indices 4683 and 4685 can have very large additional prime factors.

## 13. Questions for an independent referee

1. Recompute the integral gap-two resultant with a fully specified normalization, and certify all prime factors, including the large factor \(2325076196570957\).
2. Check all exceptional primes against the *exact* qualifying criteria and orbit membership, including the denominator locus. Confirm or refute the provisional assertion that only \(18637\) survives.
3. Verify the point arithmetic, order \(9368\), and the complete qualifying-index set for \(p=18637\) on **both** branches. The exact mean \(2341/2342\) requires the asserted complete set.
4. Independently reproduce the \(p\le100000\) sieve lists at \(n=4683,4685\); distinguish the finite-field qualifying-root test from actual bad-reduction/split-character computation on the integral elliptic-curve models.
5. Assess whether the finite-period product theorem can yield a nontrivial statement about **joint** sign correlations, rather than just the already-forced parity of the number of negative factors within each period.

**Summary for review:** The norm identity \(N(H(2+i))=2^5\cdot18637\) and the 2-torsion midpoint give a concrete algebraic explanation of the genuine periodic gap-two counterexample. The complete-period cancellation is an exact elementary consequence of reflection symmetry. The proposed full exceptional-prime classification and the small-prime sieve lists remain independently auditable claims, not new certified theorems in this document.
