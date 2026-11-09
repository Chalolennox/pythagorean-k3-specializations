# The index-four obstruction: a proof, the face identity, and what it says about partially split primes (revised 9 November 2026, third revision)

Written by Claude (a language model) from a conjecture supplied by the person directing the project. The algebra is verified exactly in sympy; the statements are tested on 2 382 primes (original T_p) and 9 664 primes (S_p) up to 1.2·10⁹, and the partial-split statements on 6 903 primes below 1.5·10⁵. No human referee has read it. Code: `code/verify_square_class_identity.py` (7 s), `code/verify_partial_split.py` (40 s), `code/verify_local_sign.py` (1 s), `code/verify_index_four.py` (2 s), `code/index_four/`.

**Convention.** This note uses f(t) = t⁶ − 30t⁴ − 24t² − 1 (the sextic of the paper), which is the negative of the polynomial F(t) = −t⁶ + 30t⁴ + 24t² + 1 of the original conjecture: F = −f, F(1) = 54, F(i) = 8, f(1) = −54, f(i) = −8. Consequently f(t) = −h(t)h(−t) here is F(t) = h(t)h(−t) in the F-normalization, uv = −f(1) = F(1) = 54 and wx = −f(i) = F(i) = 8 in both, and the complementary face h′(t) = −h(−t) satisfies h′(t)h′(−t) = h(t)h(−t) = F(t), so every identity below is sign-consistent with either normalization (checked in `verify_square_class_identity.py`). The roots of f and F coincide, so all statements about roots, characters and candidates are unaffected.

## 0. What changed since the first revision

* **The proof of the identity is now elementary.** The Type I identity is a *polynomial identity in a and b* (no relation between them is needed) plus the single value f(i) = −8; Type II follows from Type I applied to the complementary face, and the factor 3 is explained by f(1)f(i)(1 + i)² = 864i = 3·(12(1 + i))². The quartic Q_c is not needed for the proof (§2).
* **The specialization needs only a Frobenius-stable face**, so the identity holds in every Frobenius class that has one (§5). The class (1,1,2,2) splits into two kinds, with 4 and 0 stable faces.

## 1. Definitions, and the structure of the argument

C : y² = x³ − 2x² + 2x, P = (1, 1), f(t) = t⁶ − 30t⁴ − 24t² − 1 = g(t²), g(s) = s³ − 30s² − 24s − 1; roots come in pairs ±τ_j. χ is the Legendre symbol; for p ≡ 1 (mod 4), i² = −1 and η = χ(1 + i). For a root t in 𝔽_p:

* **T_p** (original): number of roots with χ(2t(1 − t²)) = 1 and χ((1 − t)(1 + t²)) = 1, arguments nonzero. (Since ab = 2v⁴t(1 − t²) for t = u/v, the first condition says (ab/p) = +1, that is the local sign w_p = −(ab/p) of §4.1 is −1.)
* **S_p**: 1 − t a nonzero square and χ((1 − t)(1 + t²)) = 1.
* d_p = [C(𝔽_p) : ⟨P⟩]; D_p = number of the six candidate points (x = 1 − t) lying in 2C(𝔽_p).

**Part G** (group theory, independent of the rest; p ≡ 1 mod 8): ⟨P⟩ ⊆ 2C, and d_p/4 odd ⇔ η = −1. **Part A** (face identity): for every Frobenius-stable face F, χ(ε_F)·η·∏_{r∈F}χ(1 − r)χ(r + i) = 1. **Part T**: T_p = 6 ⇒ S_p = 6, p ≡ 1 (mod 24), and χ(r) = χ(1 − r) = χ(1 + r) = χ(1 + r²) = 1 at all six roots. **Part D**: D_p = 2·#{j : χ(τ_j + i) = 1}. **Conclusion**: (−1)^{D_p/2} = −η, and d_p = 4 ⇒ η = −1 ⇒ D_p ≤ 4.

## 2. The face identity, with the coefficient comparison written out

