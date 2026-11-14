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
paper/paper.md                 the paper (snapshot export, revision 236)
paper/figures/                  Figure B.1 as PNG and PDF (paper.md shows images as a text placeholder; paper.pdf contains the figure)
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
code/verify_chebotarev_mod8.py        checks of the Chebotarev mod-8 draft on every prime p = 7 mod 8 below 3e5 (notes/REVIEW_2026-11-12_chebotarev_mod8_density.md)
code/check_problem_h_definition.py   checks that Problem H is defined the same way in README.md, STATE.md and the paper
code/figure_p_plus_t_orbit.py   draws Figure B.1 (orbit of P + T on the unit circle); --check runs only its exact computation and assertions
code/verify_fourfold_separation.py   F.50 (ii): four-way coprimality of the values along 1 -+ x(nP), 1 -+ 2/x(nP) (resultants, orbit test, brute force)
code/mirror_projection_eps.py   F.50 (iii): periodic part of the sign along the four sequences (proved laws as control; rotation law of the mirror sequences)
code/verify_mirror_collapse.py   F.51 (b): finite exact verification of eps = h(n) s_n along 1 + x(nP), 1 + 2/x(nP) for all n (--quick for CI)
code/verify_rotation_coding.py   F.51 (a), (c): rotation coding of sign F_s from the elliptic-logarithm definitions, exact consequences (--quick for CI)
code/verify_twist_rank_over_F5.py   F.49: point counts over F_5^k, Frobenius polynomials of the genus-0 twists (embeds and compiles its C counter; needs gcc)
code/verify_integral_resolution_note.py   F.49: audit of the smooth model of S^d over Z_(5), twist selected by TWIST_D (default t(t-1))
data/point_counts_*.jsonl      point counts N_1..N_4 for the covers
STATE.md                       where the research stands and what to do next (start here to resume)
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
