# Response to the second review of the mirror rotation law (14 November 2026, paper revision 236)

Written by Claude (a language model): a record of questions and answers, not a referee's report. Paper: F.51 (rotation coding, consequences) and the new F.52 (the proof of the periodic part); code `code/verify_mirror_collapse.py`, `code/verify_rotation_coding.py` (full runs about 2 to 4 minutes, `--quick` seconds).

## The central objection, accepted
Revision 227 justified the periodicity of the 2- and 3-adic data "by compactness". That is not an argument: it needs local constancy of the data on the closure of ⟨P⟩, in particular near the factor 2B² + A of unbounded 3-adic valuation. Corrections-log entry 10. **F.52 now supplies:**
* **Lemma R** (the reciprocity identity): statement with all coprimality and parity hypotheses, hand proof by quadratic reciprocity; also checked against 596 direct Jacobi values.
* **Lemma L** (local periodicity): the data depend only on the coset nP + E_m, where E_m is the level-m kernel of reduction, because (1) reduction modulo p^m is a homomorphism on the non-singular locus of the minimal Weierstrass model (a smooth group scheme), so Q + Q′ ≡ Q for Q′ ∈ E_m; (2) p^mP ∈ E_m (levels of p^jP computed to j = 6 resp. 8; [3] raises the level by exactly one at 3; the formal group has additive reduction at 2); (3) for p ∤ B the data are functions of x mod p^K, and for p | B they depend only on min(k, 4) because A ≡ C² ≡ 1 (mod 8, resp. mod 3) from C² = A³ − 2A²B² + 2AB⁴. Hence the data at p are p⁸-periodic, and the finite computation over full cycles shows the actual periods 8 and 729 (joint 5832).
* **Lemma F** (the free factor): the unbounded valuation of 2B² + A is eliminated because the right-hand side of Lemma R does not change when its valuation (≥ 6, either parity) and leading digit are changed, in the 16 residue classes modulo 5832 where the valuation is ≥ 6 (computed, both signs, both sequences). Below the cutoff its valuation and digit are ordinary periodic data (a function of n mod 3⁶, checked).

## What is still cited rather than proved
The smooth-group-scheme congruence for the non-singular locus of a minimal Weierstrass model and the additivity of the formal-group reduction at 2 are standard facts that F.52 cites. The same compactness phrase occurs in Appendix B (the proof that ε_n of the original sequences is periodic); there the paper already lists the local-constancy step under "What remains", and Lemma L supplies the missing mechanism, but Appendix B has not been rewritten.

## Other points
3. **Normalization and the half-turn.** F.51 (a) now defines λ : C(ℝ) → ℝ/Ωℤ explicitly (λ(Q) = ±u(x(Q))), shows it is an isomorphism of the connected circle C(ℝ) (invariant differential, Abel's theorem), and that T, the unique point of order 2, goes to Ω/2 (directly λ(T) = u(0) = Ω/2).
4. **27-lag.** Stated as a limiting frequency (natural density), 2‖27θ‖ = 0.0332868…, distinguished from the finite-sample percentage 0.9667 observed for n ≤ 10⁶; since 3 | 27 the same applies to the full ε⁺.
5. **Fourfold product identity.** It is a consequence of F.25 (b) (ε(1 − x_n)ε(1 − 2/x_n) = (−1)ⁿ, proved there) and the identity ε(1 + x_n)ε(1 + 2/x_n) = −s_n s′_n, not an independent observation; the 148 values are a consistency test.
6. **Rank problem.** Unchanged: nothing here bears on Problem H or on ranks; the mirror sequences carry no section.

## Status of each statement (after revision 236)
| Statement | Status |
| --- | --- |
| real elliptic rotation, irrationality of θ | Proved (F.51 (a)) |
| algebraic threshold x₀ and the real-sign coding | Proved (F.51 (a)); numerical values of θ, ρ computed |
| reciprocity identity | Proved by hand (Lemma R), not refereed |
| local periodicity, periods 8 and 729, the free factor | Proved from two cited standard facts plus finite checks (Lemma L, Lemma F) |
| ε⁺_n = h(n)·s_n for all n | Certified: finite exact computation over n mod 5832 |
| non-periodicity, limiting mean, 27-lag frequency | Proved, given the identity |
| fourfold product identity | Proved, given the identity and F.25 (b) |
| anything about the parity of the prime-factor count | Open (Problem H and its mirror analogue) |
