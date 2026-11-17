# Review, 17 November 2026: "Gap-two coincidences in the qualifying-prime sets" (review dossier)

Status: language-model derivation and recomputation. No human has checked the proofs or this assessment. The paper is not changed by this note (revision 273 stays); the dossier is recorded word for word in `notes/drafts/gap2_review.md`, and the checks are in `code/verify_gap_two.py`.

## 1. What the dossier claims

For the sets Q_n of F.57 (primes p >= 5 dividing F_n with (a_n b_n / p) = +1) it asks whether Q_n and Q_{n+2} can meet. It reports (a) a genuine coincidence at p = 18637 on the branch nP + T (n = 4683, 4685), explained by the 2-torsion midpoint 4684P + T; (b) the Gaussian identity N(H(2+i)) = 2^5 * 18637; (c) an exact resultant with candidate primes 23, 47, 947, 4241, 18637, 36997, 2325076196570957, and a statement that "only 18637 survives" which it labels provisional; (d) a period-product statement for the local sign; (e) sieve lists for p <= 100000 at n = 4683 and 4685.

## 2. Recomputed (all by `code/verify_gap_two.py`, standard library only)

* **The coincidence at 18637 is genuine.** P has order 9368 modulo 18637; 4683P + T = (3765, 7534), 4685P + T = (3765, 11103); 4684P + T = (14872, 0) has order 2; t = 14873 is a root of f with q = 2329 and r = 11491 non-zero squares ((2/18637) = -1, so no condition on 1 - t). Over a full period the qualifying indices are exactly {} on nP and {4683, 4685} on nP + T, so the local sign sequence is the one stated in section 11 of the dossier and its mean 9364/9368 = 2341/2342 is a fact, not conditional on a scan.
* **The Gaussian norm.** H(2 + i) = 20 - 772i, norm 596384 = 2^5 * 18637. The 2-torsion points (1 +- i, 0) give t = 2 -+ i (for P = (1,1)), and the equal-parameter gap-two relation reduces to the diagonal G2(t, t) = 16 t (t + 1)(t^2 - 4t + 5), whose roots are 0, -1 and 2 +- i. Since f(0) = -1 and f(-1) = -54, the only prime p >= 5 with a midpoint coincidence at one parameter is 18637.
* **The sieve lists** for p <= 100000 on nP + T are exactly {397, 2969, 18637} at n = 4683 and {18637, 93053} at n = 4685; the truncated sign product is -1; the common prime is 18637. (For p <= 100000 the lists are exact: p | F_n if and only if f(t_n) is 0 modulo p for p not dividing V_n.)
* **The period-product statement** (section 11) is correct: n -> -n maps qualifying indices to qualifying indices, a fixed index would be 0 or a point with y = 0, and neither qualifies; so the number of qualifying indices per period is even. It is the elementary parity of a reflection and does not touch the global root number.

## 3. Corrections and a complete classification

**Candidates.** From the consecutive relation Psi of F.57 (i), eliminating the middle parameter gives a relation G2(t_n, t_{n+2}) = 0 (the resultant is divisible by (t - u)^2; the quotient G2 has 8 terms and degree 2 in each variable; checked exactly for n = 0..8 on both branches). If p >= 5 lies in Q_n and Q_{n+2}, then p does not divide V_n or V_{n+2}, both parameters are p-integral roots of f modulo p, and p divides the exact norm of G2 on Q[t, u]/(f(t), f(u)). That norm (a 36 x 36 determinant) is

  2^42 * 3^27 * 47^2 * 947^2 * 18637 * 36997^2 * 2325076196570957^2,

with cofactor 1. So the candidate primes are 47, 947, 18637, 36997 and 2325076196570957. **23 and 4241 are not candidates.** They enter the dossier's resultant through the denominator locus x = 1/4: the numerator of f(3/4) is -97543 = -23 * 4241, and 3/4 = t_2 pairs with the pole t_0 = infinity, which no F_n sees. The dossier's own caution about the denominator locus explains them. (The dossier's normalisation 2^186 and the multiplicities 23^12, 4241^12 were not reproduced; only the odd prime factors above were compared.)

**Exclusions.** 47 (order of P 7) and 947 (order 467): no qualifying index on either branch. 36997 (order 18336): qualifying indices only 606 and 17730 on nP + T, a reflection pair (606 + 17730 = 18336), no gap-two pair. 2325076196570957: f has two roots in F_p, neither qualifying (a root finder validated against brute force on every prime below 400), so this prime lies in no Q_n; no orbit walk is needed. 18637: exactly one gap-two pair.

**Result (Proved given these computations).** For p >= 5, Q_n and Q_{n+2} meet only in 18637, on the branch nP + T, at n = 4683 + 9368k. This completes the classification that the dossier calls provisional. As a consistency check, a scan of the full orbits of every prime below 10000 (both branches) finds no gap-one and no gap-two coincidence, in line with F.57 (a).

## 4. What this does and does not say

* The gap-one theorem of F.57 (a) is unchanged: gap two differs only through the reflection about a 2-torsion midpoint, the same mechanism as the prime 3532913 for the reflection pairs of C_{-11/5} in Appendix C.
* Answer to question 3 of the dossier: on the orbit the finite-field test is equivalent to p in Q_n. If p divides F_n then p does not divide V_n, and (a_n b_n / p) = (q(a) / p) by F.56 (a); the conditions on r(a) and on 1 - a hold automatically along the orbit (F.57, Necessity); conversely f(t) = 0 and (q/p) = +1 give p | F_n and (a_n b_n / p) = +1.
* No consequence for Problem H: the statement restricts which primes can be shared by two indices at distance two, and says nothing on the parity of #Q_n or on W(E_{t_n}).
* The root-number sign of a shared prime (-1 at both indices, so +1 in the product) is local; the global products at n = 4683 and 4685 need all primes, and only the truncation at 100000 was computed.

## 5. Open

An F.58 paragraph for the paper has not been written; if it is added, the label should be "Proved for the classification, given the exact norm and the orbit computations; derived with a language model; no human has checked it", with no consequence for Problem H. The proofs above and the code are the author's derivations. Two bugs in earlier scratch versions of the checking code (a term-dropping reduction in the multiplication matrix, and a truncating subtraction in the root finder that made 18637-type roots invisible) were found and fixed before the numbers above were produced; the final script includes a root-finder validation against brute force for that reason.
