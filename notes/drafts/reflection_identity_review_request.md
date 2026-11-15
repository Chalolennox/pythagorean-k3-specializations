<!-- Provenance: pasted into the chat by the repository owner on 15 November 2026 as an attachment (83c5defe-attachment.txt): an independent-review request on a reflection identity for the root numbers of E_t and E_u, u = (t+1)/(t-1).
     Reviewed in notes/REVIEW_2026-11-15_reflection_identity_note.md. The text below the line is unmodified. -->

---

# Independent Review Request: A Reflection Identity for Root Numbers of a Pythagorean Elliptic-Curve Family

## 1. Objective

We are investigating the family of elliptic curves over \(\mathbb Q\)

\[
E_t:\quad y^2=x^3+4A(t)x-8B(t),
\]

where

\[
A(t)=\frac{1-t^2}{1+t^2},
\qquad
B(t)=\frac{2t}{1+t^2},
\qquad t\in\mathbb Q.
\]

The original research question is whether infinitely many rational parameters \(t\) satisfy

\[
\operatorname{rank}E_t(\mathbb Q)\ge2.
\]

The present investigation concerns an auxiliary arithmetic problem: deriving a uniform formula for the product of global root numbers under the involution

\[
M(t)=\frac{t+1}{t-1}.
\]

This involution arises from translation by the rational 2-torsion point \(T=(0,0)\) on

\[
C:\quad y^2=x^3-2x^2+2x.
\]

For \(P=(1,1)\), writing \(t_n=1-x(nP)\), one has

\[
t(nP+T)=M(t_n).
\]

The immediate objective is to prove a root-number identity for **all nonexceptional rational \(t\)**, not merely for the orbit \(t_n\).

---

## 2. Discriminant and quadratic character

Write \(t=a/b\), where \(a,b\in\mathbb Z\), \(\gcd(a,b)=1\), \(b>0\). Define

\[
D(a,b)=a^2+b^2
\]

and

\[
H(a,b)=a^6-30a^4b^2-24a^2b^4-b^6.
\]

The elliptic curve has invariants

\[
c_4=-192\frac{b^2-a^2}{D},
\qquad
c_6=13824\frac{ab}{D},
\]

and

\[
\Delta=\frac{4096H(a,b)}{D^3}.
\]

For primes \(p\ge5\) dividing \(H(a,b)\), one obtains multiplicative reduction and the local root number

\[
W_p(E_t)
=
-\left(\frac{C(a,b)}p\right),
\]

where

\[
C(a,b)=-6ab(a^2+b^2).
\]

The proof uses \(p\nmid D\), \(v_p(c_4)=0\), and the standard multiplicative local-root-number formula

\[
W_p(E)=-\left(\frac{-c_6}{p}\right).
\]

Let

\[
R_t=\prod_{\substack{p\ge5\\p\mid H(a,b)}}p.
\]

Then the contribution from these multiplicative primes is

\[
(-1)^{\omega(R_t)}
\left(\frac{C(a,b)}{R_t}\right).
\]

**Reviewer task:** Verify the invariants and this local formula carefully, including exceptional primes, possible additive reduction, and the validity of the Jacobi symbols.

---

## 3. Denominator primes and reflection

The involution satisfies

\[
A(M(t))=-B(t),
\qquad
B(M(t))=-A(t).
\]

For \(u=M(t)\), the primitive numerator-denominator pair is obtained from \((a+b,a-b)\), after division by their gcd.

The corresponding sum of squares differs from \(D(a,b)\) by a power of \(2\). Therefore, for every odd prime \(p\),

\[
v_p(D_t)=v_p(D_u).
\]

For \(p\ge5\) dividing \(D_t\), the reduction is potentially good. If \(k=v_p(D_t)\), the proposed reduction-type pattern is

| \(k\bmod4\) | \(v_p(\Delta_{\min})\) | Kodaira type |
|---|---:|---|
| 0 | 0 | Good |
| 1 | 9 | III* |
| 2 | 6 | I₀* |
| 3 | 3 | III |

The proposed cancellation is

\[
W_p(E_t)W_p(E_u)=1
\qquad(p\ge5,\ p\mid D_t).
\]

This cancellation has a plausible local explanation, but the reviewer should independently verify it using the appropriate local-root-number classification, rather than treating the Kodaira type alone as sufficient proof.

---

## 4. Separate-character root-number formula

Define the exceptional local correction

\[
\ell(t)=
W_2(E_t)W_3(E_t)
W_2(E_u)W_3(E_u).
\]

Since both real-place root numbers equal \(-1\), their product is \(+1\).

The resulting proposed uniform formula is

\[
\boxed{
W(E_t)W(E_u)
=
\ell(t)
(-1)^{\omega(R_t)+\omega(R_u)}
\left(\frac{C_t}{R_t}\right)
\left(\frac{C_u}{R_u}\right).
}
\tag{1}
\]

Here \(C_t=C(a,b)\), and \(C_u\) is defined using primitive coordinates for \(u\).

**Status:** The multiplicative-prime contribution has a direct proof. The denominator-prime cancellation needs an independent local verification before (1) is accepted as a fully proved theorem.

---

## 5. Square-class identity under reflection

Define

\[
J(a,b)=2ab(a^2-b^2).
\]

For nondegenerate parameters, an exact algebraic identity gives

\[
\boxed{
[C_tC_u]=[J(a,b)]
\quad\text{in }\mathbb Q^\times/\mathbb Q^{\times2}.
}
\tag{2}
\]

This was checked exactly in Magma for eight specializations.

The stronger desired identity is

