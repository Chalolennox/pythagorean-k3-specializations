# Review, 17 November 2026: "Universal gap-three exclusion" (review dossier) and the theorem "no geometric exceptional gaps"

Status: language-model derivation and recomputation. No human has checked the proofs or this assessment. The dossier is recorded word for word in `notes/drafts/gap_three_independent_review.md`, the pasted theorem in `notes/drafts/no_geometric_exceptional_gaps_theorem.md`, and the checks are in `code/verify_gap_three.py` (standard library, about 4 s, `--quick` for CI). The paper text is changed only in F.57 (e) (revision 278).

## 1. What the dossier claims

For the sets R_{p,ε} of qualifying indices (equivalently Q_n of F.57) it proposes R ∩ (R − 3) = ∅ for every prime p ≥ 5 and both branches, i.e. Q_n ∩ Q_{n+3} = ∅. The method: x(Q+3P) = (A(x) + 1722y)/D(x), the polynomial G = W⁶ − 30W⁴D² − 24W²D⁴ − D⁶ with W = D − A − 1722y, the norm N = G₀² − f_C G₁², and R₃ = Res_x(h, N), which Magma reports as nonzero with eleven prime divisors; seven of them survive a first test and are then eliminated by local group-law computations; a brute-force orbit scan of 9590 primes below 10⁵ finds nothing.

## 2. Recomputed

* **The formula for x(Q+3P)** is exact: 3P = (49/9, −287/27), and x(Q+3P)·D = 81 f_C(x) + 82369/9 + (2 − x − 49/9) D + 1722 y = A(x) + 1722 y (the polynomial part is a cubic identity checked at eight points and at 19 orbit points). It fails only at 9x = 49, i.e. Q = ±3P.
* **The resultant R₃** was reproduced exactly (6×6 determinant over ℚ[x]/(h)): negative, |R₃| = 2¹⁸·3⁴⁵·7²·71²·307¹²·397²·4919²·8887²·19427·7743563¹²·206215327·49831710601²·π² with π = 286414695690956651258188903406027. Cofactor 1.
* **The local tests.** For each of the nine primes 7, 71, 397, 4919, 8887, 19427, 206215327, 49831710601, π (the dossier reran only seven) the roots of f over F_p were found, the points above every root taken, Q ± 3P computed by the group law, and no pair with both endpoints qualifying exists. The numbers of geometric pairs agree with the dossier (71: 2, 19427: 1, 206215327: 1, 49831710601: 2, π: 2).
* **The orbit scan.** A scan of the full orbits of all primes 5 ≤ p < 10⁵ (9590 primes, C program, 35 s) finds no gap-one and no gap-three coincidence and exactly one gap-two coincidence, 18637 (the prime of the gap-two note). `code/verify_gap_three.py` repeats this for p < 10⁴ (3000 with `--quick`) with a positive control at 18637.

## 3. Corrections and what is proved

**The audit of denominators (question 4 of the dossier).** The elimination can be done without the pole x = 49/9. From the consecutive relation Ψ of F.57 (i), eliminating the two middle parameters gives a relation G3(t_n, t_{n+3}) = 0 that holds over ℚ (resultant of G2(t,s) and Ψ(s,w) in s, divided by Ψ(t,w); the division is exact in ℤ[t,w]):

  G3(t,w) = 81t²w² + 720t²w + 720tw² + 1600t² + 1600w² − 4802tw + 1044t + 1044w − 1683,

symmetric, of degree 2 in each variable; it vanishes exactly at (t_n, t_{n+3}) for n = 0..9 on both branches. If p ≥ 5 is in Q_n and Q_{n+3} then p does not divide the denominators of t_n and t_{n+3} (F.57, as for gap two), so both are p-integral roots of f modulo p and G3 of their reductions is 0 modulo p, whatever happens to the two middle parameters. Hence p divides the exact norm of G3 on ℚ[t,w]/(f(t), f(w)) (a 36×36 determinant):

  2¹⁸·3⁴⁵·7²·71²·397²·4919²·8887²·19427·206215327·49831710601²·π²,

cofactor 1. **Candidate primes ≥ 5: 7, 71, 397, 4919, 8887, 19427, 206215327, 49831710601, π.** The diagonal G3(t,t) = 81t⁴ + 1440t³ − 1602t² + 2088t − 1683 (equal parameters, a reflection) has Res(f, G3(t,t)) = 2⁶·3¹⁵·7²·19427·206215327, so 7, 19427, 206215327 are the primes where equal parameters occur; unlike gap two there is no 2-torsion midpoint, since 3 is odd.

**307 and 7743563 are not candidates.** They enter the dossier's R₃ only through the denominator locus: 3P has t = 1 − 49/9 = −40/9, and 9⁶ f(−40/9) = −2377273841 = −307·7743563. They are poles of the construction (as 23 and 4241 were for gap two), not primes where qualifying points can differ by 3P; the dossier's "denominator-zero root, not resolved" rows are of this kind. Neither prime divides the norm of G3.

**Primality of π.** The dossier asks (question 3) for a primality check of the largest factor. π − 1 = 2·17·179·2819·6529·2556946286738816232541, and a Pocklington chain of six steps (2556946286738816232541 → 6087967349378133887 → 1420431019453601 → 623214733 → 1059889 → 311, 71, with witnesses recorded in `code/verify_gap_three.py`) proves π prime. All other candidates are below 10¹² and are proved by trial division. So the local tests are tests at primes.

