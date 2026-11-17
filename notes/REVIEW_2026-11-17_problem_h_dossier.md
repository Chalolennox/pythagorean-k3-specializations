# Review of "Problem H: Independent review dossier" (md + Magma file), 17 November 2026

Status: my own checks, in Python and C (no Magma, no sympy here). No human has checked this review.

## Part A (consecutive qualifying-prime sets)
* Phi(t,u) = (t^2 u - t + 2)^2 - 4(1-t)(1+t^2) vanishes at (t_n, t_{n+1}) for n <= 39 (exact rationals), also on the nP+T branch (24 pairs), and for (t_{n+1}, t_n). In fact Phi = t^2 * Psi with Psi = t^2 u^2 - 2tu + 4(t+u) - 3 = (tu-1)^2 + 4(t+u-1), symmetric, whose two roots in u are t_{n+1}, t_{n-1} (checked: sum and product).
* D = Res_t(H, Res_u(Phi, H(u))) computed exactly (8x8 Sylvester determinants at 34 integer t, interpolated: degree 24 in t, integer coefficients): D = 9614636096894416865021741068691729461542912 = 2^18 3^30 7 103 113^3 13085561^2, all four primes proved prime; D != 0 so gcd(H, R) = 1.
* Necessary condition, argued: if p >= 5 divides N_n and N_{n+1} then V_n, V_{n+1} are units mod p (p | Phi(U,V) with p | V forces p | U), so t_n, t_{n+1} are p-integral, H(t_n) = H(t_{n+1}) = Psi = 0 mod p, so p | D. Poles are therefore excluded.
* Orbit walk over a full period of P mod p (C, exact): p = 7, 103, 113: no n with p | N_n at all, on either branch. p = 13085561: order of P is 3272847; on nP the six hits are n = 1126542, 1126543, 1545769, 1727078, 2146304, 2146305, so p divides BOTH N_n and N_{n+1} for n = 1126542 and 2146304 (mod 3272847); none on nP+T. At those n, (a_n b_n / p) = -1 in both (independent EDS computation mod p). So Q_n cap Q_{n+1} is empty for all n, on both branches, but gcd(N_n, N_{n+1}) is not always 1.

## Part B (density of primes with no qualifying root)
* sqrt(2) in L: the algebra is right (prod(1+u_i) = 8, and sqrt(1+a^2) = sqrt(r)/sqrt(x)).
* The dossier's L equals the paper's L* of F.5 and F.6: sqrt(q) = sqrt(D A B)/(1+a^2), sqrt(r) = sqrt(A C), sqrt(x) = sqrt(A), and the six roots +-a_i give B_i, sqrt(-1). So |Gal| = 24576 is already proved in F.5 (rank certificate) and reported from Magma in F.6.
* The qualifying conditions are necessary for a prime to lie in some Q_n (checked on p < 1500: 166 hits, 78 with (ab/p) = +1, 0 violations). q square <=> (ab/p) = +1; r is automatically a square (y^2 = r(a)); x(nP) is a square (F.18), x(nP+T) = 2/x(nP).
* Counting (C, 5,761,453 primes 5 <= p < 10^8, every prime counted): empty fraction 0.84905 against 20867/24576 = 0.84908; p = +-1 mod 8: 0.89632 against 11013/12288 = 0.89624; p = +-3 mod 8: 0.80178 against 9854/12288 = 0.80192. All within one standard error. This tests the weakest point of the dossier, the inferred 9854, but cannot fix the numerator (4 * 10^-5 per count against a standard error of about 2 * 10^-4).
* The finite counts reproduce: p <= 20000: 2260, 348, 263, 85. For p <= 10^5 I get 1470 nonempty among 9590 primes against the dossier's 1466 among 9582: the dossier's 8 "excluded exceptional primes" are not defined, so I cannot match them.

## Not reproduced
Rm, Rp (degrees, irreducibility), the totals 19709 and 22035, the group computation and the exact identification of the degree-24 action: they need Magma or an equivalent.

## What it does for Problem H
Nothing directly. It bounds the set of primes that can lie in some Q_n (density at most 3709/24576, if certified, against 175/1024 for the admissible primes in F.3), and it gives the disjointness of consecutive Q_n. It gives no parity information. The orbit-contributing density is an Artin-type condition (F.4), not a Chebotarev one, so its existence is open.

## Addendum: Magma run of the dossier script (17 November 2026) and F.57

The Magma V2.30 run agrees with the checks above: the resultant factorization and gcd(H,R) = 1; the common roots of H and R modulo p (degrees 1, 1, 3, 2 for p = 7, 103, 113, 13085561), where for 13085561 the polynomial a^2 + 4490562a + 5471570 has sum 8594999 and product 5471570 (mod p), equal to those of the t-values 5812945 and 2782054 at n = 1126542, 1126543; Rm and Rp of degrees 24 and 48, both irreducible; the counts 2260, 348, 263, 85. The script has DO_GALOIS false, so the group order and the fixed-point-free counts 19709, 22035, 11013, 9854 are the values reported earlier, not recomputed. A draft density 2609/3072 that assumed sqrt(2) not in L is discarded. F.57 states the disjointness theorem (Proved) and the candidate density 20867/24576 (Conditional on the arithmetic identification of the degree-24 action and a certified Galois-group computation).

After the reviewers' reply: F.57 (b) now states the existence of the density separately (Proved, by Chebotarev; the field L* and the order 24576 are taken from F.5/F.6) and F.57 (b') the exact value 20867/24576 as Conditional. The agreement of the count for p < 10^8 is recorded as evidence only.