**Faces.** A *face* F is a set of three roots of f containing exactly one root of each pair ±τ_j (8 faces). Put h(t) = h_F(t) = ∏_{r∈F}(t − r) = t³ + at² + bt + c, so a = −Σ_{r∈F} r, b = Σ r r′ over pairs in F, c = −∏_{r∈F} r. Since (∏_{r∈F} r)² = ∏ s_j = −g(0) = 1, c = ±1: **type I** (c = +1) or **type II** (c = −1); F ↦ −F exchanges them.

**Coefficient comparison.** Write h(t) = (at² + c) + (t³ + bt), h(−t) = (at² + c) − (t³ + bt). Then h(t)h(−t) = (at² + c)² − (t³ + bt)² and

 −h(t)h(−t) = t⁶ + (2b − a²)t⁴ + (b² − 2ac)t² − c².

The roots of h(−t) are the negatives of those of h, so f(t) = −h(t)h(−t), and comparison with f gives c² = 1, 2b − a² = −30, b² − 2ac = −24. Eliminating b = (a² − 30)/2: Q_c(a) = a⁴ − 60a² − 8c·a + 996 = 0. This is all that specialization uses: *any* monic cubic h over a field k (char ≠ 2, 3) with f(t) = −h(t)h(−t) in k[t] has c = ±1, and if k ⊆ 𝔽_p it is the face polynomial of a Frobenius-stable face; a, b, c are then elements of 𝔽_p, no roots of f need lie in 𝔽_p.

**Two evaluations.** Let u = h(1), v = h(−1), w = h(i), x = h(−i). From f = −h(t)h(−t): **uv = −f(1) = 54** and **wx = −f(i) = 8** (f(1) = −54, f(±i) = −8). Since ∏_{r∈F}(1 − r) = u and ∏_{r∈F}(r + i) = −x, we have ∏_{r∈F}(1 − r)(r + i) = −ux.

**Type I (c = 1).** Then u = 2 + a + b, v = a − b, w = (1 − a) + i(b − 1), x = (1 − a) − i(b − 1). Put W = ((1 + i)u + (1 − i)v)/2 = (1 + a) + i(1 + b). With a, b free (checked by expansion):

 W² + (1 + i)·u·x + i·(w x − 8) = 0.

Hence, since wx = 8, **(1 + i)·∏_{r∈F}(1 − r)(r + i) = −(1 + i)ux = W²** with W = (1 + a) + i(1 + b) = (i/2)(a² − 2ia − 28 − 2i) (using b = (a² − 30)/2). Hand check: expanding W² and −(1 + i)ux both gives iu² − 4iu + uv after substituting x = 2 + 2i − W.

**Type II (c = −1).** The complementary face F′ = −F has h′(t) = −h(−t), c′ = +1, (a′, b′) = (−a, b), W′ = (1 − a) + i(1 + b), and h′(1) = −v, h′(−i) = −w, h′(i)h′(−i) = wx = 8. The type I identity for F′ reads W′² = −(1 + i)vw. Multiplying, (−3(1 + i)ux)·W′² = 3(1 + i)²·(uv)(wx) = 3·2i·54·8 = 2592i = (36(1 + i))², hence

 **3(1 + i)·∏_{r∈F}(1 − r)(r + i) = −3(1 + i)ux = (36(1 + i)/W′)²**, W′ = (1 − a) + i(1 + b) (W′ ≠ 0 because W′² = −(1 + i)vw and v, w ≠ 0).

The factor 3 is thus the squarefree part of (1 + i)²f(1)f(i) = 864i = 3·(12(1 + i))²: it comes from f(1) = −54 = −2·3³. Type I uses only f(i) = −8.

(The exact forms in ℚ[a, i]/(Q_c) are w_I = (i/2)(a² − 2ia − 28 − 2i), w_II = (i/6)(a³ + a² − 32a − 24 − 54i); they agree with the above modulo Q_c.)

