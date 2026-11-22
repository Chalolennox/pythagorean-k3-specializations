# pythagorean-k3-specializations

Elliptic curves **y² = x³ + 4Ax − 8B**, where (A, B) is a rational point of the unit circle (a Pythagorean triple), form an elliptic **K3 surface** over the projective line. This repository holds the working paper, the code and the data of a study of their conductors, root numbers and rank jumps, and of one open problem, **Problem H: is the root number W(E_{t_n}) = +1 for infinitely many n along the orbit t_n = 1 − x(nP)?** By the 2-parity theorem, a yes would give infinitely many members of rank ≥ 2 or infinite Sha[2^∞], and rank ≥ 2 if Sha[2^∞] is finite (paper §6).

> **Project status (7 November 2026): open problem; project paused; this repository is a reproducible record of what was tried.** Problem H is not solved, and no work is in progress. Start with [`STATE.md`](STATE.md): it says what is proved, what was tried and closed, and what has not been tried.

> **Status.** LLM-assisted research notes, code and data. **Partly unverified. Not peer reviewed.** The research and the write-up were done with large language models working with the person who directed the project: Claude (Anthropic) wrote the text, code and proofs, and OpenAI ChatGPT and DeepSeek were also used for research (exploring ideas and searching the literature); nothing they suggested is treated as verified unless the paper says that it was checked. Read the section "Limitations and provenance" of the paper before relying on any result.

## What is established, and what is not

| Result | Status | Where in the paper |
| --- | --- | --- |
| The surface has Picard number 16 and generic rank 0; conductor and Kodaira types of E_t for every rational t | Proved | §2, §3 |
| The global root number W(E_t) for every rational t, in closed form | Proved | §4, F.28 |
| Along the orbit, the sign of the root number is periodic (period 6 along nP, period 3 along nP + T) up to one parity bit; valuations at 2 and 3 are explicit | Proved | Appendix B, F.20–F.22 |
| Problem H is equivalent to one parity statement about the number of prime factors of F_n | Proved | F.24, F.40 |
| No identity of rational functions relates the values F_n; no second section exists on 18 constant-x covers examined | Proved / Conditional | F.19, F.34, F.36, F.41, F.44–F.46 |
| No section of the shape X = X_P + λN_c² on the twist of any constant-x cover with rational c (other shapes are not covered) | Certified | F.47 |
| Conjectured patterns of the parity bit (period 4; δ_2n = δ_n) | Refuted by factorizations up to 163 digits | F.31–F.38 |
| For fixed distinct rational a, b, only finitely many t have rational points at both x = a and x = b (genus 2 or 3 fibre product) | Proved | F.48 |
| **Problem H: W(E_{t_n}) = +1 for infinitely many n** | **Open** | Appendix B, F.24 |
| Infinitely many members of rank ≥ 2 | Open; follows from Problem H if Sha[2^∞] is finite (unconditionally, Problem H gives rank ≥ 2 or infinite Sha[2^∞]) | §6, §9 |

The labels are those of the paper: Proved, Certified, Observed, Conditional, Open. "Conditional" results depend on stated hypotheses (for example the Tate conjecture for K3 surfaces over finite fields).

## Repository layout

