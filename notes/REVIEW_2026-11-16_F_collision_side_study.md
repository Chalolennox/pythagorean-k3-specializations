# Review of "Repeated Values of F(t) and Discriminant Rigidity" (request of 16 Nov 2026) and of the orbit-distinctness sketch

Sources: `drafts/F_collision_dossier.md` and `drafts/F_orbit_distinctness_review.md` (verbatim). Checks: `code/verify_F_collisions.py`. Paper: the remark at the end of F.54.
Labels: formulas and the genus-5 reduction **Proved**; searches and the orbit data **Observed**; the Magma data in the dossier **not reproduced**. **No human has checked this.**

## Verdict
The algebra of the dossier is correct. The collision conjecture (F(t) = F(u) implies u = ±t on all of Q) is open; what can be proved is finiteness (Faltings, ineffective). The statement that matters for the paper is different: the values F(t_n) along t_n = 1 - x(nP) are pairwise distinct for n ≥ 1. It is Observed for n ≤ 120 and reduces to a finite computation (height argument) or to the strict growth of the odd part of U_n² + V_n²; neither is proved. Nothing here bears on Problem H.

## Checked exactly
- F(t) - F(u) = -4(t²-u²)Q(t²,u²)/((1+t²)³(1+u²)³) with the dossier's Q; the parametrisation x = A0/B0, y = -C0/D0 satisfies Q = 0 and G(x) = G(y).
- Q(x,x) = 3(x-1)(11x+7)(x+1)²: the only coincidence with t² = u² is x = y = 1; x = -7/11 is not a square.
- Q = 0 has bidegree (2,2) in (x,y), not a conic; the parametrisation is birational onto it; its node is (-1,-1), at m = 27 ± 4√-3 (not rational), irrelevant since x = -1 is not a square. Only the quotient by x <-> y is a conic: Q = 33p² + 27ps + 2s² - 20p - 27s - 21 with s = x+y, p = xy. m = infinity gives (x,y) = (1,-23/31), y < 0. B0 and D0 have non-square discriminants (both 465 mod squares), so there are no rational poles.
- The octic -A0B0C0D0 is squarefree: discriminants of the four quadratics 3588, 1860, 57408, 29760, all six resultants nonzero (primes 2, 3, 7, 11 only). So H3 has genus 3.
- sigma(m) = (31m-897)/(m-31) satisfies f(sigma m)(m-31)^8 = 4096² f(m), sigma² = 1, sigma swaps x and y; fixed points m = 23, 39 (the two points found in the dossier). With M = (m-23)/(m-39) the octic is an even polynomial h(M²); the quotient v² = h(N) is isomorphic over Q to the dossier's E_1 (same j, twist factor the square 110592²); the other quotient is w² = N·h(N), with rational branch points N = 0, infinity, and h a product of two rational quadratics with fields Q(√897), Q(√465), as in the dossier's H2 (the explicit Moebius map to the dossier's z was not checked).
- The collision curve is the fibre product C of w1² = A0B0 and w2² = -C0D0: irreducible (squarefree octic), genus 5 by Riemann-Hurwitz, quotients E_A, E_B (genus 1), H3 (genus 3). Faltings: finitely many collisions with t² ≠ u².
- E_A and E_B are isomorphic over Q (sigma swaps the two conditions; invariants differ by u² = 16; equal a_p for 233 primes). Short model y² = x³ - 154587x - 22664054. Rational points found at m = infinity, 23, -481/8 (x = (881/449)² there) generate Z x Z/2, so rank E_A ≥ 1. E_A is not isogenous to E_1 (a_7 = 0 against -4). Hence Jac(C) ~ E_A² x E_1 x J_2, rank ≥ 3 + rank J_2 (using the dossier's rank E_1 = 1, not reproduced).

## Observed (bounded)
- H3(Q): only m = 23, 39 for |p|, q ≤ 12000. x a square: m = infinity, 23, -481/8; y a square: m = 31, 23, 22087/729 (the sigma-image of -481/8; beyond the search bound). Both: only m = 23.
- No F(t) = F(u), 0 ≤ t < u, with t = a/b, a,b ≤ 3000 (5.47 million values).
- Orbit: F(t_n) pairwise distinct for 1 ≤ n ≤ 120; h(F(t_n)) - 12 ĥ(P) n² in [-1.21, 4.05], ĥ(P) = 0.21616; the denominator of F(t_n) is (U_n²+V_n²)³; the odd part of U_n²+V_n² grows by a factor ≥ 25 per step.

## Not done / not reproduced
- Selmer dimension 4, rank bound 2, rank E_1 = 1, the automorphism group of order 4 (sigma and the hyperelliptic involution were verified; that there are no others was not), and the rank of J2: no Magma or PARI was available. rank J2 ≤ 1 would allow Chabauty on H2, then on H3 (rank ≤ 2 < 3); rank J2 = 2 defeats Chabauty on H3 and on C. The rank of E_A and E_B was not computed (suggested: `EllipticCurve([-154587,-22664054])` in Magma, `Rank`).
- Explicit height constants for the orbit argument.

## Review of the orbit-distinctness sketch (drafts/F_orbit_distinctness_review.md)
Its opening ("does not prove") contradicts its body, which shows the argument works for n ≥ 1 once C0 and C1 are explicit. Accepted corrections: t_{-n} = t_n, so n ≥ 1; n²-m² ≥ n+m (stronger than 2 min(n,m)+1) bounds both indices; the result concerns the orbit only, not the global conjecture. Added: a route without height constants (odd part of U²+V²).