**Specialization.** Take p ≥ 5, p ≡ 1 (mod 4), and any Frobenius-stable face over 𝔽_p, that is a cubic h ∈ 𝔽_p[t] with f = −h(t)h(−t). The polynomial identities above hold in 𝔽_p for the actual values of a, b, c, for either square root of −1; wx = 8 and uv = 54 hold because f = −h(t)h(−t) in 𝔽_p[t]. So, with ε = 1 (type I) or 3 (type II): ε(1 + i)·(−h(1)h(−i)) is a square in 𝔽_p, i.e.

 **χ(h(1)·h(−i)) = χ(1 + i)·χ(ε)** (p ≡ 1 mod 4, χ(−1) = 1). (A′)

If all six roots lie in 𝔽_p, h(1) = ∏_{r∈F}(1 − r) and h(−i) = −∏_{r∈F}(r + i), and (A′) is **Theorem A**: ∏_{r∈F}χ(r + i) = η·χ(ε)·∏_{r∈F}χ(1 − r).

## 3. Descent lemmas (explicit)

**Lemma 1.** Let p ≡ 1 (mod 8), r₁ = 0, r₂ = 1 + i, r₃ = 1 − i, so C : y² = (x − r₁)(x − r₂)(x − r₃). The map δ(Q) = (x − r₁, x − r₂, x − r₃) mod squares, with the first/second/third entry at the 2-torsion point (r_k, 0) replaced by the product of the other two differences r_k − r_j, is a homomorphism C(𝔽_p) → (𝔽_p*/□)³ with kernel exactly 2C(𝔽_p) and |C/2C| = 4. With χ(−1) = χ(2) = χ(i) = 1, r₂r₃ = 2, r₂ − r₃ = 2i, χ(r₂) = χ(r₃) = η:

* T₀ = (0, 0): δ = ((r₁ − r₂)(r₁ − r₃), r₁ − r₂, r₁ − r₃) = (2, −(1 + i), −(1 − i)) → (1, η, η);
* T₁ = (r₂, 0): δ = (r₂ − r₁, (r₂ − r₁)(r₂ − r₃), r₂ − r₃) = (1 + i, (1 + i)·2i, 2i) → (η, η, 1);
* T₂ = (r₃, 0): δ = (r₃ − r₁, r₃ − r₂, (r₃ − r₁)(r₃ − r₂)) = (1 − i, −2i, (1 − i)(−2i)) → (η, 1, η);
* P = (1, 1): δ = (1, −i, i) → (1, 1, 1).

Hence ⟨P⟩ ⊆ 2C. If η = +1, C[2] ⊆ 2C; if η = −1, δ is injective on C[2], so C[2] ∩ 2C = 0 and 2C has odd order. Consequently d_p/4 = [2C : ⟨P⟩] is odd ⇔ η = −1 (if η = −1, 2C has odd order; if η = +1, 2C ⊇ C[2] ≅ (ℤ/2)² is not cyclic, so [2C : ⟨P⟩] is even), and d_p = 4 ⇒ ⟨P⟩ = 2C cyclic ⇒ η = −1. (Checked at all 4 466 primes p ≡ 1 mod 8 below 2·10⁵.)

**Lemma 2 (character formula for D_p).** Let t be a root of f with (1 − t)(1 + t²) a nonzero square and χ(1 − t) = 1, x = 1 − t. Then x − r₂ = −(t + i), x − r₃ = −(t − i), and χ(x)χ(x − r₂)χ(x − r₃) = χ(y²) = 1 with χ(x) = 1 give χ(t + i) = χ(t − i). So the point is in 2C ⇔ χ(t + i) = 1. For −t one has x′ = 1 + t, x′ − r₂ = t − i, hence the same character: the candidates ±τ_j are both in 2C or both not, and D_p = 2·#{j : χ(τ_j + i) = 1}.

## 4. T_p = 6 ⇒ S_p = 6, and the conclusion

**Part T.** If all six roots satisfy both conditions, then at t and −t: χ(1 − t) = χ(1 + t) = χ(1 + t²) =: α, so χ(1 − t²) = 1. From f(t) = 0, (1 − t²)³ + 27t²(1 + t²) = −f(t) gives χ(1 − t²) = χ(−3)χ(1 + t²), so α = χ(−3). The conditions χ(2t(1 − t²)) = 1 at t and −t give χ(2t) = 1 = χ(−2t), so χ(−1) = 1 and χ(t) = χ(2). Since (τ₁τ₂τ₃)² = 1: 1 = χ(τ₁τ₂τ₃) = χ(2)³, so χ(2) = 1 (p ≡ 1 mod 8), χ(τ_j) = 1. Finally ∏(1 + s_j) = −g(−1) = 8 gives α³ = χ(8) = 1, so α = 1, χ(−3) = 1, p ≡ 1 (mod 3). So p ≡ 1 (mod 24) and all four characters are +1 at all six roots; in particular S_p = 6.