```
paper/paper.md                 the paper (snapshot export, revision 305; see paper/REVISION)
paper/REVISION                 the revision number of paper.md (single source; code/check_revision.py checks README.md and STATE.md against it)
paper/paper.pdf                built from paper.md by CI (.github/workflows/paper-pdf.yml) on every push to main; do not edit or supply it by hand
paper/pdf-build/                   the PDF build: build_pdf.sh (pandoc + WeasyPrint, figure substitution, glyph check) and paper.css
paper/figures/                  Figure B.1 as PNG and PDF; figures.txt maps the figure placeholders of paper.md to these files for the PDF build
code/fibrecount.c              point counts on the fibres of the twist surface over F_(p^k)
code/lfunc.py                  from the counts to the Picard number and the discriminant class
code/validate.py               reproduces the validation table of Appendix G
code/verify_factorizations.py  re-checks every factorization in data/
code/scripts_as_run/           the working scripts behind individual claims (not cleaned; see its README)
code/curated/                  ten CAS scripts (reconstructed, not executed) and a Python check of their checkable parts
data/factorizations.json       prime factorizations along both orbits, up to 163 digits
notes/                         research notes from collaborators, each with a review
code/verify_local_i0star.py    symbolic check of the 7 Nov 2026 note on the I0* fibres
code/verify_fibre_configuration.py   exact check of the fibre configuration of S_c for every rational c (F.43, F.47)
code/verify_two_cover_note.py   checks of the two-cover note (notes/REVIEW_2026-11-07_constant_x_two_cover_note.md)
code/verify_square_class_identity.py  exact check of the face identity and of its specialization mod p (notes/index_four_obstruction.md)
code/verify_partial_split.py          the identity in every Frobenius class of f mod p, and the rational-root relations R1-R3
code/verify_index_four.py             scan of the parity law and the index-four obstruction (counts T_p and S_p)
code/verify_local_sign.py             closed form of the local sign at the primes dividing F_n (both orbits)
code/index_four/                      C scanner (scan.c) and point-counting helper (curve.py) used by the scripts above
code/verify_reviewer_context.py   recomputation of the data in the independent reviewer's files (notes/REVIEW_2026-11-07_independent_reviewer_context.md)
code/ec.py                     exact elliptic-curve arithmetic and canonical heights (used by verify_reviewer_context.py and curated/check_curated_python.py)
code/verify_18P_note.py               checks of the 18P memorandum (notes/REVIEW_2026-11-11_18P_symmetry_note.md; finds an index shift in its sign factor)
code/odd_order_density.c              density of primes where P = (1,1) has odd order, vs. Liang-Rouse (notes/odd_order_density_check.md; not in CI)
code/tau_image/                       2-adic image of the Kummer representation of P and the exact odd-order density (Python, replaces Magma; see its README; not in CI)
data/odd_order_classes_C_P_1e8.txt    odd-order counts of P by class of p mod 8, 16, 32, 64 (primes up to 1e8)
data/gap_coincidences_p300000.txt   coincidences of qualifying indices at the gaps 1..12 for all primes up to 300000 (output of code/scan_gaps.c)
data/root_number_crosscheck_pari.txt   PARI/GP root numbers of 877 curves E_t, input of code/root_number_crosscheck.py --check
code/verify_chebotarev_mod8.py        checks of the Chebotarev mod-8 draft on every prime p = 7 mod 8 below 3e5 (notes/REVIEW_2026-11-12_chebotarev_mod8_density.md)
code/check_problem_h_definition.py   checks that Problem H is defined the same way in README.md, STATE.md and the paper
code/figure_p_plus_t_orbit.py   draws Figure B.1 (orbit of P + T on the unit circle); --check runs only its exact computation and assertions
code/verify_fourfold_separation.py   F.50 (ii): four-way coprimality of the values along 1 -+ x(nP), 1 -+ 2/x(nP) (resultants, orbit test, brute force)
code/mirror_projection_eps.py   F.50 (iii): periodic part of the sign along the four sequences (proved laws as control; rotation law of the mirror sequences)
code/verify_orbit_laws.py   F.53: the period laws along nP and nP + T for all n >= 2 (Lemma R, Lemma L, four real-sign classes; --quick for CI)
code/verify_angular_symmetry.py   z(Q+T) = -i conj z(Q) on C, explicit Haar density on the circle, moments mu_1..mu_4 (notes/REVIEW_2026-11-14_angular_symmetry_note.md)
code/verify_paired_root_numbers_note.py   audit of the paired-root-numbers draft, 19 checks (notes/REVIEW_2026-11-14_paired_root_numbers_note.md; uses root_number_formula.py)
code/verify_F_collisions.py   F.54 remark: F(t)-F(u) factorisation, Q = 0 parametrisation, proof that F°(t_n) are pairwise distinct (explicit constants + finite check), direct search for repeated values (notes/REVIEW_2026-11-16_F_collision_side_study.md; --quick for CI)
code/verify_2adic_law.py       F.55: the 2-adic law v2(F_n - F_m) = 1 + v2(n^2 - m^2), the arithmetic of psi_n (parity, v2, coprimality) and the interface inequalities of the proof (notes/REVIEW_2026-11-16_2adic_law_F55.md; --quick for CI)
code/verify_jacobi_identities.py  F.56: coprimality of ab with F, the parity functions h_n and h~_n (h_n h~_n = (-1)^D_n), the reciprocity form of (ab/N_n), and the scan of p^2 | F_n (notes/REVIEW_2026-11-16_F56_parity_functions_and_proposal.md; --quick for CI)
code/verify_consecutive_qualifying.py  F.57: the relation between t_n and t_{n+1}, the resultant, the orbits modulo 7, 103, 113, 13085561 and the counts of primes with a qualifying root (notes/REVIEW_2026-11-17_problem_h_dossier.md; --quick for CI)
code/verify_gap_two.py  gap two: the relation between t_n and t_{n+2}, its exact norm, the orbits modulo 47, 947, 18637, 36997, the prime 2325076196570957, the sieve at n = 4683, 4685 and the scan of all primes below 10^4 for gap-one and gap-two coincidences (notes/REVIEW_2026-11-17_gap_two_dossier.md; --quick for CI)
code/verify_gap_three.py  gap three and all gaps: the relation G3 between t_n and t_{n+3}, its exact norm, the dossier's resultant, the local tests at the nine candidate primes (with a Pocklington certificate for the largest), the scan of all primes below 10^4 for gap-one, gap-two and gap-three coincidences, the premises of the theorem 'no geometric exceptional gaps' and the universal correspondence Phi_{u_k} for every gap (notes/REVIEW_2026-11-17_gap_three_dossier.md; --quick for CI)
code/verify_gap_k.py  gaps k = 4..7 from the universal correspondence: exact norms and their factorizations, primality certificates, local group-law tests at every prime found, orbit indices of the coincidences, scan of all primes below 10^4 for gaps 1..12, why 47, 83, 113 divide O_k for two gaps each, and the shifted-gcd bound v_p(gcd(F_n, F_{n+k})) <= v_p(N_k) (notes/REVIEW_2026-11-17_gap_k_classification.md; --quick for CI)
code/coq/F28_identities.v  the polynomial identities behind the proof of F.28 (character identity, discriminant, c4, c6, the triple and sextic forms of F, Delta = 2^12 c0^9 F(U,V), F = -54 V^6 mod V^2 - U^2 and -8 V^6 mod U^2 + V^2), checked with ring in Coq and compiled in CI (.github/workflows/coq.yml); the quadratic-character reasoning and Rizzo's tables are not formalized (notes/REVIEW_2026-11-22_F28_coq_identities.md)
code/coq/F28_divisibility.v  F.28 section 3: the divisibility lemmas of the owner's second file and the theorem that a prime p >= 5 dividing F does not divide abc (primality, a^2 + b^2 = c^2, gcd(a,b) = 1 as hypotheses); compiled in CI (notes/REVIEW_2026-11-22_F28_coq_identities.md)
code/coq/F28_reduction.v  F.28 section 3: the owner's conditional reduction (p | F and four assumed facts give p does not divide abc), with a proof that the four facts hold for primes p >= 5 and primitive triples, and the unconditional corollary; compiled in CI (notes/REVIEW_2026-11-22_F28_coq_identities.md)
code/coq/F28_arithmetic.v  F.28 section 3: the owner's consolidated file (identities, divisibility, conditional reduction, cancellation, main arithmetic theorem: a prime p >= 5 dividing F divides none of a, b, c and not c4) plus c4 of the integral model with the powers of c; supersedes the three files above for reading; compiled in CI
code/coq/F28_certificate.v  F.28 section 4: the owner's standalone square-certificate algebra (p | F and p not dividing a give x = abc(-c6) a square mod p; products, congruences) with cancellation (eleventh file) plus the split criterion (ab/p) = +1 iff (-c6/p) = +1 for c a square; the nonvanishing complement is in F28_arithmetic.v; compiled in CI
code/coq/F28_character_comparison.v  F.28 section 4: the owner's twelfth file: (ab) times (-6912 b c) is a square mod p when p | F, and (ab/p) = +1 iff (-6912 b c/p) = +1 as certificates (p >= 5, p not dividing abc); compiled in CI
code/coq/F28_primitive_character.v  F.28 section 4: the owner's thirteenth, integrated file: for a prime p >= 5, a primitive triple and p | F, (ab/p) = +1 iff (-6912 b c/p) = +1 as certificates, with the nondivisibility derived inside; plus the paper's form given c a square mod p; compiled in CI
code/coq/F28_reduction_invariants.v  F.28 section 3: the owner's fourteenth file: for the integral model (A = 4ac^3, B = -8bc^5) c4 = -192ac^3, Delta = -1024c^9 F, p | F gives p | Delta, and p >= 5 not dividing a, c gives p not dividing c4; the combination for primitive triples is F28_integral_model_conditions in F28_arithmetic.v; compiled in CI
code/coq/F28_primitive_reduction.v  F.28 section 3: the owner's fifteenth, integrated file: for a prime p >= 5, a primitive triple and p | F, p | Delta and p does not divide c4 of the integral model Y^2 = X^3 + 4ac^3 X - 8bc^5; the passage to multiplicative reduction is not in Coq; compiled in CI
code/coq/F28_tangent_character.v  F.28 section 3: the owner's seventeenth file: at a double root r of the cubic X^3 + AX + B mod p, (-c6)(3r) is a square certificate (864 B (3r) - (72 r^2)^2 = 2592 r f(r) - 2592 r^2 f'(r)), and (-c6/p) = (3r/p) for prime p; compiled in CI
code/coq/F28_singular_root.v  F.28 section 3: the owner's nineteenth file: p | f'(r) and p not dividing A give p not dividing r, and p not dividing B (for p odd prime); the nonvanishing inputs of F28_nodal_split_criterion (F28_tangent_character.v), the split criterion at a double root with all nonvanishing hypotheses discharged; compiled in CI
code/coq/F28_large_prime_constants.v  F.28 section 3: the owner's twentieth file: a prime p >= 5 does not divide 2, 3, 864 = 2^5 3^3; hence 3r and 864 B are not divisible by p when r, B are not; compiled in CI
code/coq/F28_large_prime_tangent.v  F.28 section 3: the owner's twenty-first, integrated file: prime p >= 5, double root r, p not dividing A: (-c6/p) = (3r/p) as certificates; plus (added) the existence of the integer double root from p | Delta and the combined criterion; compiled in CI
code/coq/F28_discriminant_root.v  F.28 section 3: the owner's twenty-second file: (-3B : 2A) is a double root mod p when p | Delta (scaled identities), with (added) the integral model: Delta = -64 c^9 F and 3 n d = ab (24 c^4)^2; compiled in CI
code/coq/F28_root_transport.v  F.28 section 3: the owner's twenty-third file: transport identities from a rational root q/s to the integer root q u when s u = 1 mod p; compiled in CI
code/coq/F28_candidate_root.v  F.28 section 3: the owner's twenty-fourth file: p | Delta and p | 2Au - 1 give p | f(r), p | f'(r) for r = -3Bu; compiled in CI
code/coq/F28_root_denominator.v  F.28 section 3: the owner's twenty-fifth file: prime p >= 5, p not dividing A gives p not dividing 2A; compiled in CI
code/coq/F28_bezout_inverse.v  F.28 section 3: the owner's twenty-sixth file: p k + 2Au = 1 gives p | 2Au - 1; compiled in CI
code/coq/F28_inverse_existence.v  F.28 section 3: the owner's twenty-seventh file: prime p not dividing s gives u with p | s u - 1 (Z.gcd_bezout); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_discriminant_singular_root.v  F.28 section 3: the owner's twenty-eighth, integrated file: prime p >= 5, p | -4A^3 - 27B^2, p not dividing A gives an integer double root r; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_family_specialization.v  F.28 section 3: the owner's twenty-ninth file: Delta = -64 c^9 F for the model A = 4ac^3, B = -8bc^5; p | F gives p | Delta; p >= 5, p not dividing a, c gives p not dividing A; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_specialized_singular_root.v  F.28 section 3: the owner's thirtieth, integrated file: prime p >= 5, p | F, p not dividing a, c gives an integer double root r of the paper's model; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_tangent_cone.v  F.28 section 3: the owner's thirty-first file: tangent coefficient 3r nonzero mod p, f(r+U) = f(r) + f'(r)U + U^2(U+3r); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_tangent_product_square.v  F.28 section 3: the owner's thirty-second file: p >= 5, p | f(r), p | f'(r) gives certificate(864B * 3r); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_square_class_cancellation.v  F.28 section 3: the owner's thirty-third file: certificate cancellation and the tangent character equivalence; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_square_scaling.v  F.28 section 3: the owner's thirty-fourth file: certificate(x) iff certificate(y) when p | x u^2 - y v^2; certificate(3r) iff certificate(ab) when p | a^2(3r) - (3c)^2(ab); plus (added) the candidate root's class; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_candidate_root_relation.v  F.28 section 3: the owner's thirty-fifth file: a^2(3r) - (3c)^2(ab) = (2Au - 1) * 9abc^2 for r = -3Bu on the integral model; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_two_A_nonzero.v  F.28 section 3: the owner's thirty-sixth file: prime p >= 5, p not dividing a, c gives p not dividing 2A; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_arithmetic_character.v  F.28 section 3: the owner's thirty-seventh file: prime p >= 5, p not dividing a, c gives r with certificate(3r) iff certificate(ab); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_candidate_singular.v  F.28 section 3: the owner's thirty-eighth file: the candidate root 24bc^5u is a double root of the paper's model when p | F; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_integrated_candidate_bridge.v  F.28 section 3: the owner's thirty-ninth, integrated file: the candidate root is a double root and certificate(3r) iff certificate(ab); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_complete_arithmetic_bridge.v  F.28 section 3: the owner's fortieth, integrated file: prime p >= 5, p | F, p not dividing a, c gives a double root r of the paper's model with certificate(3r) iff certificate(ab); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_tangent_directions.v  F.28 section 3: the owner's forty-first file: rational tangent directions of the node iff certificate(3r); f(r+u) = f(r) + f'(r)u + u^2(u+3r); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_tangent_arithmetic.v  F.28 section 3: the owner's forty-second file: with certificate(3r) iff certificate(ab), the node's rational tangent directions iff certificate(ab); tangent cone at (1,0) is -(3r); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_tangent_certificate.v  F.28 section 3: the owner's forty-third file: the 42nd plus p not dividing A, p | f'(r) gives p not dividing r, 3r and the tangent cone at (1,0); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_split_node.v  F.28 section 3: the owner's forty-fourth file: the curve near a double root reads V^2 = U^3 + 3rU^2; 'split node' := rational tangent directions; split iff certificate(ab) given the bridge; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_integral_invariants.v  F.28 section 3: the owner's forty-fifth file: c4 = -192ac^3, c6 = 6912bc^5, Delta = -1024c^9 F for the integral model; p | F and p not dividing 192ac^3 give p | Delta, p not dividing c4; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_large_prime_reduction.v  F.28 section 3: the owner's forty-sixth file: prime p >= 5, p not dividing a, c, p | F gives p | Delta and p not dividing c4 for the integral model; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_stage4_certificate.v  F.28 section 3: the owner's forty-seventh file (Stage 4): prime p >= 5, p not dividing a, c, p | F, p | f'(r): invariant certificate, p not dividing r, 3r, nonzero tangent cone at (1,0); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_stage5_certificate.v  F.28 section 3: the owner's forty-eighth file (Stage 5): the Stage 4 certificate plus split-node certificate iff certificate(3r) and nonzero square representations; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_stage6_certificate.v  F.28 section 3: the owner's forty-ninth file (Stage 6): given the square-class bridge, split node iff certificate(ab) and nonsplit iff not; translation identities; packaging, bridge and invariant certificate are hypotheses; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_unconditional_bridge.v  F.28 section 3: the owner's fiftieth file: for EVERY double root r mod p of the paper's model (prime p >= 5, p not dividing c, 3r, ab): certificate(3r) iff certificate(ab), via a r = 3 b c^2; split/nonsplit node criteria; imports adapted to Coq 8.20; compiled in CI
code/coq/F28_stage7_nodal_reduction.v  F.28 section 3: the owner's fifty-first file (Stage 7): for the paper's model, prime p >= 5, p not dividing a, c, p | F and a double root r: p | Delta, p not dividing c4, ordinary node (p not dividing 3r, 3r tangent coefficient nonzero); imports adapted to Coq 8.20; compiled in CI
code/coq/F28_stage8a_reduced_model.v  F.28 section 3: Stage 8a, written in review by Claude (not an owner file): elementary model of the reduction type via the reduced curve over F_p: minimality criterion (c4 = u^4 c4', p not dividing c4 => p not dividing u), existence and uniqueness of the singular point mod p, node, split iff ab is a square class; no Q_p, no Tate's algorithm, root numbers cited only; compiled in CI
code/coq/F28_stage8_factorization.v  F.28 section 3: the owner's fifty-second file (Stage 8): for any A, B, prime p and r with p | f(r), p | f'(r), p not dividing 3r: f is congruent mod p to (x - r)^2 (x + 2r), second root -2r distinct and simple, tangent cone nonzero (certificate, family instance); import adapted to Coq 8.20; compiled in CI
code/verify_group_G.py  F.57 (b'): the group G of order 24576 built from the three relations among the thirteen radicals, its action on the 48 roots of Rp and the 24 roots of Rm, the character chi2 (the subgroup fixing sqrt 2), the fixed-point-free counts 22035, 19709, 11013, 9854 and the density 20867/24576 (notes/REVIEW_2026-11-17_group_G_sqrt2.md; numpy, about 5 seconds)
code/verify_support_two.py  support-two review: exact discriminants and norms, phi_hat(P') = P, |ker delta| = N_p/2 and the even index [C(F_p):<P>], scan of S_p and R_p below 10^4, the class A / class B split (notes/REVIEW_2026-11-19_support_two.md; standard library, about 6 seconds)
code/support_two_densities.py  the densities 633/4096, 39/512, 321/4096 from the model of G (numpy)
code/support_two_affine_probability.py  the local probability beta_l = (l^3 - l - 1)/(l^2 (l-1)^2 (l+1)) that l divides j_p in the maximal affine model, by brute force for l = 3, 5, 7 (standard library, about 3 seconds)
code/verify_neutrality_circle.py  neutral points on the rational circle: the Magma summary (662 / 174 / 20, 71, 63, 177), the reflection proposition, the sharp congruence, the prime-value families t = 1/(12k) and t = 6w, the orbit checks and the negative result that these families miss the orbit (notes/REVIEW_2026-11-19_neutrality_circle.md; standard library, about 1 second)
code/scan_gaps.c  C scan of all primes up to 3*10^5 for coincidences at the gaps 1..12 (output data/gap_coincidences_p300000.txt; not in CI)
code/density_qualifying_primes.c  F.57 (c): the density of primes without a qualifying root for p < 10^8 (C; not in CI)
code/root_number_formula.py   closed formula of section 4 for W(E_t) as a module; run as a script it checks twelve independent Magma values (n <= 6 along nP and nP + T)
code/root_number_crosscheck.py   compares PARI/Magma root numbers with the closed formula and the reflection formula (F.25 remark; a new PARI or Magma run is needed for new curves, see its docstring; CI re-checks the stored PARI output with --check)
code/verify_mirror_collapse.py   F.51 (b): finite exact verification of eps = h(n) s_n along 1 + x(nP), 1 + 2/x(nP) for all n (--quick for CI)
code/verify_rotation_coding.py   F.51 (a), (c): rotation coding of sign F_s from the elliptic-logarithm definitions, exact consequences (--quick for CI)
code/verify_twist_rank_over_F5.py   F.49: point counts over F_5^k, Frobenius polynomials of the genus-0 twists (embeds and compiles its C counter; needs gcc)
code/verify_integral_resolution_note.py   F.49: audit of the smooth model of S^d over Z_(5), twist selected by TWIST_D (default t(t-1))
code/apparition_pattern.py   F.54: which primes can divide F(t_n): the psi-form, the rank-of-apparition classes N_p, checks against exact values (notes/apparition_pattern_F_n.md)
code/rotation_coding_F_n.py   F.54: the real sign of F(t_n) and G(t'_n) as an exact coding of the rotation by theta: closed forms (k = cos(pi/8)), four real classes, first-return gaps (notes/rotation_coding_sign_F_n.md)
data/point_counts_*.jsonl      point counts N_1..N_4 for the covers
STATE.md                       where the research stands and what to do next (start here to resume)
WORKFLOW.md                    how changes enter this repository (branch and pull request, revision number, figures, code); read before every change
ERRATA.md                      errors found and corrected
CONTRIBUTING.md               how to contribute and the claims policy
```

## Reproducing the computations

```
pip install -r requirements.txt
python3 code/validate.py                  # about a minute; add --full for more primes
python3 code/verify_factorizations.py
```

`validate.py` needs a C compiler (`gcc`). Both scripts exit with status 0 only if every check agrees. They were run on 6 November 2026 in a Linux sandbox; the GitHub Actions workflow in `.github/workflows/` runs them, together with the other verification scripts in `code/`, on every push and pull request.

## How far to trust it

Everything in the paper was produced in conversation with language models, which make characteristic errors: confident wrong statements, references recalled from memory, arguments that look complete but are not. Several occurred and are recorded in `ERRATA.md`. Treat each "Proved" as a claim to be checked by a human, and see the paper's section "Limitations and provenance" for the list of what has not been independently verified.

## Contributing

Corrections, independent verifications and counter-examples are the most useful contributions. Please read `CONTRIBUTING.md`; in particular, say whether any text or code you contribute was written or checked with a language model.

## License

MIT, see `LICENSE`. This covers the code, the data and the text.

## Citation

See `CITATION.cff`.
