# Review of "Angular Haar-measure symmetry for an elliptic-curve orbit" (draft of 14 Nov 2026)

Source text: `drafts/angular_symmetry_proof.md` (verbatim). Checks: `code/verify_angular_symmetry.py`. Labels: symmetry **Proved**; moments **Computed**. **No human has checked this.**

## Verdict
Correct, and small. It is the half-turn identity already in the paper (translation by T is the shift by Ω/2 in the rotation coding; u(2)/Ω = ½ − θ) read through z = (1+it)/(1−it). Worth a short remark, not a theorem.

## What was checked
- z(τ(t)) = −i·conj z(t) holds exactly on 2000 random rationals; x(nP+T)·x(nP) = 2 for n = 1..24 on the actual group law; 2P = (1/4, −5/8).
- The exceptional points are consistent: z(O) = −1, z(T) = i, and −i·conj z(O) = i, −i·conj z(T) = −1, so the involution swaps O and T. This answers reviewer questions 1 and 2.
- Question 3 (Haar, not uniform in θ): the limit of the unsigned orbit averages is Haar measure on the circle group C(ℝ) because P has infinite order; the density in θ is g(θ) = 1/(2^{5/4}Ω√(cos(θ/2)cos(θ/2+π/4))) on (−π, π/2), Ω = 4.0364616539116674; it integrates to 1, satisfies g(θ) = g(−θ−π/2), and reproduces μ₁..μ₄ to 4.5·10⁻¹². Orbit averages for N = 10⁶ are within 1.1·10⁻⁶ of the μ_k. (μ₅ = −0.0047062537 + 0.0047062537i, μ₆ = 0.1750176405i.)
- Question 4: Lutz–Nagell is used correctly (2P non-integral, so 2P and P are not torsion); the paper already proves infinite order, so cite that instead.
- Question 5: the note itself states the distinction correctly: this is a symmetry of the limiting unsigned measure, not pointwise on the finite orbit (nP and nP+T lie in different cosets), and not a root-number identity.

## Recommendation
A remark after F.51/F.54 (the explicit density, the phase rules μ_{4j} real, μ_{4j+2} imaginary, Im μ_{4j+1} = −Re μ_{4j+1}, Im μ_{4j+3} = Re μ_{4j+3}; one line stating that it is a corollary of the half-turn and has no signed analogue). See `drafts/candidate_paper_text_F55.md`.
