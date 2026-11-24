# Independent finite check of the eligible-prime triple nonintersection claim

Written by Claude (a language model), 24 November 2026; no human has checked it.  Status: **proof given in PR #89 comments (7135709265, 7136747343); the two finite checks below were reproduced independently and found consistent.  This is not a new proof and has no bearing on Problem H.**

## What is claimed (in the #89 comments)
Let C: y^2 = x^3 - 2x^2 + 2x, t = 1 - x, H(t) = t^6 - 30t^4 - 24t^2 - 1, f(x) = H(1-x), g(t) = 2t(1-t^2), and D = the 12 geometric points of C with f(x) = 0.  Then D and D+D are disjoint (no d1 + d2 = d3 inside D) over the algebraic closure of Q; consequently, outside a finite exceptional set of primes, no prime is eligible at Q, R and Q+R simultaneously.  The comments give the exceptional set {609613} for triples inside <P> and {609613, 1386618529213} for <P,T>.

## What `code/verify_eligible_triples.py` checks (stdlib only)
1. **Characteristic 5** (replaces the SymPy Groebner basis [1] over GF(5)).  5 is a good prime (f squarefree mod 5; the cubic x(x^2-2x+2) has discriminant -4), f mod 5 is a product of two cubics, so D lies in C(F_{5^6}).  The script builds F_{5^6}, lists the 12 points and tests all 144 sums (including doublings and d2 = -d1): no sum lies in D.  By reduction (the 12 points stay distinct, the group law commutes with reduction) the intersection is empty in characteristic 0.
2. **F_p for all primes 7 <= p <= 700000, plus the two large primes.**  Eligible reading: t a root of H, g(t) a nonzero square mod p, and Y = x^3 - 2x^2 + 2x a nonzero square (so the point lies on C(F_p)).  Result: the only primes <= 700000 with a triple d1 + d2 = d3 in D_p(F_p) are **229 and 609613**, as stated in the comments; the script also confirms triples at p = 1386618529213.

## Caveats
* The result depends on the definition of "eligible".  If the condition "g(t) is a square" is dropped (only Y a square), the extra primes 83, 12113, 363773 also show triples.  The reading above is the one that reproduces the comments; the definition should be stated explicitly in any write-up.
* The check does **not** certify that the exceptional set is complete (that rests on the resultant factorization and baby-step giant-step runs in the comments) and it does not cover primes above 700000 other than 1386618529213.  Primes 2, 3, 23 (disc f = 2^6 3^18 23^2) are of bad reduction and are not covered by the lifting argument above; the F_p scan treats them as sets of roots only.
* Run time: about 1 s with `--quick` (bound 20000, used in CI), about 30 s for the full default bound.
