# Which primes can divide F_n: the ψ-form and the rank-of-apparition pattern

Written by Claude (a language model); not refereed by a human. Code: `code/apparition_pattern.py` (full run about 10 s, `--quick` 2 s; needs numpy and sympy).

## Setting
C : y² = x³ − 2x² + 2x, P = (1,1), T = (0,0), ψ_n = ψ_n(P) the elliptic divisibility sequence (1, 2, 3, −20, −187, −1722, 10951, …); t_n = 1 − x(nP) = u_n/v_n in lowest terms.
H(t) = t⁶ − 30t⁴ − 24t² − 1, Φ(X,Y) = X⁶ − 30X⁴Y² − 24X²Y⁴ − Y⁶ = Y⁶·H(X/Y).

## The ψ-form (exact; checked for 2 ≤ n ≤ 120 against exact integers)
u_n = ψ_{n−1}ψ_{n+1}, v_n = ψ_n² (this is x(nP) − 1 = −ψ_{n−1}ψ_{n+1}/ψ_n²), d_n = 1 for n ≥ 2 (u_n and v_n are never both odd), so

    F_n = 4a³ + 27b²c = −4·Φ(ψ_{n−1}ψ_{n+1}, ψ_n²) = −4·∏_{τ : H(τ)=0} (ψ_{n−1}ψ_{n+1} − τψ_n²).

Normalisation: this is −4 times the sextic value that Appendix B of the paper calls F_n. v₂(F_n) = 2, v₃(F_n) = 0, so |F_n|/4 is the part prime to 6.

## Theorem (apparition). Proved; the proof is the one line below.
Let p ≥ 5 be a prime (C has good reduction at p), r = r_p the order of P̄ in C(𝔽_p), and
Z_p = { Q ∈ C(𝔽_p) \ {O} : H(1 − x(Q)) = 0 }, the 𝔽_p-rational points among the twelve points over the roots of H, and N_p = { n mod r : nP̄ ∈ Z_p }.
Then for every n ≥ 2:  p | F_n  ⇔  n mod r ∈ N_p.

*Proof.* Φ(u,v) ≡ u⁶ ≢ 0 (mod p) if p | v, because gcd(u,v) = 1; so p | F_n forces p ∤ v_n = ψ_n², i.e. nP̄ ≠ O, and then x(nP̄) = 1 − ū/v̄ ∈ 𝔽_p and Φ(u,v) = v⁶H(ū/v̄)-congruent to 0 exactly when H(1 − x(nP̄)) = 0, i.e. when nP̄ ∈ Z_p. Conversely nP̄ ∈ Z_p excludes nP̄ = O, so v is a unit and the same computation gives p | F_n. □

(The paper already states this equivalence in the paragraph "Structure available to a solver" (Appendix D area, line "A prime p ≥ 5 divides F(t(R)) exactly when …") and in "The twelve points"; what follows makes it explicit and checks it.)

## Corollaries (proved from the Theorem)
1. **Periodicity.** Whether p divides F_n depends only on n mod r_p.
2. **Symmetry.** Q ∈ Z_p ⇒ −Q ∈ Z_p (same x), so N_p = −N_p.
3. **Excluded classes.** O ∉ Z_p; the 2-torsion points have x ∈ {0, 1 ± i}, giving H(1) = −54 and H(∓i) = −8, nonzero mod p ≥ 5; x(±P) = 1 gives H(0) = −1. Hence N_p contains none of the classes 0, ±1, r/2, N_p has even cardinality, and, since p | ψ_m ⇔ r_p | m,
   **p | F_n ⇒ p ∤ ψ_{n−1}ψ_nψ_{n+1}ψ_{2n}.**
4. **At most twelve classes.** |N_p| = |Z_p ∩ ⟨P̄⟩| ≤ |Z_p| ≤ 12. So a prime divides F_n for at most 12 of the r_p ≈ p residue classes of n: density ≤ 12/r_p.
5. **The translate (F.25).** p | G_n (the sextic along nP + T) iff nP̄ ∈ Z_p + T, so a common prime of F_n and G_n needs Z_p ∩ (Z_p + T) ∩ ⟨P̄⟩ ≠ ∅. Res_t(H, 27t⁶ − 27t⁴ − 32t³ − 27t² + 27) = 2¹¹·7·103·519521², so only p ∈ {7, 103, 519521} are possible; at 7 and 103 no 𝔽_p-point lies in both sets, and at 519521 the two common x-coordinates (37492, 384583) are not x(nP) for any n (order of P is 698). This is F.25 in this language.
6. **Exponents.** For p | F_n the exponent is governed by the p-adic centre of the class (F.15, F.22 remark, "p-adic structure" paragraph); not re-derived here.

## Computed (all with `code/apparition_pattern.py`)
* The Theorem on exact F_n: all n ∈ [2,120] and all primes 5 ≤ p < 6000 (92,939 prime–index pairs): 0 disagreements.
* Corollaries 2–4 for every prime p < 30000 with N_p nonempty: 0 violations.
* 358 of the 3243 primes 5 ≤ p < 30000 divide some F_n (the paper's count; 11%). |N_p| = 2 for 230 of them, 4 for 119, 6 for 2, 8 for 7.
* Primes below 200 that ever divide some F_n: p = 23 (r = 10, N_p = {2, 8}), 83 (r = 39, {12, 16, 23, 27}), 149 (r = 84, {16, 68}), 197 (r = 92, {33, 59}).
* The summed densities Σ_{p<y} |N_p|/r_p (the expected number of distinct such primes below y dividing a "random" F_n): 0.30 (y = 100), 0.51 (10³), 0.81 (10⁴), 0.94 (3·10⁴); for comparison Σ_{5≤p<3·10⁴} 1/p = 1.76. So the explicit small primes carry noticeably less than a generic integer would, and nearly all of F_n's size sits in a large unfactored part.

## What this does not give
The pattern says which primes can divide F_n and in which classes; it says nothing about the *number* of prime factors of F_n, whose parity is Problem H. Each prime contributes a completely explicit class structure, but the parity of Ω(|F_n|/4) depends on the large prime factors, which this does not see (the "rough part" of F.15 and the parity barrier of F.24).
