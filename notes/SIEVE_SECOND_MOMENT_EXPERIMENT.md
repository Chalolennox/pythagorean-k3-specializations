# Sieve and second-moment experiment around the geometric Sidon bound

26 November 2026.  AI-authored (Claude, a language model); no human review.  **Observed numerics and an explicitly heuristic reading; no theorem; no claim about Problem H.**  Script: `code/verify/pr92_sieve_second_moment.py` (stdlib only); full output: `notes/data/pr92_sieve_second_moment_output.txt` (B = 2 000 000, N = 1 000 000, about 3 minutes).

## Setting
D_p^+ is the set of eligible rational points (H(1-x)=0, g(1-x) a nonzero square, point on C(F_p)); d_p = ord(P mod p); A_p = {n mod d_p : nP in D_p^+}, so p is in Q(n) iff n mod d_p is in A_p.  X_B(n) counts the primes p <= B with n mod d_p in A_p.  The notes of this PR reduce Problem H to the existence of infinitely many n with Q(n) empty (stated there as "infinitely many complete empty Q(n) would imply H"); this note is about the finite-prime coverage that precedes that question.

## Part 1: direct check of the Sidon / orbit bound for every prime 7 <= p <= 2 000 000
Using all rational points, not only the 33 candidate primes of `GEOMETRIC_SIDON.md`:
* max over nonzero R of |D_p ∩ (D_p+R)| is 4, first reached at p = 64811;
* for D_p^+ the maximum is 2 at every prime except p = 519521, R = T = (0,0), where it is 4;
* for the orbit-accessible part S_p = D_p^+ ∩ <P mod p> the maximum is 2 (first reached at p = 83) at every prime in range.
This agrees with the classification table of `GEOMETRIC_SIDON.md` (the p values with maxima above 2 that occur below 2·10^6 are 83, 55009, 64811, 103967, 138679, 519521, 609571) and does not use the owner's Magma transcripts.  It is an independent finite check, not a proof for p > 2·10^6; the all-p statement still rests on the resultant argument of that note.

## Part 2: coverage of n in [1, 10^6] by primes p <= B
(sieve of the residue classes A_p; independent model = prod (1 - c_p), c_p the exact fraction of n <= N covered by p)

| B | primes with A_p nonempty | survivors/N | product | E[X] | Var/E | kappa_eff |
|---:|---:|---:|---:|---:|---:|---:|
| 10^4 | 74 | 0.7001 | 0.7006 | 0.348 | 0.956 | 0.485 |
| 10^5 | 642 | 0.6224 | 0.6203 | 0.470 | 0.984 | 0.509 |
| 10^6 | 5123 | 0.5695 | 0.5674 | 0.559 | 0.988 | 0.494 |
| 2·10^6 | 9674 | 0.5562 | 0.5541 | 0.583 | 0.988 | 0.482 |

kappa_eff is the slope of E[X_B] against log log B between consecutive checkpoints (full table in the data file).

**Observations.**
1. The survivor fraction matches the independent-model product to within 0.4 percent although the periods d_p are far from pairwise coprime (about 43 percent of pairs of periods share a factor).  The slight excess of survivors is the sign expected from positive overlaps between shared-period classes.
2. Var/E is below 1 and tends to about 0.99: no sign of super-Poisson clustering in the coverage count.  This is the quantitative form in which the uniform shift bound |S_p ∩ (S_p+R)| <= 2 would enter a second-moment argument: it bounds the same-prime autocorrelation of the coverage indicator at every shift by 2/d_p, so the same-prime contribution to the variance is at most of the order of the mean.  That is a statement about autocorrelation of coverage over n and n+k; it does not by itself say anything about primes with d_p larger than the window.
3. kappa_eff is about 0.48 to 0.51 for B >= 3·10^4 (earlier rows are noisy: 0.29 to 0.58).  The fluctuation from the random number of eligible primes is of this size, so this is consistent with 1/2 but does not determine it.  I have not derived the constant; it should be computable by Chebotarev from the Galois structure of the eligible cover and the index of <P> (compare `orbit_free_split_nonsplit_densities.md` and `density_qualifying_primes.c`).

