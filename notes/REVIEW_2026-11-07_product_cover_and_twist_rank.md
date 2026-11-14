# Review: the product-cover construction and the rank of the twists E^{t(t−1)}, E^{t(t+1)}, E^{t²−1} (7 November 2026)

Reviewer: Claude (a language model). This is a check by recomputation, not a human referee's report. Scripts: `code/verify_twist_rank_over_F5.py` (5 seconds) and `code/verify_integral_resolution_note.py` (30 seconds per twist; set `TWIST_D` to choose the twist, default t(t−1)).

## Verdict

1. **The theorem in the pasted text is correct, and it is the result already in the paper as F.48** (revision 206): for fixed distinct rational a, b the normalized fibre product D_{a,b} has genus 2 or 3, so only finitely many rational t have rational points at both x = a and x = b. Nothing needs to be added to the paper for it.
2. **The endpoint named in the context, rank E^{t(t−1)}(ℚ(t)) = 0, is now established, and so are the two companion twists t(t+1) and t²−1.** Together they cover every pair (a, b) for which the third quotient of the biquadratic cover has genus 0. This closes one specific mechanism, not the product-cover method as a whole (section 4).

## 1. The pasted theorem

I verified each step: disc N_a = 4(64 + 16a² − a⁶) never vanishes for rational a (the sextic is negative for |a| ≤ 2 and positive for |a| ≥ 3, so it has no integer, hence no rational, root); N_a ≡ 8a − 16t modulo t² + 1, which cannot vanish at t = ±i; N_a and N_b cannot share both roots; the genus is r − 3 with r = 6 or 5 branch points. These are the same identities as in my earlier review of the note, now with a cleaner proof of the first step. Two remarks:

