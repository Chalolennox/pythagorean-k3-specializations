# Odd-order reductions of P = (1,1) on C: the 2-adic image of the Kummer representation, and a comparison with Liang–Rouse (11–12 November 2026)

Written by Claude (a language model); no human has refereed it. Code: `code/odd_order_density.c` (counts), `code/tau_image/` (image and density; see its README). Data: `data/odd_order_classes_C_P_1e8.txt`.
The comparison table is Table 1 of Liang–Rouse, *The density of odd order reductions for elliptic curves with a rational point of order 2* (arXiv 1810.10583), which I read in full.

## Question

For C : y² = x³ − 2x² + 2x and P = (1,1), what is the density of primes p at which P has odd order in C(𝔽_p)?

## Direct count

For all primes up to 10⁸ (BSGS in the Hasse interval; the program reproduces the published fractions of Liang–Rouse at 10⁷ to six digits on four of their curves: 0.237796, 0.476216, 0.247027, 0.142902):

| primes up to | odd order | fraction |
| --- | --- | --- |
| 10⁷ | 281 912 of 664 578 | 0.424197 |
| 10⁸ | 2 445 403 of 5 761 454 | **0.424442** (standard error 0.0002) |

Exactly 1 at p ≡ 3 (mod 8), exactly 0 at p ≡ 5 (mod 8) (explained by the 2-descent of the index-four note); 0.531 at p ≡ 1 and 0.1668 at p ≡ 7 (mod 8). None of the 21 Liang–Rouse densities matches (nearest 25/56 = 0.4464): their theorem assumes the 2-adic image of ρ is the full Γ₀(2), i.e. −1, 2, b, a² − 4b independent modulo squares, whereas for C the square classes are (−1, 2, 2, −1), of rank 2.

## The image of the Kummer representation, computed

`code/tau_image` implements the Liang–Rouse method in Python (no Magma available): the numerical coset criterion of Dokchitser–Dokchitser, descent through maximal subgroups, and their density formula (§5). **Validation:** the density formula reproduces rows 1–17 of their Table 1 exactly; the whole pipeline gives 5/21, 10/21, 83/336, 1/7 for the curves [3,3,1], [−3,1,3], [2,3,1], [2,−5,1] (Table 1). Two silent pitfalls were found and fixed on the way (README): Y must be built from β_k, and the published exponents (1,1,2) make Y symmetric under A ↔ B and give false positives (we use (1,2,3)).

Result for C (frame fixed by β_k, A_k, B_k; each level found by the coset test, not by fitting):

| level | image order | full preimage of the level below | density (assuming the full preimage above) |
| --- | --- | --- | --- |
| mod 8 | 2⁸ (index 128 in Γ₀^⊙(2)) | – | 95/224 = 0.424107 |
| mod 16 | 2¹³ | 2¹⁴ | 1521/3584 = 0.424386 |
| mod 32 | 2¹⁸ | 2¹⁹ | 48673/114688 = 0.424395 |

The generators are in `code/tau_image/image_generators_-2_1_1.json` (2, 2 and 4 generators).

## Do the data confirm the extra constraints at levels 16 and 32?

Yes. For primes in classes mod 2^r the predicted odd-order fraction comes from the image (class densities, `descend.class_densities`). The full preimage of the lower-level image would give very different values, and the data side with the computed images (`fullpre_test.py`, `fullpre_test32.py`; standard errors from the class sizes, about 720 000 and 360 000 primes):

| class | measured | image computed | full preimage of the level below |
| --- | --- | --- | --- |
| 1 mod 16 | 0.56213 | 0.56176 (+0.6σ) | 0.53088 (+53σ) |
| 9 mod 16 | 0.49984 | 0.50000 (−0.3σ) | 0.52865 (−49σ) |
| 7 mod 16 | 0 | 0 | 1/6 (off) |
| 15 mod 16 | 0.33371 | 0.33333 (+0.7σ) | 1/6 (+380σ) |
| 1 mod 32 | 0.54051 | 0.54032 (+0.2σ) | 0.56183 (−26σ) |
| 17 mod 32 | 0.58376 | 0.58333 (+0.5σ) | 0.56169 (+27σ) |
| 15 mod 32 | 0.50063 | 0.50000 (+0.8σ) | 1/3 (+213σ) |
| 31 mod 32 | 0.16680 | 0.16667 (+0.2σ) | 1/3 (−212σ) |

All 16 classes mod 32 agree with the level-32 image within 0.8 standard errors (the classes with fraction 0 or 1 agree exactly).

## What is not settled

* **Stability.** The image is not shown stable at level 32 (each level so far adds one constraint). The data mod 64 show a further splitting of the classes 1 and 31 (mod 32): 1 mod 64: 0.52876, 33 mod 64: 0.55227 (mean 0.54052 = the level-32 value); 31 mod 64: 0.25038, 63 mod 64: 0.08326 (mean 0.16682 = 1/6); all other classes show no splitting within errors. Level 64 (2²⁴ elements) is too large for this implementation, and I do not know whether the full preimage of I32 would already reproduce this splitting, so I do not claim a level-64 constraint. The density corrections shrink fast (+0.000279, then +0.000009), so I expect the exact density to be 0.42440 up to a correction of about 10⁻⁵, but this is an extrapolation, not a proof.
* The coset criterion is a numerical heuristic (integer test at 10⁻⁴⁰ on 100-digit values); it is validated at level 8 on four published curves and at levels 16 and 32 only by the class densities above.
* This does not test the index-four parity law and has no bearing on Problem H. It does show that (C, P) has substantial 2-adic entanglement (rank-2 square classes, and constraints at every level so far).