## Heuristic reading (explicitly unproved)
If the coverage of a fixed n by all primes behaves like a sieve of dimension kappa, then the probability that no prime covers n is of the order of (log D(n))^(-kappa), where D(n) is the integer attached to nP and log D(n) grows like a constant times n^2 (height of nP).  With kappa = 1/2 this is about n^(-1), so the expected number of n <= X with Q(n) empty would grow like log X: borderline between "finitely many" and "infinitely many".  If kappa were larger than 1/2 the same heuristic would predict only finitely many empty n; if smaller, a positive-power growth.  This is Cramer-style reasoning that ignores parity obstructions, the correlations coming from the shared factors of the d_p, and the constants; it only locates the problem at the critical exponent, and it is the reason the value of kappa should be pinned down exactly (by a density computation, not by numerics).

## Limits
* Primes above B and all primes dividing D(n) for large n are outside this experiment: the experiment only covers the finite sieve over p <= B.
* The window N = 10^6 cannot see large-prime coverage (d_p > N contributes only the residue itself).
* No statement about Q(n) being empty for any particular n; no statement about Problem H.

## Addendum: the sieve dimension by Chebotarev (26 Nov 2026)
AI-authored, no human review.  Script `code/verify/pr92_sieve_dimension.py` (stdlib; default about 25 s; full output for B = 2·10^6 in `notes/data/pr92_sieve_dimension_output.txt`).

**Claim.** The sieve dimension kappa = lim (1/log log B) sum_{p<=B} a_p/d_p equals 1/2 (a_p = |D_p^+ ∩ <P mod p>|, d_p = ord(P mod p)), assuming no Kummer-type entanglement between the eligible points and <P>.  Status: Steps 1 to 3 are **proof given** (finite computations only); Step 4 is **conditional/heuristic** with numerical support.

* **Step 1 (proof given).** h(x) = H(1-x) = x^6-6x^5-15x^4+100x^3-189x^2+162x-54 is irreducible over Q.  Mod 11 it factors with degrees 3+3 and mod 29 with degrees 2+4; a factorization over Q would refine both patterns, which forces a single factor of degree 6.
* **Step 2 (proof given).** Let L = Q[x]/(h) and Y = x^3-2x^2+2x, g = g(1-x) = 2(1-x)x(2-x).  Each of Y, g, Yg is a non-square in L, because a square in L is a square mod p at every root x in F_p; witnesses: Y and g at p = 7, x = 4, and Yg at p = 19, x = 18.  Hence L[y,w]/(y^2-Y, w^2-g) is a field of degree 4 over L, so the 24 geometric points (x,y,w) form one Galois orbit (and the 12 points (x,y) form one orbit, the 6 roots one orbit).
* **Step 3 (proof given from 1 and 2, by Chebotarev).** The mean over primes of the number of Frobenius-fixed points of a Galois set is its number of orbits.  Therefore mean #roots(h mod p) = 1, mean |D_p| = 1, mean |D_p^+| = 1/2 (each eligible point gives the two points (x,y,±w)).  Numerics up to 2·10^6 (148 929 primes): 0.997, 0.993, 0.495.
* **Step 4 (conditional).** The coverage weight of p is a_p/d_p.  For a point U of J(F_p) "random with respect to <P>", E[1_{U in <P>}/d_p] = 1/#J(F_p), and sum_p |D_p^+|/#J(F_p) differs from sum_p |D_p^+|/p by a convergent series (the correction is of order 1/p^2 on average).  So sum_{p<=B} a_p/d_p ~ C (1/2) log log B, where C = 1 unless the Kummer fields of the eligible points and of P are entangled.  A rigorous version needs the usual Artin-type input (Chebotarev in the extensions generated by division points of P and of the eligible points, with GRH for the density).
* **Numerical test of Step 4.** Over B in [31622, 2·10^6]: kappa_A (slope of sum a_p/d_p against log log B) = 0.494, kappa_D (same for sum |D_p^+|/p) = 0.501, ratio C = 0.986; the difference sum a_p/d_p - sum |D_p^+|/p stays between -0.3835 and -0.3972 (it does not drift), so C = 1 to within the noise (a few percent).  An Artin-type constant different from 1 by more than a few percent is excluded numerically; an exactly-1 statement is not proved.

