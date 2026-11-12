# tau_image: the 2-adic image of the Kummer representation of a point, and the density of odd-order reductions

Python implementation (replacing the Magma computations of Liang–Rouse, arXiv 1810.10583) for E : y² = x³ + ax² + bx with rational 2-torsion point T = (0,0) and α = (c, ck), b = ck² − ac − c².
Our curve C : y² = x³ − 2x² + 2x with P = (1,1) is [a,c,k] = [−2,1,1]. Written by Claude (a language model); no human referee.

| file | purpose |
| --- | --- |
| `density.py` | density of primes with odd-order reduction from a subgroup of AGL₂(ℤ/2^r) (Liang–Rouse §5, Lemmas 6–10), exact fractions |
| `image.py` | numerical coset criterion (mpmath, 100 digits), group arithmetic, maximal subgroups |
| `descend.py` | level 8: descent from Γ₀^⊙(2); prints image order, density, class densities |
| `levels.py` | levels 8 → 16 → 32 (…) in one fixed frame, with the stability criterion; `python3 levels.py a c k [kmax]` |
| `validate.py` | density formula on rows 1–17 of Liang–Rouse Table 1 + the whole pipeline on four of their curves (about 2 min) |
| `test_density.py` | rows 1–17 only |
| `fullpre_test.py`, `fullpre_test32.py` | data check: computed image versus the full preimage of the level below, class densities mod 16 / mod 32 against `data/odd_order_classes_C_P_1e8.txt` |
| `image_densities.py` | Chebotarev densities of the draft 'Chebotarev density calculation for C' read off the computed images: density 1/8, Theorem B as a finite statement, valuation laws, Pr(P in 2^j C), odd-order laws, matrix/translation split |
| `stability_mod64.py` | tests whether the image above level 32 is the full preimage of I_32: predicts the odd-order fractions mod 64 and compares with the 10^8 prime data. Result: it is not (classes p = +-1 mod 32 split; up to 128 sigma). About 10 s for classes 1, 31 |
| `check_ours.py` | rebuilds our images mod 8, 16, 32 from `image_generators_-2_1_1.json` and recomputes the densities (about 1 min) |
| `verify_identity.py` | confirms that the computed images belong to exactly C : y² = x³ − 2x² + 2x, P = (1,1): parameter map, numerical objects, an independent naive recount of the odd-order primes, frame independence (about 3 min) |
| `save_generators.py` | stores an image as a small generating set |

## Method in one paragraph

Elements of AGL₂(ℤ/2^k) are maps x ↦ (e,f) + xM on row vectors (σ(A) = aA + bB, σ(B) = cA + dB, σ(β_k) = β_k + eA + fB). The basis has 2^(k−1)B = T, so the image lies in Γ₀^⊙(2) (c even).
For a subgroup H, the left-coset sums ζ_{gH} = Σ_{h∈H} Y^{g∘h}, Y = x(β_k+A)·x(β_k+B)²·x(β_k+A+B)³, are algebraic integers, and some ζ_{gH} is an integer exactly when H contains a conjugate of the image (Dokchitser–Dokchitser, as used by Liang–Rouse).
Descending through maximal (index 2) subgroups finds the image. From level k to k+1 only maximal subgroups of the full preimage that do not contain the kernel need testing, with g over lifts of the normaliser.
If the image at level k+1 is the full preimage of the level-k image (k ≥ 3), it is stable at all higher levels (Frattini argument of Liang–Rouse, Theorem 4).

## Two pitfalls found while validating (both give false results silently)

1. Y built from β₂ = 2^(k−2)β_k instead of β_k: the coset sums acquire denominators (e.g. 3) and are not algebraic integers.
2. The exponents (1,1,2) of the published Y make Y symmetric under A ↔ B (Y^{g∘z} = Y^g, z = [[0,1],[1,0]]); the criterion then tests ⟨H, z⟩ and gives false positives (e.g. for M_{a²−4b}). Distinct exponents (1,2,3) make Y injective on AGL₂(ℤ/8) (checked: 98 304 distinct values).

## Validation (all exact)

* Density formula: rows 1–17 of Liang–Rouse Table 1 reproduced exactly (5/21, 10/21, 5123/21504, 83/336, 13/42, 1/7, …).
* Whole pipeline: [3,3,1] → 5/21, [−3,1,3] → 10/21, [2,3,1] → 83/336, [2,−5,1] → 1/7 (their Table 1).
* The numerical criterion at levels 16 and 32 has not been validated against a published curve; for our curve it is validated by the class densities of the data (see `notes/odd_order_density_check.md`).

## Results for [−2,1,1]

| level | image order | full preimage | density assuming the full preimage above |
| --- | --- | --- | --- |
| 8 | 2⁸ | – | 95/224 = 0.424107 |
| 16 | 2¹³ | 2¹⁴ | 1521/3584 = 0.424386 |
| 32 | 2¹⁸ | 2¹⁹ | 48673/114688 = 0.424395 |

Not shown stable (each level so far adds one constraint); level 64 is too large for this implementation (2²⁴ elements). The data (p ≤ 10⁸) confirm the constraints at levels 16 and 32 and show further splitting of the classes 1 and 31 mod 32 at mod 64; see `notes/odd_order_density_check.md`.
