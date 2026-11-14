# Review of "Paired root numbers under a torsion involution" (draft of 14 Nov 2026)

Source text: `drafts/paired_root_numbers_independent_review.md` (verbatim). Checks: `code/verify_paired_root_numbers_note.py` (19 checks, all pass; sympy-free).
Status of everything below: **Computed / Proved by hand from the paper's own theorems. No human has checked this.**

## Verdict
The note is a restatement, in new notation, of F.25, F.26 and F.28 of the paper, plus one genuinely open item of its own (the factor at primes p | c). That item is now closed. Three details need correcting. Nothing here approaches Problem H.

## Dictionary to the paper
| Draft | Paper |
|---|---|
| R(t) = −(1+t)/(1−t) = (t+1)/(t−1), (A,B) → (−B,−A) | t(nP) → t(nP+T), x → 2/x (F.25, F.26); the same map as F.25's (t+1)/(t−1), checked for n = 1..11 |
| z = t + R(t) = (t²+1)/(t−1) | z = 2 − u, u = x + 2/x, the quotient coordinate of F.26 (checked) |
| P(z) | −R(2−z)/2 with R the quotient sextic of F.26 (checked); disc P = 2¹⁰·3¹⁸·23²·519521² = 56642762775035360714056704 (the draft's value), a perfect square |
| J(t) | numerator of D(R(t)): (1−t)⁶H(R(t)) = −2J(t) (checked); the paper's G₂ = −2J up to homogenisation, which is why the paper's resultant has 2¹⁷ and the draft's 2¹¹ |
| Res(H,J) = 2¹¹·7·103·519521² | F.25 (same primes, same square) |
| §2 multiplicative formula | F.28 (theorem, proved) |

## Answers to the draft's questions
1. **Multiplicative primes p ≥ 5, p ∤ c (Q1).** This is F.28: p | F gives p ∤ c, p ∤ c₄, type I_e, split iff (−c₆/p) = 1, and the proved square identity of F.8 turns that into (ab/p) = 1. For G the same holds because the primitive triple of R(t) is (−b, −a, c) (checked on 1958 pairs), so a′b′ = ab exactly and F(R(t)) = G = −4b³+27a²c (checked).
2. **Primes p ≥ 5 dividing c (Q2, the draft's priority). The factor C_c(t) is 1.** By the paper's Appendix B (Rizzo's Table I), for every p ≥ 5 dividing c, w_p(E_t) = (2/p)^{v_p(c)}; the "additive potentially good" cases are exactly the types good, III*, I₀*, III treated there, and no residual character remains. The primitive triple of R(t) has the same hypotenuse c, so v_p(c) is the same for t and R(t) and the product is (2/p)^{2v_p(c)} = 1. The same reason shows the Jacobi symbol (2/c) cancels in the pair. Checked: c(R(t)) = c(t) for all 1958 coprime (u,v) with |u|,|v| ≤ 40; 1956 of them have a prime ≥ 5 dividing c. The paper's formula reproduces the draft's twelve Magma signs for n ≤ 6 (several of those t have 5 | c).
3. **Quotient identity and genus 2 (Q3).** Δ(E_t)Δ(E_{R(t)}) = −2²²·P(z)/z⁶ checked at 300 rational t (the draft's constant is right). P is squarefree (disc ≠ 0), so y² = −P(z) has genus 2 and Faltings gives finitely many rational z with Δ·Δ′ a square. Excluded points: z = 0 is t² + 1 = 0 (not rational); t = 1 has R(t) = ∞ and z = ∞. This bounds only the discriminant square class of the *displayed* models; it says nothing about root numbers. It is not stated in F.26, so it could be added there as a single sentence.
4. **Resultant versus primitive F, G (Q4).** F.25 proves it: a prime ≥ 5 dividing both primitive F and G divides Res(H,J) (coprime (u,v)), p = 2 is excluded (F odd), and p | c is excluded (F ≡ 4a³). On the 1958 sample the common primes ≥ 5 are 7 and 103 only (519521 needs far larger t); along the orbit there are none at all (F.25).
5. **Role of [−P(z)] in the local formula (Q5).** None. It is the square class of the discriminant product only; F.19 excludes any square-class identity between the two sequences.
6. **Novelty (Q6).** Not new. The local formula for p ∤ 6c is the standard multiplicative one; the decomposition below is F.25(b), which F.25 states "assuming F.24" and which is now unconditional because F.28 made the exact formula a theorem.

## The decomposition, stated for every t (proved, from F.28 plus c(R(t)) = c(t))
K(t) = W(E_t)W(E_{R(t)}) = C₂(t)·C₃(t)·∏_{p ≥ 5, p | F xor p | G} [−(ab/p)], where C₂ = w₂(E_t)w₂(E_{R(t)}), C₃ likewise. Verified identically against the closed formula on all 1958 pairs.
Explicit 2- and 3-adic parts (computed from the paper's tables; A = a/c, B = b/c as residues):
- C₂ = −1 exactly for (A,B) mod 16 in {(0,15),(1,0),(4,9),(7,4),(7,12),(9,4),(12,7),(12,9)};
- C₃ = −1 exactly for (A,B) mod 9 in {(1,6),(3,8)} (the class (3,8) is the paper's bad class for t, and (1,6) is its mirror).
Both depend only on (A,B) mod 144, so they are periodic along the orbit.

## Corrections to the draft
- Δ(E_t) = **−1024·F/c³** (= 4096·H(t)/(1+t²)³), not −4096·F/c³: from Δ = −16(4(4A)³ + 27(8B)²). The square class is unchanged and the product formula −2²²P/z⁶ is right.
- §6: the recurrence cannot start at n = 1 (t₁ = 0 divides); the draft already supplies t₂ = 3/4. Checked from n = 2 to 11, and t(nP+T) = R(t(nP)).
- §6, rows n = 7, 8: I did not reproduce them (F₇ has about 55 digits and F₈ about 70, beyond the trial division and Pollard rho I used). Rows n ≤ 6 are reproduced by `code/root_number_formula.py`.

## Recommendation
Do not add a new section. Add to F.25(b) one sentence: "the factor at p | c cancels because the primitive triple of t′ is (−b, −a, c), so w_p(E_t)w_p(E_{t′}) = (2/p)^{2v_p(c)} = 1; with F.28 the statement is unconditional", and to F.26(e) one sentence on the genus-2 curve y² = −R(2−z)/2.