**Conclusion.** Theorem A with all χ(1 − r) = 1 gives ∏_j χ(τ_j + i) = η; with k = D_p/2, (−1)^{3 − k} = η, i.e. **(−1)^{D_p/2} = −η**. If d_p = 4, Lemma 1 gives η = −1, so k is even, k ≠ 3 and **D_p ≤ 4**; also ⟨P⟩ = 2C, so H_p = D_p. ∎

## 5. Partially split primes

**Frobenius classes.** The Galois group of f is W(D₃) ≅ S₄ (signed permutations of the three pairs with an even number of sign changes), acting on the six roots. Its classes, with the number of Frobenius-stable faces (the checked columns of `verify_partial_split.py`):

| cycle type of f mod p | density | stable faces | rational roots |
| --- | --- | --- | --- |
| (1,1,1,1,1,1) | 1/24 | 8 | 6 |
| (1,1,2,2), kind **B**: g has exactly one root mod p, f = (t² − s₁)·q(t)·q(−t) | 6/24 | 4 | ±τ |
| (1,1,2,2), kind **A**: g splits completely, s₁ a square, s₂, s₃ not (t² − s₂, t² − s₃ irreducible) | 3/24 | 0 | ±τ |
| (3,3): f = −h(t)h(−t), h irreducible cubic | 8/24 | 2 | none |
| (2,4) | 6/24 | 0 | none |

Observed on 6 903 primes p ≡ 1 (mod 4) below 1.5·10⁵: 0.039, 0.257, 0.123, 0.333, 0.248, against 0.042, 0.250, 0.125, 0.333, 0.250. (A′) holds as an equality of residues at all 13 830 stable cubic factors in all classes.

**What this gives for rational roots.** A prime can divide F_n only if f has a root mod p (t_n ≡ root), so only the classes with rational roots matter for H_p: 1⁶, (1,1,2,2)A, (1,1,2,2)B (together 10/24 of the primes). For a root t at which (1 − t)(1 + t²) is a nonzero square, put u(r) = χ(1 − r)χ(r + i).

* **R1** (any p ≥ 5; from f(t) = 0 alone, for a root with (1 − t)(1 + t²) a nonzero square): χ(1 + t) = χ(−3). Consequence for the local sign: see §6.
* **R2** (p ≡ 1 mod 4; from f(t) = 0 alone, any class with a rational pair): u(τ)u(−τ) = χ(3). So at p ≡ 1 (mod 24) the two rational candidates behave alike, and at p ≡ 17 (mod 24) at most one of them can lie in 2C, hence in ⟨P⟩. Observed (p ≡ 1 mod 8): at p ≡ 1 mod 3 the number of rational roots in 2C is even for the pair (0 or 2); at p ≡ 2 mod 3 it is 0 or 1, in both kinds of (1,1,2,2).
* **R3** (kind B, uses the face identity): for the face (t − r₀)q(t), r₀ = ±τ: u(r₀) = η·χ(ε)·χ(q(1)·q(−i)), where q(1)q(−i) = N(1 − ρ)N(ρ + i) for a root ρ of q; that is, u(r₀) is the quadratic character of (1 − ρ)(ρ + i) in 𝔽_{p²}. (Checked at 3 542 rational roots.)
* **Kind A**: no stable face, hence no relation beyond R1 and R2.

