# The group G, the subgroup fixing sqrt 2, and the degree-24 action (F.57 (b'))

Status: derived with a language model, 17 November 2026; no human has checked it. Code: code/verify_group_G.py (numpy, about 5 seconds, in CI).

## Question
F.57 (b') listed two open items: (1) the degree-24 action (roots of Rm) was not identified inside the degree-48 action (roots of Rp); (2) the permutation group was not obtained with a certified Galois-group computation. In addition the index-two subgroup H of G fixing sqrt 2 (the character chi_2 of (2/p)) had to be identified inside the degree-48 action.

## Answer
1. sqrt 2 in L*: gamma_i = sqrt(1 + a_i^2) lie in L*, (gamma_1 gamma_2 gamma_3)^2 = prod(1 + z_i) = -g(-1) = 8, and gamma_1 gamma_2 gamma_3 = 2 sqrt 2 (positive in the embedding used). So g(sqrt 2) = psi(g) sqrt 2, where psi(g) is the product of the three signs with which g acts on gamma_1, gamma_2, gamma_3.
2. H = ker psi = Gal(L*/Q(sqrt 2)), of order 12288. psi is not the sign character of the action on 6, 24 or 48 points.
3. G as a permutation group. Thirteen radicals generate L* over N: sqrt(1 - b) for the six roots b, gamma_i (one symbol for +-a_i), g_i = sqrt(2 a_i (1 - a_i^2)), and sqrt(-1) (sqrt g(-a_i) = sqrt(-1) g_i). With T_i = sqrt(1 - a_i) sqrt(1 + a_i) gamma_i (T_i^2 = 1 - a_i^4) and s(a) = a (26 + 29 a^2 - a^4)/3 (s^2 = 3 (a^4 - 1) modulo g, checked exactly) the relations are
   - (R1) T_1/T_2 = s(a_1)/s(a_2), (R2) T_2/T_3 = -s(a_2)/s(a_3),
   - (R3) gamma_1 gamma_2 gamma_3 g_1 g_2 g_3 prod_i sqrt(1 - a_i) sqrt(1 + a_i) = -432 (the square is 8 (-432)(-54) = 432^2).
   The signs on the right were read off numerically in one embedding. These three cut 13 generators down to dimension 10, the dimension of F.5.
   Pairs (sigma, signs) with sigma in S = Gal(N/Q) (order 24, a_i -> s_i a_pi(i), prod s_i = 1) and signs in {+-1}^13 that respect (R1)-(R3): exactly 24 * 2^10 = 24576 (enumeration). G lies in this set (every automorphism respects the true relations) and |G| = 24576 by F.5, so G is this set.
4. The 48 roots rho = e1 sqrt q(b) + e2 sqrt r(b) + e3 sqrt(1 - b), sqrt q(b) = g(b)/(1 + b^2), sqrt r(b) = sqrt(1 - b) gamma(b). The action of G is faithful (24576 distinct permutations) and transitive; the action on the 24 roots of Rm is transitive too (so Rp and Rm are irreducible).
5. Degree 24: the sign of sqrt(1 - a) is attached to the root a, so the pairs {rho(a; e1, e2, +), rho(a; e1, e2, -)} are blocks of G. The half-sum of a pair is e1 sqrt q + e2 sqrt r, a root of Rm, so the action on Rm's roots is the action on the 24 blocks.
6. Counts (fixed-point-free elements): degree 48: 22035; degree 24: 19709; in H, degree 48: 11013; in G minus H, degree 24: 9854 (not used: H, degree 24: 9855; G minus H, degree 48: 11022). These equal the values reported from Magma V2.30. Density of the primes with no qualifying root: (11013 + 9854)/24576 = 20867/24576.

## Empirical check
For the 5618 primes p = +-1 (mod 8) and the 5681 primes p = +-3 (mod 8) below 120000, the distribution of the number of qualifying roots agrees with the group's distribution (fixed points / 8 in H in degree 48, fixed points / 4 in G minus H in degree 24); the largest deviation is about two standard errors (k = 1 for p = +-3 mod 8: 930 observed, 879 expected).

## What it rests on
Double-precision signs and matching (differences about 1 against tolerance 1e-6), not interval arithmetic; |G| = 24576 and the dimension 10 from F.5 (lower bound: computed symbol-rank certificate); not repeated with a Galois-group routine.
