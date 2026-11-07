# Review of "Finiteness of simultaneous constant-x specializations" (note of 7 November 2026)

Reviewer: Claude (a language model), 7 November 2026. This is a check by recomputation, not a human referee's report. Everything marked "verified" was recomputed by `code/verify_two_cover_note.py` (sympy, numpy, mpmath; 9 seconds).

## Verdict

The note is correct. Its theorem (for fixed distinct rational a, b only finitely many rational t have rational points at both x = a and x = b) follows from the branch-divisor argument and Faltings' theorem, and I found no gap. It is a clean and exact version of a remark that §6 of the paper already makes qualitatively ("a fibre product of two covers has genus ≥ 2 and finitely many rational points"). New relative to the paper: the exact genus (3, or 2 exactly when N_a and N_b share a moving root), the proof via branch divisors, and the identification of the genus-2 case with full rational 2-torsion. The note's scope statements are right: it says nothing about varying pairs (a, b), a second section on one cover, or x-coordinates that vary with t.

## Answers to the six questions of section 8 of the note

1. **Identities.** disc_t N_c = 4(64 + 16c² − c⁶), Res_t(N_c, 1+t²) = 64(c²+4) and Res_t(N_a, N_b) = 64(a−b)²F(a,b) are verified exactly.
2. **Branch description for every rational c.** Verified, including c = 0, ±2 (degree 3 with distinct roots, branch set {i, −i, 0 or 1 or −1, ∞}). The 2-adic argument for c⁶ − 16c² − 64 ≠ 0 is correct.
3. **Connectedness and distinct moving divisors.** The argument is complete. Two functions on ℙ¹ have the same square class over ℚ̄ exactly when their odd-valuation divisors (∞ included) coincide, because ℙ¹ has trivial class group. I confirmed that M_a·M_b with M_c = (1+t²)N_c is never a square class for distinct a, b among 60 rationals (1770 pairs, degree-drop cases included). The degree-drop cases have no hidden degeneracy: the moving divisors are {∞, 0}, {∞, 1}, {∞, −1}.
4. **Inertia of order two, genus 2 not 1.** Verified by a second method. The biquadratic cover has the three quotients C_a, C_b (genus 1 each) and u² = N_aN_b (genus 1, or genus 0 when a moving root is shared). So g = 1 + 1 + (1 or 0), which agrees with m − 3 on 190 pairs. All six ordered pairs from {0, 2, −2} have genus 2 (they share the root at ∞, and u² = N_aN_b is a conic).
5. **The exceptional equation F(a,b) = 0.** More can be said than the note claims (details below).
6. **Scope.** Correct as stated; nothing follows for rank ≥ 2 in the original family.

## Added when F.48 was written

* For the fifteen pairs among the six covers through t = −7 (§6 of the paper), F(a, b) ≠ 0 (checked exactly), so their fibre products have genus exactly 3. §6 now says "genus 3 (F.48)" instead of "genus ≥ 2".
* The paragraph F.48 was inserted with one sentence for this and is labelled Proved; the search results are stated there as Observed.

## What can be added about F(a,b) = 0

* **Finiteness.** A rational solution with a ≠ b gives the rational circle point (A, B) with x³ + 4Ax − 8B = (x−a)(x−b)(x+a+b) (exact). If A ≠ −1, then t₀ = B/(1+A) is rational and E_{t₀} has full rational 2-torsion, so (1+t₀²)f(t₀) is a square, a rational point of the genus-3 curve of the note. If A = −1, the roots are {−2, 0, 2}. So F = 0 has finitely many rational solutions: at most six ordered pairs per t₀ plus the six pairs at ∞. Faltings' theorem is ineffective, so the explicit list is not determined.
* **Search.** The only rational solutions with |numerator| ≤ 250 and denominator ≤ 80 are the six ordered pairs from {−2, 0, 2}. No finite t = u/v with |u| ≤ 600, v ≤ 300 lies on the genus-3 curve (Observed).
* **The "repeated roots" qualification is resolved.** F(a, a) = F(a, −2a) = 4(a⁶ + 9a⁴ − 16), and this polynomial has no rational root (it is a factor of Res_t(N_c, f) in F.47). Also f has no rational root, so Δ ≠ 0 at every rational t. Hence a rational solution of F = 0 with a ≠ b always has three distinct cubic roots.

## Small suggestions for the note

* In section 5, say where the finitely many exceptional t come from (the singular points of the fibre product and rational points that do not lift to the normalization).
* In section 4, use the third quotient u² = N_aN_b as the explanation of "3 or 2"; it is a second proof of the genus.
* In section 7, item 4 can be sharpened: genus 2 occurs exactly when F(a, b) = 0, and over ℚ that is only the finitely many pairs coming from rational t₀ with full 2-torsion.

## Text inserted into the paper as paragraph F.48 (revision 206)

**F.48 The fibre product of two constant-x covers (Proved; Faltings’ theorem is ineffective).** For c ∈ ℚ the cover C_c : w² = (1 + t²)N_c(t) has the four branch points ±i and the two roots of N_c (for c = 0, ±2 the second root is t = ∞). They are distinct because disc_t N_c = −4(c⁶ − 16c² − 64) and Res_t(N_c, 1 + t²) = 64(c² + 4) have no rational root, so C_c has genus one for every rational c. For distinct rational a, b the branch divisors differ (N_a and N_b are not proportional: both have t-coefficient −16, and equality forces a = b; the degree-drop cases have moving divisors {∞, 0}, {∞, 1}, {∞, −1}), so the two quadratic extensions generate a biquadratic extension and the normalized fibre product D_{a,b} is geometrically connected. Riemann–Hurwitz gives g(D_{a,b}) = m − 3 with m = 6 or 5 branch points; equivalently g(D_{a,b}) = g(C_a) + g(C_b) + g(u² = N_aN_b) = 1 + 1 + (1 or 0). The genus is 2 exactly when N_a and N_b have a common moving root, that is, when Res_t(N_a, N_b) = 64(a − b)²F(a, b) vanishes, with F(a, b) = a²b²(a + b)² + 4((a² + ab + b²)² − 16). In that case the circle point (A, B) = (−(a² + ab + b²)/4, −ab(a + b)/8) has x³ + 4Ax − 8B = (x − a)(x − b)(x + a + b), so t₀ = B/(1 + A) (or t₀ = ∞) is a rational parameter with full rational 2-torsion; there are finitely many of these (they lie on the genus-3 curve z² = (1 + t²)f(t)), and the repeated-root cases give 4(a⁶ + 9a⁴ − 16), which has no rational root. Hence for every pair of distinct rational a, b only finitely many rational t have rational points at both x = a and x = b. This says nothing about pairs (a, b) that vary, about a second section on one cover, or about x-coordinates that vary with t. In a search with |numerator| ≤ 250 and denominator ≤ 80 the only rational solutions of F(a, b) = 0 with a ≠ b are the six ordered pairs from {−2, 0, 2}, which come from t = ∞, and no finite t = u/v with |u| ≤ 600, v ≤ 300 lies on the genus-3 curve (Observed). Code: code/verify_two_cover_note.py.

## Limits of this review

The theorem's proof is verified line by line and its identities exactly. The genus count and the square-class statement were tested on sampled pairs (the arguments themselves are proofs, so the sampling is a sanity check). The note's source and the model that wrote it are not stated in the file. No human referee has checked it.
