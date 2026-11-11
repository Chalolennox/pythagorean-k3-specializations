# Review of the memorandum "Translation by 18P, bad-fiber disjointness, and the infinite-nonneutral-prime obstruction" (11 November 2026)

Reviewer: Claude (a language model). This is a check by recomputation, not a referee's report. Script: `code/verify_18P_note.py` (1 s; imports the local factor from `code/scripts_as_run/eps.py`, reads `data/factorizations.json` and `paper/paper.md`).

## Verdict

The geometric and arithmetic content is correct and I could reproduce every exact statement. **One input is wrong: the sign factor f(n) is shifted by one index relative to the memo's own definition of the orbit.** With Q_n = nP + T and t_3 = 31/49 as in the memo, the correct values are f(3) = −1 and W(E_{31/49}) = −1, not +1. This does not break Theorems 1–4 as mathematical statements, but it removes the memo's "positive-sign class with a neutral anchor at n = 3" and changes how Theorem 4 may be read. A correct anchor exists (Q₀ = T, i.e. t = 1, in the class n ≡ 0 mod 18; and the orbit nP), and with it the intended implication holds (§3 below). **Update after the independent assessment (§7):** the one remaining conditional input, f = +1 on the class n ≡ 0 (mod 18), is now proved (for every n ≡ 0 mod 6) by a short local lemma, so the corrected implication needs no observed periodicity.

## 1. What I verified (all exact)

| item | result |
| --- | --- |
| homogeneous identity 4(v²−u²)³ + 27(2uv)²(v²+u²) = −4v⁶g(u/v) | holds (sympy); at v = 0 it equals −4u⁶ ≠ 0 |
| 3P = (49/9, −287/27) and 3P ≡ T (mod 7); ord₇(P) = 6 | holds, so 6kP ≡ O (mod 7) and 18kP ≡ O (mod 7) |
| g mod 7 = (t−3)(t+3)(t²−2t+2)(t²+2t+2), squarefree, coprime to (1−t)(1+t²) | holds (so reduction is injective on the 12 points of D) |
| t₃ = 31/49, (a,b,c) = (720,1519,1681), F = 106217185707 = 3³·23·83·2060749, 2060749 prime | holds |
| (ab/23) = (ab/83) = (ab/2060749) = −1, so B₃ = ∅, s(3) = 0 | holds |
| finite-field recurrence Q_{r+18(k+m_p)} ≡ Q_{r+18k} (mod p) | 32 cases (p < 60), no failure |
| Theorem 2, empirical: common primes ≥ 5 of F(t_n), F(t_{n+18j}), n < 40 | j = 1: {83}; j = 2: {23}; j = 3: {23} |
| 12 geometric points of D, distinct reductions mod 7, y ≢ 0 | follows from the two lines above (g squarefree mod 7, coprime to (1−t)(1+t²)) |

