# State of the research (start here)

*As of 7 November 2026: **the project is paused.** Problem H is open and no work is in progress; this file and the repository are kept as a reproducible record of what was tried. The paper snapshot in `paper/paper.md` is revision 227 of the working document.*

## In one paragraph

For the elliptic K3 surface E_t : y² = x³ + 4A(t)x − 8B(t), A² + B² = 1, we know the conductor and the root number of E_t for every rational t. Along the orbit t_n = 1 − x(nP) (P = (1, 1) on y² = z³ − 2z² + 2z) the root number is a periodic sign times one bit: the parity of the number of prime factors of the values F_n of an irreducible binary sextic. **Problem H (infinitely many n with W(E_{t_n}) = +1) is open and blocked by the parity barrier.** Everything else needed for it is proved. The unconditional alternative, a second section on a constant-x cover, is excluded for 18 covers (conditionally on standard hypotheses).

## Where things are

| Question | Answer | Where |
| --- | --- | --- |
| What exactly is open? | W_n = ε_n·(−1)^{ω(N_n)}·η_n with ε_n periodic and η_n explicit; H fails iff a_n = (−1)^{ω(N_n)}η_n = −ε_n for all large n | F.24, F.40 |
| What was tried and fails? | function-field identities, degree reduction, primitive divisors, multisections, second sections on covers, two covers at once (finite for every fixed pair), doubling/tripling laws, patterns in the bit | F.13–F.15, F.18–F.19, F.26–F.27, F.34–F.36, F.41, F.43–F.46, F.48 |
| What is known about the I₀* fibres of the covers? | no section of the shape X = X_P + λN_c² for any rational c; sections meeting the identity components are not covered; every rational c has the fibres 2·III + 2·I₀* + 6·I₁, and the branch points of the genus-3 curve of F.47 are fibre-collision parameters | F.43, F.47, `notes/` |
| What do the independent reviewer's files add or contradict? | the data agree with the paper where recomputed; two rank entries (t = -3/2, 2/3) and one discriminant coefficient are wrong in the reviewer's text; new, verified: nine points at t = -46/9 | `notes/REVIEW_2026-11-07_independent_reviewer_context.md` |
| Which conjectures were refuted? | period-4 pattern; δ_2n = δ_n | F.31–F.38 |
| What is the data? | 19 complete factorizations (n ≤ 12); W = +1 at 7 of them | `data/factorizations.json`, F.31, F.38 |

## If the work is resumed: next steps, in order of value

1. **Independent verification.** Have someone (or a second tool) re-derive the periodicity theorem of Appendix B and the proofs of §3.1 and §4.1. Every "Proved" label in those parts is inherited, not re-checked.
2. **Verify the ranks of §5** with a second system (the four rank-3 fibres t = −46/9, −12/11, −17/31, 15/8 are certified there; three more are only reported).
3. **Run the curated CAS scripts** of `code/curated/` in Sage, Magma and PARI/GP and fill `code/curated/RUN_LOG_TEMPLATE.md` (copy it to `RUN_LOG.md`); compare with section 4 of `code/curated/README_INTEGRATION.md`. Scripts 01/02 give the ranks for step 2 (and new data at t = −7/4, 2/5); script 04 is the second-system check of F.47.
4. **A second implementation of the point counts** in PARI or Magma, to confirm `code/fibrecount.c` and `code/lfunc.py` beyond the values in `validate.py`.
5. **Finish the cover scan.** For the 12 undecided values of c in F.46, add the primes 29 and 31 (counts at p = 29 and 31 took 1 to 2 minutes each with the faster counter).
6. **N₅ at p = 19 for c = 13/9** (`./fibrecount 19 5 …`, about 10 minutes) to decide between the discriminant classes 15 and 69. It does not change the conclusion ρ = 13.
7. **Factor the open cofactors:** the 94-digit cofactor of N(10P), the 136-digit composite N(11P), and N(12P + T) (data in `data/factorizations.json`; use CADO-NFS, msieve or PARI). A result would add a data point only; it cannot prove H.
8. **Check the references** 7–16 of the paper (written from memory).
9. **Unexamined ideas** (F.34): arithmetic identities at the points nP that are not identities of functions; Heegner-type or descent constructions of a second point; the ideal-class route in the sextic field.
10. **Presentation:** turn the bold lead-ins of F.1–F.46 into headings; decide whether `paper/paper.md` or the claude.ai working document is the source of truth.

## Index-four obstruction (a smaller result; it does not bear on Problem H)

For p = 1 (mod 8) with all six candidate roots of f qualifying (T_p = 6 or S_p = 6, see the note), the number D_p of candidate points in 2C(F_p) satisfies (-1)^(D_p/2) = -chi_p(1+i); hence d_p = 4 implies D_p <= 4.
The proof rests on an identity of square classes for the cubic factors of f (a polynomial identity plus f(i) = -8), on 2-descent, and on T_p = 6 implying S_p = 6 and p = 1 (mod 24).
Status: **Conditional on a human reading of the proof.** The algebra is checked exactly in sympy and the statements on 2 382 (T_p) and 9 664 (S_p) primes up to 1.2e9; no human has refereed it. Details: `notes/index_four_obstruction.md`; checks: `code/verify_square_class_identity.py`, `code/verify_partial_split.py`, `code/verify_index_four.py`, `code/verify_local_sign.py`.
The extension to partially split primes gives no restriction on H_p beyond 2-descent, and the local-sign formula sigma_p = -chi(-6) chi(t_n) is a reformulation of (ab/p); neither is a route to H.

## What went wrong before (do not repeat)

- H was claimed equivalent to Chowla's conjecture for F(u, v); it is not (Helfgott's result is about averages over the whole family).
- dim Sel₂ ≥ 2 was equated with "rank ≥ 2 or Sha[2^∞] infinite"; these are two statements with different proofs.
- "All algebraic routes are excluded" was too strong (F.34).
- A wrong sign of the functional equation gave wrong discriminant classes at p = 19 (F.45). The sign rule must be used, and checked with N₅ when in doubt.
- A point-counting bug for fibres with small-order points went unnoticed until p = 37 gave a non-Weil polynomial (F.44).
- The period-4 pattern of the parity bit was an artifact of small n.

## Rules for anyone, human or model, who resumes this work

1. Do not label a result **Proved** without a proof that a human has read, or **Certified** without an independent computation; use **Observed** or **Conditional** and name the hypothesis.
2. Run `python3 code/validate.py` and `python3 code/verify_factorizations.py` before trusting the code or the data.
3. Record where every number comes from (script, command, date). Do not recall references or constants from memory; look them up.
4. A language model has no memory between sessions. Give it this file, the paper's section "Limitations and provenance", and the relevant script; tell it which claims are unverified.
5. Add every correction to `ERRATA.md`.