* **Notation clash.** The context calls "D_{0,2}" the third quadratic subcover v² = t(t−1) (genus 0, with infinitely many rational points), while the theorem calls D_{a,b} the full fibre product, which for (0, 2) has genus 2. The conic having infinitely many points does not contradict the theorem: a rational point of the conic is not a point of C_0 and C_2 above it. I suggest writing W_{a,b} for the third quotient u² = N_aN_b and D_{a,b} for the fibre product.
* **The rank identity.** Over K_{a,b} = ℚ(t)(√d_a, √d_b), with d_c = (1 + t²)N_c, rank E(K_{a,b}) = rank E(ℚ(t)) + rank E^{d_a}(ℚ(t)) + rank E^{d_b}(ℚ(t)) + rank E^{N_aN_b}(ℚ(t)) = 0 + 1 + 1 + rank E^{N_aN_b}(ℚ(t)) (the 1's from the sections P_a, P_b). The pasted identity for the quadratic field ℚ(t)(√(t(t−1))) is the last summand.

## 2. Three ways the construction can produce rank ≥ 2

| Mechanism | What it needs | Status |
| --- | --- | --- |
| (i) both points rational at the same t | a rational point of D_{a,b} | finite for each pair (F.48, Proved; Faltings is ineffective) |
| (ii) a second section on one cover's twist S^{d_c} | ρ(S^{d_c}) ≥ 14 | excluded over ℚ̄ for 18 values of c, conditionally (F.44–F.46); restricted ansatz excluded for every rational c (F.47) |
| (iii) a section of the twist by N_aN_b | infinitely many rational points on W_{a,b} : u² = N_aN_b and rank E^{N_aN_b}(ℚ(t)) ≥ 1 | **closed here for the pairs with genus-0 W_{a,b}**; open for the others |

W_{a,b} has genus 0 exactly when N_a and N_b share a root, that is F(a, b) = 0 (F.48). Among the rational solutions found these are the pairs {0, 2}, {0, −2}, {2, −2}, with W : w² = 256t(t−1), 256t(t+1), 256(t²−1). A further solution would be a rational t₀ with full rational 2-torsion; there are finitely many possible and none was found. For every other pair W_{a,b} is a genus-1 curve.

## 3. The new result and its proof

**Claim.** For d ∈ {t(t−1), t(t+1), t²−1}: rank E^d(ℚ̄(t)) = 0, hence rank E^d(ℚ(t)) = 0.

1. **The surface.** S^d : Y² = X³ + 4(1−t²)d²q³X − 16td³q⁵ with q = t²+1 has χ = 3 and fibres 2·I₀\* + 2·III\* + 6·I₁ over ℚ and over 𝔽₅ (the factors of Δ = 4096d⁶q⁹f are pairwise coprime over both fields and f is squarefree mod 5). Trivial lattice of rank 2 + 2·4 + 2·7 = 24; b₂ = 34, so the non-trivial part of H² has dimension 10.
2. **Smooth model.** The blowup construction of the previous note (seven blowups along centres finite étale over ℤ₍₅₎ for each III\* fibre, two for each I₀\* fibre) gives a smooth proper model over ℤ₍₅₎. The audit passes for all three twists: 108, 106 and 106 checks, none failing, covering every chart over ℚ and over 𝔽₅. Hence NS(S_ℚ̄) → NS(S_𝔽̄₅) is injective, with the same trivial lattice.
3. **Point counts.** N_k = Σ_{t ∈ ℙ¹(𝔽_{5^k})} a_t for k = 1, …, 6 (a C program), checked against an independent pure-Python implementation for k = 1, 2, 3. For t(t−1) and t(t+1): 2, 22, 140, −506, −2448, 8074; for t²−1: 0, −42, −540, 718, 11100, −5322.
4. **The polynomial.** The power sums p_k = −N_k give integer elementary symmetric functions, and N₆ fixes the sign of the functional equation (ε = +1), consistently: e₆ = 25·e₄ exactly. The characteristic polynomial of Frobenius on the 10-dimensional part is, for t(t−1) and t(t+1),
   x¹⁰ + 2x⁹ + 13x⁸ + 70x⁷ + 50x⁶ + 1250x⁴ + 43750x³ + 203125x² + 781250x + 9765625,
   and for t²−1,
   x¹⁰ − 21x⁸ − 180x⁷ + 400x⁶ + 6000x⁵ + 10000x⁴ − 112500x³ − 328125x² + 9765625.
   Both are irreducible over ℚ, all roots have modulus exactly 5 (the Weil bound, a strong check on the counts), and no root has the form 5ζ with ζ a root of unity. Also χ(5) ≠ 0, so the analytic rank over 𝔽₅(t) is 0, as the context states.
5. **Conclusion.** Tate's inequality (a theorem; no conjecture needed) gives ρ(S_𝔽̄₅) ≤ 24 + 0 = 24, so ρ = 24 and rank E^d(𝔽̄₅(t)) = 0. By step 2, ρ(S_ℚ̄) ≤ 24, hence rank E^d(ℚ̄(t)) = 0.
6. **The twist t(t+1)** is the image of t(t−1) under t ↦ −t followed by a twist by −1, trivial over ℚ̄; its counts over 𝔽₅ coincide, as expected, but its model was also audited separately.

**Dependencies.** The smooth model rests on my sympy audit (Magma was not used); the counts rest on the C program and the independent check. Tate's inequality and the injectivity of specialization are standard theorems. Nothing relies on the Tate conjecture.

## 4. What this does not give

* It does not touch Problem H.
* It closes mechanism (iii) only for the three pairs with a genus-0 third quotient. For all other pairs W_{a,b} has genus 1 and rank E^{N_aN_b}(ℚ(t)) is a separate question for each pair (the paper's scan of polynomial twists in §8 found no rank near 2, but that is an estimate).
* It excludes only a generic section, not isolated rank jumps at particular t.
* F.48 does not rule out using infinitely many different pairs (a, b), nor x-coordinates varying with t. So "the product-cover construction cannot help" is not established; what is established is that it fails for each fixed pair in the ways (i) and, for genus-0 pairs, (iii).

## 5. Paper text: inserted as F.49 in revision 221 (14 November 2026)

The paragraph below was inserted unchanged except for one added sentence, "Dependencies and limits" (sympy audit instead of Magma, the C program with its independent check, standard theorems only, generic sections only, no human referee). Before the insertion the three audits (`verify_integral_resolution_note.py` with TWIST_D = t*(t-1), t*(t+1), t**2-1: 108, 106, 106 passing checks, no failure; the one FINDING reported for t(t−1) is the discrepancy z³ − 128 versus z³ − 512 in the older proposed note, not in the audited model) and `verify_twist_rank_over_F5.py` (ALL CHECKS PASS) were rerun.

**F.49 Rank of the twists E^{t(t−1)}, E^{t(t+1)} and E^{t²−1} (Certified; Tate’s inequality and specialization of Néron–Severi groups are used).** In the biquadratic cover of two constant-x covers C_a and C_b the third quotient is W_{a,b} : u² = N_aN_b. It has genus 0 exactly when N_a and N_b share a root, which among the rational solutions found in F.48 happens for the pairs {0, 2}, {0, −2}, {2, −2}, with W : w² = 256t(t−1), 256t(t+1), 256(t²−1). At a rational point of W the curve E_t is isomorphic to its twist E_t^d with d = t(t−1), t(t+1), t²−1, so a section of E^d over ℚ(t) would give points on E_t for infinitely many t. We show that E^d has rank 0 over ℚ̄(t), hence over ℚ(t). The surface S^d : Y² = X³ + 4(1 − t²)d²q³X − 16td³q⁵ (q = t² + 1) has χ = 3 and fibres 2·I₀\* + 2·III\* + 6·I₁ over ℚ and over 𝔽₅ (the factors of Δ = 4096d⁶q⁹f are pairwise coprime over both fields and f is squarefree mod 5), a trivial lattice of rank 2 + 2·4 + 2·7 = 24, and b₂ = 34. Seven blowups along reduced centres that are finite étale over ℤ₍₅₎ for each III\* fibre, and two for each I₀\* fibre, give a smooth proper model over ℤ₍₅₎; every chart was checked over ℚ and over 𝔽₅ (code/verify_integral_resolution_note.py with TWIST_D = d), so NS(S_ℚ̄) → NS(S_𝔽̄₅) is injective with the same trivial lattice. Counting points over 𝔽_{5^k}, k = 1, …, 6, gives the characteristic polynomial of Frobenius on the 10-dimensional non-trivial part of H²: for d = t(t−1) and t(t+1) it is x¹⁰ + 2x⁹ + 13x⁸ + 70x⁷ + 50x⁶ + 1250x⁴ + 43750x³ + 203125x² + 781250x + 9765625, and for d = t² − 1 it is x¹⁰ − 21x⁸ − 180x⁷ + 400x⁶ + 6000x⁵ + 10000x⁴ − 112500x³ − 328125x² + 9765625. Both are irreducible over ℚ, have all roots of modulus 5, and have no root of the form 5ζ with ζ a root of unity. By Tate’s inequality ρ(S_𝔽̄₅) = 24, so rank E^d(𝔽̄₅(t)) = 0, and by specialization rank E^d(ℚ̄(t)) = 0; the twist t(t+1) is the image of t(t−1) under t ↦ −t followed by a twist by −1, trivial over ℚ̄. Hence a genus-0 third quotient supplies no generic section for these three pairs. This says nothing about pairs whose third quotient has genus 1, about isolated rank jumps, or about Problem H. Code: code/verify_twist_rank_over_F5.py and code/verify_integral_resolution_note.py.

## 6. Limits of this review

The pasted text contains interface debris (a name, a site name, "27s nachgedacht", "12 Websites durchsucht") from a chat session; its sources were not checked and nothing was taken from them. No human referee has checked any of this.
