# Integrating the curated scripts into the repository and the paper

Date of this evaluation: 7 November 2026. Evaluated by Claude (a language model), working in a sandbox **without** Sage, Magma or PARI/GP.

## 1. What the archive is, and what it is not

The archive's own README states that the ten scripts are *reconstructions* of computations reported in earlier sessions, not the original scripts, and that they were never run in Sage, Magma or PARI/GP when the archive was packaged. It contains **no recorded outputs**: the only "values" are the parameters and points written into the scripts. So nothing in the archive, as it stands, can serve as evidence for a result in the paper. It can serve as a *recipe*: someone with the three systems can run it and produce the evidence.

I could not run the CAS scripts either. What I did instead:

* read all ten scripts for syntax and mathematics;
* re-implemented every part that needs no CAS in Python (exact rational arithmetic, sympy, and a from-scratch canonical-height routine, calibrated to reproduce the paper's E₋₇ values 2.7953, 3.7225, −2.3785 and regulator 4.7483 to four digits);
* compared every parameter and claim with the paper.

The Python check is `code/curated/check_curated_python.py` (about 2 seconds). Its output is in `code/curated/check_output_expected.txt`; all checks pass.

## 2. Evaluation, script by script

| # | Script | Verified here | Already in the paper? | Recommendation |
| --- | --- | --- | --- | --- |
| 01, 02 | rank bounds for 16 values of t | the 16 curves are nonsingular; **ranks not computed** | 14 of 16 values appear in §5 with ranks (four of rank 3, eight of rank 2, two of rank 0 among them). **t = −7/4 and t = 2/5 do not appear in §5**: if run they give new data | keep; run; compare with §5; add the two new values to the table if they confirm |
| 03 | exact circle recursion, 12 steps | yes, exact; it generates A + iB = ((3+4i)/5)ⁿ and agrees with script 07's (aₙ, bₙ) | the sequence is the origin of the family (Introduction) | keep (tiny, exact) |
| 04 | Gröbner elimination of F.47 in Magma | the same ideal in sympy contains G(c) = c(c⁶ + 16c⁴ + 432c² + 1472), and G is the last basis element | F.47 | **keep: this is the second-system check that the Limitations table asks for** |
| 05 | genus and branch data of the cover C_c | disc_t N_c = −4(c⁶ − 16c² − 64); Res_t(N_c, t²+1) = 64(c² + 4); squarefreeness for c = 0, 1, 2, 4, −3 | §6 (C_c has genus one), F.47 | keep |
| 06 | genus-three curve v² = H(c) | H = (c² + 4)(c⁶ + 36c⁴ − 1024) squarefree of degree 8; H(c) is not a square at the 12 listed c | F.47 | keep |
| 07 | rank bounds, root numbers for the powers (3+4i)ⁿ | only the sequence; **no rank or root number computed** | §3.1 tabulates the Kodaira types and the conductors for n = 1..5; §4 gives the formula. Root numbers and ranks for n ≤ 12 and n ≤ 8 are new data | keep; run; compare with §4 |
| 08 | PARI local reduction at 2 along (3+4i)ⁿ | the integral model is E_n scaled by 5ⁿ, nonsingular for n ≤ 11; **PARI output not computed** | §3.1: expected Kodaira type at 2 is I₃\* for n even and I₂\* for n odd (PARI codes −7 and −6, conductor exponents 5 and 6) | keep; see the oracle in section 4 below |
| 09 | four points at t = −46/9 | **yes, strongly**: all four on the curve; P₁ + P₃ + P₄ = O exactly; Gram matrix of canonical heights has exactly one zero eigenvalue (rank 3); every independent triple has regulator 87.594–87.597 against the 87.60 recorded in §5; no 2-torsion | §5 lists only the regulators, not the generators | **keep and add the points to §5** (text in `paper_insert.md`) |
| 10 | P_c lies on S_c | exact identity | F.47, §7 | keep (already in `code/verify_local_i0star.py`) |

## 3. Risks in the CAS scripts (not run; to check when you run them)

1. **Scripts 01 and 09 call `E.rank_bounds()`.** I believe that in Sage this method returns only *cached* information and does not start a computation, so it may print trivial bounds. Check with `E.rank_bounds?` in your Sage. If so, replace it by `E.simon_two_descent()` (returns lower bound, upper bound and generators) or `E.pari_curve().ellrank()`. I did not test either replacement.
2. **Script 07 calls `RankBounds` for n ≤ 8.** The conductors grow quickly (n = 5: 3.3·10¹⁴); it may be slow or fail for the larger n.
3. **Script 04** creates the ideal twice (the second time for the membership test); Magma may recompute the Gröbner basis. Harmless.
4. **Syntax.** I found no syntax error by reading, but none of the Magma, Sage or PARI code was executed, by me or by the archive's author.

## 4. Expected outputs from the paper, to compare against once the scripts are run

* **Script 08, n = 0..11:** `elllocalred(E,2)` should give Kodaira code −7 (type I₃\*, conductor exponent 5) for n even and −6 (type I₂\*, exponent 6) for n odd (§3.1, with ε = −1; check that the script's sign convention matches that model).
* **Conductors for n = 1..5** (add `print(ellglobalred(E)[1])` to script 08, or `Conductor(E)` to script 07): 907200, 77485600, 17006400, 555649376, 327672840715200 (§3.1).
* **Scripts 01/02:** ranks as in §5. Rank 3 at t = −46/9, −12/11, −17/31, 15/8; rank 2 at t = −7, −4, 8, −4/3, −1/3, 4/3, −5/7, 1/9; rank 0 at t = 1/2, 1. No expectation exists for t = −7/4 and t = 2/5.
* **Script 07, root numbers:** from §4, w₂ = −1 exactly when 4 | n and w₅ = (−1)ⁿ; the paper does not tabulate the global root numbers of this orbit, so the script's output is new data to be checked against the formula of §4.
* **Script 04:** the last basis element should be G(c) = c(c⁶ + 16c⁴ + 432c² + 1472).

## 5. How to integrate

### 5.1 Repository

```
unzip curated-scripts-integration.zip -d /tmp/curated
cp -r /tmp/curated/code/curated  <your clone>/code/
cd <your clone>
python3 code/curated/check_curated_python.py        # must end with ALL CHECKS PASS
git add code/curated
git commit -m "Add curated CAS scripts (reconstructed, not executed) and a Python check of their checkable parts

Written and checked with a language model (Claude). The Sage, Magma and PARI/GP scripts have not been run."
git push
```

Then three one-line edits:

* `README.md`, in the layout block, after the `code/scripts_as_run/` line:
  `code/curated/                  ten CAS scripts (reconstructed, not executed) and a Python check of their checkable parts`
* `STATE.md`, in "Next steps": `Run the scripts of code/curated in Sage, Magma and PARI/GP and fill code/curated/RUN_LOG_TEMPLATE.md (copy it to RUN_LOG.md); compare with README_INTEGRATION.md section 4.`
* `.github/workflows/validate.yml`, add a step: `- run: python3 code/curated/check_curated_python.py`

### 5.2 Paper

`paper_insert.md` has three ready-to-paste blocks, each with its place:

1. §5, after the bullet "Four rank-3 specializations": the generators at t = −46/9 and their independent height check (only this block adds a *result*).
2. Appendix G, at the end: a new paragraph G.3 that states the status of the scripts honestly.
3. "Limitations and provenance": one new table row.

Tell me and I will insert them into the document directly (and give you the updated `paper.patch`, `paper.md` and `paper.pdf`).

### 5.3 Promoting a script from "reconstructed" to "executed"

Run it, save the output, fill its row in `RUN_LOG.md` (software version, date, command, output file, SHA-256), and compare with section 4. Only then change the status in G.3, and only for the scripts whose output agrees. If an output disagrees with the paper, add a row to `ERRATA.md` instead.

## 6. Contents of this archive

```
README_INTEGRATION.md                 this file
paper_insert.md                       three text blocks for the paper
code/curated/01..10_*                 the ten scripts, exactly as you supplied them
code/curated/README_ORIGINAL.md       the README that came with them
code/curated/check_curated_python.py  Python/sympy re-implementation of the checkable parts
code/curated/ec.py                    exact elliptic-curve arithmetic and canonical heights (used by the check)
code/curated/check_output_expected.txt  output of the check, 7 November 2026
code/curated/RUN_LOG_TEMPLATE.md      table for recording real runs
```
