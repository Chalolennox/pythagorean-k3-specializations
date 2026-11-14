<!-- Provenance: uploaded to the chat by the repository owner on 14 November 2026 as global_sign_natural_boundary_review.md. Reviewed in notes/REVIEW_2026-11-14_global_sign_natural_boundary_note.md.
     The text below the line is unmodified. -->

---

# Global-sign generating functions and the reappearance of the unit circle

## A note for independent mathematical review

**Status:** Conditional analytic consequence; no proof of Problem H.

### Setting

Let \(W_n\in\{-1,+1\}\) denote the global signs associated with the chosen elliptic orbit, and let \(\varepsilon_n\in\{-1,+1\}\) be a known periodic comparison sequence of period \(r\). Define the correction coefficients and generating function

\[
 d_n=W_n-\varepsilon_n\in\{-2,0,2\},\qquad
 D(z)=\sum_{n\ge 1}d_nz^n.
\]

For real \(s>0\), the corresponding discrete Laplace transform is \(D(e^{-s})\). The series converges absolutely on \(|z|<1\).

### Proposition

**Proposition.** The following are equivalent:

1. \(W_n\) is not eventually periodic.
2. \(D(z)\) is not a rational function.
3. The unit circle \(|z|=1\) is a natural boundary for \(D(z)\).

Here, a *natural boundary* means that the analytic function on \(|z|<1\) cannot be analytically continued through any point of the unit circle.

### Proof

The generating function of the periodic sequence \(\varepsilon_n\) is rational. Hence \(D(z)\) is rational if and only if \(\sum_{n\ge1}W_nz^n\) is rational.

A rational generating function whose coefficients belong to a finite set is eventually periodic. One proof uses the constant-coefficient linear recurrence satisfied by the coefficients beyond the numerator's degree: the recurrence's state is a fixed-length tuple of coefficients, and only finitely many such tuples exist. Deterministic recurrence evolution therefore eventually repeats. Conversely, an eventually periodic sequence has a rational generating function, obtained by summing geometric series. This proves (1) \(\Longleftrightarrow\) (2).

If \(D(z)\) is not rational, its bounded integer coefficients cannot be eventually zero, so infinitely many coefficients are nonzero. Since the nonzero coefficients have absolute value 2, the radius of convergence is exactly 1. The **Pólya–Carlson theorem** states that a power series with integer coefficients and radius of convergence 1 is either rational or has the unit circle as a natural boundary. Thus (2) implies (3). A rational function cannot have the entire unit circle as a natural boundary, proving the converse.

### Relation to Problem H

If Problem H asks whether \(W_n=+1\) infinitely often, then any proof of non-eventual-periodicity of \(W_n\) would solve it: a sequence that is eventually \(-1\) is eventually periodic. However, non-eventual-periodicity is **strictly stronger** than Problem H. For example, \(W_n=(-1)^n\) has infinitely many positive signs but a rational generating function.

The theorem therefore classifies the analytic consequences of a hypothetical arithmetic nonperiodicity result; it does **not** establish nonperiodicity for the elliptic-orbit signs.

### Eventual negativity and the Laplace transform

If \(W_n=-1\) for every \(n\ge N_0\), then \(D(z)\) is rational, with an eventually periodic tail

\[
 D(z)=P(z)+z^{N_0}\frac{\sum_{j=0}^{r-1}(-1-\varepsilon_{N_0+j})z^j}{1-z^r},
\]

where \(P\) is a polynomial encoding the preceding coefficients. Thus eventual negativity rules out a natural boundary. Conversely, a natural boundary rules out eventual negativity, but it also rules out *every* eventually periodic sign pattern.

### Why a circle appears

The original Pythagorean specialization is parameterized by rational points of the geometric circle \(A^2+B^2=1\). The unit circle \(|z|=1\) in the present theorem is a **different object**: it is the boundary of the disk of convergence of a complex generating function. Its radius equals 1 because the correction coefficients are bounded integers and infinitely many are nonzero in the nonperiodic case. The recurrence of the circle is mathematically suggestive, but **no geometric or arithmetic connection between these two circles has been established**.

### Limitations and questions for review

- The equivalence above is a general theorem about bounded integer sequences and a periodic comparison sequence; it uses no special property of the elliptic curve.
- No conclusion about natural boundaries can be inferred from finitely many computed signs: every finite prefix extends both to an eventually constant sequence and to a non-eventually-periodic one.
- Known algebraic results on elliptic orbits and squarefree parts do not, by themselves, determine the parity of the number of qualifying prime factors.
- The central missing arithmetic step is to prove either that \(W_n=+1\) infinitely often (the weaker target) or that \(W_n\) is not eventually periodic (the stronger target).

**Review request:** Check the proposition and proof, identify whether any existing theorem about arithmetic functions along elliptic orbits supplies the missing nonperiodicity hypothesis, and assess whether this analytic reformulation offers more than a change of language.

### Classical references to verify

- G. Pólya, *Über gewisse notwendige Determinantenkriterien für die Fortsetzbarkeit einer Potenzreihe* (1921), and F. Carlson's related work on the rational-or-natural-boundary dichotomy.
- Standard treatments of rational generating functions and linear recurrence sequences (e.g., R. P. Stanley, *Enumerative Combinatorics*, vol. 1).

These references identify the relevant classical results; bibliographic details should be checked before formal citation in a paper.