**Consequence (heuristic).** With kappa = 1/2 the critical-exponent reading of the first part of this note is no longer a numerical coincidence: the mean number of eligible primes covering a fixed n grows like (1/2) log log of the size of the attached integer, so P(Q(n) empty) is of order (log D(n))^(-1/2), about 1/n if log D(n) grows like n^2, and the expected number of empty n <= X is of order log X: the borderline.  What would change this: (i) a different kappa (it is 2^(1-r) in general, where r in {0,1,2} is the rank of <Y, g> in L*/L*^2; here r = 2, Step 2); (ii) a constant C not equal to 1; (iii) correlations among the large primes (parity-type obstructions) which the heuristic ignores.  Note for review: the relation "H would follow from infinitely many empty Q(n)" is the statement of the PR notes; this addendum does not prove or use it.

## Addendum 2: parity balance of the finite coverage count (26 Nov 2026)
AI-authored, no human review.  Observed numerics only.  Script `code/verify/pr92_parity_balance.py`, output `notes/data/pr92_parity_balance_output.txt`.  Prompted by the strategic clarification on #83 (comment 7200962556), which points out that Problem H needs only an even qualifying support infinitely often, not an empty one.

For n in [1, 10^6] and primes p <= B, the fraction of n with X_B(n) even is compared with the independent-Bernoulli prediction (1 + prod (1 - 2 c_p))/2:

| B | even (observed) | model | empty (observed) | model prod(1-c_p) |
|---:|---:|---:|---:|---:|
| 10^3 | 0.7977 | 0.8007 | 0.7805 | 0.7821 |
| 10^4 | 0.7402 | 0.7413 | 0.7001 | 0.7006 |
| 10^5 | 0.6918 | 0.6891 | 0.6224 | 0.6203 |
| 3·10^5 | 0.6758 | 0.6732 | 0.5958 | 0.5937 |

The observed parity matches the model to about 0.3 percent at every cutoff, with no detectable parity bias beyond it.  The bias prod(1 - 2 c_p) is expected to decay like (log B)^(-C + o(1)), i.e. very slowly, so the fraction of even supports approaches 1/2 only at astronomically large B in this model; the table shows the first stage of that decay and nothing more.  Limits as before: fixed finite sieve, window 10^6, no large primes, and the parity that matters for Problem H is that of the complete support |Q(n)| (all primes), not of X_B.  Observed numerics, not a proof of parity balance for the orbit.

## Addendum 3: where a constant C different from 1 could come from (26 Nov 2026)
AI-authored, no human review.  Script `code/verify/pr92_descent_entanglement.py` (stdlib, about 20 s).  Status: Part A **proof given** (elementary), Part B **proof given** (finite computation), Part C **heuristic** with the remaining hypothesis stated explicitly.  No claim about Problem H.

**A. Uniform lemma.**  For a finite abelian group G, a subgroup H = <P> and U uniform on G independent of P: E[ [G:H] * 1_{U in H} ] = [G:H] * |H|/|G| = 1, for every P.  So if the eligible points U are equidistributed in J(F_p) given Frobenius and independent of P, the weighted sum sum_p a_p/d_p has the same mean as sum_p |D_p^+|/#J(F_p), i.e. C = 1.  A constant C != 1 requires a correlation between the distribution of U (conditioned on eligibility) and the subgroup <P>.

