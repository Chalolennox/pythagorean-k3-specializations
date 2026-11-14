# The real sign of F_n as an exact rotation coding

Written by Claude (a language model); not refereed by a human. Code: `code/rotation_coding_F_n.py` (full run about 1 minute, `--quick` 1 second; needs mpmath, sympy, numpy and `code/mirror_projection_eps.py`). Same normalisation as F.51 (a).

## Constants (computed from the definitions, not fitted)
C : y² = x³ − 2x² + 2x, ω = dx/(2y), Ω = ∫₀^∞ dx/√(x³ − 2x² + 2x), u(x) = ∫_x^∞ dx′/(2√(x′³ − 2x′² + 2x′)), λ : C(ℝ) → ℝ/Ωℤ the real elliptic logarithm (λ(Q) = ±u(x(Q))), θ = u(1)/Ω.
H(t) = t⁶ − 30t⁴ − 24t² − 1 has exactly the real roots ±t₀, t₀ = 5.54804138598128…; put c₁ = 1 + t₀ = 6.54804138598128… and ρ₁ = u(c₁)/Ω.

| quantity | value |
| --- | --- |
| Ω | 4.036461653911667430313407… |
| θ | 0.2956798735253436710878454… |
| ρ₁ | 0.101933656459737224875741… |
| ½ − θ | 0.20432012647465632891… |
| 2ρ₁, 4ρ₁ | 0.203867312919…, 0.407734625839… |
| continued fraction of θ | [0; 3, 2, 1, 1, 1, 1, 1, 1, 2, 8, 1, …], q_k = 1, 3, 7, 10, 17, 27, 44, 71, 115, 301, 2523, 2824, … |

**Closed forms.** With the modulus k = cos(π/8) (k² = (2 + √2)/4):
Ω = 2K(k)/2^{1/4},  u(c)/Ω = F(φ_c, k)/(4K(k)),  cos φ_c = (c − √2)/(c + √2)
(checked to 20 digits; the substitution is the standard one for a cubic with one real root 0 and the complex pair 1 ± i, |1 ± i| = √2). Hence θ = F(φ₁,k)/(4K) with cos φ₁ = −(3 − 2√2), and ρ₁ = F(φ_{c₁},k)/(4K).
**The half-turn as an identity.** cos φ₂ = (2 − √2)/(2 + √2) = 3 − 2√2 = −cos φ₁, so φ₂ = π − φ₁ and u(2)/Ω = ½ − θ exactly; this is x(P + T) = 2 and λ(T) = Ω/2 seen from the integral. In the same way u(2/c₁)/Ω = ½ − ρ₁.

## Theorem (Proved; the constants are computed). For every n ≥ 2, with θ_n = ‖nθ‖ and θ′_n = ‖nθ + ½‖ = ½ − θ_n:
1. **sign F_n = −1 ⇔ θ_n < ρ₁.** Along nP + T (G_n the same sextic value −4Φ along t′_n): **sign G_n = −1 ⇔ θ′_n < ρ₁ ⇔ θ_n > ½ − ρ₁.**
2. **The four real classes** of t = U/V (for t_n and, with θ′_n, for t′_n), as the triple (sign U, sign(V + U), sign F_s):
   θ_n > θ: (+,+,−) (x < 1);  ½ − θ < θ_n < θ: (−,+,−) (1 < x < 2);  ρ₁ < θ_n < ½ − θ: (−,−,−) (2 < x < c₁);  θ_n < ρ₁: (−,−,+) (x > c₁). (V > 0 and P′ > 0 throughout; F_n = −4F_s.)
3. F_n < 0 and G_n < 0 never occur together (ρ₁ < ¼, so the two arcs are disjoint); F_nG_n < 0 exactly when θ_n < ρ₁ or θ_n > ½ − ρ₁.

*Proof.* As in F.51 (a): λ is an isomorphism C(ℝ) → ℝ/Ωℤ with λ(nP) = nθΩ, x is an even strictly decreasing function of λ on (0, Ω/2), so {x > c} = {‖λ/Ω‖ < u(c)/Ω}; F_s(1 − x) = Y⁶H(1 − x) is positive exactly for |1 − x| > t₀, i.e. x > c₁ (x ≥ 0 excludes the other root), and F_n = −4F_s. The classes follow from x = 1 ↔ θ, x = 2 ↔ ½ − θ (the half-turn), x = c₁ ↔ ρ₁. There is no boundary case: x_n = 1 only for n = ±1, x_n ≠ 2 (since 2 = x(P + T) and T ∉ ⟨P⟩), c₁ is irrational (H has no rational root) and x_n is rational. Along nP + T, x(nP + T) = 2/x_n is a shift of λ by Ω/2. □

## Consequences
* **Density.** {n : F_n < 0} has density 2ρ₁ = 0.2038673…, {n : G_n < 0} the same, and {n : F_nG_n < 0} density 4ρ₁ = 0.4077346… (Weyl equidistribution, θ irrational because P has infinite order). Exact counts for 2 ≤ n ≤ 400: 81/399 = 0.2030, 82/399 = 0.2055, 163/399 = 0.4085.
* **Not periodic.** A periodic sign sequence would make the arc invariant under rotation by qθ ≢ 0 (the orbit is dense and there is no boundary case), impossible for an arc of length 0 < 2ρ₁ < 1.
* **First returns (three-distance theorem), computed exactly.** The gaps between consecutive n with F_n < 0 take exactly three values, 3, 4 and 7 (3 + 4 = 7), with frequencies 0.44591226, 0.10373325 and 0.45035449; the first values are n = 7, 10, 17, 20, 24, 27, 34, 37, 44, 51, 54, …. Checked against the exact signs for n ≤ 400 (gaps {3,4,7}) and against the coding for n ≤ 10⁶ (frequencies agree to 3·10⁻⁴).
* **Margins.** For 2 ≤ n ≤ 10⁶ the closest approach of θ_n to the breakpoints ρ₁, ½ − θ, θ is 2.4·10⁻⁷, 1.0·10⁻⁷, 6.7·10⁻⁷, so the floating-point coding is reliable there.

## The four sequences side by side (F_s > 0 means: the sextic value is positive)
| sequence | F_s > 0 exactly when | radius |
| --- | --- | --- |
| t = 1 − x_n (this note) | ‖nθ‖ < ρ₁ | ρ₁ = 0.10193366… (x > 1 + t₀) |
| t = 1 − 2/x_n | ‖nθ − ½‖ < ρ₁ | ρ₁ |
| t = 1 + x_n (F.51) | ‖nθ‖ < ρ | ρ = 0.12509443… (x > t₀ − 1) |
| t = 1 + 2/x_n (F.51) | ‖nθ − ½‖ < ρ | ρ |

## What this does and does not give
It makes the archimedean part of F_n completely explicit: the sign and the real class of every t_n are read off from one irrational rotation. For the original sequences it does not enter the root number: by F.53 the formula for ε is independent of the real class (verified over all four classes), so W(E_{t_n}) = ε_nδ_nκ_n does not see the sign of F_n. The parity bit δ_n = λ(|F_n|/4) is the Liouville sign of an integer whose real sign is deterministic and whose size is ≈ 10^{1.1266 n²}; the coding says nothing about its prime factors, and Problem H is unaffected.
