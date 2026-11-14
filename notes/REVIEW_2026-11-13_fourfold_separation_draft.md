# Review of the draft "Fourfold Prime-Support Separation for an Elliptic Orbit" (13 November 2026)

Reviewer: Claude (a language model); a check by recomputation, not a referee's report. Script: `code/verify_fourfold_separation.py` (5 s, sympy only).

## Verdict
Correct. Every exact statement and every finite-field value was recomputed independently, without Magma. The result is an extension of F.25 (the pair 1 − x, 1 − 2/x) to the four parameters 1 ∓ x_n, 1 ∓ 2/x_n: a lemma, not a new idea. It is recorded as F.50 (ii) of the paper, with the corrections below.

## Checked
* the Step 2 identity d³F(t) = −4v⁶H(u/v) (exact), and the four polynomials G_∓, J_∓ as stated;
* all six resultants (exact factorizations as in the draft) and E = {7, 79, 103, 113, 13327, 66601, 519521};
* the orders of P mod p (6, 22, 54, 14, 3358, 8366, 698) and **zero** orbit collisions at each prime, by direct group arithmetic;
* brute force: no pair of the four integers shares a prime ≥ 5 for 1 ≤ n ≤ 200 (the verification script runs 120 by default).

## Corrections and remarks
1. **p ≥ 5, not only p > 5.** The prime 5 divides no resultant and no leading or constant coefficient, and the brute force finds no shared 5.
2. **At 79 and 13327 there is no common root in 𝔽_p** (the resultant is divisible only through squares; the common root lives in 𝔽_{p²}), so the "exhaustive orbit test" there is vacuous. The cases with content are 7, 103, 113, 66601, 519521.
3. **Reproducibility.** The draft depends on Magma output no reader can rerun; the script reproduces it.
4. **Scope** (as the draft says): fixed n only; it does not make the Liouville signs independent; only the pair (1 − x, 1 − 2/x) is attached to sections.

## Relation to the paper
F.25 proves the pair (G_−, J_−) with the same method (primes 7, 103, 519521). The other five pairs are new, with the extra primes 66601 (the mirror pair) and 79, 113, 13327 (the cross pairs).