**Honest assessment.** R3 expresses the descent character of a rational candidate through the cofactor q, but both sides are directly computable, so it gives **no new restriction on H_p beyond 2-descent**: Q_{r₀} ∈ 2C is already decided by χ(1 − r₀) and χ(r₀ + i). A necessary condition for r₀ ∈ H_p (p ≡ 1 mod 8) is u(r₀) = 1, equivalently χ(q(1)q(−i)) = ηχ(ε); this is a consistency statement, not a sieve. The restriction that is genuinely structural is R2, which does not use faces at all. The full-split theorem is a statement about 1/24 of the primes; it does not extend to a statement about the six-fold pattern when only two roots are rational.

## 6. The local sign at a candidate prime

**Definition.** Let t = u/v in lowest terms (the point is t_n = U_n/V_n, or t′_n for the translated orbit) and p ≥ 5 a prime with p | F(u, v) = u⁶ − 30u⁴v² − 24u²v⁴ − v⁶; then p ∤ v and τ := t mod p is a root of f in 𝔽_p. By §4.1 of the paper the local root number of E_t at p (multiplicative reduction) is w_p = −(−c₆/p) = −(ab/p), with a = v² − u², b = 2uv. Define **σ_p := −(ab/p)**; this is the *split-multiplicative criterion* (σ_p = −1 iff the reduction is split).

**Proposition.** For every prime p ≥ 5 dividing F(U_n, V_n) (orbit nP), and every prime p ≥ 5 dividing F(U′_n, V′_n) (orbit nP + T, t′_n = 1 − x(nP + T) = 1 − 2/x(nP)):

 σ_p = −χ_p(−6)·χ_p(t_n) (orbit nP),  σ_p = −χ_p(−3)·χ_p(t′_n) (orbit nP + T).

For p ≡ 1 (mod 8) both constants equal χ_p(3) (χ(−1) = χ(2) = 1), which is the formula σ_p = −χ_p(3)χ_p(t); the proposition holds for *all* p ≥ 5, with no congruence condition and without using 2C.

**Derivation from the criterion (orbit nP).** (i) ab = (v² − u²)·2uv ≡ 2v⁴·τ(1 − τ²) (mod p), so (ab/p) = χ(2τ(1 − τ)(1 + τ)). (ii) x = 1 − t_n = x(nP) is a rational square (F.18) with denominator prime to p, and τ ≠ 1 (f(1) = −54), so χ(1 − τ) = 1. (iii) The point nP gives y² = x(1 + t²) with y p-integral, so χ(1 + τ²) = χ(x) = 1 (1 + τ² ≠ 0 since f(±i) = −8). (iv) From f(τ) = 0 and the identity (1 − t²)³ + 27t²(1 + t²) = −f(t): χ(1 − τ²) = χ(−3)χ(1 + τ²) = χ(−3), hence χ(1 + τ) = χ(−3). (v) Therefore (ab/p) = χ(2)χ(τ)·1·χ(−3) = χ(−6)χ(τ). For the orbit nP + T: x′ = 2/x is 2 times a square, so χ(1 − τ′) = χ(2) and χ(1 + τ′²) = χ(2); then χ(1 − τ′²) = χ(−3)χ(2), χ(1 + τ′) = χ(−3), and (ab/p) = χ(2)χ(τ′)χ(2)χ(−3) = χ(−3)χ(τ′).

**Checked** (`code/verify_local_sign.py`): the formulas agree with −(ab/p) at all 33 + 35 primes of the complete factorizations (n = 2..12) and at all 52 + 38 primes p < 3·10⁵ dividing F(U_n, V_n), n = 2..40; every residue class mod 24 that can occur does occur.

**What it is and is not.**

