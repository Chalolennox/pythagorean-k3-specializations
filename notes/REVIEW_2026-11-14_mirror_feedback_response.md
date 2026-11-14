# Response to the independent assessment of the mirror sequences (14 November 2026)

Reviewer of this note: Claude (a language model); a record of questions and answers, not a referee's report. Paper: F.50 (trimmed) and the new F.51; scripts `code/verify_rotation_coding.py`, `code/verify_mirror_collapse.py` (full runs about 2 minutes each, `--quick` about 2 s).

## Corrections accepted
* **"Sturmian" was wrong.** The coding is by an interval of length 2ρ = 0.25018886…; PSLQ finds no integer relation a·2ρ + bθ + c = 0 with coefficients ≤ 10⁴, so it is a generic interval coding of an irrational rotation.
* **"Bounded valuations" was wrong for one factor.** Q′ = (V + U)/d along 1 + x(nP) (U along 1 + 2/x(nP): the same integer 2B² + A) vanishes at x = −2 and has unbounded 3-adic valuation (6 at n = 70, 9 at n = 2117). It is now handled explicitly (F.51 (b), step 3).
* **149 versus 148.** 3 ≤ n ≤ 150 has 148 values; the sign test used 2 ≤ n ≤ 150 (149). Replaced by 1 ≤ n ≤ 330 (330 of 330); the product identity uses the 148 values 3 ≤ n ≤ 150.
* **The archimedean root number is the constant −1** and sits in the leading minus of f(t) = −w₂w₃(2/c); the sign of F_s enters through the Jacobi symbol (ab/N), not through a local root number.
All three are in the paper's corrections log (entry 9).

## Answers
1. **θ and ρ.** Ω = ∫₀^∞ dx/√(x³ − 2x² + 2x) = 4.0364616539…, u(x) = ∫ₓ^∞ dx′/(2√(x′³ − 2x′² + 2x′)), θ = u(1)/Ω = 0.29567987352534367…, ρ = u(x₀)/Ω = 0.12509443218654407…; computed by quadrature from these definitions, not fitted.
2. **The threshold.** D(t) = t⁶ − 30t⁴ − 24t² − 1 is irreducible with exactly two real roots ±t₀ (s³ − 30s² − 24s − 1 has one sign change); G₊(X) = D(1 + X) has real roots −1 ± t₀, so its only positive root is x₀ = t₀ − 1 = 4.548041385981…, and F_s(1 + x) > 0 iff x > x₀. Along 1 + 2/x the threshold is 2/x₀ (translation by T).
3. **Sturmian?** No (see above).
4. **Every n, boundary cases.** x₀ has degree 6 and x_n is rational, so ‖nθ‖ ≠ ρ for all n; the coding of sign F_s is then an exact consequence of the uniformization (F.51 (a), Proved). The periodic part (F.51 (b)) is proved for every n by a finite exact computation (Certified), not by hand; what remains outside the computation is stated there.
   Non-periodicity: proved given (a) and (b) (F.51 (c) (1)).
5. **F_s and the sign.** F_s(U, V) = U⁶ − 30U⁴V² − 24U²V⁴ − V⁶ = V⁶D(U/V), F = −4F_s/d³. It enters ε through the exact reciprocity formula of F.51 (b); on the original sequences the same formula has no real dependence, on the mirror ones exactly sign F_s. **I have no conceptual explanation**: a Hilbert-symbol accounting predicts a real factor (−1)^{[ab<0 and F_s<0]} on the original sequence (for x ∈ (1, 2)) that the data do not show, so none is claimed.
6. **h(n).** Obtained from the finite computation: 2-adic data of period 8, 3-adic data of period 729 (joint period 5832), all valuations bounded except the factor above, which lies in 16 residue classes mod 5832 and does not matter. It is not derived by hand.
7. **27-lag.** 2‖27θ‖ = 0.03328683 (exact, since ‖27θ‖ < min(2ρ, 1 − 2ρ)); agreement 0.96671317 against 0.9667 observed (F.51 (c) (3)).
8. **Mean.** (1 − 4ρ)/3 = 0.16654076 along 1 + x(nP), the negative along 1 + 2/x(nP) (F.51 (c) (2)).
9. **Fourfold separation and δ, κ.** It gives disjoint prime supports at each n; it does not simplify δ⁺ or κ⁺. The product of the four periodic parts is −(−1)ⁿ s_n s′_n (n ≥ 3, 148 of 148), which is a statement about the periodic parts only.
10. **A relation between the parity factors of the original and mirror sequences:** none found. A square-class identity is excluded (the divisors of F(1 − x) and F(1 + x) are reduced and disjoint), supports are disjoint, and no congruence is known.
11. **A theorem that applies to δ⁺.** None that I can identify; F.51 (d) says so. Davenport's theorem concerns λ at the index n, not λ(N_n).

## What remains open
The parity bit δκ itself (Problem H and its mirror analogue); a conceptual explanation of why the real sign enters only through sign F_s on 1 + x and cancels on 1 − x; a hand proof of the periodicity of the 2- and 3-adic data (verified over many periods and argued by compactness); human refereeing of the reciprocity derivation.
