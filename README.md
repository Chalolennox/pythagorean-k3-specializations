# pythagorean-k3-specializations

Elliptic curves **y² = x³ + 4Ax − 8B**, where (A, B) is a rational point of the unit circle (a Pythagorean triple), form an elliptic **K3 surface** over the projective line. This repository holds the working paper, the code and the data of a study of their conductors, root numbers and rank jumps, and of one open problem: **are there infinitely many members of rank ≥ 2 along the orbit t_n = 1 − x(nP)?**

> **Status.** LLM-assisted research notes, code and data. **Partly unverified. Not peer reviewed.** The research and the write-up were done with a large language model (Claude, by Anthropic) working with the person who directed the project. Read the section "Limitations and provenance" of the paper before relying on any result.

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
| **Infinitely many members of rank ≥ 2 (Problem H)** | **Open** | Appendix B, F.24 |

The labels are those of the paper: Proved, Certified, Observed, Conditional, Open. "Conditional" results depend on stated hypotheses (for example the Tate conjecture for K3 surfaces over finite fields).

## Repository layout

```
paper/paper.md                 the paper (snapshot export, revision 198)
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
code/verify_reviewer_context.py   recomputation of the data in the independent reviewer's files (notes/REVIEW_2026-11-07_independent_reviewer_context.md)
code/ec.py                     exact elliptic-curve arithmetic and canonical heights (used by the previous script)
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

`validate.py` needs a C compiler (`gcc`). Both scripts exit with status 0 only if every check agrees. They were run on 6 November 2026 in a Linux sandbox; the GitHub Actions workflow in `.github/workflows/` runs the same checks but has not yet been exercised on GitHub.

## How far to trust it

Everything in the paper was produced in conversation with a language model, which makes characteristic errors: confident wrong statements, references recalled from memory, arguments that look complete but are not. Several occurred and are recorded in `ERRATA.md`. Treat each "Proved" as a claim to be checked by a human, and see the paper's section "Limitations and provenance" for the list of what has not been independently verified.

## Contributing

Corrections, independent verifications and counter-examples are the most useful contributions. Please read `CONTRIBUTING.md`; in particular, say whether any text or code you contribute was written or checked with a language model.

## License

MIT, see `LICENSE`. This covers the code, the data and the text.

## Citation

See `CITATION.cff`.
