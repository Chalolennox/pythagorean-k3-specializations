# Gaps k >= 4: which primes can lie in both Q_n and Q_{n+k}? (exploration, 17 November 2026)

Status: language-model computation. No human has checked it. The paper takes from this note only one sentence in F.57 (g) (revision 292, condensed F.57); the gaps four and five are not written out in the paper (section 4). Code: `code/verify_gap_k.py` (stdlib, 5 s, `--quick` 1 s, in CI), `code/scan_gaps.c` (not in CI), output `data/gap_coincidences_p300000.txt`.

## 1. Method

By the universal correspondence (F.57 (e)) the relation between t_n and t_{n+k} is G_k(t,w) = Phi_{u_k}(1-t, 1-w), u_k = x(kP). If p >= 5 lies in Q_n and Q_{n+k}, both parameters are p-integral roots of f modulo p, so p divides the exact norm N_k of G_k (cleared of its denominator) on Q[t,w]/(f(t), f(w)), a 36x36 determinant. Because G_k is symmetric, N_k = D_k * O_k^2, where D_k = Res(f, G_k(t,t)) (equal parameters, 6x6 determinant) and O_k is an integer; D_k and O_k are much smaller than N_k and can be factored by Pollard rho. Then for every prime p >= 5 of D_k O_k the roots of f modulo p, the points above them and the points Q +- kP by the group law (including the case kP = O modulo p) decide whether two qualifying points differ by kP; an index pair then follows by a discrete logarithm. Factorizations are checked in `code/verify_gap_k.py`; the large prime factors are proved prime by Pocklington (p-1) and Lucas (p+1) certificates verified in the script.

