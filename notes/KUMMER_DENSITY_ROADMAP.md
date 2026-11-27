# Kummer and density roadmap (27 November 2026)

AI-authored synthesis, human review pending. Based on Addendum 12 of SIEVE_SECOND_MOMENT_EXPERIMENT.md at c2a959eee8ad6fa0d564bdb70584f29f4f7ec426 and archived local-factor output. No new computational run or theorem claimed.

## Numerical target
For 10^7 <= p <= 3*10^7, C2=0.9979 +/- 0.0032 and joint factor for S={2,3,5,7,11,13,23} is 1.0016 +/- 0.0054 (reported block standard errors). For p>=30000 the corresponding values are 0.9957 +/- 0.0041 and 1.0033 +/- 0.0024. The conjecture C=1 and kappa=1/2 is consistent with these observations, not established. Finite-window statistical errors are not rigorous bounds on the limiting constant. The joint factor need not equal the product of marginal factors. Within individual 2-primary group types the mean weight can differ from one.

## Workstream A: exact 2-adic structure and weighted average
Known: first-level dimension 2 over L_inf; P in 4J(Q(J[16])); index divisible by 16384. See KUMMER_TWO_ADIC_INTERSECTION.md and KUMMER_TWO_ADIC_P_QUARTER.md.
A1. Exact P projection (eighth-divisibility and subsequent layers).
A2. Geometric translation constraints, full congruence submodule and exact affine image, including eligibility field and torsion action.
A3. Compute C2 using the weighted Frobenius statistic, not the index alone. Seek an exact cancellation identity. A finite-index image does not by itself make the unbounded weight a finite-level function: prove an exact summation of the deeper congruence strata or a controlled convergent Haar integral. A finite average is sufficient only if justified by such a reduction.
A4. Joint conditioning on cross-prime characters; verify whether the odd components average to one conditionally, rather than assuming factorization.

## Workstream B: odd saturation and exceptional primes
Known: rank-seven independent module (owner-attested Galois group); 3- and 23-saturation and full corresponding translation images by the central -I argument. Other odd saturation not established. Mod-l torsion image tests through 199 are reported in Addendum 11.
B1. Find a rigorous finite bound or structural argument for odd primes dividing the saturation index. Finite index alone does not identify these primes. Use the signed permutation action to reduce each odd saturation test to P and one U; seek a height or descent bound rather than unbounded prime scanning.
B2. Verify torsion image and cohomological inputs for all remaining odd primes. Distinguish torsion-image exceptions, saturation exceptions and cross-prime entanglement.
B3. Prove conditional uniformity in the full joint eligibility/torsion extension before asserting local factors equal one.

## Workstream C: analytic passage and Problem H
C1. Prove the weighted Chebotarev limit and uniform tail control needed for sum_{p<=B} a_p/d_p ~ (C/2) log log B. Specify any GRH or other analytic hypotheses.
C2. Separately control primes beyond a finite sieve for the complete support of nP. A mean intensity or even an exact C=1 does not establish parity distribution.
C3. Central target: infinitely many n with even complete qualifying support. Empty support is sufficient but unnecessarily stronger. No conclusion on Problem H follows from the numerical local factors.

Priority: A1/A2 and B1 can proceed independently; avoid repeating broad numerical scans unless needed to discriminate an explicit algebraic prediction. C1/C2 are distinct tail problems. The exact 2-adic group is a useful intermediate objective, not a proof of Problem H.
