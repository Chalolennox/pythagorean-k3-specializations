# The mirror projection t = 1 + x(Q): is the periodic part periodic? (13 November 2026)

**Status: numerical, with a derivation sketch; not a theorem. Nothing here bears on Problem H beyond the structural comparison below.**

## Question
Along t = 1 − x(nP) and t = 1 − x(nP + T) the periodic part ε_n = f(t_n)·(ab/N_n) of the sign W = ε·δ·κ (F.24) is exactly periodic (periods 6 and 3, proved: Appendix B, F.21). Is the same true for the "mirror" sequences t = 1 + x(nP) = 2 − t_n and t = 1 + x(nP + T)? They lie on none of the six known constant-x covers (n ≤ 40) and the natural cover C_{−2} (on the twist y² = x³ + 2x² + 2x) has rank 0, so they carry no section; the question is only about the parity structure.

## Result (observed)
`code/mirror_projection_eps.py` computes ε_n from full Jacobi symbols (no factorization). Control: the proved laws hold for 2 ≤ n ≤ 72. For the mirror sequences:

1. **ε⁺_n = h(n)·s_n** with s_n = sign F_s(t⁺_n) and h of period 3: along 1 + x(nP), h(n) = +1 iff 3 | n; along 1 + x(nP+T), h(n) = −1 iff 3 | n. (The table g(r, s) of ε for n ≡ r mod 6 and sign s satisfies g(r, −) = −g(r, +) for every r; zero conflicts on 3 ≤ n ≤ 150. For the control sequences g does not depend on s.)
2. **s_n is a rotation sequence.** Let u be the elliptic logarithm on the real component of C, Ω its period, θ = u(P)/Ω = 0.29567987352534367… (continued fraction [0; 3, 2, 1, 1, 1, 1, 1, 1, 2, …]) and ρ = 0.12509443218654… = u(x₀)/Ω with x₀ = t₀ − 1 = 4.548…, t₀ = 5.548… the largest real root of t⁶ − 30t⁴ − 24t² − 1. Then s_n = + iff ‖nθ‖ < ρ along 1 + x(nP), and iff ‖nθ − 1/2‖ < ρ along 1 + x(nP+T) (translation by T is a shift by 1/2). Agreement with the exact sign: 149 of 149 values of n for each sequence (n ≤ 150).
3. **Out-of-sample check.** 16 direct Jacobi evaluations at n ∈ {156, 178, 212, 216, 227, 231, 260, 271} (five of them within 0.001 to 0.008 of the threshold, on both sides): 0 disagreements with ε_n = h(n)·s_n.
4. **Valuations** of F_s at 2 and 3 are bounded and functions of n mod 9 for n ≤ 330: (v₂, v₃) ∈ {(0,0), (0,3), (0,4)} along 1 + x(nP) and {(1,0), (1,3)} along 1 + x(nP+T).

## Consequences
* **ε⁺ is never periodic**: θ is irrational (P has infinite order), so ε⁺ is a period-3 pattern times a Sturmian sequence. The apparent period 27 seen up to n ≈ 72 is the convergent 8/27 of θ: ε_n = ε_{n+27} for 96.7 % of n.
* **Why 1 − x is special.** There t ≤ 1 (x ≥ 0 on C(ℝ)), the real place contributes nothing (F.21 (3)) and the sign is purely 2- and 3-adic, hence periodic. For t > 1, F_s changes sign when x(nP) crosses x₀ (resp. x₁ = 2/x₀ = 0.4397 along nP + T), and that sign enters ε.
* **Long-run mean.** s_n = + with density 2ρ = 0.25019, so by equidistribution of (n mod 3, nθ) the mean of ε⁺ is ∓(1/3)·(2·0.25019 − 1) = ±0.1665 (+ along 1 + x(nP), − along 1 + x(nP+T); law evaluated for n ≤ 10⁶).
* **For H.** W⁺ = ε⁺·δ⁺·κ⁺ as in F.24 (same derivation, assuming the §4 formula). The failure of the mirror analogue of H would require the Liouville sign δ⁺κ⁺ to follow the Sturmian-modulated pattern −ε⁺ eventually. This is more rigid than for the original orbit but just as out of reach (parity barrier), and the mirror carries no section, hence no rank consequence. The only new feature is that the target is non-correlation with a quasi-periodic (zero-entropy, almost periodic) sequence instead of a periodic one.

## Why one expects this (sketch, not written out)
ε = L·(ab/N). Quadratic reciprocity reduces (ab/N) to characters of U, V, (V ∓ U)/d modulo 24 and of N modulo 8 and 12. Along both mirror sequences U, V, V + U > 0 and V − U < 0 (V = B² or A, U = V + A or V + 2B²), so the only real-place dependence is sign(F_s), which enters through N = |F_s|/(2^{e₂}3^{e₃}); all other data are 2- and 3-adic with bounded valuations, hence periodic in n. This was verified numerically, not proved.

## Limits
Checked directly for n ≤ 150 (fit) and at 16 values up to 271 (out of sample); valuations to n ≤ 330. A residue-based computation to n ~ 10⁴, which would certify the p-adic part for long ranges, was not done. The result inherits the correctness of the §4 root-number formula (validated on 12 Magma values and the paper's checks).