**B. The one visible entanglement and why it does not move C at the first descent level.**  The 2-descent map delta(Q) = x(Q) mod squares is a homomorphism on J(F_p) (delta(T) = 2), and delta(P) = delta((1,1)) = 1, so every multiple nP has x(nP) a square mod p: <P> lies in an index-2 subgroup S of J(F_p) whenever delta is nontrivial there.  (Observed: all 109 accessible eligible points found by the orbit walk up to p = 3·10^5 have x a square.)  This would force a factor 2 in C if eligibility forced delta(U) = 1, i.e. if the class of x in L*/L*^2 were in the span of the eligibility conditions.  It is not: the classes of 2, x, 1-x, 2-x, x^2-2x+2 are independent in L*/L*^2 (rank 5 over F_2 on 428 degree-one primes of L; a dependence in L*/L*^2 would force a dependence of the symbols at every such prime), hence x, Y = x(x^2-2x+2), g(1-x) = 2(1-x)x(2-x) are independent, and by Chebotarev (chi(x), chi(Y), chi(g)) is equidistributed on {+-1}^3 at the roots of h (observed over 3·10^5: all eight classes within 0.003 of 1/8; among eligible points 3230 of 6466 have x a square).  So conditioning on eligibility leaves delta(U) uniform and the 2-descent entanglement does not alter C at this level.

**C. What remains.**  C = 1 is therefore the prediction of the independence hypothesis (K): the reductions of the Galois conjugates of the eligible points and of P are equidistributed, up to the known constraint of B, in J(F_p) x J(F_p)-Kummer coordinates at every prime power l^k.  Not proved here: (i) deeper 2-adic levels (4- and 8-descent classes of U against those of P, including the role of T); (ii) odd l and the possibility of CM/isogeny coincidences (none known; J has no CM); (iii) the Kummer image itself, which depends on the rank of J over the field of definition of D and is unknown (a rigorous version would need Chebotarev in the Kummer extensions and GRH for the weighted sum, as in Artin-type results).  Numerically C = 0.986 (previous addendum) leaves little room for a correction beyond a few percent.

## Addendum 4: independent-review follow-up on the constant C (26 Nov 2026)
AI-authored, no human review.  Scripts: `code/verify/pr92_descent_entanglement.py` (Parts 3 and 4 added) and `code/verify/pr92_class_dependence.py`; output `notes/data/pr92_class_dependence_output.txt`.  No claim about Problem H.

* **Full 2-descent at p = 1 mod 4 (proof given, finite computation).** When J[2] is rational the descent uses x, x-1-i, x-1+i.  Over L(i) the classes of 2, x, 1-x, 2-x, x-1-i, x-1+i have rank 6 on 768 degree-one primes of L(i), and x, Y = x(x-1-i)(x-1+i), g = 2(1-x)x(2-x) have rank 3.  Together with Addendum 3 this shows that eligibility is independent of the whole first-level 2-descent character vector of U (including the class of 2, hence the interaction with T = (0,0) at this level), for primes of both types.  Chebotarev for this finite Kummer extension needs no GRH.
* **No point of D is torsion (proof given modulo the stated unramifiedness).** D is one Galois orbit, conjugates of a torsion point have equal order, and torsion injects into the reduction at primes of good reduction unramified in Q(D) (Res(h,Y) = +-2^7 3^3 and disc h = 2^6 3^18 23^2, so 83 is unramified).  The rational points of D mod 83 have orders 13, 26 and 39, not all equal, hence no point of D is torsion.
* **Kummer input needed for C (hypothesis, not proved).** J has j = 128, not a CM value, so End J = Z.  Let K = Q(D) and M the subgroup of J(K) generated by P and D.  If P and the conjugates of U are independent in J(K) tensor Q, Kummer theory of Bashmakov-Ribet type (to be checked against the literature before it is cited) gives a Kummer image of finite index, full for all but finitely many l; then C = product over finitely many l of explicit local factors C_l computed from the finite image, and C_l = 1 for the remaining l by the uniform lemma of Addendum 3 (A).  Independence in J(K) tensor Q is a rank/height statement that no finite-prime computation here certifies.  The Sidon bound and the triple nonintersection theorem exclude only low-coefficient relations among D.
* **Class dependence (observed).** Because Q(J[8]) contains sqrt 2 and eligibility involves chi(2), eligibility could correlate with the 2-adic structure of J(F_p).  Ratio of sum a_p/d_p to sum |D_p^+|/#J(F_p) for 10007 <= p <= 10^6 (15 059 primes; ambiguous orders skipped): overall 1.040; p = 1 mod 4: 1.072 +- 0.068, p = 3 mod 4: 1.008 +- 0.052; mod 8: 1.197 +- 0.137, 0.983 +- 0.045, 0.964 +- 0.054, 1.035 +- 0.107; mod 16 between 0.882 +- 0.066 and 1.381 +- 0.244.  All classes are within about 1.8 sigma of 1; the precision is 5 to 20 percent per class, so a small correction at l = 2 is not excluded.