Reformulation (local, immediate from the definitions): p is in Q_n and Q_{n+k} for some n iff k is congruent modulo m_p = ord(P mod p) to a difference r - r' of two qualifying indices r, r' of one branch (r = r' only when m_p divides k). So every prime contributes a fixed finite set of residues of gaps, at most |R|(|R|-1) <= 132 of them modulo m_p, and the exceptional set E_L of F.57 (g) is the set of primes with such a residue <= L.

## 2. Results

| k | primes >= 5 dividing N_k | primes in Q_n and Q_{n+k} | status |
| --- | --- | --- | --- |
| 1 | 7, 103, 113, 13085561 | none | F.57 (a) |
| 2 | 47, 947, 18637, 36997, 2325076196570957 | 18637 | F.57 (f); 2325076196570957 is now proved prime |
| 3 | 7, 71, 397, 4919, 8887, 19427, 206215327, 49831710601, pi (33 digits) | none | F.57 (f) |
| 4 | 5, 23, 83, 823, 2141, 4211, 4241, 18329, 5304889, 110840087, 110873747, 5473007569 and a 60-digit prime | **83, 823, 4241** | complete (all primes proved prime) |
| 5 | 7, 11, 17, 47, 67, 137, 151, 631, 1009, 8849, 11393, 19391, 24337, 6164369, 33898211, 2136952387, 11513351653907, 52679765626351 and a 95-digit prime | none | complete (the 95-digit prime is proved prime by a 17-node chain of Lucas and Pocklington certificates) |
| 6 | many; a 165-digit composite cofactor of O_6 is not factored | at least **307** and **34389517** | **incomplete** |
| 7 | many; a 264-digit composite cofactor of O_7 is not factored | at least 83; at 79734735126883 two qualifying points differ by 7P (orbit membership not checked) | **incomplete** |

Details for the complete cases (indices are those of the orbit nP + eps T, "branch" = eps).

* k = 4: p = 83 (m = 39, branch 0): qualifying indices {12, 16, 23, 27}; gaps 4 (12 to 16, 23 to 27), 7 (16 to 23), 11 (12 to 23, 16 to 27) all occur. p = 823 (m = 426): pairs (211, 215) on branch 0 and (424, 428) on branch 1. p = 4241 (m = 1029, branch 0): pair (1027, 2) (cyclically 1027 + 4 = 1031 = 2 mod 1029). All other primes of N_4 have no qualifying pair at distance 4, among them the 60-digit prime (no qualifying root at all).
* k = 5: no prime. Several small primes divide N_5 only because of poles or of non-qualifying roots (for example 11 and 17, where m_p divides 5 and f has no root).
* k = 6: p = 307 (m = 163): qualifying indices 3 and 160 = -3 on branch 0 (the points 3P and -3P), so 160 + 6 = 3 mod 163; this is the prime 307 that appeared as a pole artifact for gap three (the point 3P has t = -40/9). p = 34389517 (m about 1.7e7): indices (7782035, 7782041) and (9412587, 9412593) on branch 0, with the roots t = 17072652 and 17316865 = -17072652 modulo p; this prime is far outside the scan range and was found only from the norm.
* Local scan (all primes 5 <= p <= 300000, gaps 1..12, both branches, `data/gap_coincidences_p300000.txt`): the only hits are gap 2: 18637; gap 4: 83, 823 (both branches), 4241; gap 6: 307; gap 7: 83; gap 9: 673, 2381; gap 10: 12281; gap 11: 83; gap 12: 757, 2549, 6907. Every hit divides the exact norm N_g (checked for g <= 12). The scan alone would have missed 34389517.

## 3. What this shows and does not show

* Coincidences are real and sporadic: for k = 4 the set E_4 is exactly {83, 823, 4241}, and larger gaps have more. This is consistent with F.57 (g) (finite E_L for each L) and with the remark there that no single finite set serves all gaps once infinitely many primes have a qualifying index; a prime such as 83 with R = {12, 16, 23, 27} contributes the gaps 4, 7, 11 (and their residues) once and for all.
* Classification for k >= 6 is not complete: the composite cofactors of O_6 (165 digits) and O_7 (264 digits) may hide prime factors with a coincidence. Closing them needs a stronger factoring method (ECM or NFS), not a new idea.
* Local, no consequence for Problem H: nothing here says anything on the parity of #Q_n or on W(E_{t_n}); F.57 (b') stays Conditional.
* The scripts of the first pass (Python scratch files for norms, factoring and certificates) are consolidated in `code/verify_gap_k.py`; the C scan is `code/scan_gaps.c`.

## 4. What went into the paper

Revision 292 condenses F.57 to (a) to (d), (e) the universal correspondence, (f) gaps two and three as examples of it, (g) all gaps in characteristic 0. The gap-k results above enter only as one sentence of (g): the difference-set description (p is in Q_n and Q_{n+k} iff k is congruent to r - r' modulo m_p for two qualifying indices), the exact sets for k = 4 (83, 823, 4241) and k = 5 (none), and the primes 307 and 34389517 for k = 6 (the latter not visible in a scan of all primes below 3*10^5). The norm factorizations, certificates and scan data stay in `code/verify_gap_k.py`, `code/scan_gaps.c` and `data/`.

## 5. The factorization D_k = Delta_k S_k^2 and the primes 47, 83, 113 (17 November 2026, note "this for today")

The owner's note (verbatim in notes/drafts/gap_resultant_factorization.md) states D_k = Delta_k S_k^2 with D_k the double resultant of h(X) = f(1 - X) against G_a, Delta_k the diagonal resultant and S_k = prod_{i<j} G_a(alpha_i, alpha_j). This is the decomposition N_k = D_k O_k^2 already used in F.57 (e) and in check 1 (S_k = O_k; the scaling of G_k by a clearing factor c multiplies D_k by c^36, Delta_k by c^6 and S_k by c^15, so the identity holds over Q as well as for the cleared form). Its proof (symmetry of G_a, symmetry of the product over the roots) is correct as written; h is monic of even degree, so Res_W(h(W), G) = prod_j G(X, beta_j) without sign.

Checked here (code/verify_gap_k.py, check 8, exact arithmetic in F_p and F_{p^2}): 47 | O_2, O_5; 83 | O_4, O_6; 113 | O_1, O_6, as listed in the note, and the three explanations hold:
- p = 47, m_p = 7: u_2 = u_5 = 12 (5 = -2 mod 7), the same pair of roots (9, 38) of f in F_47 vanishes at both gaps, no diagonal zero;
- p = 83 (m_p = 39, all six roots in F_83): the pair (33, 51) at k = 4, the pair (18, 65) at k = 6 and a diagonal zero at k = 6;
- p = 113 (m_p = 14, roots in F_{113^2}; s^2 = 3): the pair (15s, 98s) at k = 1 and (45s, 68s) at k = 6, each exchanged by Frobenius (98s = -15s).
Of these primes only 83 has coincident qualifying points (k = 4, 7, 11), not at k = 6, so p | N_k does not imply a coincidence over F_p; this agrees with the classification above. The note's Magma statement for k = 1..6 is independent of the exact norms here (k = 1..7).

## 6. The shifted-gcd bound (18 November 2026)

Statement (now in F.57 (e)): for p >= 5 with m_p not dividing k, v_p(gcd(F_n, F_{n+k})) <= v_p(N_k) for every n >= 1 and both branches; for k = 1 this means gcd(F_n, F_{n+1}) divides 2^a 3^b 7 103 113^3 13085561^2.

Proof: two Bezout identities for the nested resultant (the independent validation, verbatim in notes/drafts/shifted_gcd_validation.md). The Cayley-Hamilton argument first used here (G_k divides its norm in Z[t,w]/(f(t), f(w)), then evaluate at (t_n, t_{n+k}) modulo p^e) is also correct; the Bezout version is shorter.

Checks of the validation's three open points: (1) normalization: the unscaled nested resultant and the denominator-free N_k of the code have the same p-adic valuation for p >= 5 with m_p not dividing k, because G_k is scaled by den(u_k)^2 whose primes are 2 and primes with m_p | k; (2) N_k != 0 for every k by F.57 (g), D being stable under negation, and directly for k <= 12; (3) the branch nP + T uses the same proof (p | F_n forces p not dividing V_n there too).

Why m_p | k must be excluded: then t_{n+k} = t_n modulo p, so p | F_n implies p | F_{n+k}, and v_p(F_n) is unbounded in n; the set of such p is finite for fixed k (primes dividing the denominator of x(kP)).

Tests (code/verify_gap_k.py, check 9): n + k <= 60, k <= 7, both branches, 784 pairs, 30 with a common prime >= 5, none above v_p(N_k) (gcd with 2 and 3 removed divides N_k); no prime with m_p | k occurs in that range. For k = 4 the common primes are 23 (v_23(gcd) = 1 at most, attained at n = 28 where v_23(F_32) = 2, equal to v_23(N_4) = 1) and 83.

Observed, not in the paper: log N_k = 144 h^(P) k^2 + O(1) with h^(P) = 0.21616 (144 h^ = 31.13; data 31.55 k^2 at k = 12, remainder 57-68 for k = 6..12) and log D_k close to 24 h^ k^2 = 5.19 k^2; 144 = (deg D)^2, as expected from a Neron-Tate pairing of D with its translate. Not proved.
