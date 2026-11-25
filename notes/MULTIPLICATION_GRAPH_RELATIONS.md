# Multiplication graph: algebraic relations and birational recovery

25 November 2026. Companion to GEOMETRIC_SIDON.md (PR #92). Proof given; human review pending.

Let J: y^2=Y(x)=x^3-2x^2+2x, h=x^6-6x^5-15x^4+100x^3-189x^2+162x-54, and f_k(Q)=h(x(kQ)). All f_k belong to Q(x), since x(kQ) is invariant under negation. Let u=f_1, v=f_2, w=f_3.

## Graph constraints and limitations

The multiplication-square restrictions in GEOMETRIC_SIDON.md do not bound individual cardinalities: assigning disjoint arbitrary private prime sets to vertices satisfies intersection upper bounds. Enlarging the graph alone does not eliminate this abstract countermodel. This is not a construction of actual arithmetic prime sets.

For any finite collection of distinct positive multipliers, the functions f_k are multiplicatively independent modulo constants: choose a maximal multiplier k under divisibility among those with nonzero exponent in a putative relation. At a point of exact order k, f_k has a pole, and no other remaining multiplier has a pole. The other functions are nonzero there provided the divisor h(x)=0 contains no torsion (use the paper's F.27 non-torsion result). Thus its exponent is zero, contradiction. For k=1 use O if it is the only remaining multiplier. This proof depends on the cited non-torsion result. No multiplicative independence claim for denominator-cleared integer values is made.

## Owner computations and corrections

Owner Magma verified multiplication maps and rational function numerator/denominator degrees (6,0), (24,18), (54,48). Pairwise resultants factored as single factors of total degrees 24,54,72 with 154,364,1354 terms respectively, exact substitution PASS (seed 2499370737). The low-degree search and Groebner block in that run failed; their PASS messages are invalid.

A subsequent degree-18 matrix run reported rank 1297 and nullity 33 (seed 2499370456), but a later explicit-loop matrix construction reported rank 973 and nullity 357 at the same prime 1000003 (seed 2499369571). The minimum-degree-18 claim and earlier independence-through-17 claim are WITHDRAWN. Matrix layout and intrinsic/multiple-return issues require independent verification. The randomized search (seed 1778885693) failed its kernel assertion; do not use its support statistics. The explicit-loop search found a 312-term modular candidate with exponent bounds (17,6,2), restricted nullity one at three additional primes 1000033,1000037,1000039. Exact lift was deferred; this is Observed, not a rational identity. No minimum-support claim.

A common denominator B2^d B3^d gives degree at most 72d for cleared monomials of total degree <=d, hence the rational relation dimension is at least max(0,binomial(d+3,3)-72d-1). In particular at least 33 relations exist by degree 18, regardless of the conflicting modular ranks. This is an upper bound on minimum degree, not an equality.

## Exact birational inverse theorem

Put N=(x^2-2)^2, D=4Y, B=D^6, A=D^6 h(N/D). Then Q(h,A/B)=Q(x).

Proof: the polynomials h(Z)-h(X) and A(Z)B(X)-A(X)B(Z) share Z-X. At X=1 their gcd is exactly Z-1, verified by exact SymPy computation. A monic common factor over Q(X) divides the monic polynomial h(Z)-h(X), hence lies in Q[X][Z] by integral closedness (or Gauss lemma). Its degree is preserved under specialization, and it divides both specialized polynomials by monic division. Thus the generic gcd is exactly Z-X. Alternatively the explicit inverse below proves the field equality directly.

In Q[u,v][Z], form F=h(Z)-u and G=rem_Z(A(Z)-vB(Z),F). Compute the subresultant sequence of F,G. Its degrees are 6,5,4,3,2,1,0. Write the degree-one member as M(u,v) Z-L(u,v). L and M have 105 and 104 monomials, respectively. Exact cleared substitution verifies L(h,A/B)=x M(h,A/B), and B^5 M(h,A/B) is a nonzero polynomial of degree 200. Consequently x=L/M on the open set where the denominator is nonzero. This is a rational inverse, not a claim of injectivity at every specialization.

For every k, f_k is therefore a rational function of u,v. In particular a polynomial relation linear in w exists after clearing denominators. The graph image has function field Q(x) and dimension one. This does not imply finiteness of rational points or bounds on the number of qualifying primes. The inverse is dense; no useful sparse Diophantine equation or global parity theorem has been obtained.

## Reproduction

[Exact SymPy certificate](../code/verify/pr92_birational_inverse.py), with optional --expand to print L and M. The core computation was executed in the assistant container, yielding:
```
gcd x - 1
remainder degree 5
degrees [6, 5, 4, 3, 2, 1, 0]
terms 105 104
exact inverse PASS 200
```
The committed script consolidates the executed core; its optional print wrapper was added for convenience. Magma results above are summaries of owner-pasted output, not verbatim archived logs. No independent human review claimed.