## Addendum 5: signed permutation representation V_D and independence of P and D (26 Nov 2026)
AI-authored, no human review.  Script `code/verify/pr92_vd_character.py`, output `notes/data/pr92_vd_character_output.txt`.  Responds to the proposal on #83 (comment 7201281569).  No claim about Problem H.

**Setup.**  U_1..U_6 represent the pairs {U, -U} of D; V_D = Q-span of e_1..e_6 with sigma(e_j) = +-e_{sigma(j)}; Phi: QP + V_D -> J(K) tensor Q, (a_0, a_j) -> a_0 P + sum a_j U_j is Galois-equivariant.  This route is sound and in fact needs less than irreducibility for the P-part:
1. **V_D has no trivial constituent (proof given).**  V_D = Ind_{Stab(pair)}^{G} chi with chi(sigma) = +1 if sigma fixes U and -1 if it sends U to -U.  By Frobenius reciprocity Hom(1, V_D) = Hom(1, chi) = 0 as soon as chi is nontrivial, i.e. as soon as some sigma fixes x(U) and negates y.  That is exactly the statement that Y is not a square in L = Q[x]/(h) (rank certificate in `pr92_sieve_dimension.py`, witness p = 7, x = 4).
2. **P is not torsion (proof given).**  x(2P) = ((x^2 - 2)/(2y))^2 = 1/4 at P = (1,1), not an integer, so P is not torsion by Nagell-Lutz.
3. **Hence the kernel of Phi lies in V_D (proof given).**  By complete reducibility the kernel of Phi, being a Galois subrepresentation of QP + V_D, is the direct sum of its trivial part and its nontrivial part; the trivial isotypic part of QP + V_D is QP (by 1), and the kernel meets QP trivially because Phi(P) = P != 0 in J(K) tensor Q.
4. **If V_D is irreducible, Phi is injective (proof given from the non-torsion result of Addendum 4).**  Phi on V_D is nonzero because no point of D is torsion, and the kernel is 0 or V_D.  Then P, U_1, ..., U_6 are independent in J(K) tensor Q and J(K) has rank at least 7.  If V_D is reducible one checks each constituent W by exhibiting a vector of W whose image is non-torsion (different orders of the reduction at two unramified primes).
**Irreducibility is not certified here.**  The trace of Frob_p on V_D is chi_V(p) = sum over roots x of h in F_p of (Y(x)/p).  Over the 25 994 primes 5 <= p <= 3·10^5 (p != 23): mean chi_V = -0.0065, mean chi_V^2 = 1.0067.  A decomposition into k >= 2 constituents would force mean chi_V^2 >= 2 in the limit, so this is strong numerical evidence that V_D is (absolutely) irreducible; a proof needs the Galois group of Q(D)/Q (a finite group computation, for example in Magma or GAP, taking the 12 points of D as the action).  Observed: the number of rational roots of h mod p is only ever 0, 2 or 6.

**What this does and does not give for C.**  Granting irreducibility, the independence hypothesis of Addendum 4 holds for the module generated by P and D.  It does not by itself give C: one still needs (a) the local factors C_l for the finitely many l where the Kummer image over K can fail to be full, or where Q(J[l]) meets K (candidates: l = 2, 3, and l = 23 because disc h = (2^3 3^9 23)^2 and 23 is the only odd prime other than 3 ramified in Q(x)); (b) the Galois action of Gal(K/Q) on V_D inside the Q-Kummer image, not just the K-image; (c) the infinite-level limit for the index-weighted statistic.  These are proposals, not established.