The proofs of Theorems 1 and 2 are correct as written: reduction is a group homomorphism, injective on D, so D ∩ (D − 18kP) ≠ ∅ would give 18kP = O in characteristic 0; and for a fixed translate the closures of D and D − R in a good model meet only in finitely many fibres, since their intersection is a finite scheme with empty generic fibre. The remark that the exceptional set depends on j is right: every prime p with ord_p(P) | 18j that ever divides F(t_n) divides F(t_{n+18j'}) for all j' with ord_p(P) | 18j' (e.g. p = 7 and p = 41 have ord = 6). The strengthening from 18P to 6P is correct (ord₇(P) = 6).

## 2. The error: the sign factor is shifted by one

The memo's local data (w₂(n) = (−1)ⁿ, w₃ of period 9 with values (+,−,+,+,+,+,−,+,+), f = −w₂w₃) give f(0) = −1, f(3) = +1. The repository's exact local factor f(t) (the one that enters W = f(t)·∏_{p≥5, p|F}(−(ab/p)) of F.28, validated at 18 recorded values including the four rank-3 fibres) gives along Q_n = nP + T:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| f(t_n), repository | − | − | − | + | − | + | + | + | − | + | + | + | − | + | − | − | − | + |
| f(n), memo | − | − | + | − | + | + | + | − | + | + | + | − | + | − | − | − | + | − |

The memo's sequence equals the repository's sequence shifted by one: **f_memo(n) = f_repo(n + 1) for n = 0, …, 59**, while f_memo(n) = f_repo(n) fails at n = 3, 4, 5, 8, 9, 12, 13, 14, … (checked in the script). The period 18 is correct (observed, n ≤ 60). Consequences:

* **f(3) = −1.** With s(3) = 0 one gets **W(E_{31/49}) = −1**, which is also what the paper's table records for 3P + T ("23 N, 83 N, 2060749 N | 0 (f = −1) | −1") and what the rank-1 point (2, 4w/(1+t²)) of the c = 2 family predicts for an odd-rank fibre (w = 246/343 is rational at t = 31/49).
* **f(0) = +1** (not −1): Q₀ = T is t = 1, the fibre E₁ : y² = x³ − 8 with W = +1.
* The memo's Section 6 box "B₃ = ∅, s(3) = 0, f(3) = +1" and its consequences (Sections 7–9: "positive-sign residue class", "positive cyclic class", Summary) are therefore wrong as stated. The neutrality computation itself (B₃ = ∅) is right.

## 3. What survives, and the corrected statements

**Theorem 4 never uses the value of f**: its proof uses only s(3) = 0 (B₃ = ∅), periodicity of local states, and the hypothesis that s(3 + 18k) is odd for large k. So it stands as stated. What changes is its meaning: on the class n ≡ 3 (mod 18), where f = −1, "s odd for all large k" means **W = +1 permanently**, not cancellation. The interesting hypothesis (W = −1 permanently, i.e. a negative sign that never changes) needs an anchor in a class with f = +1. Such anchors exist:

* **Class n ≡ 0 (mod 18) on nP + T, anchor n₀ = 0.** Q₀ = T has t = 1, F = 27, no bad prime ≥ 5, f = +1 (W(E₁) = +1); f(18) = f(36) = f(54) = +1. *If W(E_{t_{18k}}) = −1 for all large k, then infinitely many distinct nonneutral primes occur among the F(t_{18k}).* (f = +1 on the whole class is proved in §7: it holds for every n ≡ 0 mod 6.)
* **The orbit nP, anchor n₀ = 1 (t = 0, F = 4) or n₀ = 9 (s = 0, f = +1, W = +1).** Here f ≡ +1 for every n (Appendix B, proved, and checked to n = 60), so no 18-periodicity input is needed and no class restriction: for any finite set S of primes ≥ 5, put L = lcm_{p∈S} ord_p(P); at n = n₀ + Lk, nP ≡ n₀P (mod p) for all p ∈ S, so no prime of S is nonneutral there. Hence: **if W(E_{t_n}) = −1 for all large n along nP (the negation of Problem H for this orbit), then infinitely many distinct nonneutral primes divide the numbers F(t_n).** (Proof: as in Theorem 4, with S = the set of all nonneutral primes if it were finite.)
* **Class n ≡ 3 (mod 18), anchor n₀ = 3.** *If W(E_{t_{3+18k}}) = +1 for all large k, then infinitely many distinct nonneutral primes occur.*

General form: let n₀ have no nonneutral prime and let f be constant (= f₀) on its class mod 18. If s(n) is odd for all large n in the class, then infinitely many distinct nonneutral primes occur in the class. This is a statement about the parity of s; the sign it corresponds to is W = −f₀ (so W = −1, permanent cancellation, exactly when f₀ = +1).

## 4. Assessment

* **Mathematically correct once the sign is fixed**, and carefully qualified (the exceptional sets depend on j; Theorem 4 is only conditional). The statement list of Section 9 is accurate except for items 4 and 6, which depend on f(3) = +1.
* **Elementary.** Everything follows from two facts: (i) the status of finitely many primes along the orbit is periodic (Section 5), and (ii) one index has no nonneutral prime. Theorem 1 (geometric disjointness) is a pleasant small statement but is not used by Theorems 3 and 4.
* **It does not touch Problem H.** The conclusion "infinitely many distinct nonneutral primes" is what one expects to be true anyway (about half of the prime divisors of F(t_n) are nonneutral); the theorem only excludes the degenerate scenario in which all nonneutral primes lie in a finite set. It says nothing about the parity of s(n) at the indices where large new primes occur, which is the open step (the memo says so in Section 8, correctly).
* The full period 18 of f along nP + T is **observed** (n ≤ 60) and is not needed: what the argument uses, f = +1 for n ≡ 0 (mod 6), is proved in §7 (relative to F.22 and the formula for f). The paper proves period 6 for ε_n and period 3 for ε′_n.

## 5. Suggested corrections to the memorandum

1. Re-index f (or the orbit): f(3) = −1, f(0) = +1; W(E_{31/49}) = −1.
2. Section 6: keep B₃ = ∅ but delete "f(3) = +1"; Section 7: "satisfies f(n) = +1" becomes f(n) = −1; Section 9 items 4 and 6 and the Summary likewise.
3. Use anchor n₀ = 0 (class 0 mod 18, f = +1) or the orbit nP to state the intended implication with W = −1.
4. Label the period 18 as Observed.

## 6. Limits

No human referee has read this. The local factor f is taken from the repository code (validated at 18 recorded signs, not by an independent implementation), and §7 proves its value only near t = 1, relative to that formula (F.28) and to the valuation law of F.22 (checked here for n ≤ 79). I did not re-derive the 2-adic and 3-adic local root numbers independently.

## 7. Response to the independent assessment: reorganized statements, and a proof of f = +1 for 6 | n

I agree with the assessment's distinctions (the translation geometry, the periodicity of individual prime contributions, and the periodicity of the global sign factor are three different statements) and with its status table, with one improvement: the conditional entry "global period 18 of f" can be replaced by a proved statement that is all the argument needs.

**Part I (geometry; no root numbers).** Theorem 1 (D ∩ (D − 6kP) = ∅, k ≠ 0) and Theorem 2 (finitely many common bad primes at each fixed translation). Proved; checked as in §1.

**Part II (arithmetic; no root numbers).** Let M ≥ 1, n₀ ≥ 0, S a finite set of primes ≥ 5, and L = L_M(S) = lcm_{p∈S} ord_p(P)/gcd(ord_p(P), M).

* **Theorem B (finite-prime avoidance, unconditional).** For every p ∈ S and k ≥ 0: Q_{n₀+MLk} ≡ Q_{n₀} (mod p), since M·ord_p(P)/gcd(ord_p(P), M) = lcm(M, ord_p(P)) is a multiple of ord_p(P). So the bad/neutral/nonneutral status of each p ∈ S at n₀ + MLk equals its status at n₀. For n₀ = 0: Q_{MLk} ≡ T, t ≡ 1 (mod p), F(1) = 27, so **no prime of S divides F(t_{MLk})** and B_{MLk} ∩ S = ∅. (Checked for S = primes in [5, 100], M = 18 and M = 6, j = 1, 2; here L = 340740400.) If B_{n₀} = ∅ then B_{n₀+MLk} ∩ S = ∅.
* **Theorem C (parity form, unconditional implication).** Let B_{n₀} = ∅. If s(n) is odd for all sufficiently large n ≡ n₀ (mod M), then ⋃_{n≡n₀ (M)} B_n is infinite. Proof: if the union were a finite set S, Theorem B gives indices n₀ + MLk, arbitrarily large, with s = 0. No f, no period 18, no root numbers are used (the assessment's observation).

**Part III (root-number reading).** W(E_{t_n}) = f(t_n)(−1)^{s(n)} (F.28). Everything about f is confined to this part.

**Lemma (local constancy of f at t = 1).** Let t = u/v ∈ ℚ in lowest terms with v₂(t − 1) ≥ 3 and v₃(t − 1) ≥ 2. Then f(t) = −w₂·w₃·(2/|c|) = +1.

*Proof.* Put t = 1 + ε. Then u, v are odd and 3 ∤ uv, so d = 2 and c = (u² + v²)/2 = v²(1 + ε + ε²/2)·(1) is odd and prime to 3, with c ≡ v² ≡ 1 (mod 8), hence (2/|c|) = +1. Moreover a/c = (1 − t²)/(1 + t²) = −ε(1 + ε/2)/(1 + ε + ε²/2) ≡ −ε (mod 32) and b/c = 2t/(1 + t²) = (1 + ε)/(1 + ε + ε²/2) ≡ 1 (mod 32) when 8 | ε; so (A16, B16) ∈ {(0,1), (8,1)}, both in the list W2 of the code, giving w₂ = −1. Modulo 9, 9 | ε gives (A9, B9) = (0, 1) ≠ (3, 8), so w₃ = +1. Hence f = −(−1)(+1)(+1) = +1. ∎ (Tested on 2 000 random rationals in this ball, all f = +1; just outside, at t ≡ 5 mod 8, every test gives f = −1, so the 2-adic condition is sharp.)

**Corollary (f = +1 for n ≡ 0 mod 6 on nP + T).** By F.22, v_p(D_n) = v_p(n) and x(nP + T) = 2/x(nP), so v₂(t_n − 1) = v₂(x(Q_n)) = 1 + 2v₂(n) ≥ 3 for even n and v₃(t_n − 1) = 2v₃(n) ≥ 2 for 3 | n (checked for n ≤ 79). By the Lemma, f(t_n) = +1 for all n ≡ 0 (mod 6) (checked n = 6, 12, …, 78 against the code). In particular f = +1 on the class n ≡ 0 (mod 18), and f(t₀) = f(1) = +1.

**Corollary D (the corrected implication).** *Orbit nP + T, anchor n₀ = 0, M = 6 or 18:* if W(E_{t_n}) = −1 for all large n ≡ 0 (mod 6) (in particular for all large n ≡ 0 mod 18), then s(n) is odd for all those n, hence by Theorem C infinitely many distinct nonneutral primes occur. *Orbit nP* (f ≡ +1, Appendix B), anchor n₀ = 1 or 9, M = 1: if W(E_{t_n}) = −1 for all large n (the negation of Problem H for this orbit), infinitely many distinct nonneutral primes divide the F(t_n). *Class n ≡ 3 (mod 18), anchor n₀ = 3 (f = −1):* if W = +1 for all large n ≡ 3 (mod 18), infinitely many nonneutral primes occur.

**Corrected status table.**

| result | status |
| --- | --- |
| D ∩ (D − 6kP) = ∅, k ≠ 0 | Proved (checked) |
| finitely many common bad primes for each fixed translation | Proved (checked on n < 40) |
| Theorem B (finite-prime avoidance, any anchor, any M) | Proved (checked) |
| Theorem C (parity form of infinite-prime necessity) | Proved, unconditional implication |
| f(t_0) = +1, f(t_3) = −1, hence W(E_{31/49}) = −1 | exact computations; agrees with the paper's table |
| f(t_n) = +1 for n ≡ 0 (mod 6) on nP + T | Proved by the Lemma, relative to F.28 and F.22 (checked n ≤ 78) |
| full period 18 of f | Observed (n ≤ 60); not needed |
| Corollary D | Conditional implication whose hypothesis is the open statement |
| infinitely many rank-two specializations | Open |

The assessment's conclusion stands: these are valid structural observations that do not advance Problem H in a decisive way. The only thing they exclude is the scenario in which all nonneutral primes along a progression lie in a finite set.
