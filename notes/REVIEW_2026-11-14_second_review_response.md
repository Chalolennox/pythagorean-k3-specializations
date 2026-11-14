# Response to the second review of the mirror rotation law (paper revision 249)

Written by Claude (a language model): a record of questions and answers, not a referee's report. The review itself is stored verbatim in `notes/drafts/second_review_mirror_rotation_law_rev227.md`.
Paper: F.51 (rotation coding, consequences), F.52 (proof of the periodic part along the mirror sequences) and F.53 (the same method for the original sequences); Appendix B rewritten where it used compactness.
Code: `code/verify_mirror_collapse.py`, `code/verify_rotation_coding.py`, `code/verify_orbit_laws.py` (full runs 2 to 4 minutes, `--quick` seconds).

## The central objection, accepted
Revision 227 justified the periodicity of the 2- and 3-adic data "by compactness". That is not an argument: it needs local constancy of the data on the closure of ⟨P⟩, in particular near the factor 2B² + A of unbounded 3-adic valuation. Corrections-log entry 10. F.52 now supplies:
* **Lemma R** (reciprocity identity): statement with all coprimality and parity hypotheses, hand proof by quadratic reciprocity; also checked against 596 direct Jacobi values.
* **Lemma L** (local periodicity): the data depend only on the coset nP + E_m (E_m the level-m kernel of reduction): (1) reduction modulo p^m is a homomorphism on the non-singular locus of the minimal Weierstrass model (a smooth group scheme), so Q + Q′ ≡ Q for Q′ in E_m; (2) p^mP has depth exactly m, which is F.22 (v_p(D_n) = v_p(n), hand proof; also computed for 3^j, j ≤ 6, and 2^j, j ≤ 8); (3) for p ∤ B the data are functions of x mod p^K, and for p | B they depend only on min(k, 4), because A ≡ C² ≡ 1 (mod 8, resp. mod 3) from C² = A³ − 2A²B² + 2AB⁴. Hence the data at p are p⁸-periodic, and the finite computation over full cycles shows the actual periods 8 and 729 (joint 5832).
* **Lemma F** (the free factor): the unbounded valuation of 2B² + A is eliminated because the formula does not change when its valuation (≥ 6, either parity) and leading digit are changed, in the 16 residue classes mod 5832 where the valuation is ≥ 6 (computed, both signs, both sequences). Below the cutoff its valuation and digit are ordinary periodic data (a function of n mod 3⁶, checked).

## Appendix B (the second omission, now done)
The same compactness phrase was in Appendix B. The Theorem of Appendix B (period six along nP, Lemmas A–E) and F.21 (period three along nP + T) are hand proofs and stand, but the older "reduction to local statements" in Appendix B argued periodicity by compactness and by the periods of t_n modulo 8 and 9 alone, which does not determine ε_n, and listed two local statements as "not yet written out"; F.21 (6) rests partly on random-point checks. What was done:
* **F.53** proves both laws (ε(t_n) = +1 iff n ≡ 0, 1, 5 mod 6; ε(t′_n) = +1 iff 3 | n; f(t_n) = +1; f(t′_n) of exact period 18) for all n ≥ 2 by Lemma R, Lemma L and a finite verification over all four real-sign classes. The real signs are not constant on these sequences (they depend on x_n relative to 1, 2, 1 + t₀), so G is evaluated on every real class; the factor vanishing at x = 1 is "high" at 2 as well as at 3 and the formula is independent of its data at both primes (373248 pairs of n and real class, 0 failures). Along nP + T Lemma L still applies because the data are functions of x(nP).
* Appendix B paragraphs rewritten: the compactness sentences, the incomplete step (5), the "What remains" sentence, "has not been carried out" and "not yet written out" are replaced by pointers to the Theorem, F.21, F.22 and F.53; the numerical experiment on 3765 points is kept but marked as not used. Corrections-log entry 11.
* Not changed: the splitting of ε into Ψ₂ and Ψ₃ (Appendix B, "Splitting ε by place") remains observed; F.53 proves the product law without it.

## Other points
3. **Normalization and the half-turn.** F.51 (a) defines λ : C(ℝ) → ℝ/Ωℤ explicitly (λ(Q) = ±u(x(Q))), shows it is an isomorphism of the connected circle C(ℝ), and that T, the unique point of order 2, goes to Ω/2 (directly λ(T) = u(0) = Ω/2).
4. **27-lag.** Stated as a limiting frequency (natural density), 2‖27θ‖ = 0.0332868…, distinguished from the finite-sample percentage 0.9667 observed for n ≤ 10⁶; since 3 | 27 the same applies to the full ε⁺.
5. **Fourfold product identity.** A consequence of F.25 (b) (ε(1 − x_n)ε(1 − 2/x_n) = (−1)ⁿ, proved there) and ε(1 + x_n)ε(1 + 2/x_n) = −s_n s′_n; the 148 values are a consistency test, not an independent observation.
6. **Rank problem.** Unchanged: nothing here bears on Problem H or on ranks; the mirror sequences carry no section.

## What is still cited rather than proved
The smooth-group-scheme congruence for the non-singular locus of a minimal Weierstrass model (the identity component of the Néron model) is a standard fact that F.52 cites; everything else in Lemma L is elementary, F.22, or computed. Lemma R is a hand proof that no human has checked. The formula of §4 for W and f is used as given.

## Status of each statement (after revision 249)
| Statement | Status |
| --- | --- |
| real elliptic rotation, irrationality of θ | Proved (F.51 (a)) |
| algebraic threshold x₀ and the real-sign coding | Proved (F.51 (a)); numerical values of θ, ρ computed |
| reciprocity identity | Proved by hand (Lemma R), not refereed |
| local periodicity, periods 8 and 729, the free factor | Proved from one cited standard fact, F.22 and finite checks (Lemma L, Lemma F) |
| ε⁺_n = h(n)·s_n for all n | Certified: finite exact computation over n mod 5832 |
| non-periodicity, limiting mean, 27-lag frequency | Proved, given the identity |
| fourfold product identity | Proved, given the identity and F.25 (b) |
| period laws along nP and nP + T (original sequences) | Proved (Theorem of Appendix B, F.21) and, independently, Certified by the uniform method of F.53 |
| anything about the parity of the prime-factor count | Open (Problem H and its mirror analogue) |
