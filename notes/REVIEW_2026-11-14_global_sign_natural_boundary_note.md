# Review of "Global-sign generating functions and the reappearance of the unit circle" (draft of 14 Nov 2026)

Source text: `drafts/global_sign_natural_boundary_review.md` (verbatim). No computation is involved. **No human has checked this.**

## Verdict
The proposition and its proof are correct. They are also general and classical, they use nothing about the elliptic family, and they give nothing toward Problem H beyond a change of language. I recommend **not** including it in the paper.

## Line by line
- (1) ⇔ (2): with ε_n periodic, D(z) is rational iff Σ W_n zⁿ is; a rational series with values in a finite set is eventually periodic (the coefficients satisfy a constant-coefficient linear recurrence, finitely many states) and conversely. Correct.
- (2) ⇒ (3): d_n ∈ {−2, 0, 2} not eventually zero gives radius exactly 1; the Pólya–Carlson theorem then gives rational or natural boundary. Correct. The theorem, in the form "an integer power series with radius of convergence 1 is either rational or has the unit circle as a natural boundary", is Carlson's (F. Carlson, *Über Potenzreihen mit ganzzahligen Koeffizienten*, Math. Z. 9 (1921), 1–13), proving a conjecture of Pólya (G. Pólya, *Sur les séries entières à coefficients entiers*, Proc. London Math. Soc. (2) 21 (1922), 22–38). I confirmed both references against the introduction of arXiv:2306.02590.
- Citation problem: the draft cites "G. Pólya, *Über gewisse notwendige Determinantenkriterien für die Fortsetzbarkeit einer Potenzreihe* (1921)". I did not find that title or date confirmed; it is not the reference used in the literature above. Do not cite it without looking it up.
- The relation to Problem H is stated correctly: non-eventual-periodicity of W_n is strictly stronger than "W_n = +1 infinitely often" (W_n = (−1)ⁿ is the example).
- "Why a circle appears": correct that the two circles are unrelated; the paragraph is only a remark and I would drop it.

## Why not in the paper
For the paper's own sequence W_n = ε_n·δ_n·κ_n (F.24) with ε_n periodic, the statement "W_n is not eventually periodic" is a restatement of "δ_nκ_n is not eventually periodic", and that is exactly the parity problem the paper already isolates (F.24, F.54). The generating-function language adds nothing that can be proved. If wanted, one sentence in the "what this does not give" paragraph of F.54 would do: "a proof that W_n is not eventually periodic would give a natural boundary for Σ(W_n − ε_n)zⁿ by the Pólya–Carlson theorem; this is a reformulation, not progress."
The excerpt attached with it ("whether Möbius-disjointness-type results for periodic-times-Sturmian sequences say anything about δ_n; I have not looked into that") is still unexamined. Möbius disjointness is known for rotations, but the sequence here is λ(F_n) along a degree-12 orbit value, not λ(n) twisted by a rotation, so those results do not apply directly.
