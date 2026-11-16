# Review note, 16 November 2026: the 2-adic law for F_n (new paragraph F.55)

**What was added to the paper (revision 262).** A new paragraph F.55 at the end of Appendix F with the full proof of: for n != m >= 1, v2(F_n - F_m) = 1 + v2(n^2 - m^2), where F_n = Phi(U_n, V_n) = -F(t_n)/4. Consequence: the integers F(t_n) are pairwise distinct (the statement left "Not proved" in the Remark at the end of F.54, which now points to F.55). Also a row F.55 in the table of Appendix F, row 5a in "Results at a glance", and a row in "Limitations and provenance". Nothing else in the paper changed (diff against main d650233: 19 lines in paper.md).

**Provenance and status.** The proof was derived with a language model (Claude) over one long session and was first formulated as a numerical law (`v2(N_n - N_m) = 1 + v2(n^2 - m^2)`, observed for all pairs up to 240). No human has read it. One independent review (notes/drafts/F55_independent_review_of_coprimality.md) audited section (a) (parity, valuation, coprimality by a minimal-counterexample argument, resultant 16) and found no gap; it also suggested the Lutz-Nagell argument for the infinite order of P, which is now in (a). It did not audit (c), (d), (e). The paper's label is "Proved" with the sentence "no human has checked it" in the heading, in F.54, in the Limitations table and in row 5a.

**Structure of the proof (details in F.55 and notes/drafts/F55_2adic_law_consolidated_proof.md).**
(a) classical facts, parity, v2(psi_n) = v2(n), gcd(psi_n, psi_{n+1}) = 1 (direct; replaces the use of Lemma A and of a cited coprimality theorem);
(b) two lemmas (block-summation lemma L, second-difference lemma S);
(c) odd indices: second-difference recurrence from Ward with m = 2, Lipschitz bound 4, symmetry n -> -n;
(d) even indices: lattice recurrence for every power of two h from Ward applied twice; Steps 1-5;
(e) reduction of the theorem to (c), (d) and the mixed-parity congruence F_n = -1, F_m = 1 mod 8.

**What the reviewer should look at first.** (c) the Lipschitz constant 4 and the use of the symmetry; (d) Step 4 (r >= 2: nu + r >= nu + 2) and Step 5 (r = 1, the adjacent-sum identity); (e) the claim v >= nu + 4 for the three other terms. Two inequalities are tight in the numerical checks ((c) Lipschitz bound, (d) Step 5).

**Checks.** code/verify_2adic_law.py (11 groups of checks, exact integers and 2-adic logarithms mod 2^200; about 30 s, --quick about 1 s). They test the stated inequalities on finite ranges. They do not prove anything.

**What is not claimed.** Nothing about |F_n| = N_n (the argument does not exclude F_n = -F_m for n odd, m even); nothing about the global question of F.54 (b); nothing about Problem H.