\[
\boxed{
\left(\frac{C_t}{R_t}\right)
\left(\frac{C_u}{R_u}\right)
=
\left(\frac{-J(a,b)}{R_tR_u}\right).
}
\tag{3}
\]

Equation (2) does **not** by itself imply (3), because the Jacobi symbols on the left have different moduli.

Assuming all relevant symbols are nonzero, the discrepancy between the two sides is

\[
\boxed{
\chi_{\mathrm{cross}}=
\left(\frac{-1}{R_tR_u}\right)
\left(\frac{C_t}{R_u}\right)
\left(\frac{C_u}{R_t}\right).
}
\tag{4}
\]

Thus (3) is equivalent to proving

\[
\boxed{\chi_{\mathrm{cross}}=1.}
\tag{5}
\]

This is the central unresolved algebraic question.

---

## 6. Computational evidence

The computations were performed in Magma V2.30-1.

For the eight orbit specializations \(n=2,\ldots,9\), the following were verified:

- The square-class identity (2) holds.
- The relevant Jacobi numerators are coprime to the tested moduli.
- The two discriminant prime supports are disjoint.
- The cross-character discrepancy (4) equals \(+1\).
- The residual correction between the global root-number product and the proposed single-character expression equals exactly the product of local root numbers at \(2\) and \(3\).

The observed data are:

| \(n\) | Global product | Combined character | Prime-count parity | Local correction |
|---:|:---:|:---:|:---:|:---:|
| 2 | −1 | −1 | −1 | −1 |
| 3 | +1 | +1 | −1 | −1 |
| 4 | +1 | +1 | +1 | +1 |
| 5 | +1 | +1 | −1 | −1 |
| 6 | −1 | +1 | −1 | +1 |
| 7 | +1 | −1 | −1 | +1 |
| 8 | +1 | +1 | +1 | +1 |
| 9 | +1 | +1 | −1 | −1 |

The complete local-factor comparison produced eight matches and zero mismatches.

These are exact computations on a finite sample, not a proof of the universal identity.

---

## 7. Possible shared bad primes

Define

\[
H(X)=X^6-30X^4-24X^2-1
\]

and

\[
G(X)=(X-1)^6H\left(\frac{X+1}{X-1}\right).
\]

A previous calculation reported

\[
G(X)=-2(27X^6-27X^4-32X^3-27X^2+27)
\]

and

\[
\operatorname{Res}(H,G)
=2^{17}\cdot7\cdot103\cdot519521^2.
\]

**Important:** These resultant and factorization values should be independently recomputed before use in a proof. They are currently reported algebraic claims, not independently certified in this review request.

If correct, they suggest that the overlap of the two multiplicative bad-prime supports is confined to a finite exceptional set.

The reviewer should also check the projective resultant argument, including roots at infinity and factors arising from primitive-coordinate normalization.

---

## 8. The desired theorem

We seek a rigorous proof, or a counterexample, to the following statement.

**Conjectured reflection formula.** For all rational \(t=a/b\) for which the expressions are defined, with \(u=(t+1)/(t-1)\),

\[
\boxed{
W(E_t)W(E_u)
=
\ell(t)
(-1)^{\omega(R_t)+\omega(R_u)}
\left(
\frac{-2ab(a^2-b^2)}{R_tR_u}
\right).
}
\tag{6}
\]

The statement may require exceptional-prime correction factors or restrictions on \(t\). We do not assume it is universally true.

A weaker theorem proving (6) under \(\gcd(R_t,R_u)=1\) would already be valuable.

---

## 9. Questions for the independent reviewer

**A. Can quadratic reciprocity prove the cross-character identity?**

Is there a uniform argument establishing

\[
\left(\frac{-1}{R_tR_u}\right)
\left(\frac{C_t}{R_u}\right)
\left(\frac{C_u}{R_t}\right)=1
\]

when the two discriminant supports are coprime?

In particular, can the fact that the moduli arise from the two sextic values \(H(a,b)\) and \(H(a+b,a-b)\) be exploited through reciprocity, resultants, or a norm identity?

**B. Is the single-character formula actually true?**

Please actively seek counterexamples outside the auxiliary elliptic-curve orbit. Eight successful orbit tests may reflect a special property of that orbit rather than a universal identity.

**C. Can the denominator-prime cancellation be proved uniformly?**

Verify the local reduction types and root numbers at every \(p\ge5\) dividing \(a^2+b^2\), including arbitrary valuations \(v_p(D)\).

**D. What happens at shared multiplicative bad primes?**

Determine whether the proposed single-character formula remains valid when \(R_t\) and \(R_u\) have a common prime divisor, or whether an explicit correction is necessary.

**E. Is there a stronger algebraic formulation?**

Could the cross-character identity be interpreted as a Hilbert-symbol reciprocity law, a norm-residue identity, or a relation in the Brauer group of \(\mathbb Q(t)\)?

Such a formulation would be preferable to proving the identity separately at each specialization.

**F. If the proposed theorem fails, what is the strongest correct replacement?**

Please identify the smallest explicit counterexample and formulate a corrected theorem with a complete proof.

---

## 10. Requested deliverable

Please provide an independent mathematical assessment with:

1. A verification or correction of the local root-number argument.
2. An exact verification of the reflection polynomial and resultant.
3. A proof or counterexample for the cross-character identity.
4. A treatment of exceptional and shared bad primes.
5. The strongest rigorously justified root-number product formula.
6. A recommendation on whether the resulting theorem has independent mathematical interest and whether it offers any genuine leverage on the original rank-\(\ge2\) infinitude question.

**Priority:** Prove or disprove the uniform reflection formula. Do not substitute additional numerical pattern searches for the missing reciprocity argument. A weaker correct theorem is preferable to a stronger conjectural one.