**Result (Proved, given the finite computations above; derived with a language model; no human has checked it).** For p ≥ 5, Q_n ∩ Q_{n+3} = ∅ on both branches: R_{p,ε} ∩ (R_{p,ε} − 3) = ∅. The qualifying criterion of the dossier is the F.57 one, and on the orbit it is equivalent to p ∈ Q_n (see the gap-two note, section 4, question 3). The local identity (1/m_p) Σ h(n)h(n+3) = 1 − 4δ_{p,ε} follows at once from I(n)I(n+3) = 0 (h = 1 − 2I); it is local and says nothing on the global sign.

## 4. The theorem "no geometric exceptional gaps" (pasted into the chat)

**Statement.** D = the 12 points of C with H(1 − x) = 0. Then D ∩ τ_{−kP}(D) = ∅ for every integer k ≠ 0.

**Premises, rechecked.** (1) h(x) = H(1 − x) is irreducible over ℚ: its factorization patterns modulo the primes 5 ≤ p < 600 are (3,3), (2,4), (1,1,2,2) and (1⁶); no divisor degree 1, 2, 3, 4 or 5 is compatible with all of them (pattern (3,3) excludes 1, 2, 4, 5; pattern (2,4) excludes 3). The 12 points are (α, ±√r(α)) with r(α) = f_C(α) = (1 − α)(1 + α²); the minimal polynomial of r(α) over ℚ is s⁶ − 66s⁵ − 29922s⁴ + 73214s³ − 62559s² + 22032s − 3456, so N(r(α)) = −3456 < 0 is not a square in ℚ, hence r(α) is not a square in ℚ(α), the polynomial g(y) = m(y²) of degree 12 is irreducible, and the 12 points form one Galois orbit. (g is even, so it is irreducible modulo no prime in the 12-cycle pattern; that is not a contradiction.) (2) 2P = (1/4, −5/8), non-integral, so P has infinite order (Nagell–Lutz).

**Proof.** valid as written: D ∩ τ_{−kP}(D) is Galois-stable because τ_{−kP} is defined over ℚ; a nonempty stable subset of a single orbit is all of D; then τ_{kP}(D) = D, and translation by a point of infinite order cannot preserve a finite set (it has no finite orbits). 

**Consequences.** (i) For each fixed k the two finite schemes D and τ_{−kP}(D) are disjoint in characteristic 0, so they meet modulo only finitely many primes (the primes dividing a nonzero integer, the norm of the resultant, such as the three computed above for k = 1, 2, 3); hence for every L a finite set E_L with I_{p,ε}(n)I_{p,ε}(n+k) = 0 for all 1 ≤ k ≤ L and p outside E_L. (ii) |R_{p,ε}| ≤ 12: a qualifying index gives a point of D reduced modulo p, there are at most 12 of them, and the index of a point in ⟨P⟩ + εT is unique modulo m_p. In fact |R| is even (n ↦ −n maps R to R, and a fixed index would be 0 or have y = 0, neither qualifies); the largest value seen below 10⁴ is 6. Hence δ_{p,ε} ≤ 12/m_p. (iii) For fixed M only finitely many primes have m_p ≤ M (nP ≠ O in C(ℚ) for 1 ≤ n ≤ M, so nP reduces to O only modulo the finitely many primes dividing the denominator of x(nP)), so m_p → ∞ and δ_{p,ε} → 0. This is unconditional and local.

**Refinement of "the exceptional set depends on L".** The dependence is forced, not a gap in the proof: if p has a qualifying index n, then −n is a different qualifying index (see above), and the pair n, n + k with k = (−2n) mod m_p ∈ [1, m_p − 1] is a coincidence at gap k. So E_L must contain every prime that has a qualifying index and whose smallest such gap is ≤ L, and no single finite set serves all gaps as soon as infinitely many primes have a qualifying index. Numerically 124 of the 1227 primes 5 ≤ p < 10⁴ do, with smallest gaps from 4 upward; whether infinitely many do is the question whether qualifying points lie in ⟨P, T⟩ modulo infinitely many primes, which F.57 (b) (a density of primes with a qualifying root) does not decide. The check is in `code/verify_gap_three.py`, check 10.

## 5. What this does and does not say

* F.57 (a) (gap one, exceptional primes 7, 103, 113, 13085561) and the gap-two classification (only 18637) are unchanged; gap three adds that no prime lies in both Q_n and Q_{n+3}; the theorem puts gaps 1, 2, 3 and all further gaps in one frame (a finite exceptional set for each L).
* No consequence for Problem H: all of this restricts which primes can be shared by two indices, or bounds the local density δ_{p,ε}; none of it says anything on the parity of #Q_n or on W(E_{t_n}) (the global sign needs the sum over all primes, and δ_{p,ε} → 0 gives no summability).
* F.57 (b′) stays Conditional.

## 6. Open

* A human check of all of the above, in particular of the exact norm computation (36×36 determinant; the code builds it from the definition of G3 and compares with the product above) and of the proof of the theorem.
* Whether infinitely many primes have a qualifying index (see section 4).
* The scratch scripts of the first pass (orbit scan in C, dossier reproduction) are not in the repository; the script in `code/` contains every check that the numbers above rely on except the C scan to 10⁵ (reported, not repeated in CI).
