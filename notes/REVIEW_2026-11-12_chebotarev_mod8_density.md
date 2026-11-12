# Review of "A Chebotarev density calculation for y² = x³ − 2x² + 2x" (extended independent-review draft, 11 November 2026)

Draft reviewed (as received, unchanged): `notes/drafts/chebotarev_density_mod8_extended_independent_review.md`.
Reviewer: Claude (a language model); a check by recomputation, not a referee's report. Scripts: `code/verify_chebotarev_mod8.py` (20 s), `code/tau_image/image_densities.py` (30 s).
I could not rerun the Magma computations quoted in the draft (Galois group of f of order 32 and its coset counts; the relative orders 8, 8, 8; the joint counts (3, 5, 0, 0)). What I did instead: (a) checked every exact identity and every deterministic claim of the draft directly; (b) re-derived the draft's densities from a *different* finite computation, the 2-adic image of the Kummer representation of (C, P) computed in `code/tau_image`.

## Verdict

The draft is correct where it can be checked, with one false sentence (harmless) and one false conjecture (Addendum D, "separate conjecture"). The headline density **1/8 (conditional 1/2)** for {p ≡ 7 mod 8 : 8 | #C(𝔽_p)} and Theorem B (**8 | #C(𝔽_p) ⇔ P ∈ 4C(𝔽_p) for p ≡ 7 mod 8**) are confirmed by an independent finite computation. The conjecture Pr(P ∈ 2^jC | p ≡ 7 mod 8) = 2^{−(j−1)} is **false for j ≥ 4**.

## What I verified

| claim | check | result |
| --- | --- | --- |
| H_s, f = H_{√2}H_{−√2} = X⁸ − 40X⁶ + 128X⁵ − 232X⁴ + 256X³ − 160X² + 16, f irreducible | sympy | correct |
| F(s) = 4(s − 1), F(−s) = −4(s + 1), product −16 | sympy | correct |
| disc H_s = 2²⁰(2s − 3) = −(2¹⁰(s − 1))²; disc F_s = −2²⁰(17 + 12s) = −2²⁰(3 + 2s)² | sympy | correct |
| Q = (2 + s, 2 + 2s) lies on C and 2Q = P = (1,1); F_P = (X² − 4X + 2)(X² + 2) | sympy, exact | correct (Addendum A) |
| "for p ≡ 7 mod 8 both 2 and −2 are squares" | Legendre symbols | **false**: (2/p) = 1 but (−2/p) = −1 (since (−1/p) = −1). Harmless: the argument only needs 2 to be a square |
| cycle type of f mod p for p ≡ 7 mod 8 is 1⁴2² or 4² | all 6 522 such primes p < 3·10⁵ (sympy factorization mod p) | only these two types, 3 270 and 3 252 times (≈ 1/2 each) |
| f has a root mod p ⇔ 8 \| #C(𝔽_p) | same primes, #C by BSGS | no exception |
| P ∈ 2C(𝔽_p) for every p ≡ 7 mod 8 | same | no exception |
| Theorem B: 8 \| #C(𝔽_p) ⇔ P ∈ 4C(𝔽_p) | same | no exception |
| level-16 analogue false; p = 31: #C = 32, 2P = (8,11), 4P = (0,0), 8P = O | exact | correct |
| Addendum C table (301, 294, 307, 1497) and Addendum D census (r-distribution, 412 odd-order primes of 2 399) for p ≤ 10⁵ | recomputed | reproduced exactly |

The logic of Section 5 and Addendum B.1 is sound: a root of the halving quartic over 𝔽_p gives a rational point R or −R, and Frobenius cannot send R to −R because it fixes Q = 2R, which has order > 2. The one non-elementary input is the synchronization of the two quartics (both have roots or neither), supplied by the Magma coset counts; the cycle-type census above confirms exactly that behaviour.

## Update (same day): the image is NOT stable at level 32

`code/tau_image/stability_mod64.py` predicts the odd-order fractions mod 64 under the assumption that the image at level 64 is the full preimage of I₃₂, and compares them with the 10⁸ prime data. The prediction has **no split** of the classes 1, 33 and 31, 63 (mod 64) (0.54032 and 0.54031; 1/6 and 1/6). The data split them: 0.52876 versus 0.55227 (about 10σ from the prediction) and 0.25038 versus 0.08326 (82σ and 128σ), i.e. 1/4 versus 1/12 to within 0.4σ. All other classes mod 32 are unsplit. Hence the image at level 64 is a proper subgroup of the full preimage of I₃₂, and the level-32 image is **not** the stable image. The new constraint involves only the classes p ≡ ±1 mod 32 and, to the precision of the data, leaves the class means unchanged (class 31 mod 32: mean 0.16682 against 1/6; class 1: 0.54052 against 0.54032). Consequences for this note: the level-32 weights (item 6 and the value 1/6 computed from them) are **not** the final values; the exact statements of items 1–5 (finite levels ≤ 32) are unaffected; the pattern in item 7 (a_j for j ≤ 5) is exact but its limit is unproved. My statement that the matrix part is stable from level 32 on (Rouse–Zureick-Brown) stands; the new constraint is in the joint structure of the Kummer and the cyclotomic part.

## An independent proof route: the finite image

`image_densities.py` reads the computed images I₈, I₁₆, I₃₂ of the Kummer representation of (C, P) (README of `code/tau_image`). For a Frobenius class (v, M): #C(𝔽_p) ≡ det(I − M), p ≡ det M mod 2^k, and P ∈ 2^jC(𝔽_p) iff x ↦ v + xM has a fixed point mod 2^j. By Chebotarev every statement below is an exact count in a finite group; it is **conditional on the image having been computed correctly** (numerical coset criterion, validated in the README).

1. **Density 1/8.** In I₈ (order 256): 64 classes have det M ≡ 7 mod 8, and 32 of them have det(I − M) ≡ 0 mod 8: density 32/256 = **1/8**, conditional 1/2. This agrees with the draft's Magma-based count (4/32) although it comes from a different group.
2. **Theorem B as a finite statement.** For all 64 classes in I₈ with det M ≡ 7 mod 8: 8 | det(I − M) ⇔ the affine map has a fixed point mod 4. No exception, so the equivalence holds for every unramified prime p ≡ 7 mod 8 (by Chebotarev every class occurs). The level-16 analogue fails for 512 of 2 048 classes.
3. **The valuation law.** From I₃₂: Pr(v₂(#C) = 2, 3, 4 | p ≡ 7 mod 8) = 1/2, 1/4, 1/8, and Pr(v₂ ≥ 5) = 1/8, exactly the draft's model 2^{−(k−1)}.
4. **P in 2^jC (exact at each level).** Pr(P ∈ 2^jC | p ≡ 7 mod 8) = 1, 1/2, 1/4, **3/16, 11/64** for j = 1, …, 5. The draft's "separate conjecture" predicts 2^{−(j−1)} = 1/8, 1/16 at j = 4, 5. Prime data (p < 3·10⁵, 6 522 primes): 0.189 and 0.177 at j = 4, 5, in agreement with the image and not with the conjecture.
5. **Why the conjecture must fail.** If P has odd order it is divisible by 2^j for every j (P = 2^j(mP) with 2^jm ≡ 1 mod ord P). So Pr(P ∈ 2^jC) ≥ Pr(odd order) for all j, and 2^{−(j−1)} < 1/6 for j ≥ 4. The draft's own conjectured density 1/6 contradicts its separate conjecture.
6. **Conditional odd-order laws.** With the Liang–Rouse weights at level 32: Pr(odd | r = 2, 3, 4) = 0, 1/2, 1/4 and Pr(odd | r ≥ 5) = 1/12, which is exactly what the draft's heuristic Pr(odd | r = k) = 2^{−(k−2)} gives (aggregated over k ≥ 5: 1/12). The total is exactly **1/6** (and 1/6 is also the exact value at levels 8, 16, 32 of the class-by-class prediction for p ≡ 7 mod 8). This assumed the image above level 32 to be the full preimage; the update above shows that assumption is false (a new constraint at level 64), so these level-32 numbers are a model, not the density.
7. **A pattern, not a proof.** a_j = Pr(P ∈ 2^jC | 7 mod 8) = 1/4, 3/16, 11/64 for j = 3, 4, 5 equals 1/6 + (1/12)·4^{−(j−3)}, whose limit is 1/6. This is a three-parameter fit to three points; a_6 would test it and needs level 64.

## The matrix part and the translation part

Splitting the computed images: the image of ρ_{C,2^k} has index **24, 48, 96** in GL₂(ℤ/2^k) at k = 3, 4, 5, while the translation part keeps constant index 16. So the extra constraints at levels 16 and 32 are constraints on the 2-adic Galois image of C itself. For non-CM E/ℚ the index of the 2-adic image divides 64 or 96 and the image is determined mod 32 (Rouse–Zureick-Brown, which I confirmed in the sources); C has j = 128, which is not a CM j-invariant. Hence the index-96 image found at level 32 is the 2-adic image of C, stable from level 32 on (conditional on the computed matrix part). The *joint* image of (v, M) is not stable at level 32 (see the update); the level at which it stabilizes is unknown, and a proof of the infinite-level odd-order density needs it.

## Status

| statement | status |
| --- | --- |
| density 1/8, conditional 1/2 (Theorem 1) | proved given the finite Galois computation of the draft; independently confirmed by an exact count in the computed image I₈ |
| Theorem B (8 \| #C ⇔ P ∈ 4C, p ≡ 7 mod 8) | proved given the joint counts; independently confirmed for every class of I₈ and for 6 522 primes |
| P ∈ 2C(𝔽_p) for p ≡ 7 mod 8 (Addendum A) | proved (exact; it holds for p ≡ ±1 mod 8) |
| level-16 analogue false (Addendum C) | proved (p = 31; 512 of 2 048 classes) |
| valuation law Pr(r = k) = 2^{−(k−1)} | exact for k ≤ 4 from I₃₂ (conditional on the image) |
| Pr(P ∈ 2^jC) = 2^{−(j−1)} for j ≥ 4 | **false** (3/16, 11/64; and Pr ≥ 1/6 by the odd-order argument) |
| odd-order density 1/6 | supported (exact at levels 8, 16, 32; data 0.1668 ± 0.0003); not proved; the level-32 image is not stable (new constraint at level 64 for p ≡ ±1 mod 32) |

## Suggested corrections to the draft

1. Replace "both 2 and −2 are squares" by "2 is a square and −1, −2 are not".
2. Delete or restate the "separate conjecture" of Addendum D: Pr(P ∈ 2^jC) decreases to the odd-order density, not to 0.
3. Keep the level-16 frequencies, the 1/6 density and the heuristic laws labelled numerical/heuristic (the draft already does).

## Limits

No human has refereed this. The finite-group computations rest on the numerical coset criterion (validated at level 8 on four published curves and at levels 16 and 32 by class densities of the prime data). I did not rerun the draft's Magma computations.
