# Candidate paper text (applied to paper/paper.md on 14 November 2026 at the repository owner's request: (a) in F.25(b), (b) in F.26(e), (c) as a remark after F.54 (d); (d) not applied)

## (a) Sentence for F.25(b)
The factor at the primes p ≥ 5 dividing c cancels in the pair: the primitive triple of t′ = R(t) is (−b, −a, c), so v_p(c) is the same for t and t′ and w_p(E_t)w_p(E_{t′}) = (2/p)^{2v_p(c)} = 1 (Appendix B); likewise (2/c) cancels. With F.28 the displayed product formula for W(E_{t_n})W(E_{t′_n}) is therefore unconditional. *(Proved from F.28 and Appendix B; checked on 1958 pairs, code/verify_paired_root_numbers_note.py.)*

## (b) Sentence for F.26(e)
With z = 2 − u the quotient sextic gives the genus-2 curve y² = −R(2−z)/2 = −P(z), P = 27z⁶ − 999z⁴ − 2030z³ − 1365z² − 312z − 32, disc P = 2¹⁰·3¹⁸·23²·519521²; by Faltings only finitely many rational z make Δ(E_t)Δ(E_{t′}) = −2²²P(z)/z⁶ a square. This concerns the displayed discriminants only and does not constrain the signs. *(Proved; identity checked at 300 rational t.)*

## (c) Remark after F.54: angular symmetry of the limit measure
Let m be Haar measure on C(ℝ) and z(Q) = (1+it)/(1−it), t = 1 − x(Q). Since x(Q+T) = 2/x(Q), one has z(Q+T) = −i·conj z(Q) (O and T are swapped, z(O) = −1, z(T) = i), so the pushforward ν = z_*m is invariant under θ ↦ −θ − π/2, with density 1/(2^{5/4}Ω√(cos(θ/2)cos(θ/2+π/4))) on (−π, π/2). Hence μ_k = ∫z^k dν satisfies μ_k = (−i)^k·conj μ_k; numerically μ₁ = −0.03492019045(1−i), μ₂ = 0.28677307940i, μ₃ = −0.25037057779(1+i), μ₄ = 0.22436879093. Because P has infinite order, (1/N)Σ z(nP)^k → μ_k. This is the half-turn λ(T) = Ω/2 seen on the circle; it is a statement about the limit measure only: nP and nP+T lie in different cosets of ⟨P⟩, so nothing follows pointwise and no root-number identity is implied. *(Symmetry Proved; moments Computed, code/verify_angular_symmetry.py.)*

## (d) Not proposed
The natural-boundary proposition (see REVIEW_2026-11-14_global_sign_natural_boundary_note.md) is not proposed for inclusion.