* **It is a statement about one candidate.** σ_p depends only on p and on the root τ = t_n mod p that the orbit hits; n enters only through which root is hit. It gives the local contribution of an individual candidate.
* **Relations among candidates.** For a pair ±τ, χ(−τ) = χ(τ) if p ≡ 1 (mod 4), so the two candidates (when both are candidates) have the *same* sign; if p ≡ 3 (mod 4) the signs are opposite. That is all: there is no relation between different primes, different n, or different roots τ_j, τ_k of the same prime.
* **It is a reformulation of (ab/p), not new information.** For the whole number, K_n = (ab/M) = ∏_{p | N_n} χ_p(−6τ)^{e_p} = (−6t_n / N_n), the Jacobi symbol that Appendix B evaluates (period six), and W_n = f(t_n)·∏_{p | N_n distinct}σ_p = ε_n·(−1)^{ω(N_n)}·η_n with η_n = ∏_{e_p even}(ab/p): the decomposition of F.24. The proposition rewrites the factors of η_n and of the odd-exponent part in terms of the single character χ_p(t_n); it does not touch the parity of ω(N_n) or the value of η_n, which is exactly the part that Problem H leaves open. To use it one would need control of χ_p(t_n) over the primes dividing F_n, which is the original problem.
* **The face identity is not needed for it.** The proposition follows from f(τ) = 0 and the descent fact x(nP) ∈ □; it holds at every candidate whether or not the six roots are in 𝔽_p.

## 7. Is there a norm or resolvent interpretation?

* **The quartic.** With τ₁τ₂τ₃ = −1 the four type I values are a = −(e₁τ₁ + e₂τ₂ + e₃τ₃), e₁e₂e₃ = +1; two of them add up to −2e·τ_j, so (a + a′)² = 4s_j, which is the resolvent relation y = 4s − 60 for the roots y of the resolvent cubic (checked numerically at 50 digits and exactly). Type II values are the negatives. So Q_c is the quartic of the sign sums ±τ₁ ± τ₂ ± τ₃, the two types being the two parities of sign patterns. Also u = h(1) satisfies u⁴ − 8u³ + 2916 = 0 (exactly), and (2916 = 2²·3⁶).
* **Norm form.** ∏_{r∈F}(1 − r)(r + i) = N_{L/K}((1 − r)(r + i)) for L = K[t]/h_F; since N∘res = cube, nothing is gained from this alone.
* **What the elementary proof says.** All the content is in the four values of h at the fourth roots of unity 1, −1, i, −i (the roots of t⁴ − 1): for c = 1 the two real values determine the two imaginary ones (x = 2 + 2i − W), the norms uv = 54 and wx = 8 come from f, and the combination (1 + i)u·x is a square exactly when wx = 8. In descent terms (x = 1 − r, x − r₂ = −(r + i), r₂ = 1 + i): the identity says ∏_{r∈F} x_r(x_r − r₂) ≡ r₂ modulo squares in ℚ(a, i) (type I), so the first two descent coordinates of the three candidate points of a face multiply to the class of the 2-descent root r₂. I have no explanation of why this should hold beyond the derivation above; in particular it is a statement about square classes, not a relation among points (no sum Q(τ₁) ± Q(τ₂) ± Q(τ₃) is 2-torsion, checked at 30 primes).

## 8. Evidence for the theorem

| definition | primes (p ≤ 1.2·10⁹) | Part A, parity law, "d_p/4 odd ⇔ η = −1" | d_p = 4 | D_p at d_p = 4 | D_p = 6 | D_p over all |
| --- | --- | --- | --- | --- | --- | --- |
| T_p = 6 (original) | 2 382 | all 2 382 | 910 (η = −1 at all) | 4: 702, 0: 208 | 250, all with 8 \| d_p | 0: 278, 2: 920, 4: 934, 6: 250 |
| S_p = 6 | 9 664 | all 9 664 | 3 670 (η = −1 at all) | 4: 2 772, 0: 898 | 1 165, all with 8 \| d_p | 0: 1 224, 2: 3 585, 4: 3 690, 6: 1 165 |

Among the first 28 primes with T_p = 6 (up to 1.5·10⁷), d_p = 4 occurs at ten primes with D_p ∈ {0, 4}. Group orders by baby-step giant-step (unique in the Hasse interval, confirmed against five random points).

## 9. Limits

* The number of roots mod p of f and the class (1,1,2,2)A/B are determined by g; the face-count table is a computation in W(D₃) and was checked against the data, not derived from first principles beyond that.
* Not covered: primes p ≡ 7 (mod 24) (S_p = 6 occurs but [C : 2C] = 2; T_p = 6 never occurs there).
* Nothing here changes the status of Problem H: the local sign formula of §6 is a reformulation of the split-multiplicative criterion.
