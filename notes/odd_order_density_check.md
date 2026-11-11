# Odd-order reductions of P = (1,1) on C: comparison with the Liang–Rouse densities (11 November 2026)

Written by Claude (a language model). Computation: `code/odd_order_density.c` (about 44 s for primes up to 10⁷; about 14 minutes up to 10⁸). The comparison table is taken from Table 1 of Liang–Rouse, *The density of odd order reductions for elliptic curves with a rational point of order 2* (arXiv 1810.10583), which I read in full; I did not read the references it relies on.

## Question

Is the density of primes p at which P = (1,1) has odd order in C(𝔽_p), C : y² = x³ − 2x² + 2x, one of the 21 values that Liang–Rouse compute for curves with a rational point of order 2?

## Method and validation

For every prime p (p ∤ 2b(a² − 4b)c) the order of α = (c, ck) on E : y² = x³ + ax² + bx, b = ck² − ac − c², is found by baby-step giant-step in the Hasse interval, and we test whether it is odd. The program reproduces the fractions π_S(10⁷)/π(10⁷) that Liang–Rouse list, to six digits, on four of their curves:

| [a, c, k] | Liang–Rouse at 10⁷ | this program at 10⁷ | limit density |
| --- | --- | --- | --- |
| [3, 3, 1] | 0.237796 | 0.237796 | 5/21 |
| [−3, 1, 3] | 0.476216 | 0.476216 | 10/21 |
| [2, 3, 1] | 0.247027 | 0.247027 | 83/336 |
| [2, −5, 1] | 0.142902 | 0.142902 | 1/7 |

## Result for our curve ([a, c, k] = [−2, 1, 1], b = 2, a² − 4b = −4)

| primes up to | odd order | fraction |
| --- | --- | --- |
| 10⁷ | 281 912 of 664 578 | 0.424197 |
| 10⁸ | 2 445 403 of 5 761 454 | **0.424442** (standard error 0.0002) |

By class of p (10⁸): p ≡ 1 (mod 8): 0.53099; p ≡ 3: **1** exactly; p ≡ 5: **0** exactly; p ≡ 7: 0.16680 (compatible with 1/6). Mod 3 there is no bias (0.42443 and 0.42445).

**None of the 21 Liang–Rouse densities matches.** The nearest are 25/56 ≈ 0.4464 and 19/42 ≈ 0.4524, more than 100 standard errors away.

## Why: our curve is outside their hypotheses

Theorem 1 of Liang–Rouse assumes the 2-adic image of ρ is the full Γ₀(2). In their parametrization the four index-2 subgroups of Γ₀(2) have fixed fields ℚ(√−1), ℚ(√2), ℚ(√b), ℚ(√(a² − 4b)), so full image forces −1, 2, b, a² − 4b to be independent modulo squares. For our curve they are not: b = 2 and a² − 4b = −4 ≡ −1, so the square classes (−1, 2, b, a² − 4b) = (−1, 2, 2, −1) span rank **2** (the four Liang–Rouse example curves all have rank 4). Hence the image of ρ_{C,2^k} is a proper subgroup of Γ₀(2), the 63-image classification does not apply, and the density for (C, P) must be computed from the actual image of τ_{C,2^k} by their formula (1) (needs a group computation, e.g. in Magma, which I did not do).

## The classes mod 8 are explained by the 2-descent of the index-four note

* p ≡ 5 (mod 8): δ(P) = (1, χ(−i), χ(i)) = (1, −1, −1) ≠ 1, so P ∉ 2C(𝔽_p) and the order is even: fraction 0 (observed 0.00000).
* p ≡ 3 (mod 8): v₂(|C(𝔽_p)|) = 1 (checked at all 140 primes below 4000), the 2-part is ℤ/2, and x(P) = 1 is a square, so P has odd order: fraction 1 (observed 1.00000).
* p ≡ 1 (mod 8) and p ≡ 7 (mod 8): genuinely 2-adic Kummer questions; observed 0.531 and 0.1668. I did not derive exact values. (A numerological guess, a₁ = 17/32 and a₇ = 1/6, gives the overall density 163/384 ≈ 0.42448, which agrees with the measurement; the denominator has no factor 7 whereas every Liang–Rouse density has one, so I do not trust the guess.)

## What this does and does not give

It confirms that (C, P) has extra 2-adic entanglement beyond the generic case (the coincidences ℚ(√b) = ℚ(√2) and ℚ(√(a² − 4b)) = ℚ(i) lie inside ℚ(ζ₈)), which is consistent with the cyclotomic character η = χ(1 + i) of the index-four note being tied to the arithmetic of the 2-power Kummer fields. It does not test the index-four parity law itself and has no bearing on Problem H.
